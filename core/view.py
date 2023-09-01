from jinja2 import Environment, FileSystemLoader, select_autoescape


class Views:
    ENCODING = 'utf-8'
    env = Environment(loader=FileSystemLoader('../views'))

    # Отображение главной страницы
    @staticmethod
    def main_page():
        tm = Views.env.get_template('main_page.html')
        msg = tm.render()
        return msg.encode(encoding=Views.ENCODING)

    # Отображение страницы создания нового матча
    @staticmethod
    def new_match(validation_of_empty_name=None, validation_of_equal_name=None):
        tm = Views.env.get_template('new_match.html')
        msg = tm.render(validation_of_empty_name=validation_of_empty_name,
                        validation_of_equal_name=validation_of_equal_name)
        return msg.encode(encoding=Views.ENCODING)

    # Отображение табло со счетом
    @staticmethod
    def match_score(info, UID, winner=None):
        # Имя первого игрока
        player1 = info[0]
        # Имя второго игрока
        player2 = info[1]
        # Ситуация по очкам внутри гейма
        game = info[2]
        # Ситуация по сетам
        set = info[3]
        # Ситуация по матчу вообще
        best_of_3 = info[4]
        tm = Views.env.get_template('match_score.html')
        msg = tm.render(player1=player1, player2=player2, game=game, set=set,
                        best_of_3=best_of_3, uuid=UID, winner=winner)
        return msg.encode(encoding=Views.ENCODING)

    # Отображение страницы со сыгранными матчами
    @staticmethod
    def matches(matches_for_print, page, filter_by_player_name):
        tm = Views.env.get_template('matches.html')
        msg = tm.render(matches_for_print=matches_for_print, page=page, filter_by_player_name=filter_by_player_name)
        return msg.encode(encoding=Views.ENCODING)

