#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests as req
import json


# In[2]:


districts = ['西屯區','北屯區','南屯區']


# In[3]:


urls = ['https://lvr.land.moi.gov.tw/SERVICE/QueryPrice/4a8a5023b066ce8e52946eb1d6cd7420?q=VTJGc2RHVmtYMTkwVXBwZ25TZmliN3dEazBHa3Ara21SNDRvUjJxYVFyYVJEVk5tYzFJa1cxTGZpS1BrN1VudUN2RVcveHFGaHU3cWd1ckphQkhZdDIvbjlrWEhiSHRvZW1lRFlGeTV0akdrbXhjalFnVTdzSkFGWWZDZGtIVmZxY0E3Z0FOYjJsV1R5RTZwVDdvZklLSDIxT0JIZHhCa3VHc0NKVFdNdE5XZjBWZmxiVG1xS1dNTUxZZXhyZzR3MTc0djdHNTdFOExhSndSQ29CU3RVWnpCajhzSkFXcFVGQVREd2d1V1h6aFpOdDFseGRKVFRnUkJXZGxZWjlOL2RWWWpZZ2tpK1hMaGNXbU5CajhOazRzN241UmJOSXF4WlY1bVRRTDhBblFGOTdQcmxwU0d6bkNpWHhhYmo0ZVNKNjJzaGp5alZodGpteHFqWnJNOGFha21vTis0ZlJucXhDVXBGM0laVHdnZnNrWFduYnQwM1VIaWlrQXNhcUxTU283YzREMFc0dTUvT0ZjeU1BY0tiTmpTdTgrQzk3dS9LY2wyV3BLTDlJQU5MU1BsQW5oNFpuelZBMlVOMFRpWE1iakxDTXRBblgraUlISG1qV29zK1VnaWFsblJlVHJZaVYxS3dRNXlxZHJPNGJLaFpyK3M5UEJqUlFLcVUralBPb0xRc205OWpaS3BWMHVXTHBTd2IwTFlZTXljWE9KRWRmNE02bStDRVBDL3dSekZsMnhaNjE0bE9tbGtRSFR4dXY5U1hsbTBBUUIrK1d0bUdrZEgwOU93T3dkcklRc3BOcDBsbERYc1RPWHl2STluQjc3bnkwc3d0UnNuNTlVa3MvVng2ZzN0c3dFUEk5cFVUbExqZG9LZDlTZnY3aGkxcnpoYTdTVjIwT3c5NnJXV2ZKUFFtd0FMaDFYb0hOTW5rdzNGbnQ2YnphR0hVMkp5em5zV0VjRnI0YkJpWlJiWnd4M1o5ejZ1Rm1zPQ==',
        'https://lvr.land.moi.gov.tw/SERVICE/QueryPrice/3fdb47abdbaaf5b169b6d72d7de43ffc?q=VTJGc2RHVmtYMS9iU2VUNVNWVEkybXVRK0U0TXJIUlNaRDU4dWhsZ1djb0NibnVUanpLZ0FCaUdoaVBEazBrZ1NqTTJ5SlJGMDNFZHRlMUNCY1kvZnVwZndueU00eDU5dFBpZDhKQ3Fmb1NuTnN4TitQc1ovMzcycGFnTkk2bUVUYWpzK2hvVWZ1UmJEQi80R0JabksrR2ZET2Vlc0dLTXZHVkp6cmcxbTdaY0MrNHVtRzFVY3FiOVc5UEtzS1h2NDlzaXFiVlNHWUE5TnlBWi9YQzNLWGQxRVFMTWoybm5Yd0Zvcjh1aS9PVFZqOW5aTzdaWnVpdER5aEtQbE5ZcUhkUnBaWGZXamZoNXFPWDc3VnorVTFBYW9ZUFdYTndmT2V3K09xOW5xT00zam42d0ZlaEZNNEwxQ252K0hZRXdkT0o5cjI4eG9LT1RlYmtDMy9ONXVub0I1VnUzZTZnbXFoLy92d1dXWWozSHd1R0NFeU9lOW1pTHJPUytqNXB0bXBHOFdiQzQrYWtvZWtHaUROUjNwNklCNTF6VUM3SVZkQ1djeUMxSG53QkZFQkVPUjgxZGh0RlZGKy9FSllFbVhjNnZuOWN4bGl3S0pGMGdSNFc5bXY3MzFGWGpBb0ZwdVpGaVdwdW5LTi81Y3JKRm5vdG5Nc2x4a1l1bWNvQ2hqSDQzbml1UFd0UC93Q0FHODBFUFFCRTBReDJNNEkzMWtuOXR4ZHdzS3B0aWhET0tydEIrcFpCZnhuWkdIL1JvRzdxOXROVkEyUGxDenZOMFQvNTRuckJqQ0pJVHo5TTJNVmNtWk80cDdaM1ZCRkFGL3JOVk0yL2pBR2hMUFY4Ym1jdkhxeXZSSEM0TU9Ndm9rOExrRnNBVDNTSFRrd0xBOEsrVDFqS3RsL3RSSmFkMUt2cXhyTU5VYnlxWW1wdXU1NFBRWmF0bEd2enF2TGtkTnZUdGFnPT0=',
        'https://lvr.land.moi.gov.tw/SERVICE/QueryPrice/2c86dcabd89785e3659406dcd1406403?q=VTJGc2RHVmtYMTlZdGNWc0tsQ2dyNUYzS2ZScXZhclNBZkdobi93TlUxMXJzR0N2bjBVNnpUNTZmY09GQlNUQlFUbUNsOVB0ZE9mVXJZNlE4bVQ0OTFXNWpUWlhjaTdQNHhaTEM5YVE3MVR2cVlob0VUbndFZ2QyUGxTU1g0R09iL0hDaTFWK2Jad2VhSmZTNTlLLzFVRERwc1Y3ZTY4cUZoUXdkTXJwVCtHVjRjSVpTL09GZ3o4TkJWTnBhN05yNGx6dHRZMDlvSnBwYWE3enN0ZGpTdTBaUEUxa0k5TVEwTmYyVEFiaW12YkJLVGN0R2p6Rm4wQ01yczdWUDJWbFlPZ1prVEJFaGtjd29qMVVjT3c0b2pWL3BqSnp1eWQ1VjhiVElFUUhId0t6Sk5iSzVmV3REL1BlYi8zaEttV0wrZVJ1NUNISTRiVm1KRXJlcUd6RnpXYm9XMFE4SS9FWWtGNlVtMklucjhTMFR1bUtxWk9oOVJpb2lnZjk1ODNCVjJ0OC9GTzVUUEwzSUJqUmJxaVZ3NnQrL2xrUTlNSldvQXZTNld4Q2VkQXprMVFnbnljcFRFK3NlYlhyZkF5Q0s0bEtPaHA0OUlSL0VJeS83REhuSGxSQnVvUzFYVlN3YmF2bDZLSnB5aWRZSFdIZ1N6aGFYZnlUU2VYTmhxbnZhbkRXQVVKekRxMmI2TnV4MHRySTRKcHlWUzBuVFlHUDdDVVBsNUNRcDBmU2xveUl2azlZeC9oMXpEdjZZaWZWR21hbG5rcDVucWZBSHVlNmkvbnRnOUVDSEhnOGIxVGJLOWdRUDVTTWlSUXB4b0Y5TjlIRzRXaVpwSHlQaWpCcDJ2SGl0eitUSDYyeVdhZ3dRSllFbHpsVnVwZ1ROS1F6QkMybXBvUU1RbzNaRW05NVhMeENyRmtENHE4L25uVEcxZHZ0NmlZNjJWYzVHQjRFM2lzYnNnPT0=',
        ]


