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

    # Парсинг GET-параметров
    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    # Повторяющийся код по формированию запроса
    def create_response(self, code, header, view):
        self.send_response(code)
        self.send_header(*header)
        self.end_headers()
        self.wfile.write(view)

    # Обработка главной страницы
    def main_page(self):
        self.create_response(200, ('content-type', 'text/html; charset=utf-8'), Views.main_page())

    # Обработка создания нового матча
    def new_match(self):
        self.create_response(200, ('content-type', 'text/html; charset=utf-8'), Views.new_match())

    # Обработка табло со счетом
    def match_score(self):
        UID = self.query_data['uuid']
        # Получаем всю информацию по текущей ситуации матча
        info = Service.get_cur_situation(UID)
        self.create_response(200, ('content-type', 'text/html; charset=utf-8'), Views.match_score(info, UID))

    # Обработка страницы с матчами
    def matches(self):
        # Необходимая информация для пагинации и фильтрации
        page = self.query_data.get('page', 1)
        filter_by_player_name = self.query_data.get('filter_by_player_name', '')
        # Ситуация, если применен фильтр
        if filter_by_player_name:
            matches_for_print = Service.return_filtered_matches(filter_by_player_name)
        # Если без фильтра
        else:
            matches_for_print = Service.return_all_matches()
        self.create_response(200, ('content-type', 'text/html; charset=utf-8'),
                             Views.matches(matches_for_print, page, filter_by_player_name))

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

    # Обработка создания нового матча
    def post_new_match(self):
        # Вытаскиваем информацию из тела POST-запроса об именах игроков
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        answer = parse_qs(str(body)[2:-1])
        player1 = answer.get('player1', [None])[0]
        player2 = answer.get('player2', [None])[0]

        # Валидация правильности введенных имен
        # Обработка, если оказалось пустым поле
        if not player1 or not player2:
            self.create_response(400, ('content-type', 'text/html; charset=utf-8'),
                                 Views.new_match(validation_of_empty_name=True))
        # Обработка, если введено два одинаковых имени
        elif player1 == player2:
            self.create_response(400, ('content-type', 'text/html; charset=utf-8'),
                                 Views.new_match(validation_of_equal_name=True))
        # Если валидация прошла, то редирект на табло
        else:
            UID = Service.start_new_game(player1, player2)
            self.send_response(301)
            self.send_header('Location', f'match-score?uuid={UID}')
            self.end_headers()

    # Обработка табло со счетом
    def post_match_score(self):
        # Вытаскиваем информацию из тела POST-запроса - имя игрока, который забил мяч
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        answer = parse_qs(str(body)[2:-1])
        player = answer['player'][0]

        # Вытаскивает информацию из GET-параметра - UID матча
        UID = self.query_data['uuid']

        # Обрабатываем реализованный мяч
        Service.win_point(player, UID)
        # Получаем информацию о текущей ситуации в матче
        info = Service.get_cur_situation(UID)
        # Если матч закончился
        if Service.flag_end_match:
            Service.flag_end_match = False
            Service.end_game(UID, player)
            self.create_response(200, ('content-type', 'text/html; charset=utf-8'), Views.match_score(info, UID, player))
        # Если матч продолжается
        else:
            self.create_response(200, ('content-type', 'text/html; charset=utf-8'),
                                 Views.match_score(info, UID))

    def do_POST(self):
        if self.path[:10] == '/new-match':
            HTTPHandler.post_new_match(self)
        elif self.path[:12] == '/match-score':
            HTTPHandler.post_match_score(self)
