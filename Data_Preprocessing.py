#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
sns.set_theme(style='whitegrid',palette='deep', font='Microsoft YaHei', font_scale=1, rc={'figure.dpi':120})
get_ipython().run_line_magic('matplotlib', 'inline')
data = pd.read_csv('D://台中市房價.csv', encoding='cp950')


# In[2]:


data = data[['經度', '緯度', '屋齡', '面積', '建物類型', '用途', '樓別/樓高', '佈局', '電梯', '管理員',
'車位數量', '行政區', '交易年份','價格']]


# In[3]:


#補值前 資料裡有一些數字比較大 有用到逗號 要先把逗號去掉

data['價格'] = data['價格'].replace(',', '', regex=True).astype(float)
data['面積'] = data['面積'].replace(',', '', regex=True).astype(float)


data.info()


# In[4]:


data = data.drop_duplicates()
data.info()


# In[5]:


data['建物類型'].value_counts()


# In[6]:


data['用途'].value_counts()


# In[7]:


data['建物類型'].fillna('住宅大樓(11層含以上有電梯)',inplace=True)
data['用途'].fillna('住家用',inplace=True)
data.dropna(subset=['佈局'],inplace=True)
data.describe()


# In[8]:


s = data['價格'].describe()
IQR = s['75%'] - s['25%']
upper_lim = s['75%'] + IQR*1.5
lower_lim = s['25%'] - IQR*1.5
data = data[data['價格'] < upper_lim]

s = data['面積'].describe()
IQR = s['75%'] - s['25%']
upper_lim = s['75%'] + IQR*1.5
lower_lim = s['25%'] - IQR*1.5
data = data[data['面積'] < upper_lim]

data.describe()


# In[9]:


plt.hist(data['價格']/10000, bins=20, color='steelblue', edgecolor='black')
plt.title('台中市屯區房價分佈(交易時間111/01/01-112/12/31)')
plt.xlabel('價格(萬)')
plt.ylabel('數量')


# In[10]:


df = data.sort_values(by='交易年份',ascending=True)
df['價格']=df['價格']/10000
sns.relplot(x='交易年份', y='價格', hue='行政區', data=df,kind='line',ci=None)
plt.xlabel('年度')
plt.ylabel('價格(萬)')


# In[11]:


data.loc[data['建物類型'].isin(['工廠','廠辦','農舍','倉庫']), '建物類型'] = '其他'
data['建物類型'] = data['建物類型'].str.split("\(",expand=True)[0]
data.loc[data['建物類型'].isin(['店面（店舖)']), '建物類型'] = '店面'


# In[12]:


cross_table = pd.crosstab(data['行政區'],data['建物類型'])
plt.figure(figsize=(12,8))
sns.heatmap(cross_table,cmap='YlGnBu',annot=True,fmt='d')


# In[13]:


data.loc[data['用途'].isin(['住家用\)']), '用途'] = '住家用'
data.loc[~data['用途'].isin(['住家用','住商用','商業用','辦公用','其他']), '用途'] = '其他'


# In[14]:


data['樓別'] = data['樓別/樓高'].str.split('/',expand=True)[0] #樓別/樓高
data['樓高'] = data['樓別/樓高'].str.split('/',expand=True)[1] #樓別/樓高
data.drop(['樓別/樓高'],axis=1,inplace=True)


# In[15]:


data.樓別.value_counts().tail(100)


# In[16]:


print('處理前一共有',len(data.樓別.unique()),'不同的資料')
data['樓別'] = data['樓別'].str.split(',', expand=True)[0]
print('處理後一共有',len(data.樓別.unique()),'不同的資料')


# In[17]:


data.樓別.unique()


# In[18]:


data.loc[data['樓別'].isin(['見其他登記事項','屋頂突出物','夾層','地下','','騎樓']), '樓別'] = '其他'
data['樓別'] = data['樓別'].apply(
lambda x: '地下' if '地下' in x
else '其他' if x in '其他'
else '全層' if x in '全'
else '低層' if x in ['一層', '二層', '三層', '四層', '五層']
else '中層' if x in ['六層', '七層', '八層', '九層', '十層', '十一層', '十二層', '十三層', '十四層', '十五層']
else '高層')

data['樓別'].value_counts()


# In[19]:


data.loc[data['樓高'].isin(['(空白)']), '樓高'] = '十五層' # 填補眾數
data['樓高'] = data['樓高'].apply(
lambda x:  '低層' if x in ['一層', '二層', '三層', '四層', '五層']
else '中層' if x in ['六層', '七層', '八層', '九層', '十層', '十一層', '十二層', '十三層', '十四層', '十五層']
else '高層')

data['樓高'].value_counts()


# In[20]:


data['房'] = data['佈局'].str.split('房',expand=True)[0]
data['廳'] = data['佈局'].str.split('房',expand=True)[1].str.split('廳',expand=True)[0]
data['衛'] = data['佈局'].str.split('房',expand=True)[1].str.split('廳',expand=True)[1].str.split('衛',expand=True)[0]
data.drop('佈局',axis=1,inplace=True)
data.describe()


# In[21]:


data['房'] = data['房'].str.extract('(\d+)').astype(float).fillna(0)
data['廳'] = data['廳'].str.extract('(\d+)').astype(float).fillna(0)
data['衛'] = data['衛'].str.extract('(\d+)').astype(float).fillna(0)
data.info()


# In[22]:


# One-Hot Encoding
data_encoded = pd.get_dummies(data, columns=['建物類型','用途','行政區'])
# Label Encoding
code_dict = {'地下': 0, '其他': 1, '低層': 2,'中層':3,'高層':4,'全層':5}
data_encoded['樓別'] = data_encoded['樓別'].map(code_dict)
code_dict = {'低層': 0, '中層': 1, '高層': 2}
data_encoded['樓高'] = data_encoded['樓高'].map(code_dict)
code_dict = {'無':0, '有':1}
data_encoded['電梯'] = data_encoded['電梯'].map(code_dict)
data_encoded['管理員'] = data_encoded['管理員'].map(code_dict)


# In[23]:


data_encoded.columns


# In[24]:


data_encoded = data_encoded.drop(['用途_其他'],axis=1)


# In[25]:


data_encoded.to_csv('D://preprocessed_data.csv', index=False, encoding='cp950')

