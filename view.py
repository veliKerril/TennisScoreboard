from jinja2 import Environment, FileSystemLoader, select_autoescape


class Views:
    ENCODING = 'utf-8'
    env = Environment(loader=FileSystemLoader('views'))

    @staticmethod
    def main_page():
        tm = Views.env.get_template('main_page.html')
        msg = tm.render()
        return msg.encode(encoding=Views.ENCODING)

    @staticmethod
    def new_match():
        tm = Views.env.get_template('new_match.html')
        msg = tm.render()
        return msg.encode(encoding=Views.ENCODING)

    @staticmethod
    def match_score(player1, player2):
        tm = Views.env.get_template('match_score.html')
        msg = tm.render(player1=player1, player2=player2)
        return msg.encode(encoding=Views.ENCODING)

    @staticmethod
    def matches(matches_for_print):
        tm = Views.env.get_template('matches.html')
        msg = tm.render(matches_for_print=matches_for_print)
        return msg.encode(encoding=Views.ENCODING)

    @staticmethod
    def wrong():
        tm = Views.env.get_template('wrong.html')
        msg = tm.render()
        return msg.encode(encoding=Views.ENCODING)
