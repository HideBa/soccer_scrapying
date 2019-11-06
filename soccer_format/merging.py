#!/usr/bin/env python
# coding: utf-8

# In[1]:


import glob
import pandas as pd


# In[2]:


in_file = "./datatomerge"
files = glob.glob(in_file+"/*.csv")
frame = pd.DataFrame()
listo = []
for fl in files:
    df = pd.read_csv(fl,index_col=None, header=0)
    listo.append(df)
all_df = pd.concat(listo)
all_df.head()


# In[3]:


all_df = pd.concat([all_df,all_df["time"].str.split("+",expand=True)],axis=1).drop("time", axis=1).fillna(-1)
all_df.rename(columns={0: 'n_time', 1: 'a_time'}, inplace=True)
all_df["n_time"] =all_df["n_time"].astype(int)
all_df["a_time"] =all_df["a_time"].astype(int)


# In[4]:


all_df.sort_values(["year","leagu_name","id","n_time","a_time"],ascending=[True,False,True,True,True])
all_df.reset_index(drop=True, inplace=True)
all_df


# In[5]:


#additional timeをプラス表記に
all_df["time"] = all_df["n_time"]
all_df.loc[ (all_df["a_time"] !=-1 ), "time"] = all_df["n_time"].astype(str) + str("+") + all_df["a_time"].astype(str)


# In[6]:


#列の整理
all_df=all_df.loc[:,['id','leagu_name','year','month','day','round','team_home','team_away','url','results_away','results_home','goal_away','goal_home','time','player']]


# In[7]:


all_df


# In[8]:


# タイムスタンプ
import os
from datetime import datetime
t = os.path.getmtime(in_file)
# エポック秒をdatetimeに変換
dt = datetime.fromtimestamp(t)
datadate = dt.strftime('%m%d%H%M')
print (datadate)


# In[9]:


# CSV出力
all_df.to_csv("./kakoufinal" + "_1_" + datadate + ".csv", 
          index=False   # インデックスを削除
         )


# In[10]:


# py出力
import subprocess
subprocess.run(['jupyter', 'nbconvert', '--to', 'python', 'merging.ipynb'])

