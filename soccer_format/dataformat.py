#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


u18_df = pd.read_csv("U18_3_1.csv")


# In[3]:


#列の順番を整理する
#最後にやりたい
# u18_df=u18_df.loc[:,['id','leagu_name','year','month','day','round','team_home','team_away','goal_away','goal_home','results_away','results_home','url','time','player']]
# time,playerの列を削除
u18_df=u18_df.loc[:,['id','leagu_name','year','month','day','round','team_home','team_away','url','results_away','results_home','goal_away','goal_home']]
u18_df.head(2)


# In[4]:


# スコアがNone(=未実施)の試合の行を削除
u18_df=u18_df[u18_df['results_away'] != "None"]
u18_df.tail(3)


# In[5]:


#awayチームの得点者とその試合のidのみを抜き出す
df_spr_away = pd.DataFrame(u18_df['goal_away'].str.split(',', expand=True))
df_spr_away["id"] =u18_df["id"]

# df_spr_away.head()
df_spr_away


# In[6]:


# 先ほどの表から、1ゴール目のデータだけの表を作り、ゴールのない試合は削除
df_spr_away0 = pd.DataFrame({
    "goal":df_spr_away[0],
    "id":df_spr_away["id"]
})
df_spr_away0=df_spr_away0[df_spr_away0['goal'] != "None"] # df_spr_away0.dropna(inplace=True) はもともと"None"なので、使えない
df_spr_away0["count_away"]=1
df_spr_away0.head(3)


# In[7]:


#2ゴール目以降のデータも追加
for repeat in range(1, ( (len(df_spr_away.columns)) -1) ):
    df_spr_away_n = pd.DataFrame({
    "goal":df_spr_away[repeat],
    "id":df_spr_away["id"],
    })
    df_spr_away_n.dropna(inplace=True)
    df_spr_away_n["count_away"]=1+repeat
    df_spr_away0 = pd.concat([df_spr_away0,df_spr_away_n],sort=True,copy=False,ignore_index=True)

df_spr_away0


# In[8]:


#選手名と時間を分ける
# df3 = pd.concat([df['local'], df['domain'].str.split('.', expand=True)], axis=1)
df_spr_away0 = pd.concat([df_spr_away0,df_spr_away0["goal"].str.split("分",expand=True)],axis=1).drop("goal", axis=1)
df_spr_away0.rename(columns={0: 'time', 1: 'player'}, inplace=True)
df_spr_away0.head()


# In[9]:


#並び変える（ソート）
#最後にやりたい
df_spr_away0=df_spr_away0.sort_values(["id","time"])
df_spr_away0.head()


# In[10]:


#試合情報を結合
df_away = pd.merge(df_spr_away0,u18_df, on="id")
df_away=df_away.loc[:,['id','leagu_name','year','month','day','round','team_home','team_away','url','results_away','results_home','goal_away','goal_home','time','player','count_away']]

df_away


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[11]:


# CSV出力
df_away.to_csv("./u18_19_away.csv", 
          index=False   # 行インデックスを削除
         )

