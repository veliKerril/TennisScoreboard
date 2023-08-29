from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import Session, declarative_base


Base = declarative_base()
class Players(Base):
    __tablename__ = 'players'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)


class Matches(Base):
    __tablename__ = 'matches'
    id = Column(Integer, autoincrement=True, primary_key=True)
    Player1 = Column(ForeignKey('players.id'))
    Player2 = Column(ForeignKey('players.id'))
    Winner = Column(ForeignKey('players.id'))


class Model:
    ### Просто создание всех таблиц
    engine = create_engine('sqlite+pysqlite:///:memory:')
    Base.metadata.create_all(engine)


    ### Функции по добавлению игроков и матчей в бд
    @staticmethod
    def add_player(player):
        session = Session(bind=Model.engine)
        player1 = Players(name=player)
        session.add(player1)
        session.commit()

    @staticmethod
    def add_match(player1, player2, winner):
        session = Session(bind=Model.engine)
        match = Matches(Player1=session.query(Players).filter(Players.name == player1).scalar().id,
                        Player2=session.query(Players).filter(Players.name == player2).scalar().id,
                        Winner=session.query(Players).filter(Players.name == winner).scalar().id)
        session.add(match)
        session.commit()

    # Заполнение базы данных тестовыми данными
    """
    ПО ХОРОШЕМУ ПРИ РАБОТЕ С НЕЙ НАДО ПРОХОДИТЬ ВАЛИДАЦИЮ ДАННЫХ.
    НО ЭТО НЕ ТОЧНО
    """

    @staticmethod
    def add_test_values():
        Model.add_player('Вася')
        Model.add_player('Петя')
        Model.add_player('Коля')
        Model.add_player('Ваня')
        Model.add_player('Сережа')
        Model.add_player('Кирилл')

        Model.add_match('Вася', 'Петя', 'Вася')
        Model.add_match('Вася', 'Коля', 'Коля')
        Model.add_match('Вася', 'Ваня', 'Вася')
        Model.add_match('Вася', 'Сережа', 'Сережа')
        Model.add_match('Вася', 'Кирилл', 'Вася')
        Model.add_match('Кирилл', 'Петя', 'Кирилл')

    @staticmethod
    def print_all():
        session = Session(bind=Model.engine)
        for elem in session.query(Players.id, Players.name):
            print(elem)
        print('###########')
        for elem in session.query(Matches.id, Matches.Player1, Matches.Player2, Matches.Winner):
            print(elem)
        print('###########')
        for elem in session.query(Matches.id, Matches.Player1, Matches.Player2, Matches.Winner):
            print(elem[0], session.query(Players).get(elem[1]).name, session.query(Players).get(elem[2]).name, session.query(Players).get(elem[3]).name)

    @staticmethod
    def return_all_mathes():
        session = Session(bind=Model.engine)
        res = []
        for elem in session.query(Matches.id, Matches.Player1, Matches.Player2, Matches.Winner):
            res.append([elem[0], session.query(Players).get(elem[1]).name, session.query(Players).get(elem[2]).name, session.query(Players).get(elem[3]).name])
        return res

    @staticmethod
    def check_and_add_player(player):
        session = Session(bind=Model.engine)
        if session.query(Players).filter(Players.name == player).count() == 0:
            Model.add_player(player)


class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.score = {self.player1: 0, self.player2: 0}
        self.set = {self.player1: 0, self.player2: 0}
        self.best_of_3 = {self.player1: 0, self.player2: 0}


if __name__ == '__main__':
    # Проверка того, что заполнение бд произошло успешно
    Model.test_values()
    Model.print_all()
