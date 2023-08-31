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
        UID = self.query_data['uuid']
        print('Редерект произошел успешно')
        info = Service.get_cur_situation(UID)
        self.send_response(200)
        self.send_header('content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(Views.match_score(info, UID))

    def matches(self):
        matches_for_print = Service.return_all_matches()
        page = self.query_data.get('page', 1)
        filter_by_player_name = self.query_data.get('filter_by_player_name', '')
        if filter_by_player_name:
            matches_for_print = Service.return_filtered_matches(filter_by_player_name)
        else:
            matches_for_print = Service.return_all_matches()
        self.send_response(200)
        self.send_header('content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(Views.matches(matches_for_print, page, filter_by_player_name))

    def wrong(self):
        self.send_response(500)
        self.send_header('content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(Views.wrong())

    def do_GET(self):
        if self.path[:10] == '/main-page' or self.path == '/':
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
        UID = Service.start_new_game(player1, player2)
        self.send_response(301)
        self.send_header('Location', f'match-score?uuid={UID}')
        self.end_headers()

    def post_match_score(self):
        # Этот блок вытаскивает информацию из тела POST-запроса
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        answer = parse_qs(str(body)[2:-1])
        player = answer['player'][0]

        # Этот блок вытаскивает информацию из URL запроса
        UID = self.query_data['uuid']

        # А тут загружаем информацию о том, кто победил
        Service.win_point(player, UID)
        info = Service.get_cur_situation(UID)
        # Если матч закончился
        if Service.flag:
            Service.flag = False
            Service.end_game(UID, player)
            self.send_response(200)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.match_score(info, UID, player))
        # Иначе
        else:
            # И получаем всю нужную нам информацию
            self.send_response(200)
            self.send_header('content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Views.match_score(info, UID))

    def do_POST(self):
        if self.path[:10] == '/new-match':
            HTTPHandler.post_new_match(self)
        elif self.path[:12] == '/match-score':
            HTTPHandler.post_match_score(self)
