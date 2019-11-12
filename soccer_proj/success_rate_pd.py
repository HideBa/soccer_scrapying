import pandas as pd
import numpy as np


class GetSuccessRatio:

    def get_u18_url_nums(self):
        df_u18_all = pd.read_csv('results_all/all_year_u18_2.csv')
        no_url_nums = df_u18_all['results_home'] == 'None'
        no_url_nums = no_url_nums.sum()
        print('u18_no url nums ====== ' + str(no_url_nums))
        record_num_game_url = len(df_u18_all)
        record_num_record = record_num_game_url
        record_num_game_url_exist = 0
        record_num_game_url_noexist = 0
        record_num_game_url_noexist += no_url_nums
        record_num_game_unknown = 0
        record_num_game_url_exist += len(df_u18_all) - \
            record_num_game_url_noexist
        ratio_success = (record_num_game_url_exist/record_num_game_url) * 100
        ratio_failure = (record_num_game_url_noexist/record_num_game_url) * 100

        return record_num_record, record_num_game_url, record_num_game_url_exist, record_num_game_url_noexist, record_num_game_unknown, ratio_success, ratio_failure

    def get_u12_url_nums(self):
        df_u12_all = pd.read_csv('results_all/all_year_u12.csv')
        record_num_game_url = len(df_u12_all)
        record_num_record = record_num_game_url
        record_num_game_url_exist = 0
        record_num_game_url_noexist = 0
        record_num_game_unknown = 0
        record_num_game_url_exist += len(df_u12_all)
        ratio_success = (record_num_game_url_exist/record_num_game_url) * 100
        ratio_failure = (record_num_game_url_noexist/record_num_game_url) * 100
        return record_num_record, record_num_game_url, record_num_game_url_exist, record_num_game_url_noexist, record_num_game_unknown, ratio_success, ratio_failure

    def get_u15_url_nums(self):
        df_u15_success_all = pd.read_csv('results_all/all_year_u15.csv')
        # df_u15_2013 = pd.read_csv('results_all/soccer_2013.csv')
        # df_u15_2007 = pd.read_csv('results_all/soccer_2007.csv')
        df_u15_2008_2009_rounds = pd.read_csv('results_all/u15_2008_2009.csv')
        df_u15_2007_rounds = pd.read_csv('results_all/u15_2007.csv')
        # df_u15_2006 = pd.read_csv('results_all/soccer_2006.csv')
        df_u15_2006_rounds = pd.read_csv('results_all/u15_2006.csv')
        df_u15_2005_rounds = pd.read_csv('results_all/u15_2005.csv')

        record_num_game_url = len(df_u15_success_all) + len(df_u15_2008_2009_rounds) + len(
            df_u15_2007_rounds) + len(df_u15_2006_rounds) + len(df_u15_2005_rounds)
        record_num_record = record_num_game_url
        record_num_game_url_exist = 0
        record_num_game_url_exist += len(df_u15_success_all)
        record_num_game_url_noexist = 0
        record_num_game_unknown = 0
        record_num_game_url_noexist += len(df_u15_2008_2009_rounds) + len(df_u15_2007_rounds) + len(
            df_u15_2006_rounds) + len(df_u15_2005_rounds)
        ratio_success = (record_num_game_url_exist/record_num_game_url) * 100
        ratio_failure = (record_num_game_url_noexist/record_num_game_url) * 100
        return record_num_record, record_num_game_url, record_num_game_url_exist, record_num_game_url_noexist, record_num_game_unknown, ratio_success, ratio_failure

    def make_u15_no_url_frame(self):
        df_u15_2008_2009_rounds = pd.read_csv('results_all/u15_2008_2009.csv')
        df_u15_2007_rounds = pd.read_csv('results_all/u15_2007.csv')
        df_u15_2006_rounds = pd.read_csv('results_all/u15_2006.csv')
        df_u15_2005_rounds = pd.read_csv('results_all/u15_2005.csv')
        df = pd.concat([df_u15_2008_2009_rounds, df_u15_2007_rounds,
                        df_u15_2006_rounds, df_u15_2005_rounds], ignore_index=True)
        df = df.drop(columns='goal_away')
        df = df.drop(columns='goal_home')
        df = df.drop(columns='id')
        df = df.drop(columns='player')
        df = df.drop(columns='time')
        df = df.drop(columns='round')
        print(df)
        df.to_csv("result_else/u15.csv")

    def sample(self):
        df_u18 = pd.read_csv('results_all/all_year_u18_2.csv')
        nums = df_u18['year'] == '2019'
        print("num===" + str(nums.sum()))
    # def get_summary(self):
    #     u18_1, u18_2, u18_3, u18_4, u18_5, u18_6, u18_7 = self.get_u18_url_nums()
    #     print("u18-----------------------------------------")
    #     print("record_num_game_url_exist=" + str(u18_1))
    #     print("record_num_url_noexist=" + str(u18_2))
    #     print("ratio_success=" + str(u18_3))
    #     print("ratio_failure=" + str(u18_4))

    #     u15_1, u15_2, u15_3, u15_4, u15_5, u15_6, u15_7 = self.get_u15_url_nums()
    #     print("u15-----------------------------------------")
    #     print("record_num_game_url_exist=" + str(u15_1))
    #     print("record_num_url_noexist=" + str(u15_2))
    #     print("ratio_success=" + str(u15_3))
    #     print("ratio_failure=" + str(u15_4))

    #     u12_1, u12_2, u12_3, u12_4, u12_5, u12_6, u12_7 = self.get_u12_url_nums()

    #     print("u15-----------------------------------------")
    #     print("record_num_game_url_exist=" + str(u12_1))
    #     print("record_num_url_noexist=" + str(u12_2))
    #     print("ratio_success=" + str(u12_3))
    #     print("ratio_failure=" + str(u12_4))

    def make_frame(self):
        df = pd.DataFrame(np.arange(24).reshape(3, 8), columns=[
            'status', 'record_num_game_url', 'record_num_record', 'record_num_game_url_exist', 'record_num_game_url_noexist', 'record_num_game_unknown', 'ratio_success', 'ratio_failure'],
            index=['高円宮杯　JFA U-18サッカープレミアリーグ', '高円宮杯　JFA 第31回全日本U-15サッカー選手権大会', 'JFA 第43回全日本U-12サッカー選手権大会'])
        # print(df)
        u18_1, u18_2, u18_3, u18_4, u18_5, u18_6, u18_7 = self.get_u18_url_nums()
        u15_1, u15_2, u15_3, u15_4, u15_5, u15_6, u15_7 = self.get_u15_url_nums()
        u12_1, u12_2, u12_3, u12_4, u12_5, u12_6, u12_7 = self.get_u12_url_nums()
        df.loc['高円宮杯　JFA U-18サッカープレミアリーグ', :] = ['Done',
                                                 u18_1, u18_2, u18_3, u18_4, u18_5, u18_6, u18_7]
        df.loc['高円宮杯　JFA 第31回全日本U-15サッカー選手権大会', :] = ['Done',
                                                      u15_1, u15_2, u15_3, u15_4, u15_5, u15_6, u15_7]
        df.loc['JFA 第43回全日本U-12サッカー選手権大会', :] = ['Done',
                                                 u12_1, u12_2, u12_3, u12_4, u12_5, u12_6, u12_7]
        print(df)
        df.to_csv("result_summary/success_ratio.csv")


test = GetSuccessRatio()
# test.get_summary()
test.make_frame()
# test.make_u15_no_url_frame()
# test.sample()
