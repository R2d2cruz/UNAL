import os

if os.name != "nt":
    from Server import Server
else:
    from server.Server import Server

server = Server()
server.run()
