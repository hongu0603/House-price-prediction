#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import cross_val_score


# In[2]:


data = pd.read_csv('D://preprocessed_data.csv', encoding='cp950')


# In[4]:


# 先將屋齡是空的和不是空的分開
Age_Na = data[data["屋齡"].isnull()]
Age_not_Na = data[data["屋齡"].notnull()]


# In[5]:


Y = Age_not_Na['屋齡']
X = Age_not_Na.drop('屋齡',axis=1)


# In[6]:


X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.2,random_state=42)
rfModel_age = RandomForestRegressor(n_estimators=100,random_state=42)

rfModel_age.fit(X_train, y_train)


# In[7]:


# 預測測試集
from sklearn.metrics import r2_score
y_pred =rfModel_age.predict(X_test)
r2 = r2_score(y_test, y_pred)
print('R方得分:', r2)


# In[8]:


#預測屋齡空值
Age_Na.drop('屋齡',axis=1,inplace=True)
Age_Na_value = rfModel_age.predict(Age_Na)
Age_Na['屋齡'] = Age_Na_value
#整合資料
data = pd.concat([Age_not_Na,Age_Na],axis=0)
data.sort_index(inplace=True)


# In[9]:


y = data['價格']
X = data.drop('價格',axis=1)

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
rfModel = RandomForestRegressor(n_estimators=100,random_state=42)
rfModel.fit(X_train, y_train)

y_pred =rfModel.predict(X_test)
r2 = r2_score(y_test, y_pred)

print('R方得分:', r2)


# In[10]:


from sklearn.metrics import mean_squared_error
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print("RMSE: ",round(rmse/10000),'萬')


# In[11]:


from sklearn.model_selection import cross_val_score
rfModel_cv = RandomForestRegressor(n_estimators=100, random_state=42)
scores = cross_val_score(rfModel_cv, X, y, cv=5, scoring='r2')
print("隨機森林迴歸 R2 score: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


# In[12]:


#西屯區,屋齡 30,面積 75坪,有電梯、管理員,車位:1,樓別:中層,樓高:高層,5房 2廳 2衛,建物類型:住宅大樓,用途:住家用
test= np.array(
[120.64359,#經度
 24.179285, #緯度
 15, #屋齡
 75, #面積
 1,  #電梯
 1,  #管理員
 1,  #車位數量
 111,#交易年分
 3,  #樓別
 2,  #樓高
 5,  #房
 2,  #廳
 2,  #衛
 1,  #住宅大樓
 0,  #公寓
 0,  #店面
 0,  #華夏
 0,  #透天厝
 0,  #住商用
 1,  #住家用
 0,  #商業用
 0,  #辦公用
 0,  #北屯
 0,  #南屯
 1   #西屯
]).reshape(1,25)


# In[13]:


price_pred = rfModel.predict(test)
print("預估價格為: %0.2f萬" % (price_pred/10000))
print("誤差範圍介於: %0.2f 萬 到 %0.2f 萬元之間" % (price_pred/10000-rmse/10000,price_pred/10000+rmse/10000))


# In[ ]:




