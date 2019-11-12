import pandas as pd
import argparse

def kessyo(u18_df):
    kes_df = u18_df[u18_df["id"].isnull()]
    kes_df = kes_df.sort_values(["year","month","day"],ascending=[False,True,True]).reset_index(drop=True)
    kes_df["id"] = range(1,(len(kes_df))+1)
    #2006,2007の6試合のidがないなら↓
    # kes_df["round"] = ["準決勝1", "準決勝2", "決勝","準決勝1", "準決勝2", "決勝"]
    new_df = pd.concat([u18_df,kes_df],sort=True,copy=False,ignore_index=True)
    return new_df

def normalize(u18_df):
    if u18_df["id"].isnull().sum() != 0:
        u18_df=kessyo(u18_df)
        u18_df = u18_df[u18_df["id"].isnull() != True ]
    else:
        pass
    u18_df["id"]= u18_df["id"].astype(int)

    #列の順番を整理する time,playerの列を削除
    u18_df=u18_df.loc[:,['id','leagu_name','year','month','day','round','team_home','team_away','url','results_away','results_home','goal_away','goal_home']]
    # スコアがNone(=未実施)の試合の行を削除
    u18_df['results_away']=u18_df['results_away'].astype(str)
    u18_df=u18_df[u18_df['results_away'] != "None"]
    # 年が変わるときの行(カラム名が入っている行)を削除(一応...)
    u18_df=u18_df[u18_df['results_away'] != "results_away"]
    u18_df['results_away']=u18_df['results_away'].astype(int)
    
    #eastとwestでidかぶりを防ぐ：east→77  west→88
    u18_df["url"] = u18_df["url"].astype(str)
    u18_df["area"]=int("77")
    u18_df.loc[(u18_df['url'].str.contains('west')), "area"] = int("88")
    #idの混同を避けるため、idとyearを合わせる
    u18_df["merg_id"] = u18_df["year"].astype(str)+u18_df["area"].astype(str)+u18_df["id"].astype(str)
    u18_df["merg_id"] = u18_df["merg_id"].astype(int)
    return u18_df

# ここからaway
def sprit_away(u18_df):
    #awayチームの得点者とその試合のidのみを抜き出す
    df_spr_away = pd.DataFrame(u18_df['goal_away'].str.split(',', expand=True))
    df_spr_away["merg_id"] =u18_df["merg_id"]
    return df_spr_away

def goal_frame(df_spr):
    # 先ほどの表から、1ゴール目のデータだけの表を作る
    df_spr_0 = pd.DataFrame({
        "goal":df_spr[0],
        "merg_id":df_spr["merg_id"]
    })
    df_spr_0["count_away"]=int("1")
    #2ゴール目以降のデータも追加
    for repeat in range(1, ( (len(df_spr.columns)) -2) ):
        df_spr_n = pd.DataFrame({
        "goal":df_spr[repeat],
        "merg_id":df_spr["merg_id"],
        })
        df_spr_n["count_away"]=int(repeat+1)
        df_spr_0 = pd.concat([df_spr_0,df_spr_n],sort=True,copy=False,ignore_index=True)
    # 空白やNoneを消す
    df_spr_0 = df_spr_0[df_spr_0['goal'] != "None"]
    df_spr_0 = df_spr_0[df_spr_0['goal'] != ""]
    df_spr_0.dropna(inplace=True) 
    return df_spr_0
# ！注意！ homeに使うときは、count_awayをcount_homeにrename！

# 名前に「分」が入ってる人
def inc_hunn(df):
    try:
        df.loc[ (df[3] != -1 ), "player"] = df["player"].astype(str) + str("分") + df[2].astype(str)
        del df[3]
        return df
    except:
        try:
            df.loc[ (df[2] != -1 ), "player"] = df["player"].astype(str) + str("分") + df[2].astype(str)
            del df[2]
            return df
        except:
            return df

def sprit_pat(df):
    #選手名と時間を分ける
    df = pd.concat([df,df["goal"].str.split("分",expand=True)],axis=1).drop("goal", axis=1)
    df.rename(columns={0: 'time', 1: 'player'}, inplace=True)
    # additional timeで別カラム
    try:
        df = pd.concat([df,df["time"].str.split("+",expand=True)],axis=1).drop("time", axis=1).fillna(-1)
        df.rename(columns={0: 'n_time', 1: 'a_time'}, inplace=True)
        df["n_time"] =df["n_time"].astype(int)
        df["a_time"] =df["a_time"].astype(int)
    except:
        df["n_time"] =df["n_time"].astype(int)
        df["a_time"] =int("-1")
    #名前に「分」が入ってる人
    df=inc_hunn(df)
    return df

#ここからhome
def home_all(u18_df):
    #homeチームの得点者とその試合のidのみを抜き出す
    df_spr_home = pd.DataFrame(u18_df['goal_home'].str.split(',', expand=True))
    df_spr_home["merg_id"] =u18_df["merg_id"]
    df_spr_home0=goal_frame(df_spr_home)
    df_spr_home0.rename(columns={"count_away": 'count_home'}, inplace=True) 
    df_spr_home0=sprit_pat(df_spr_home0)
    return df_spr_home0

#ここからまとめて
def noside(u18_df,df_spr_away0,df_spr_home0):
    #homeとawayを合体 #並び変える（ソート）
    df_merge = pd.concat([df_spr_away0,df_spr_home0],sort=True,copy=False,ignore_index=True)

    #試合情報を結合
    u18_df["id"]=u18_df["id"].astype(int)
    df_merged = pd.merge(df_merge,u18_df, on="merg_id").sort_values(["year","merg_id","n_time","a_time"],ascending=[False,True,True,True]).reset_index(drop=True)
    
    return df_merged

def counting(df):
    #試合が変わる行を示すカラムを作る（一行目はNaNになるので、1で埋める)
    df["differ"] =df["merg_id"].diff().fillna(1)
    
    #idが変わる試合 かつ counthomeがnullのもの(=相手が先制しているので、counthomeは0になるべき)
    df.loc[(df["differ"] != 0.0) &  (df["count_home"].isnull() ), "count_home"] = 0
    df.loc[(df["differ"] != 0.0) &  (df["count_away"].isnull() ), "count_away"] = 0

    #残りのNaNは、相手ゴール分なので、一つ上の行のデータで埋める
    df["count_away"]=df["count_away"].fillna(method='ffill')
    df["count_home"]=df["count_home"].fillna(method='ffill')
    
    #整数表記にする
    df["goal_away"]=df["count_away"].astype(int)
    df["goal_home"]=df["count_home"].astype(int)
    
    #additional timeをプラス表記に
    df["time"] = df["n_time"]
    df.loc[ (df["a_time"] !=-1 ), "time"] = df["n_time"].astype(str) + str("+") + df["a_time"].astype(str)

    df=df.loc[:,['id','leagu_name','year','month','day','round','team_home','team_away','url','results_away','results_home','goal_away','goal_home','time','player']]

    return df

def naming(in_file):
    # 出力CSVの名前
    from pathlib import Path
    newname = Path(in_file).stem
    # タイムスタンプ
    import os
    from datetime import datetime
    t = os.path.getmtime(in_file)
    # エポック秒をdatetimeに変換
    dt = datetime.fromtimestamp(t)
    # datadate = dt.strftime('%Y%m%d%H%M')で、「年」から
    datadate = dt.strftime('%m%d%H%M')

    return newname + "_" + datadate

def main(u18_df,in_file):
    u18_df=normalize(u18_df)
    df_spr_away = sprit_away(u18_df)
    df_spr_away0=goal_frame(df_spr_away)
    df_spr_away0=sprit_pat(df_spr_away0)
    df_spr_home0 = home_all(u18_df)
    df_merged = noside(u18_df,df_spr_away0,df_spr_home0)
    df_merged = counting(df_merged)
    adjname = naming(in_file)
    return (df_merged, adjname)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(epilog="which file should be adjusted?")
    parser.add_argument('-f', '--importfile', required=True)
    args = parser.parse_args()
    in_file = "./"+ args.importfile +".csv"
    u18_df = pd.read_csv(in_file,encoding="UTF-8")
    # 抽出 (任意)
    # u18_df=u18_df[u18_df['year'] != int("2013")]

    #関数の実行
    df_merged, adjname = main(u18_df,in_file)
    #CSV出力
    df_merged.to_csv("./adj_" + adjname + ".csv", 
          index=False   # インデックスを削除
         )


    if df_merged.isnull().values.sum()==0:
        print("adj_{0}.csv を正常に出力しました。".format(adjname))
        print("データ個数：\n{0}".format(df_merged.count()) )   
    else:
        print("adj_{0}.csv は出力されましたが、問題があります。".format(adjname))
        print("データ個数：\n{0}\n".format(df_merged.count()) )   
        print("欠損値：\n{0}\n".format(df_merged.isnull().sum()))