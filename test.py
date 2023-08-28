from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import Session, declarative_base
import uuid

'''
Аккуратно - в этом файле есть много моментов, которые надо переписывать для классового подхода
В частности, здесь определение сессии глобальное. Так что с этим надо быть аккуратнее
'''


### Просто создание всех таблиц
engine = create_engine('sqlite+pysqlite:///:memory:')
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


Base.metadata.create_all(engine)
###


### Функции по добавлению игроков и матчей в бд
def add_player(player):
    session = Session(bind=engine)
    player1 = Players(name=player)
    session.add(player1)
    session.commit()


def add_match(player1, player2, winner):
    session = Session(bind=engine)
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
def test_values():
    add_player('Вася')
    add_player('Петя')
    add_player('Коля')
    add_player('Ваня')
    add_player('Сережа')
    add_player('Кирилл')

    add_match('Вася', 'Петя', 'Вася')
    add_match('Вася', 'Коля', 'Коля')
    add_match('Вася', 'Ваня', 'Вася')
    add_match('Вася', 'Сережа', 'Сережа')
    add_match('Вася', 'Кирилл', 'Вася')
    add_match('Кирилл', 'Петя', 'Кирилл')

def print_all():
    session = Session(bind=engine)
    for elem in session.query(Players.id, Players.name):
        print(elem)
    print('###########')
    for elem in session.query(Matches.id, Matches.Player1, Matches.Player2, Matches.Winner):
        print(elem)
    print('###########')
    for elem in session.query(Matches.id, Matches.Player1, Matches.Player2, Matches.Winner):
        print(elem[0], session.query(Players).get(elem[1]).name, session.query(Players).get(elem[2]).name, session.query(Players).get(elem[3]).name)


### Проверка того, что заполнение бд произошло успешно
test_values()
print_all()


# Функция, которая проверяет наличие игрока в бд, если нет - добавляет
def check_and_add_player(player):
    session = Session(bind=engine)
    if session.query(Players).filter(Players.name == player).count() == 0:
        add_player(player)

'''
Что осталось сделать?
1. Создать класс Match, экземлпяры которых будут хранить информацию о текущем матче.
2. Реализовать функции, которые будут работать со словарем текущего матча и uuid - надо туда ложить, извлекать
3. Запись законченного матча в базу данных
4. Функция, которая вернет все матчи, в которых есть определенный игрок
'''

class Match:
    def __init__(self, player1, player2):
        session = Session(bind=engine)
        check_and_add_player(player1)
        check_and_add_player(player2)
        self.player1 = session.query(Players).filter(Players.name == player1).scalar().id
        self.player2 = session.query(Players).filter(Players.name == player2).scalar().id
        ### И вот каким-то чудом надо хранить текущий счет
        self.score = 0

    # Реализовать таким образом, чтобы он возвращал id человека, который выиграл матч
    def winner(self):
        session = Session(bind=engine)
        return session.query(Players).filter(Players.name == self.player1).scalar().id


uuid = uuid.uuid4()
matches = {uuid: Match(player1='Ваня', player2='Кирилл')}



'''
Все, что ниже, уже лезу на уровень Serves как будто
'''
def add_match_from_brauser(match):
    session = Session(bind=engine)
    res_match = Matches(match.player1, match.player2, match.winner())
    session.add(res_match)
    session.commit()
