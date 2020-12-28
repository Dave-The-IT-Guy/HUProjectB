import Pyro5


@Pyro5.expose
class dispatcher(object):
    def __init__(self):
        self.name = "Dispatcher"
        self.version = "0.1"

    def request_work(self):
        print("Someone requested work!")
        return ['Work']

disp = dispatcher()
daemon = Pyro5.Daemon(host="192.168.192.24", port=9090)
Pyro5.Daemon.serveSimple(
    { disp: "test.dispatcher" },
    ns=False,
    daemon=daemon,
    verbose = True
)