#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
in_file = "./u12_2018_2014.csv"
u18_df = pd.read_csv(in_file,encoding="UTF-8")


# In[4]:


#列の順番を整理する time,playerの列を削除
u18_df=u18_df.loc[:,['id','leagu_name','year','month','day','round','team_home','team_away','url','results_away','results_home','goal_away','goal_home']]
u18_df.head(12)
# u18_df.shape


# In[5]:


# スコアがNone(=未実施)の試合の行を削除
u18_df=u18_df[u18_df['results_away'] != "None"]
u18_df.shape


# In[6]:


# 年が変わるときの行(カラム名が入っている)を削除(一応...)
u18_df=u18_df[u18_df['results_away'] != "results_away"]
u18_df.shape


# In[ ]:





# In[7]:


# # yearに"2002"が入ってしまっているものの対処(未実装)
# u18_df=u18_df[u18_df['year'].str.match('.*,2002')!= "True"]
# u18_df.shape


# In[8]:


#idの混同を避けるため、idとyearを合わせる
u18_df["merg_id"] = u18_df["year"].astype(str)+u18_df["id"].astype(str)
u18_df["merg_id"] = u18_df["merg_id"].astype(int)
u18_df.dtypes


# In[9]:


# ここからaway


# In[10]:


#awayチームの得点者とその試合のidのみを抜き出す
df_spr_away = pd.DataFrame(u18_df['goal_away'].str.split(',', expand=True))
df_spr_away["merg_id"] =u18_df["merg_id"]


# In[11]:


# 先ほどの表から、1ゴール目のデータだけの表を作り、ゴールのない試合は削除
df_spr_away0 = pd.DataFrame({
    "goal":df_spr_away[0],
    "merg_id":df_spr_away["merg_id"]
})
df_spr_away0=df_spr_away0[df_spr_away0['goal'] != "None"] # df_spr_away0.dropna(inplace=True) はもともと"None"なので、使えない
df_spr_away0["count_away"]=int(1)
df_spr_away0.head(3)


# In[12]:


#2ゴール目以降のデータも追加
for repeat in range(1, ( (len(df_spr_away.columns)) -1) ):
    df_spr_away_n = pd.DataFrame({
    "goal":df_spr_away[repeat],
    "merg_id":df_spr_away["merg_id"],
    })
    df_spr_away_n.dropna(inplace=True)
    df_spr_away_n["count_away"]=int(1+repeat)
    df_spr_away0 = pd.concat([df_spr_away0,df_spr_away_n],sort=True,copy=False,ignore_index=True)

df_spr_away0


# In[13]:


#選手名と時間を分ける
df_spr_away0 = pd.concat([df_spr_away0,df_spr_away0["goal"].str.split("分",expand=True)],axis=1).drop("goal", axis=1)
df_spr_away0.rename(columns={0: 'time', 1: 'player'}, inplace=True)

# additional timeで別カラム
df_spr_away0 = pd.concat([df_spr_away0,df_spr_away0["time"].str.split("+",expand=True)],axis=1).drop("time", axis=1).fillna(-1)
df_spr_away0.rename(columns={0: 'n_time', 1: 'a_time'}, inplace=True)
df_spr_away0["n_time"] =df_spr_away0["n_time"].astype(int)
df_spr_away0["n_time"] =df_spr_away0["n_time"].astype(int)

# df_spr_away0["a_time"] =pd.to_numeric(df_spr_away0["a_time"], errors='coerce')

df_spr_away0


# In[14]:


# 名前に「分」が入ってる人
def inc_hunn(df):
    try:
        df.loc[ (df[3] != -1 ), "player"] = df["player"].astype(str) + str("分") + df[2].astype(str)
        del df[3]
    except:
        try:
            df.loc[ (df[2] != -1 ), "player"] = df["player"].astype(str) + str("分") + df[2].astype(str)
            del df[2]
        except:
            pass
inc_hunn(df_spr_away0)


# In[15]:


#ここからhome


# In[16]:


#homeチームの得点者とその試合のidのみを抜き出す
df_spr_home = pd.DataFrame(u18_df['goal_home'].str.split(',', expand=True))
df_spr_home["merg_id"] =u18_df["merg_id"]


# In[17]:


# 先ほどの表から、1ゴール目のデータだけの表を作り、ゴールのない試合は削除
df_spr_home0 = pd.DataFrame({
    "goal":df_spr_home[0],
    "merg_id":df_spr_home["merg_id"]
})
df_spr_home0=df_spr_home0[df_spr_home0['goal'] != "None"] # df_spr_home0.dropna(inplace=True) はもともと"None"なので、使えない
df_spr_home0["count_home"]=int(1)

