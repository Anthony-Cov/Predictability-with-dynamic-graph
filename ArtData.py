# -*- coding: utf-8 -*-
"""
Как делали искусственные ряды
"""
import numpy as np
import pandas as pd
from itertools import product
# Везде n - длина ряда, который должен получиться
def trans(n):   # Дрейф\переходный процесс типа сигмоиды
    x=np.linspace(-n*.034, n*.01, n)
    y=1-1/(1+np.exp(x))
    return y
def period(n):  # Сезонность \ периодичность
    x=np.linspace(0,16*np.pi, n)
    y=np.sin(x)/2+.5
    return y
def noise(n):   # Шум с нормальным распределением
    y=np.random.randn(n)
    y=(y-min(y))/(max(y)-min(y)) # В масштаб [0..1]
    return y
def rndwalk(n): # Случайное блуждание
    y=[0.]
    for i in range(n-1):
        k=np.random.rand()
        sign = 1. if np.random.randint(2) else -1. #x(t+1)=x(t)+-1
        y.append(y[-1]+sign*k)
    y=np.array(y)
    y=(y-min(y))/(max(y)-min(y)) # В масштаб [0..1]
    return y
def compose(n,kt,kp,kn,kr): # Собрать всё вместе с весами
    y=kt*trans(n) + kp * period(n) + kn * noise(n) + kr * rndwalk(n)
    y=(y-min(y))/(max(y)-min(y))
    return y

''' По всем параметрам :) '''
i=0
n=750
dataset=pd.DataFrame()
dataset['t']=np.arange(n)
for k in product([0.0, .3, .6, 1.], repeat=4): # по всем комбинациям
    i+=1 
    if sum(k) < 0.3: # вырожденные не интересны
        continue
    y=compose(n,k[0],k[1],k[2],k[3])
    y=(y-min(y))/(max(y)-min(y)) # В масштаб [0..1]
    ser=pd.DataFrame({'t':np.arange(n), 'val':y}) # вместо t можно естественные даты/время
    '''Можно собрать в одну таблицу'''
    dataset=pd.merge(dataset, pd.DataFrame({'t':np.arange(n), 'val'+str(i-1).zfill(4):y}), on='t', how='inner')
    '''Можно каждый ряд в отдельный файл'''
    #ser.to_csv('../_DataSets/Artificial/art'+str(i-1).zfill(4)+'.csv', index=False)
print('%i artificial series created'%i)
print(dataset.head())