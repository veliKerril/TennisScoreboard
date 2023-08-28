from model import Model

# class Match:
#     def __init__(self, player1, player2):
#         session = Session(bind=engine)
#         check_and_add_player(player1)
#         check_and_add_player(player2)
#         self.player1 = session.query(Players).filter(Players.name == player1).scalar().id
#         self.player2 = session.query(Players).filter(Players.name == player2).scalar().id
#         ### И вот каким-то чудом надо хранить текущий счет
#         self.score = 0
#
#     # Реализовать таким образом, чтобы он возвращал id человека, который выиграл матч
#     def winner(self):
#         session = Session(bind=engine)
#         return session.query(Players).filter(Players.name == self.player1).scalar().id

'''
ЯВНО НЕ ТАК НАДО НАЧИНАТЬ СТАРТ БАЗЫ ДАННЫХ. НЕ ЧЕРЕЗ ФУКНЦИЮ НОВЫЙ МАТЧ
'''
class Service:
    @staticmethod
    def start_bd():
        Model.add_test_values()

    @staticmethod
    def check_and_add_players(player1, player2):
        Model.check_and_add_player(player1)
        Model.check_and_add_player(player2)
        Model.print_all()

    @staticmethod
    def return_all_matches():
        return Model.return_all_mathes()


