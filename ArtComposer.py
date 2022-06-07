import numpy as np
import pandas as pd
# Везде n - длина ряда, который должен получиться
def period(n):  # Сезонность \ периодичность
    x=np.linspace(0,16*np.pi, n)
    y=np.abs(np.sin(x))*.6+.2
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

''' По всем параметрам :) '''
i=0
n=500
amt=1000
dataset=pd.DataFrame()
dataset['t']=np.arange(n)
for gamma in np.linspace(0,1,amt//4): # по всем комбинациям
    for _ in range(4):
        i+=1 
        y=(1-gamma)*period(n)+gamma*rndwalk(n)
        ser=pd.DataFrame({'t':np.arange(n), 'val':y}) # вместо t можно естественные даты/время
        '''Можно собрать в одну таблицу'''
        dataset=pd.merge(dataset, pd.DataFrame({'t':np.arange(n), str(i-1).zfill(3):y}), on='t', how='inner')
print('%i artificial series created'%i)