import model
from model import Model
import uuid


class Service:
    # В эту переменную буду записывать очередной матч
    dict_match = {}

    # Метка того, что матч закончился
    flag = False

    @staticmethod
    def create_test_values_in_bd():
        Model.add_test_values()

    @staticmethod
    def check_and_add_players(player1, player2):
        Model.check_and_add_player(player1)
        Model.check_and_add_player(player2)
        Model.print_all()

    @staticmethod
    def start_new_game(player1, player2):
        Service.check_and_add_players(player1, player2)
        UID = str(uuid.uuid4())
        # Service.match = model.Match(player1, player2)
        Service.dict_match[UID] = model.Match(player1, player2)
        return UID

    @staticmethod
    def return_all_matches():
        return Model.return_all_matches()

    @staticmethod
    def return_filtered_matches(player):
        return Model.return_filtered_matches(player)
    # Главный метод - его вызываем, когда один из игроков забил очки
    # Все методы ниже его так или иначе обслуживают
    @staticmethod
    def win_point(player, UID):
        match = Service.dict_match[UID]
        # В любом из исходов добавляем игроку выигранное очко
        match.score[player] += 1

        # Сначала смотрим, ситуация тайм-брейка или нет
        if sum(match.set.values()) != 12:
            # Если ситуация больше-меньше - переходим в обработку больше-меньше
            if match.score[match.player1] >= 3 and match.score[match.player2] >= 3:
                Service.deuce(player, UID)

            # Если игра закончилась до больше-меньше, то заканчиваем гейм
            if 4 in match.score.values() and sum(match.score.values()) <= 6:
                Service.end_set(player, UID)
        # Иначе у нас ситуация тайм-брейка
        else:
            # Если ситуация больше-меньше - переходим в обработку больше-меньше
            if match.score[match.player1] >= 6 and match.score[match.player2] >= 6:
                Service.deuce(player, UID)

            # Если игра закончилась до больше-меньше, то заканчиваем гейм
            if 7 in match.score.values() and sum(match.score.values()) <= 12:
                Service.end_set(player, UID)

    # Обработка ситуации больше-меньше
    @staticmethod
    def deuce(player, UID):
        # Если достиглась разница в два очка, то происходит новый гейм.
        # Текущий счет обнуляестя, сет увеличивается
        match = Service.dict_match[UID]
        if abs(match.score[match.player1] - match.score[match.player2]) == 2:
            Service.end_set(player, UID)

    # Тут проверяем ситуацию по сетам и в игре
    @staticmethod
    def end_set(player, UID):
        match = Service.dict_match[UID]
        for players in match.score:
            match.score[players] = 0
        match.set[player] += 1
        # Проверка перехода на следующий этап игры по сетам
        if 7 in match.set.values():
            for players in match.set:
                match.set[players] = 0
            match.best_of_3[player] += 1
        if 2 in match.best_of_3.values():
            Service.flag = True

    @staticmethod
    # Проверка на окончание игры в целом
    def end_game(UID, player):
        match = Service.dict_match[UID]
        Model.add_match(match.player1, match.player2, player)
        Service.dict_match.pop(UID)

    # Возвращает текущую ситуации по игре
    @staticmethod
    def get_cur_situation(UID):
        match = Service.dict_match[UID]
        game = {match.player1: 0, match.player2: 0}
        if sum(Service.dict_match[UID].set.values()) != 12:
            for elem in match.score:
                if match.score[elem] == 0:
                    game[elem] = 0
                elif match.score[elem] == 1:
                    game[elem] = 15
                elif match.score[elem] == 2:
                    game[elem] = 30
                elif match.score[elem] == 3:
                    game[elem] = 40

            # Как отображать, если началось больше-меньше
            if match.score[match.player1] >= 3 and match.score[match.player2] >= 3:
                if match.score[match.player1] == match.score[match.player2]:
                    game[match.player1] = 40
                    game[match.player2] = 40
                else:
                    if match.score[match.player1] > match.score[match.player2]:
                        game[match.player1] = 'AD'
                        game[match.player2] = 40
                    else:
                        game[match.player1] = 40
                        game[match.player2] = 'AD'
        # В противном случае у нас тайм-брейк, и надо отображать очки так, как они есть
        else:
            for elem in Service.dict_match[UID].score:
                game[elem] = match.score[elem]

        set = match.set
        best_of_3 = match.best_of_3

        return match.player1, match.player2, game, set, best_of_3


