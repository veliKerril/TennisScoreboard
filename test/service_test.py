from unittest import TestCase, main
from core.service import Service
from core import model


def create_info_by_win_points(player1, player2, *winner):
    UID = Service.start_new_game(player1, player2)
    for player in winner:
        Service.win_point(player, UID)
    return Service.get_cur_situation(UID)


def create_info_for_time_break(player1, player2, *winner):
    UID = Service.start_new_game(player1, player2)
    temp1 = ['Test1' for _ in range(24)]
    temp2 = ['Test2' for _ in range(24)]
    time_break = temp1 + temp2
    for player in time_break:
        Service.win_point(player, UID)
    for player in winner:
        Service.win_point(player, UID)
    return Service.get_cur_situation(UID)


# Класс, посвященный правильному начислению очков до больше-меньше внутри гейма
class ServiceTestPointsIntoGame(TestCase):
    def test_0_0(self):
        info = create_info_by_win_points('Test1', 'Test2')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)

    def test_15_0(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test1')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 15)
        self.assertEqual(score2, 0)

    def test_30_0(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test1', 'Test1')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 30)
        self.assertEqual(score2, 0)

    def test_40_0(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test1', 'Test1', 'Test1')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 40)
        self.assertEqual(score2, 0)

    def test_0_15(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test2')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 15)

    def test_0_30(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test2', 'Test2')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 30)

    def test_0_40(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test2', 'Test2', 'Test2')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 40)

    def test_15_40(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test2', 'Test2', 'Test1', 'Test2')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 15)
        self.assertEqual(score2, 40)

    def test_40_30(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test1', 'Test2', 'Test1', 'Test2', 'Test1')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 40)
        self.assertEqual(score2, 30)

    def test_40_40(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test1', 'Test2', 'Test2', 'Test1', 'Test1', 'Test2')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 40)
        self.assertEqual(score2, 40)


# Класс, посвященный проверке больше-меньше внутри обычного гейма
class ServiceTestPointsDeuce(TestCase):
    def test_AD_40(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test1', 'Test2', 'Test2', 'Test1', 'Test1', 'Test2', 'Test1')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 'AD')
        self.assertEqual(score2, 40)

    def test_40_AD(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test1', 'Test2', 'Test2', 'Test1', 'Test1', 'Test2', 'Test2')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 40)
        self.assertEqual(score2, 'AD')

    def test_40_40_4_4(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test1', 'Test2', 'Test2', 'Test1', 'Test1', 'Test2',
                                         'Test2', 'Test1')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 40)
        self.assertEqual(score2, 40)

    def test_lot_of_points_40_40(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test1', 'Test2', 'Test2', 'Test1', 'Test1', 'Test2',
                                         'Test2', 'Test1', 'Test1', 'Test2', 'Test1', 'Test2',
                                         'Test1', 'Test2', 'Test2', 'Test1', 'Test2', 'Test1')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 40)
        self.assertEqual(score2, 40)

    def test_lot_of_points_AD_40(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test1', 'Test2', 'Test2', 'Test1', 'Test1', 'Test2',
                                         'Test2', 'Test1', 'Test1', 'Test2', 'Test1', 'Test2',
                                         'Test1', 'Test2', 'Test2', 'Test1', 'Test2', 'Test1',
                                         'Test1')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 'AD')
        self.assertEqual(score2, 40)

    def test_lot_of_points_40_AD(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test1', 'Test2', 'Test2', 'Test1', 'Test1', 'Test2',
                                         'Test2', 'Test1', 'Test1', 'Test2', 'Test1', 'Test2',
                                         'Test1', 'Test2', 'Test2', 'Test1', 'Test2', 'Test1',
                                         'Test2')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 40)
        self.assertEqual(score2, 'AD')


# Класс, посвященный проверке перехода в новый сет
class ServiceTestNewSet(TestCase):
    def test_new_set_after_40_0(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test1', 'Test1', 'Test1', 'Test1')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        set1 = info[3]['Test1']
        set2 = info[3]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(set1, 1)
        self.assertEqual(set2, 0)

    def test_new_set_after_0_40(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test2', 'Test2', 'Test2', 'Test2')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        set1 = info[3]['Test1']
        set2 = info[3]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(set1, 0)
        self.assertEqual(set2, 1)

    def test_new_set_after_40_15(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test1', 'Test1', 'Test2', 'Test1', 'Test1')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        set1 = info[3]['Test1']
        set2 = info[3]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(set1, 1)
        self.assertEqual(set2, 0)

    def test_new_set_after_40_30(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test1', 'Test2', 'Test1', 'Test2', 'Test1', 'Test1')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        set1 = info[3]['Test1']
        set2 = info[3]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(set1, 1)
        self.assertEqual(set2, 0)

    def test_new_set_after_AD_40(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test1', 'Test2', 'Test1', 'Test2', 'Test1', 'Test2',
                                         'Test1', 'Test1')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        set1 = info[3]['Test1']
        set2 = info[3]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(set1, 1)
        self.assertEqual(set2, 0)

    def test_new_set_after_40_AD(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test1', 'Test2', 'Test1', 'Test2', 'Test1', 'Test2',
                                         'Test2', 'Test2')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        set1 = info[3]['Test1']
        set2 = info[3]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(set1, 0)
        self.assertEqual(set2, 1)

    def test_new_set_after_a_lot_of_point(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test1', 'Test2', 'Test2', 'Test1', 'Test1', 'Test2',
                                         'Test2', 'Test1', 'Test1', 'Test2', 'Test1', 'Test2',
                                         'Test1', 'Test2', 'Test2', 'Test1', 'Test2', 'Test1',
                                         'Test2', 'Test2')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        set1 = info[3]['Test1']
        set2 = info[3]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(set1, 0)
        self.assertEqual(set2, 1)


# Класс, посвященный проверке перехода в новый сет при окончании гейма
class ServiceTestTimeBreak(TestCase):
    def test_time_break_1_0(self):
        info = create_info_for_time_break('Test1', 'Test2',
                                          'Test1')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 1)
        self.assertEqual(score2, 0)

    def test_time_break_3_0(self):
        info = create_info_for_time_break('Test1', 'Test2',
                                          'Test1', 'Test1', 'Test1')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 3)
        self.assertEqual(score2, 0)

    def test_time_break_5_0(self):
        info = create_info_for_time_break('Test1', 'Test2',
                                          'Test1', 'Test1', 'Test1', 'Test1', 'Test1')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 5)
        self.assertEqual(score2, 0)

    def test_time_break_0_1(self):
        info = create_info_for_time_break('Test1', 'Test2',
                                          'Test2')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 1)

    def test_time_break_0_2(self):
        info = create_info_for_time_break('Test1', 'Test2',
                                          'Test2', 'Test2')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 2)

    def test_time_break_0_4(self):
        info = create_info_for_time_break('Test1', 'Test2',
                                          'Test2', 'Test2', 'Test2', 'Test2')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 4)

    def test_time_break_0_6(self):
        info = create_info_for_time_break('Test1', 'Test2',
                                          'Test2', 'Test2', 'Test2', 'Test2', 'Test2', 'Test2')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 6)

    def test_time_break_6_6(self):
        info = create_info_for_time_break('Test1', 'Test2',
                                          'Test2', 'Test2', 'Test2', 'Test2', 'Test2', 'Test2',
                                          'Test1', 'Test1', 'Test1', 'Test1', 'Test1', 'Test1')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 6)
        self.assertEqual(score2, 6)

    # Проверки на больше-меньше в тайм-брейке
    def test_time_break_7_6(self):
        info = create_info_for_time_break('Test1', 'Test2',
                                          'Test2', 'Test2', 'Test2', 'Test2', 'Test2', 'Test2',
                                          'Test1', 'Test1', 'Test1', 'Test1', 'Test1', 'Test1',
                                          'Test1')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 7)
        self.assertEqual(score2, 6)

    def test_time_break_7_8(self):
        info = create_info_for_time_break('Test1', 'Test2',
                                          'Test2', 'Test2', 'Test2', 'Test2', 'Test2', 'Test2',
                                          'Test1', 'Test1', 'Test1', 'Test1', 'Test1', 'Test1',
                                          'Test1', 'Test2', 'Test2')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 7)
        self.assertEqual(score2, 8)

    def test_time_break_10_10(self):
        info = create_info_for_time_break('Test1', 'Test2',
                                          'Test2', 'Test2', 'Test2', 'Test2', 'Test2', 'Test2',
                                          'Test1', 'Test1', 'Test1', 'Test1', 'Test1', 'Test1',
                                          'Test1', 'Test2', 'Test2', 'Test1', 'Test2', 'Test1',
                                          'Test1', 'Test2')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        self.assertEqual(score1, 10)
        self.assertEqual(score2, 10)


# Класс, посвященный проверке окончания серии сетов
class ServiceTestEndSets(TestCase):
    def test_end_sets_6_0(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test1', 'Test1', 'Test1', 'Test1',
                                         'Test1', 'Test1', 'Test1', 'Test1',
                                         'Test1', 'Test1', 'Test1', 'Test1',
                                         'Test1', 'Test1', 'Test1', 'Test1',
                                         'Test1', 'Test1', 'Test1', 'Test1',
                                         'Test1', 'Test1', 'Test1', 'Test1',
                                         'Test1', 'Test1', 'Test1', 'Test1')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        set1 = info[3]['Test1']
        set2 = info[3]['Test2']
        best_or_3_1 = info[4]['Test1']
        best_or_3_2 = info[4]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(set1, 0)
        self.assertEqual(set2, 0)
        self.assertEqual(best_or_3_1, 1)
        self.assertEqual(best_or_3_2, 0)

    def test_end_sets_0_6(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test2', 'Test2', 'Test2', 'Test2',
                                         'Test2', 'Test2', 'Test2', 'Test2',
                                         'Test2', 'Test2', 'Test2', 'Test2',
                                         'Test2', 'Test2', 'Test2', 'Test2',
                                         'Test2', 'Test2', 'Test2', 'Test2',
                                         'Test2', 'Test2', 'Test2', 'Test2',
                                         'Test2', 'Test2', 'Test2', 'Test2')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        set1 = info[3]['Test1']
        set2 = info[3]['Test2']
        best_or_3_1 = info[4]['Test1']
        best_or_3_2 = info[4]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(set1, 0)
        self.assertEqual(set2, 0)
        self.assertEqual(best_or_3_1, 0)
        self.assertEqual(best_or_3_2, 1)

    def test_end_sets_6_3(self):
        info = create_info_by_win_points('Test1', 'Test2',
                                         'Test1', 'Test1', 'Test1', 'Test1',
                                         'Test2', 'Test2', 'Test2', 'Test2',
                                         'Test1', 'Test1', 'Test1', 'Test1',
                                         'Test1', 'Test1', 'Test1', 'Test1',
                                         'Test2', 'Test2', 'Test2', 'Test2',
                                         'Test1', 'Test1', 'Test1', 'Test1',
                                         'Test1', 'Test1', 'Test1', 'Test1',
                                         'Test2', 'Test2', 'Test2', 'Test2',
                                         'Test1', 'Test1', 'Test1', 'Test1',
                                         'Test1', 'Test1', 'Test1', 'Test1')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        set1 = info[3]['Test1']
        set2 = info[3]['Test2']
        best_or_3_1 = info[4]['Test1']
        best_or_3_2 = info[4]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(set1, 0)
        self.assertEqual(set2, 0)
        self.assertEqual(best_or_3_1, 1)
        self.assertEqual(best_or_3_2, 0)

    # Окончание серии сетов после таймбрейка
    def test_end_sets_after_time_break_7_5(self):
        info = create_info_for_time_break('Test1', 'Test2',
                                          'Test1', 'Test1', 'Test1', 'Test1', 'Test1',
                                          'Test2', 'Test2', 'Test2', 'Test2', 'Test2',
                                          'Test1', 'Test1')
        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        set1 = info[3]['Test1']
        set2 = info[3]['Test2']
        best_or_3_1 = info[4]['Test1']
        best_or_3_2 = info[4]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(set1, 0)
        self.assertEqual(set2, 0)
        self.assertEqual(best_or_3_1, 1)
        self.assertEqual(best_or_3_2, 0)

    def test_end_sets_after_time_break_7_0(self):
        info = create_info_for_time_break('Test1', 'Test2',
                                          'Test1', 'Test1', 'Test1', 'Test1', 'Test1', 'Test1', 'Test1')

        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        set1 = info[3]['Test1']
        set2 = info[3]['Test2']
        best_or_3_1 = info[4]['Test1']
        best_or_3_2 = info[4]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(set1, 0)
        self.assertEqual(set2, 0)
        self.assertEqual(best_or_3_1, 1)
        self.assertEqual(best_or_3_2, 0)

    # Окончания серии сетов после больше-меньше в тайм-брейке
    def test_end_sets_after_time_break_8_6(self):
        info = create_info_for_time_break('Test1', 'Test2',
                                          'Test1', 'Test2', 'Test1', 'Test2', 'Test1', 'Test2',
                                          'Test1', 'Test2', 'Test1', 'Test2', 'Test1', 'Test2',
                                          'Test1', 'Test1')

        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        set1 = info[3]['Test1']
        set2 = info[3]['Test2']
        best_or_3_1 = info[4]['Test1']
        best_or_3_2 = info[4]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(set1, 0)
        self.assertEqual(set2, 0)
        self.assertEqual(best_or_3_1, 1)
        self.assertEqual(best_or_3_2, 0)

    def test_end_sets_after_time_break_10_12(self):
        info = create_info_for_time_break('Test1', 'Test2',
                                          'Test1', 'Test2', 'Test1', 'Test2', 'Test1', 'Test2',
                                          'Test1', 'Test2', 'Test1', 'Test2', 'Test1', 'Test2',
                                          'Test1', 'Test2', 'Test2', 'Test1', 'Test2', 'Test1',
                                          'Test1', 'Test2', 'Test2', 'Test2')

        score1 = info[2]['Test1']
        score2 = info[2]['Test2']
        set1 = info[3]['Test1']
        set2 = info[3]['Test2']
        best_or_3_1 = info[4]['Test1']
        best_or_3_2 = info[4]['Test2']
        self.assertEqual(score1, 0)
        self.assertEqual(score2, 0)
        self.assertEqual(set1, 0)
        self.assertEqual(set2, 0)
        self.assertEqual(best_or_3_1, 0)
        self.assertEqual(best_or_3_2, 1)


if __name__ == '__main__':
    main()