# In[4]:


df = pd.DataFrame()


# In[5]:


for i in range(0,3):
    print('正再爬取 「{0}」 111年1月至112年12月的資料'.format(districts[i]))
    resp=req.get(urls[i])
    data=json.loads(resp.text)
    print('一共抓到 {0} 筆台中市{1} 111年1月至112年12月的資料'.format(len(data),districts[i]))

    house_object=[]

    for object in data :
        one_object={}
        one_object['經度']= object['lon']            # 經度
        one_object['緯度']= object['lat']            # 緯度
        one_object['屋齡'] = object['g']             # 屋齡
        one_object['面積'] = object['s']             # 面積
        one_object['建物類型'] = object['b']         # 建物型態
        one_object['用途'] = object['pu']            # 主要用途
        one_object['樓別/樓高'] = object['f']        # 樓別/樓高
        one_object['佈局'] = object['v']            # 幾房幾衛幾廳
        one_object['電梯'] = object['el']           # 有無電梯
        one_object['管理員'] = object['m']          # 有無管理員
        one_object['車位數量'] = object['l']        # 車位數量
        one_object['成交日期'] = object['e']        # 成交日期
        one_object['價格'] = object['tp']           # 價格
        house_object.append(one_object)

    #--- 將原始數據保存到 CSV 檔案
    cols=['經度','緯度','屋齡','面積','建物類型','用途',
        '樓別/樓高','佈局','電梯','管理員','車位數量',
        '成交日期','價格']
    df_house = pd.DataFrame (house_object, columns = cols) # 將list 轉換為 dataframe
    df_house['行政區'] = districts[i]
    df_house['交易年份'] = df_house['成交日期'].apply(lambda x: x.split('/')[0])
    df = pd.concat([df,df_house],axis=0)


df.drop(['成交日期'],axis=1,inplace=True)
df = df.reset_index(drop=True)
print('完成')


# In[6]:


df.to_csv('D://台中市房價.csv', index=False, encoding='cp950')

