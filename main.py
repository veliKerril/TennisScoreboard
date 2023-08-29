from http import server
from controller import HTTPHandler
from service import Service

Service.create_test_values_in_bd()
server = server.HTTPServer(('localhost', 8000), HTTPHandler)
server.serve_forever()
