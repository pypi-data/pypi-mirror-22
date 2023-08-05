import json

import attr

from klein import Klein

from twisted.application.service import MultiService
from twisted.application.internet import TimerService
from twisted.internet.interfaces import IReactorTime
from twisted.logger import Logger


class NotSettled(Exception):
    """
    Raised when getting index of a member when group is not settled
    """


@attr.s
class SettlingGroup(object):
    """
    A group that "settles" down when there is no activity for `settle` seconds.

    :param clock: A twisted time provider that implements :obj:`IReactorTime`
    :param float settle: Number of seconds to wait before settling
    """
    clock = attr.ib(validator=attr.validators.provides(IReactorTime))
    settle = attr.ib(convert=float)
    _members = attr.ib(default=attr.Factory(dict))
    _settled = attr.ib(default=False)
    _timer = attr.ib(default=None)
    _log = Logger()

    def _reset_timer(self):
        if self._timer is not None and self._timer.active():
            self._timer.cancel()
        self._timer = self.clock.callLater(self.settle, self._do_settling)
        self._settled = False
        self._log.info('reset timer')

    def _do_settling(self):
        self._members = {p: i + 1 for i, p in enumerate(self._members.keys())}
        self._settled = True
        self._log.info('settled with {n} members', n=len(self._members))

    def add(self, member):
        """
        Add member to the group
        """
        if member in self._members:
            return
        self._members[member] = None
        self._reset_timer()

    def remove(self, member):
        """
        Remove member from the group.

        :raises: ``KeyError` if member is not in the group
        """
        del self._members[member]
        self._reset_timer()

    def index_of(self, member):
        """
        Return index allocated for the given member if group has settled

        :raises: :obj:`NotSettled` if group is not settled
        """
        if not self._settled:
            raise NotSettled(member)
        return self._members[member]

    def __len__(self):
        return len(self._members)

    def __contains__(self, member):
        return member in self._members

    @property
    def settled(self):
        """
        Is it settled?
        """
        return self._settled


@attr.s
class HeartbeatingClients(MultiService):
    """
    Group of clients that will heartbeat to remain active
    """
    clock = attr.ib(validator=attr.validators.provides(IReactorTime))
    timeout = attr.ib(convert=float)
    interval = attr.ib(convert=float)
    _remove_cb = attr.ib()
    _clients = attr.ib(default=attr.Factory(dict))
    log = Logger()

    def __attrs_post_init__(self):
        super(HeartbeatingClients, self).__init__()
        timer = TimerService(self.interval, self._check_clients)
        timer.clock = self.clock
        self.addService(timer)

    def remove(self, client):
        del self._clients[client]

    def _check_clients(self):
        # This is O(n). May have issues when n is large. See if a heap can be used instead
        now = self.clock.seconds()
        clients_to_remove = []
        for client, last_active in self._clients.items():
            inactive = now - last_active
            if inactive > self.timeout:
                self.log.info('Client {c} timed out after {t} seconds', c=client, t=inactive)
                clients_to_remove.append(client)
        for client in clients_to_remove:
            self.remove(client)
            self._remove_cb(client)

    def heartbeat(self, client):
        if client not in self._clients:
            self.log.info('Adding client {c}', c=client)
        self._clients[client] = self.clock.seconds()

    def __contains__(self, client):
        return client in self._clients


def extract_client(request):
    """
    Return session id from the request
    """
    _id = request.requestHeaders.getRawHeaders('Bloc-Session-ID', None)
    return _id[0] if _id is not None else None


class Bloc(MultiService):
    """
    Main server object that clients talk to
    """

    app = Klein()

    def __init__(self, clock, timeout, settle, interval=1):
        """
        Create Bloc object

        :param clock: A twisted time provider that implements :obj:`IReactorTime`. Typically main
            twisted reactor object.
        :param float timeout: Maximum number of seconds to wait for a client to hearbeat before
            removing it from the group and change it to SETTLING.
        :param float settle: Number of seconds to wait before settling. Ensures that all clients
            are settled for this much time before marking the group as SETTLED
        :param float interval: Internal interval to check all clients heartbeat status. Defaults to
            1 second. Mostly, this doesn't need to be changed.
        """
        self._group = SettlingGroup(clock, settle)
        self._clients = HeartbeatingClients(clock, timeout, interval, self._group.remove)
        super(Bloc, self).__init__()
        self.addService(self._clients)

    @app.route('/session', methods=['DELETE'])
    def cancel_session(self, request):
        client = extract_client(request)
        self._clients.remove(client)
        self._group.remove(client)
        return "{}".encode("utf-8")

    @app.route('/index', methods=['GET'])
    def get_index(self, request):
        client = extract_client(request)
        self._clients.heartbeat(client)
        self._group.add(client)
        if self._group.settled:
            return json.dumps(
                {'status': 'SETTLED',
                 'index': self._group.index_of(client),
                 'total': len(self._group)}).encode("utf-8")
        else:
            return json.dumps({'status': 'SETTLING'}).encode("utf-8")
