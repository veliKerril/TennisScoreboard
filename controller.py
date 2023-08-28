from functools import cached_property
from http import server
from urllib.parse import parse_qsl, urlparse, parse_qs
from service import Service
from view import Views


class HTTPHandler(server.BaseHTTPRequestHandler):
    # Парсинг URL
    @cached_property
    def url(self):
        return urlparse(self.path)

    # Запрос с выводом в словарь
    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    def main_page(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(Views.main_page())

    def new_match(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(Views.new_match())

    def match_score(self):
        print('Редерект произошел успешно')
        player1 = self.query_data['player1']
        player2 = self.query_data['player2']
        self.send_response(200)
        self.send_header('content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(Views.match_score(player1=player1, player2=player2))

    def matches(self):
        print(Service.return_all_matches())
        matches_for_print = Service.return_all_matches()
        self.send_response(200)
        self.send_header('content-type', 'text/html; charset=utf-8')
        self.end_headers()
        print('test')
        self.wfile.write(Views.matches(matches_for_print))

    def wrong(self):
        self.send_response(500)
        self.send_header('content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(Views.wrong())

    def do_GET(self):
        if self.path == '/main' or self.path == '/':
            HTTPHandler.main_page(self)
        elif self.path[:10] == '/new-match':
            HTTPHandler.new_match(self)
        elif self.path[:12] == '/match-score':
            HTTPHandler.match_score(self)
        elif self.path[:8] == '/matches':
            HTTPHandler.matches(self)
        else:
            HTTPHandler.wrong(self)

    def post_new_match(self):
        print('Ридерект начался')
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        answer = parse_qs(str(body)[2:-1])
        player1 = answer['player1'][0]
        player2 = answer['player2'][0]
        Service.check_and_add_players(player1, player2)
        self.send_response(301)
        self.send_header('Location', f'match-score?player1={player1}&player2={player2}')
        self.end_headers()

    def post_match_score(self):
        player1 = 'test1'
        player2 = 'test2'
        self.send_response(200)
        self.send_header('content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(Views.match_score(player1, player2))

    def do_POST(self):
        if self.path[:10] == '/new-match':
            HTTPHandler.post_new_match(self)
        elif self.path[:12] == '/match-score':
            HTTPHandler.post_match_score(self)
