import Pyro5.api


@Pyro5.api.expose
class dispatcher(object):
    def __init__(self):
        self.name = "Dispatcher"
        self.version = "0.1"

    def request_work(self):
        print("Someone requested work!")
        return ['Work']

disp = dispatcher()
daemon = Pyro5.api.Daemon(host="192.168.192.24", port=9090)
Pyro5.api.Daemon.serveSimple(
    { disp: "test.dispatcher" },
    ns=False,
    daemon=daemon,
    verbose = True
)