from http import server
from controller import HTTPHandler
from service import Service

Service.start_bd()
server = server.HTTPServer(('localhost', 8000), HTTPHandler)
server.serve_forever()
