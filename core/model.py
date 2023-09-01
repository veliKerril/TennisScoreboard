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
    @staticmethod
    def add_test_values():
        Model.add_player('Александр')
        Model.add_player('Михаил')
        Model.add_player('Иван')
        Model.add_player('Максим')
        Model.add_player('Артем')
        Model.add_player('Кирилл')
        Model.add_player('Дмитрий')
        Model.add_player('Егор')
        Model.add_player('Алексей')
        Model.add_player('Владимир')

        Model.add_match('Владимир', 'Максим', 'Владимир')
        Model.add_match('Михаил', 'Владимир', 'Михаил')
        Model.add_match('Максим', 'Артем', 'Максим')
        Model.add_match('Дмитрий', 'Иван', 'Иван')
        Model.add_match('Иван', 'Михаил', 'Михаил')
        Model.add_match('Владимир', 'Егор', 'Владимир')
        Model.add_match('Александр', 'Алексей', 'Алексей')
        Model.add_match('Дмитрий', 'Максим', 'Максим')
        Model.add_match('Кирилл', 'Артем', 'Артем')
        Model.add_match('Александр', 'Иван', 'Александр')
        Model.add_match('Максим', 'Кирилл', 'Максим')
        Model.add_match('Егор', 'Алексей', 'Алексей')
        Model.add_match('Артем', 'Александр', 'Артем')
        Model.add_match('Владимир', 'Алексей', 'Владимир')
        Model.add_match('Максим', 'Егор', 'Максим')
        Model.add_match('Кирилл', 'Артем', 'Артем')
        Model.add_match('Алексей', 'Михаил', 'Алексей')
        Model.add_match('Егор', 'Александр', 'Александр')
        Model.add_match('Михаил', 'Иван', 'Михаил')
        Model.add_match('Александр', 'Владимир', 'Владимир')
        Model.add_match('Артем', 'Кирилл', 'Кирилл')
        Model.add_match('Иван', 'Максим', 'Максим')
        Model.add_match('Кирилл', 'Дмитрий', 'Кирилл')
        Model.add_match('Алексей', 'Егор', 'Алексей')
        Model.add_match('Михаил', 'Владимир', 'Владимир')
        Model.add_match('Александр', 'Максим', 'Александр')
        Model.add_match('Артем', 'Михаил', 'Михаил')
        Model.add_match('Иван', 'Кирилл', 'Иван')
        Model.add_match('Дмитрий', 'Максим', 'Максим')
        Model.add_match('Артем', 'Егор', 'Егор')
        Model.add_match('Кирилл', 'Алексей', 'Кирилл')
        Model.add_match('Владимир', 'Дмитрий', 'Владимир')
        Model.add_match('Александр', 'Артем', 'Артем')
        Model.add_match('Кирилл', 'Владимир', 'Владимир')
        Model.add_match('Егор', 'Михаил', 'Егор')
        Model.add_match('Владимир', 'Максим', 'Владимир')
        Model.add_match('Михаил', 'Владимир', 'Михаил')
        Model.add_match('Максим', 'Артем', 'Максим')
        Model.add_match('Дмитрий', 'Иван', 'Иван')
        Model.add_match('Иван', 'Михаил', 'Михаил')
        Model.add_match('Владимир', 'Егор', 'Владимир')
        Model.add_match('Александр', 'Алексей', 'Алексей')
        Model.add_match('Дмитрий', 'Максим', 'Максим')
        Model.add_match('Кирилл', 'Артем', 'Артем')
        Model.add_match('Александр', 'Иван', 'Александр')
        Model.add_match('Максим', 'Кирилл', 'Максим')
        Model.add_match('Егор', 'Алексей', 'Алексей')
        Model.add_match('Артем', 'Александр', 'Артем')
        Model.add_match('Владимир', 'Алексей', 'Владимир')
        Model.add_match('Максим', 'Егор', 'Максим')
        Model.add_match('Кирилл', 'Артем', 'Артем')
        Model.add_match('Алексей', 'Михаил', 'Алексей')
        Model.add_match('Егор', 'Александр', 'Александр')
        Model.add_match('Михаил', 'Иван', 'Михаил')
        Model.add_match('Александр', 'Владимир', 'Владимир')
        Model.add_match('Артем', 'Кирилл', 'Кирилл')
        Model.add_match('Иван', 'Максим', 'Максим')
        Model.add_match('Кирилл', 'Дмитрий', 'Кирилл')
        Model.add_match('Алексей', 'Егор', 'Алексей')
        Model.add_match('Михаил', 'Владимир', 'Владимир')
        Model.add_match('Александр', 'Максим', 'Александр')
        Model.add_match('Артем', 'Михаил', 'Михаил')
        Model.add_match('Иван', 'Кирилл', 'Иван')
        Model.add_match('Дмитрий', 'Максим', 'Максим')
        Model.add_match('Артем', 'Егор', 'Егор')
        Model.add_match('Кирилл', 'Алексей', 'Кирилл')
        Model.add_match('Владимир', 'Дмитрий', 'Владимир')
        Model.add_match('Александр', 'Артем', 'Артем')
        Model.add_match('Кирилл', 'Владимир', 'Владимир')
        Model.add_match('Егор', 'Михаил', 'Егор')

    # Выводит всю информацию из бд
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
    def return_all_matches():
        session = Session(bind=Model.engine)
        res = []
        for elem in session.query(Matches.id, Matches.Player1, Matches.Player2, Matches.Winner):
            res.append([elem[0], session.query(Players).get(elem[1]).name, session.query(Players).get(elem[2]).name, session.query(Players).get(elem[3]).name])
        return res

    @staticmethod
    def return_filtered_matches(player):
        session = Session(bind=Model.engine)
        res = []
        for elem in session.query(Matches.id, Matches.Player1, Matches.Player2, Matches.Winner):
            if session.query(Players).get(elem[1]).name == player or session.query(Players).get(elem[2]).name == player:
                res.append([elem[0], session.query(Players).get(elem[1]).name, session.query(Players).get(elem[2]).name,
                            session.query(Players).get(elem[3]).name])
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
    temp1 = ['Test1' for _ in range(24)]
    temp2 = ['Test2' for _ in range(24)]
    time_break = temp1 + temp2
    print(time_break)
#     # Проверка того, что заполнение бд произошло успешно
#     # Model.add_test_values()
#     # print(Model.return_all_matches())
#     # print('########################')
#     # print(Model.return_filtered_matches('Кирилл'))

