import Pyro5.api
di = Pyro5.api.Proxy("PYRO:test.dispatcher@192.168.192.24:9090")
print(di.request_work())