import pandas as pd
import numpy as np


class GetSuccessRatio:

    def get_u18_url_nums(self):
        df_u18_all = pd.read_csv('results/soccer_all.csv')
        record_num_game_url = len(df_u18_all)
        record_num_game_url_exist = 0
        record_num_game_url_noexist = 0
        record_num_game_url_exist += len(df_u18_all)
        ratio_success = (record_num_game_url_exist/record_num_game_url) * 100
        ratio_failure = (record_num_game_url_noexist/record_num_game_url) * 100
        return record_num_game_url, record_num_game_url_exist, record_num_game_url_noexist, ratio_success, ratio_failure

    def get_u12_url_nums(self):
        df_u12_all = pd.read_csv('results_u12/soccer_all.csv')
        record_num_game_url = len(df_u12_all)
        record_num_game_url_exist = 0
        record_num_game_url_noexist = 0
        record_num_game_url_exist += len(df_u12_all)
        ratio_success = (record_num_game_url_exist/record_num_game_url) * 100
        ratio_failure = (record_num_game_url_noexist/record_num_game_url) * 100
        return record_num_game_url, record_num_game_url_exist, record_num_game_url_noexist, ratio_success, ratio_failure

    def get_u15_url_nums(self):
        df_u15_2018 = pd.read_csv('results_u15/soccer_2018.csv')
        df_u15_2013 = pd.read_csv('results_u15/soccer_2013.csv')
        df_u15_2007 = pd.read_csv('results_u15/soccer_2007.csv')
        df_u15_2007_rounds = pd.read_csv('results_u15/2007_rounds.csv')
        df_u15_2006 = pd.read_csv('results_u15/soccer_2006.csv')
        df_u15_2006_rounds = pd.read_csv('results_u15/2006_rounds.csv')
        df_u15_2005_rounds = pd.read_csv('results_u15/2005_rounds.csv')

        record_num_game_url = len(df_u15_2018) + len(df_u15_2013) + len(df_u15_2007) + len(
            df_u15_2007_rounds) + len(df_u15_2006) + len(df_u15_2006_rounds) + len(df_u15_2005_rounds)
        record_num_game_url_exist = 0
        record_num_game_url_exist += len(df_u15_2018) + len(df_u15_2013) + \
            len(df_u15_2007) + len(df_u15_2006)
        record_num_game_url_noexist = 0
        record_num_game_url_noexist += len(df_u15_2007_rounds) + len(
            df_u15_2006_rounds) + len(df_u15_2005_rounds)
        ratio_success = (record_num_game_url_exist/record_num_game_url) * 100
        ratio_failure = (record_num_game_url_noexist/record_num_game_url) * 100
        return record_num_game_url, record_num_game_url_exist, record_num_game_url_noexist, ratio_success, ratio_failure

    def get_summary(self):
        u18_1, u18_2, u18_3, u18_4, u18_5 = self.get_u18_url_nums()
        # print("u18-----------------------------------------")
        # print("record_num_game_url_exist=" + str(u18_1))
        # print("record_num_url_noexist=" + str(u18_2))
        # print("ratio_success=" + str(u18_3))
        # print("ratio_failure=" + str(u18_4))

        u15_1, u15_2, u15_3, u15_4, u15_5 = self.get_u15_url_nums()
        # print("u15-----------------------------------------")
        # print("record_num_game_url_exist=" + str(u15_1))
        # print("record_num_url_noexist=" + str(u15_2))
        # print("ratio_success=" + str(u15_3))
        # print("ratio_failure=" + str(u15_4))

        u12_1, u12_2, u12_3, u12_4, u12_5 = self.get_u12_url_nums()

        # print("u15-----------------------------------------")
        # print("record_num_game_url_exist=" + str(u12_1))
        # print("record_num_url_noexist=" + str(u12_2))
        # print("ratio_success=" + str(u12_3))
        # print("ratio_failure=" + str(u12_4))

    def make_frame(self):
        df = pd.DataFrame(np.arange(24).reshape(3, 8), columns=[
                          'status', 'record_num_game_url', 'record_num_record', 'record_num_game_url_exist', 'record_num_game_url_noexist', 'record_num_game_unknown', 'ratio_success', 'ratio_failure'],
                          index=['高円宮杯　JFA U-18サッカープレミアリーグ', '高円宮杯　JFA 第31回全日本U-15サッカー選手権大会', 'JFA 第43回全日本U-12サッカー選手権大会'])
        # print(df)
        u18_1, u18_2, u18_3, u18_4, u18_5 = self.get_u18_url_nums()
        u15_1, u15_2, u15_3, u15_4, u15_5 = self.get_u15_url_nums()
        u12_1, u12_2, u12_3, u12_4, u12_5 = self.get_u12_url_nums()
        df.loc['高円宮杯　JFA U-18サッカープレミアリーグ', :] = ['Done',
                                                 u18_1, 'None', u18_2, u18_3, 'None', u18_4, u18_5]
        df.loc['高円宮杯　JFA 第31回全日本U-15サッカー選手権大会', :] = ['Done',
                                                      u15_1, 'None', u15_2, u15_3, 'None', u15_4, u15_5]
        df.loc['JFA 第43回全日本U-12サッカー選手権大会', :] = ['Done',
                                                 u12_1, 'None', u12_2, u12_3, 'None', u12_4, u12_5]
        print(df)
        df.to_csv("result_summary/success_ratio.csv")


test = GetSuccessRatio()
test.get_summary()
test.make_frame()
