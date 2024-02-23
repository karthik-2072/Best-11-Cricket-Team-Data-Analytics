#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd
import json


# In[16]:


with open ('t20_wc_match_results.json') as f:
    data=json.load(f)
print(data)


# In[17]:


df_match=pd.DataFrame(data[0]['matchSummary'])
df_match.head()


# In[18]:


df_match.shape #rows and columns


# In[19]:


df_match.rename({'scorecard': 'match_id'}, axis = 1, inplace = True) #Use scorecard as a match id to link with other tables
df_match.head()


# Batting Summary
# 

# In[20]:


with open('t20_wc_batting_summary.json') as f:
    data = json.load(f)
    all_records = []
    for rec in data:
        all_records.extend(rec['battingSummary']) #appendings all arrays into one
  
df_batting = pd.DataFrame(all_records)
df_batting.tail()


# Enter new column based on dismissal 

# In[21]:


df_batting['out/not_out'] = df_batting.dismissal.apply(lambda x: "out" if len(x)>0 else "not_out")
df_batting.head(11)


# Remove Dismissal from data frame

# In[22]:


df_batting.drop(columns=["dismissal"], inplace=True)
df_batting.head(10)


# Cleanup weird characters

# In[24]:


df_batting['batsmanName'] = df_batting['batsmanName'].apply(lambda x: x.replace('â€', ''))
df_batting['batsmanName'] = df_batting['batsmanName'].apply(lambda x: x.replace('\xa0', ''))
df_batting.head(11)


# Create a match ids dictionary that maps team names to a unique match id. This will be useful later on to link with other tables

# In[26]:


match_ids_dict = {}

for index, row in df_match.iterrows():
    key1 = row['team1'] + ' Vs ' + row['team2']
    key2 = row['team2'] + ' Vs ' + row['team1']
    match_ids_dict[key1] = row['match_id']
    match_ids_dict[key2] = row['match_id']
match_ids_dict 


# In[27]:


df_batting['match_id'] = df_batting['match'].map(match_ids_dict)
df_batting.head() #we use thisto link two tables


# In[30]:


df_batting.to_csv('fact_bating_summary.csv', index = False) #convert to csv


# Process Bowling Summary

# In[31]:


with open('t20_wc_bowling_summary.json') as f:
    data = json.load(f)
    all_records = []
    for rec in data:
        all_records.extend(rec['bowlingSummary'])
all_records[:2]


# In[32]:


df_bowling = pd.DataFrame(all_records)
print(df_bowling.shape)
df_bowling.head()


# In[33]:


df_bowling['match_id'] = df_bowling['match'].map(match_ids_dict)
df_bowling.head()


# In[34]:


df_bowling.to_csv('fact_bowling_summary.csv', index = False)


# Process Players Information

# In[36]:


with open('t20_wc_player_info.json') as f:
    data = json.load(f)


# In[37]:


df_players = pd.DataFrame(data)

print(df_players.shape)
df_players.head(10)


# Cleanup weird characters

# In[38]:


df_players['name'] = df_players['name'].apply(lambda x: x.replace('â€', ''))
df_players['name'] = df_players['name'].apply(lambda x: x.replace('†', ''))
df_players['name'] = df_players['name'].apply(lambda x: x.replace('\xa0', ''))
df_players.head(10)


# In[39]:


df_players[df_players['team'] == 'India']


# In[40]:


df_players.to_csv('dim_players_no_images.csv', index = False)


# In[ ]:




