#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
u18_df = pd.read_csv("U18_3_1.csv")


# In[2]:


#列の順番を整理する time,playerの列を削除
u18_df=u18_df.loc[:,['id','leagu_name','year','month','day','round','team_home','team_away','url','results_away','results_home','goal_away','goal_home']]
u18_df.head(2)


# In[3]:


# スコアがNone(=未実施)の試合の行を削除
u18_df=u18_df[u18_df['results_away'] != "None"]
u18_df.shape


# In[4]:


# ここからaway


# In[5]:


#awayチームの得点者とその試合のidのみを抜き出す
df_spr_away = pd.DataFrame(u18_df['goal_away'].str.split(',', expand=True))
df_spr_away["id"] =u18_df["id"]

df_spr_away


# In[6]:


# 先ほどの表から、1ゴール目のデータだけの表を作り、ゴールのない試合は削除
df_spr_away0 = pd.DataFrame({
    "goal":df_spr_away[0],
    "id":df_spr_away["id"]
})
df_spr_away0=df_spr_away0[df_spr_away0['goal'] != "None"] # df_spr_away0.dropna(inplace=True) はもともと"None"なので、使えない
df_spr_away0["count_away"]=int(1)
df_spr_away0.head(3)


# In[7]:


#2ゴール目以降のデータも追加
for repeat in range(1, ( (len(df_spr_away.columns)) -1) ):
    df_spr_away_n = pd.DataFrame({
    "goal":df_spr_away[repeat],
    "id":df_spr_away["id"],
    })
    df_spr_away_n.dropna(inplace=True)
    df_spr_away_n["count_away"]=int(1+repeat)
    df_spr_away0 = pd.concat([df_spr_away0,df_spr_away_n],sort=True,copy=False,ignore_index=True)

df_spr_away0


# In[8]:


#選手名と時間を分ける
# df3 = pd.concat([df['local'], df['domain'].str.split('.', expand=True)], axis=1)
df_spr_away0 = pd.concat([df_spr_away0,df_spr_away0["goal"].str.split("分",expand=True)],axis=1).drop("goal", axis=1)
df_spr_away0.rename(columns={0: 'time', 1: 'player'}, inplace=True)

# additional timeで別カラム
df_spr_away0 = pd.concat([df_spr_away0,df_spr_away0["time"].str.split("+",expand=True)],axis=1).drop("time", axis=1).fillna(-1)
df_spr_away0.rename(columns={0: 'n_time', 1: 'a_time'}, inplace=True)
df_spr_away0["n_time"] =df_spr_away0["n_time"].astype(int)
df_spr_away0["n_time"] =df_spr_away0["n_time"].astype(int)

# df_spr_away0["a_time"] =pd.to_numeric(df_spr_away0["a_time"], errors='coerce')

df_spr_away0.head()


# In[9]:


#ここからhome


# In[10]:


#homeチームの得点者とその試合のidのみを抜き出す
df_spr_home = pd.DataFrame(u18_df['goal_home'].str.split(',', expand=True))
df_spr_home["id"] =u18_df["id"]


# In[11]:


# 先ほどの表から、1ゴール目のデータだけの表を作り、ゴールのない試合は削除
df_spr_home0 = pd.DataFrame({
    "goal":df_spr_home[0],
    "id":df_spr_home["id"]
})
df_spr_home0=df_spr_home0[df_spr_home0['goal'] != "None"] # df_spr_home0.dropna(inplace=True) はもともと"None"なので、使えない
df_spr_home0["count_home"]=int(1)

#2ゴール目以降のデータも追加
for repeat in range(1, ( (len(df_spr_home.columns)) -1) ):
    df_spr_home_n = pd.DataFrame({
    "goal":df_spr_home[repeat],
    "id":df_spr_home["id"],
    })
    df_spr_home_n.dropna(inplace=True)
    df_spr_home_n["count_home"]=int(1+repeat)
    df_spr_home0 = pd.concat([df_spr_home0,df_spr_home_n],sort=True,copy=False,ignore_index=True)

df_spr_home0


# In[12]:


#選手名と時間を分ける
# df3 = pd.concat([df['local'], df['domain'].str.split('.', expand=True)], axis=1)
df_spr_home0 = pd.concat([df_spr_home0,df_spr_home0["goal"].str.split("分",expand=True)],axis=1).drop("goal", axis=1)
df_spr_home0.rename(columns={0: 'time', 1: 'player'}, inplace=True)

# additional timeで別カラム
df_spr_home0 = pd.concat([df_spr_home0,df_spr_home0["time"].str.split("+",expand=True)],axis=1).drop("time", axis=1).fillna(-1)
df_spr_home0.rename(columns={0: 'n_time', 1: 'a_time'}, inplace=True)
df_spr_home0["n_time"] =df_spr_home0["n_time"].astype(int)
df_spr_home0["a_time"] =df_spr_home0["a_time"].astype(int)

# df_spr_home0["a_time"] =pd.to_numeric(df_spr_home0["a_time"], errors='coerce')

df_spr_home0.dtypes


# In[13]:


#ここからまとめて


# In[14]:


#homeとawayを合体 #並び変える（ソート）
df_merge = pd.concat([df_spr_away0,df_spr_home0],sort=True,copy=False,ignore_index=True).sort_values(["id","n_time","a_time"]).reset_index(drop=True)

df_merge["differ"] =df_merge["id"].diff().fillna(1)
df_merge


# In[15]:


#idが変わる試合 かつ counthomeがnullのもの(=相手が先制しているので、counthomeは0になるべき)
df_merge.loc[(df_merge["differ"] != 0.0) &  (df_merge["count_home"].isnull() ), "count_home"] = 0
#awayも同様
df_merge.loc[(df_merge["differ"] != 0.0) &  (df_merge["count_away"].isnull() ), "count_away"] = 0

df_merge


# In[16]:


#残りのNaNは、相手ゴール分なので、一つ上の行のデータで埋める
df_merge["count_away"]=df_merge["count_away"].fillna(method='ffill')
df_merge["count_home"]=df_merge["count_home"].fillna(method='ffill')
df_merge


# In[17]:


#試合情報を結合
df_merged = pd.merge(df_merge,u18_df, on="id")
df_merged["goal_away"]=df_merged["count_away"].astype(int)
df_merged["goal_home"]=df_merged["count_home"].astype(int)
del df_merged["count_away"]
del df_merged["count_home"]


# In[22]:


#timeをプラス表記に
# df_merged["time"]=df_merged["n_time"].astype(object) + object("+") + df_merged["n_time"].astype(object)
# df_merged=df_merged.assign(time= df_merged["n_time"])
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





# In[18]:


import subprocess
subprocess.run(['jupyter', 'nbconvert', '--to', 'python', 'dataformat.ipynb'])


# In[19]:


# CSV出力
df_merged.to_csv("./u19_both.csv", 
          index=False   # 行インデックスを削除
         )


# In[ ]:




