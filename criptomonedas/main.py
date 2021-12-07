import krakenex
from pykrakenapi import KrakenAPI
from datetime import timezone
from datetime import datetime
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
api = krakenex.API()
k = KrakenAPI(api)
def show_line_chart(date_list, value_list, titulo_grafica,eje_x,eje_y):
    plt.plot(date_list, value_list)
    plt.title(titulo_grafica)
    plt.xlabel(eje_x)
    plt.ylabel(eje_y)
    dtFmt = mdates.DateFormatter('%d-%b')  # define the formatting
    plt.gca().xaxis.set_major_formatter(dtFmt)  # apply the format to the desired axis
    plt.show()
def vwap(prices, volumes):
    prices_ = np.array(prices)
    volumes_ = np.array(volumes)
    if len(prices) > 0:
        return sum(prices_ * volumes_) / sum(volumes_)
pair = input(
        "Introduzca la criptomoneda que quiera graficar o escriba 'salir' si quiere salir de la aplicacion: ")
#pair = "XDGUSD"
time_from = datetime(2021,11,22,8)
time_to = datetime(2021,11,22,20)

t_cut = int(time.mktime(time_to.timetuple()))

unixtime = int(time.mktime(time_from.timetuple()))
df = pd.DataFrame()

i = 0

while (unixtime < t_cut):
    if i>0:
        time.sleep(1)
    # try:
    trades, last = k.get_recent_trades(pair,unixtime) #Esto solo devuelve 1000 desde la fecha
    df = df.append(trades.reset_index(),ignore_index=True)
    unixtime = int(last/1e9) #last in nanoseconds
    i+=1

    # except NameError:

    #     print(NameError)

df = df[df['dtime']<=time_to]
df.sort_values(by=['dtime'],ascending=True,inplace=True)
print(df)
#show_line_chart(df["dtime"],df["price"],"grafico_valores","fecha","valor")
df_vwap = df.groupby(pd.Grouper(key='dtime',freq='1min')).apply(lambda x: vwap(x['price'],x['volume'])).reset_index(name='vwap')
show_line_chart(df_vwap['dtime'], df_vwap['vwap'],"VWAP","fecha","valor")