#2ゴール目以降のデータも追加
for repeat in range(1, ( (len(df_spr_home.columns)) -1) ):
    df_spr_home_n = pd.DataFrame({
    "goal":df_spr_home[repeat],
    "merg_id":df_spr_home["merg_id"],
    })
    df_spr_home_n.dropna(inplace=True)
    df_spr_home_n["count_home"]=int(1+repeat)
    df_spr_home0 = pd.concat([df_spr_home0,df_spr_home_n],sort=True,copy=False,ignore_index=True)

df_spr_home0


# In[18]:


#選手名と時間を分ける
# df3 = pd.concat([df['local'], df['domain'].str.split('.', expand=True)], axis=1)
df_spr_home0 = pd.concat([df_spr_home0,df_spr_home0["goal"].str.split("分",expand=True)],axis=1).drop("goal", axis=1)
df_spr_home0.rename(columns={0: 'time', 1: 'player'}, inplace=True)

# additional timeで別カラム
df_spr_home0 = pd.concat([df_spr_home0,df_spr_home0["time"].str.split("+",expand=True)],axis=1).drop("time", axis=1).fillna(-1)
df_spr_home0.rename(columns={0: 'n_time', 1: 'a_time'}, inplace=True)
df_spr_home0["n_time"] =df_spr_home0["n_time"].astype(int)
df_spr_home0["a_time"] =df_spr_home0["a_time"].astype(int)

df_spr_home0


# In[19]:


# 名前に「分」が入ってる人(いない場合はエラー、無視して次に進む)
inc_hunn(df_spr_home0)


# In[20]:


#ここからまとめて


# In[21]:


#homeとawayを合体 #並び変える（ソート）
df_merge = pd.concat([df_spr_away0,df_spr_home0],sort=True,copy=False,ignore_index=True)
# .sort_values(["id","n_time","a_time"]).reset_index(drop=True)
df_merged = pd.merge(df_merge,u18_df, on="merg_id").sort_values(["year","id","n_time","a_time"],ascending=[False,True,True,True]).reset_index(drop=True)

df_merged["differ"] =df_merged["merg_id"].diff().fillna(1)
df_merged


# In[22]:


#idが変わる試合 かつ counthomeがnullのもの(=相手が先制しているので、counthomeは0になるべき)
df_merged.loc[(df_merged["differ"] != 0.0) &  (df_merged["count_home"].isnull() ), "count_home"] = 0
#awayも同様
df_merged.loc[(df_merged["differ"] != 0.0) &  (df_merged["count_away"].isnull() ), "count_away"] = 0

df_merged


# In[23]:


#残りのNaNは、相手ゴール分なので、一つ上の行のデータで埋める
df_merged["count_away"]=df_merged["count_away"].fillna(method='ffill')
df_merged["count_home"]=df_merged["count_home"].fillna(method='ffill')
df_merged


# In[24]:


#試合情報を結合
# df_merged = pd.merge(df_merge,u18_df, on="id").sort_values("year",ascending=False)
df_merged["goal_away"]=df_merged["count_away"].astype(int)
df_merged["goal_home"]=df_merged["count_home"].astype(int)
# del df_merged["count_away"]
# del df_merged["count_home"]
df_merged


# In[25]:


#additional timeをプラス表記に
df_merged["time"] = df_merged["n_time"]
df_merged.loc[ (df_merged["a_time"] !=-1 ), "time"] = df_merged["n_time"].astype(str) + str("+") + df_merged["a_time"].astype(str)

df_merged=df_merged.loc[:,['id','leagu_name','year','month','day','round','team_home','team_away','url','results_away','results_home','goal_away','goal_home','time','player']]
df_merged


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[26]:


# 出力CSVの名前
from pathlib import Path
newname = Path(in_file).stem
print (newname)


# In[27]:


# タイムスタンプ
import os
from datetime import datetime
t = os.path.getmtime(in_file)
# エポック秒をdatetimeに変換
dt = datetime.fromtimestamp(t)
datadate = dt.strftime('%Y%m%d%H%M')
print (datadate)


# In[28]:


# 出力
df_merged.to_csv("./adjust_" + newname + "_" + datadate + ".csv", 
          index=False   # 行インデックスを削除
         )


# In[ ]:





# In[30]:


import subprocess
subprocess.run(['jupyter', 'nbconvert', '--to', 'python', 'dataformat.ipynb'])


# In[ ]:




