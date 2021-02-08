# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns 
import time
from folium import Map
from folium.plugins import HeatMap

#crime = pd.read_csv(open(r'G:\python\crime.csv', encoding='windows-1252'))
crime = pd.read_csv(open(r'F:\百度云上存的项目\crime.csv', encoding='windows-1252'))
crime['YEAR'].value_counts()

crime=crime[crime['YEAR'].isin([2016,2017])]

######################################
###########   1      #################
######################################
plt.figure(figsize=(12,6))
sns.countplot(x='YEAR',data=crime)
plt.show()

######################################
###########   2      #################
######################################
count2017,count2016=crime['YEAR'].value_counts()
print('2017犯罪总数环比增长'+str(round((count2017-count2016)/count2016*100,2))+'%')

######################################
###########   3      #################
######################################
interest=['Missing Persons Report','Robbery','Drug Violation','Prostitution','Harassment']
crimeinterest=crime[crime['OFFENSE_CODE_GROUP'].isin(interest)]


######################################
###########   4      #################
######################################
plt.figure(figsize=(12,6))
sns.countplot(x='YEAR',hue='OFFENSE_CODE_GROUP',data=crimeinterest)
plt.show()


######################################
###########   5      #################
######################################
crime2016=crime[crime['YEAR']==2016]
crime2017=crime[crime['YEAR']==2017]
H7=crime2017[crime2017['OFFENSE_CODE_GROUP'] == 'Harassment'].count()[0]
P7=crime2017[crime2017['OFFENSE_CODE_GROUP'] == 'Prostitution'].count()[0]
MPR7=crime2017[crime2017['OFFENSE_CODE_GROUP'] == 'Missing Person Reported'].count()[0]
R7=crime2017[crime2017['OFFENSE_CODE_GROUP'] == 'Robbery'].count()[0]
DV7=crime2017[crime2017['OFFENSE_CODE_GROUP'] == 'Drug Violation'].count()[0]
H6=crime2016[crime2016['OFFENSE_CODE_GROUP'] == 'Harassment'].count()[0]
MPR6=crime2016[crime2016['OFFENSE_CODE_GROUP'] == 'Missing Person Reported'].count()[0]
R6=crime2016[crime2016['OFFENSE_CODE_GROUP'] == 'Robbery'].count()[0]
DV6=crime2016[crime2016['OFFENSE_CODE_GROUP'] == 'Drug Violation'].count()[0]
P6=crime2016[crime2016['OFFENSE_CODE_GROUP'] == 'Prostitution'].count()[0]
print('2017骚扰犯罪总数环比增长'+str(round((H7-H6)/H6*100,2))+'%')
print('2017卖yin犯罪总数环比增长'+str(round((P7-P6)/P6*100,2))+'%')
print('2017失踪报告总数环比下降'+str(round(-(MPR7-MPR6)/MPR6*100,2))+'%')
print('2017抢劫总数环比下降'+str(round(-(R7-R6)/R6*100,2))+'%')
print('2017滥药总数环比下降'+str(round(-(DV7-DV6)/DV6*100,2))+'%')



######################################
###########   6      #################
######################################
g = sns.catplot(x='MONTH', row="YEAR",
                     data=crime, kind="count",
                    height=4, aspect=3);
g = sns.catplot(x='MONTH',hue='OFFENSE_CODE_GROUP', row="YEAR",
                     data=crimeinterest, kind="count",
                    height=4, aspect=4);  
                

######################################
###########   7      #################
######################################       
   
crime['DAY']=pd.to_datetime(crime['OCCURRED_ON_DATE'],format= '%Y-%m-%d %H:%M:%S').apply(lambda x : x.strftime('%d'))
g = sns.catplot(x='DAY',row='MONTH' ,
                     data=crime2016[crime2016['MONTH'].isin([2,11,12])], kind="count",
                    height=4, aspect=4);
g = sns.catplot(x='DAY',row='MONTH' ,
                     data=crime2017[crime2017['MONTH'].isin([2,11,12])], kind="count",
                    height=4, aspect=4);    

######################################
###########   8      #################
###################################### 
#处理缺失值
crime=crime.dropna()
crime=crime.drop(crime[crime['Lat']<40].index,0)
#画热力图

for i in interest:
    m = Map([ 42.32, -71.13], zoom_start=12,title=i)
    crimeyear=crime[crime['YEAR']==2017]
    HeatMap(crimeyear[crimeyear['OFFENSE_CODE_GROUP']==i][['Lat','Long']].values,radius=20).add_to(m)
    try:m.save('2017'+i+'map.html')
    except Exception:pass
    
