#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
in_file = "./soccer_2006.csv"
u18_df = pd.read_csv(in_file,encoding="UTF-8")


# In[2]:


# 抽出(任意)
# u18_df=u18_df[u18_df['year'] == int("2013")]
u18_df = u18_df[u18_df["id"].isnull() != True ]

# u18_df


# In[3]:


def normalize(u18_df):
    #列の順番を整理する time,playerの列を削除
    u18_df=u18_df.loc[:,['id','leagu_name','year','month','day','round','team_home','team_away','url','results_away','results_home','goal_away','goal_home']]
    # スコアがNone(=未実施)の試合の行を削除
    u18_df=u18_df[u18_df['results_away'] != "None"]
    # 年が変わるときの行(カラム名が入っている行)を削除(一応...)
    u18_df=u18_df[u18_df['results_away'] != "results_away"]
    #idの混同を避けるため、idとyearを合わせる
    u18_df["merg_id"] = u18_df["year"].astype(str)+u18_df["id"].astype(str)
    u18_df["merg_id"] = u18_df["merg_id"].astype(int)
    return u18_df

u18_df=normalize(u18_df)
u18_df


# In[4]:


# ここからaway


# In[5]:


def sprit_away(u18_df):
    #awayチームの得点者とその試合のidのみを抜き出す
    df_spr_away = pd.DataFrame(u18_df['goal_away'].str.split(',', expand=True))
    df_spr_away["merg_id"] =u18_df["merg_id"]
    return df_spr_away
df_spr_away = sprit_away(u18_df)
df_spr_away.head()


# In[6]:


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

df_spr_away0=goal_frame(df_spr_away)
df_spr_away0.shape
# ！注意！ homeに使うときは、count_awayをcount_homeにrename！


# In[7]:


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


# In[8]:


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

df_spr_away0=sprit_pat(df_spr_away0)
df_spr_away0


# In[ ]:





# In[9]:


#ここからhome


# In[10]:


def sprit_home(u18_df):
    #homeチームの得点者とその試合のidのみを抜き出す
    df_spr_home = pd.DataFrame(u18_df['goal_home'].str.split(',', expand=True))
    df_spr_home["merg_id"] =u18_df["merg_id"]
    return df_spr_home
df_spr_home = sprit_home(u18_df)
df_spr_home.head()


# In[11]:


df_spr_home0=goal_frame(df_spr_home)
#home用にrename
df_spr_home0.rename(columns={"count_away": 'count_home'}, inplace=True)


# In[12]:


df_spr_home0=sprit_pat(df_spr_home0)
df_spr_home0


# In[13]:


#ここからまとめて


# In[17]:


def noside(u18_df,df_spr_away0,df_spr_home0):
    #homeとawayを合体 #並び変える（ソート）
    df_merge = pd.concat([df_spr_away0,df_spr_home0],sort=True,copy=False,ignore_index=True)

    #試合情報を結合
    u18_df["id"]=u18_df["id"].astype(int)
    df_merged = pd.merge(df_merge,u18_df, on="merg_id").sort_values(["year","merg_id","n_time","a_time"],ascending=[False,True,True,True]).reset_index(drop=True)
    
    return df_merged

df_merged = noside(u18_df,df_spr_away0,df_spr_home0)
df_merged


# In[18]:


def counting(df_merged):
    #試合が変わる行を示すカラムを作る
    df_merged["differ"] =df_merged["merg_id"].diff().fillna(1)
    
    #idが変わる試合 かつ counthomeがnullのもの(=相手が先制しているので、counthomeは0になるべき)
    df_merged.loc[(df_merged["differ"] != 0.0) &  (df_merged["count_home"].isnull() ), "count_home"] = 0
    df_merged.loc[(df_merged["differ"] != 0.0) &  (df_merged["count_away"].isnull() ), "count_away"] = 0

    #残りのNaNは、相手ゴール分なので、一つ上の行のデータで埋める
    df_merged["count_away"]=df_merged["count_away"].fillna(method='ffill')
    df_merged["count_home"]=df_merged["count_home"].fillna(method='ffill')
    
    #整数表記にする
    df_merged["goal_away"]=df_merged["count_away"].astype(int)
    df_merged["goal_home"]=df_merged["count_home"].astype(int)
    
    #additional timeをプラス表記に
    df_merged["time"] = df_merged["n_time"]
    df_merged.loc[ (df_merged["a_time"] !=-1 ), "time"] = df_merged["n_time"].astype(str) + str("+") + df_merged["a_time"].astype(str)

    df_merged=df_merged.loc[:,['id','leagu_name','year','month','day','round','team_home','team_away','url','results_away','results_home','goal_away','goal_home','time','player']]

    return df_merged

df_merged = counting(df_merged)


# In[19]:


df_merged


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[17]:


# 出力CSVの名前
from pathlib import Path
newname = Path(in_file).stem
# newname="u12_2012_2011"
print (newname)


# In[18]:


# タイムスタンプ
import os
from datetime import datetime
t = os.path.getmtime(in_file)
# エポック秒をdatetimeに変換
dt = datetime.fromtimestamp(t)
# datadate = dt.strftime('%Y%m%d%H%M')
datadate = dt.strftime('%m%d%H%M')
print (datadate)


# In[23]:


# 出力
df_merged.to_csv("./adj_" + newname + "_" + datadate + ".csv", 
          index=False   # インデックスを削除
         )


# In[ ]:





# In[21]:


import subprocess
subprocess.run(['jupyter', 'nbconvert', '--to', 'python', 'dataformat_classify.ipynb'])

