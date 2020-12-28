import Pyro4
di = Pyro4.Proxy("PYRO:test.dispatcher@192.168.192.24:9090")
print(di.request_work())