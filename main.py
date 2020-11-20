# -*- coding: utf-8 -*-
# Proyecto Integrador

# Integrantes
# Hugo Pastorino ID:41117
# Walter Torres ID:31321

# Opción 2: El mercado financiero
# Data histórica descargada desde: https://stooq.com/db/h/
# Seleccion de las 15 acciones mas operadas en Argentina 2020


import matplotlib.pyplot as plt
import pandas as pd
import time
from IPython.display import clear_output

from google.colab import drive

drive.mount('/content/drive/')


def menu():
    tickers = ['aapl', 'amzn', 'ge', 'gold', 'goog', 'jnj', 'jpm', 'mcd', 'meli', 'msft', 'nflx', 'tsla', 'wmt', 'xom']
    estado = 0
    while estado == 0:
        print('''
          aapl = Apple Inc.
          amzn = Amazon.com Inc.
          ge   = General Electric Co. 
          gold = Barrick Gold Corp.
          goog = Alphabet Inc.
          jnj  = Johnson y Johnson
          jpm  = JP Morgan & Chase Co.
          mcd  = McDonald's Corp.
          meli = Mercado Libre Inc.
          msft = Microsoft Corp
          nflx = Netflix Inc.
          tsla = Tesla Inc.
          wmt  = Walmart Inc.
          xom  = Exxon Mobil Corporation
  ''')
        seleccion = input('Seleccione la primera acción, ingrese el ticker:')
        if seleccion in tickers:
            archivo1 = pd.read_csv("/content/drive/My Drive/proyecto_integrador/" + seleccion + ".us.csv")
            tickers.remove(seleccion)
            estado = 1
        else:
            print('Es incorrecto')
            time.sleep(2)
            clear_output()

    estado = 0
    clear_output()
    while estado == 0:
        print('''
          aapl = Apple Inc.
          amzn = Amazon.com Inc.
          ge   = General Electric Co. 
          gold = Barrick Gold Corp.
          goog = Alphabet Inc.
          jnj  = Johnson y Johnson
          jpm  = JP Morgan & Chase Co.
          mcd  = McDonald's Corp.
          meli = Mercado Libre Inc.
          msft = Microsoft Corp
          nflx = Netflix Inc.
          tsla = Tesla Inc.
          wmt  = Walmart Inc.
          xom  = Exxon Mobil Corporation
  ''')
        seleccion = input('Seleccione la segunda acción, ingrese el ticker:')
        if seleccion in tickers:
            archivo2 = pd.read_csv("/content/drive/My Drive/proyecto_integrador/" + seleccion + ".us.csv")
            estado = 1
        else:
            print('Es incorrecto o igual al primer ticker seleccionado, ingrese uno diferente')
            time.sleep(2)
            clear_output()
    # Procesamos los datos para cambiar nombres de columnas y formatear las fechas
    ticker1, ticker2, ticker1dic, ticker2dic = proceso(archivo1, archivo2)
    # Analizamos los cruces en las cotizaciones
    cruces = cruce(ticker1dic, ticker2dic)
    dd, dd2 = derivada_discreta(ticker1dic, ticker2dic)
    print(ticker1)
    print(cruces)
    print(dd, dd2)


def proceso(archivo1, archivo2):
    # Procesamos los datos para cambiar nombres de columnas y formatear las fechas
    archivo1.columns = ['Ticker', 'Per', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume',
                        'Openint']
    archivo1.Date = pd.to_datetime(archivo1.Date, format='%Y%m%d')
    archivo2.columns = ['Ticker', 'Per', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume',
                        'Openint']
    archivo2.Date = pd.to_datetime(archivo2.Date, format='%Y%m%d')
    archivo1.Date = pd.to_datetime(archivo1.Date)
    ticker1 = archivo1.to_dict("list")
    ticker2 = archivo2.to_dict("list")
    ticker1dic = archivo1.to_dict("index")
    ticker2dic = archivo2.to_dict("index")
    return ticker1, ticker2, ticker1dic, ticker2dic


def cruce(ticker1dic, ticker2dic):
    # Analizamos los cruces en las cotizaciones
    cot1 = {}
    for i in ticker1dic:
        fecha1 = ticker1dic[i]['Date']
        # print(fechag)
        apertura1 = ticker1dic[i]['Open']
        # print(aperturag)
        cot1[fecha1] = apertura1
        # print(cot1)
    cot2 = {}
    for i in ticker2dic:
        fecha2 = ticker2dic[i]['Date']
        # print(fechag)
        apertura2 = ticker2dic[i]['Open']
        # print(aperturag)
        cot2[fecha2] = apertura2

    fechas_ambos = cot1.keys() & cot2.keys()
    fechas_ambos = sorted(fechas_ambos)
    x = ''
    cruces = {}
    for v in fechas_ambos:  # Compara los valores Open con el mayor valor anterior para identificar el cruce
        if cot1[v] > cot2[v]:
            if x != 'cot1':
                if x != '': cruces[v] = cot1[v]
                x = 'cot1'
        else:
            if x != 'cot2':
                if x != '': cruces[v] = cot2[v]
                x = 'cot2'
    return cruces


def derivada_discreta(ticker1dic, ticker2dic):  # Calculo de la Derivada discreta para cada ticker seleccionado
    dd = {}
    ayer = 0
    for a in ticker1dic:
        open1 = ticker1dic[a]['Open']
        date1 = ticker1dic[a]['Date']
        dd[date1] = open1 - ayer
        ayer = open1

    dd2 = {}
    ayer2 = 0
    for a in ticker2dic:
        open1 = ticker2dic[a]['Open']
        date1 = ticker2dic[a]['Date']
        dd2[date1] = open1 - ayer2
        ayer2 = open1
    return dd, dd2


def crecimento(archivo1, archivo2):  # Filtramos las fechas de interes para el calculo de crecimiento
    octubre1 = pd.DataFrame()
    septiembre1 = pd.DataFrame()
    docemeses1 = pd.DataFrame()
    octubre1 = archivo1[(archivo1.Date >= '2020-10') & (archivo1.Date < '2020-11')]
    septiembre1 = archivo1[(archivo1.Date >= '2020-09') & (archivo1.Date < '2020-10')]
    docemeses1 = archivo1[(archivo1.Date >= '2019-11') & (archivo1.Date < '2020-11')]

    octubre2 = pd.DataFrame()
    septiembre2 = pd.DataFrame()
    docemeses2 = pd.DataFrame()
    octubre2 = archivo2[(archivo2.Date >= '2020-10') & (archivo2.Date < '2020-11')]
    septiembre2 = archivo2[(archivo2.Date >= '2020-09') & (archivo2.Date < '2020-10')]
    docemeses2 = archivo2[(archivo2.Date >= '2019-11') & (archivo2.Date < '2020-11')]

    croctubre1 = ((octubre1.iloc[-1]['Open'] - octubre1.iloc[0]['Open']) / octubre1.iloc[0]['Open']) * 100
    croctubre2 = ((octubre2.iloc[-1]['Open'] - octubre2.iloc[0]['Open']) / octubre2.iloc[0]['Open']) * 100
    crseptiembre1 = ((septiembre1.iloc[-1]['Open'] - septiembre1.iloc[0]['Open']) / septiembre1.iloc[0]['Open']) * 100
    crseptiembre2 = ((septiembre2.iloc[-1]['Open'] - septiembre2.iloc[0]['Open']) / septiembre2.iloc[0]['Open']) * 100
    crdocemeses1 = ((docemeses1.iloc[-1]['Open'] - docemeses1.iloc[0]['Open']) / docemeses1.iloc[0]['Open']) * 100
    crdocemeses2 = ((docemeses2.iloc[-1]['Open'] - docemeses2.iloc[0]['Open']) / docemeses2.iloc[0]['Open']) * 100

    if croctubre1 > croctubre2:
        mayoroctubre = 'Mayor: ' + octubre1.iloc[0]['Ticker'] + ' ' + str(croctubre1) + ' %'
        menoroctubre = 'Menor: ' + octubre2.iloc[0]['Ticker'] + ' ' + str(croctubre2) + ' %'
    else:
        mayoroctubre = 'Mayor: ' + octubre2.iloc[0]['Ticker'] + ' ' + str(croctubre2) + ' %'
        menoroctubre = 'Menor: ' + octubre1.iloc[0]['Ticker'] + ' ' + str(croctubre1) + ' %'

    if crseptiembre1 > crseptiembre2:
        mayorseptiembre = 'Mayor: ' + septiembre1.iloc[0]['Ticker'] + ' ' + str(crseptiembre1) + ' %'
        menorseptiembre = 'Menor: ' + septiembre2.iloc[0]['Ticker'] + ' ' + str(crseptiembre2) + ' %'
    else:
        mayorseptiembre = 'Mayor: ' + septiembre2.iloc[0]['Ticker'] + ' ' + str(crseptiembre2) + ' %'
        menorseptiembre = 'Menor: ' + septiembre1.iloc[0]['Ticker'] + ' ' + str(crseptiembre1) + ' %'

    if crdocemeses1 > crdocemeses2:
        mayordocemeses = 'Mayor: ' + docemeses1.iloc[0]['Ticker'] + ' ' + str(crdocemeses1) + ' %'
        menordocemeses = 'Menor: ' + docemeses2.iloc[0]['Ticker'] + ' ' + str(crdocemeses2) + ' %'
    else:
        mayordocemeses = 'Mayor: ' + docemeses2.iloc[0]['Ticker'] + ' ' + str(crdocemeses2) + ' %'
        menordocemeses = 'Menor: ' + docemeses1.iloc[0]['Ticker'] + ' ' + str(crdocemeses1) + ' %'

    archivoexcel = input('Seleccione un nombre para el archivo excel de crecimiento:')

    # Creamos un Pandas Excel writer usando XlsxWriter como el engine.
    writer = pd.ExcelWriter("/content/drive/My Drive/proyecto_integrador/" + archivoexcel + '.xlsx',
                            engine='xlsxwriter')
    datoscrecimiento = pd.DataFrame({'Crecimiento Octubre': [mayoroctubre, menoroctubre],
                                     'Crecimiento Septiembre': [mayorseptiembre, menorseptiembre],
                                     'Crecimiento doce meses': [mayordocemeses, menordocemeses]})
    datoscrecimiento.to_excel(writer, sheet_name='Tabla crecimiento')
    octubre1.to_excel(writer, sheet_name='Octubre ' + str(octubre1.iloc[0]['Ticker']))
    octubre2.to_excel(writer, sheet_name='Octubre ' + str(octubre2.iloc[0]['Ticker']))
    septiembre1.to_excel(writer, sheet_name='Septiembre ' + str(septiembre1.iloc[0]['Ticker']))
    septiembre2.to_excel(writer, sheet_name='Septiembre ' + str(septiembre2.iloc[0]['Ticker']))
    docemeses1.to_excel(writer, sheet_name='12meses ' + str(docemeses1.iloc[0]['Ticker']))
    docemeses2.to_excel(writer, sheet_name='12meses ' + str(docemeses2.iloc[0]['Ticker']))

    # Cerramos el Pandas Excel writer y guardamos los datos en el archivo Excel.
    writer.save()
    print('Crecimiento Octubre')
    print(mayoroctubre)
    print(menoroctubre)
    print()
    print('Crecimiento Septiembre')
    print(mayorseptiembre)
    print(menorseptiembre)
    print()
    print('Crecimiento Ultimos 12 meses')
    print(mayordocemeses)
    print(menordocemeses)


def entre_fechas(archivo1, archivo2):  # Analisis de acciones entre fechas ingresadas por el usuario
    fecha_inicio = input('Ingrese la fecha de inicio: ')
    fecha_fin = input('Ingrese la fecha de finalizacion: ')

    rango1 = pd.DataFrame()
    rango1 = archivo1[(archivo1.Date >= fecha_inicio) & (archivo1.Date < fecha_fin)]

    rango2 = pd.DataFrame()
    rango2 = archivo2[(archivo2.Date >= fecha_inicio) & (archivo2.Date < fecha_fin)]

    crrango1 = ((rango1.iloc[-1]['Open'] - rango1.iloc[0]['Open']) / rango1.iloc[0]['Open']) * 100
    crrango2 = ((rango2.iloc[-1]['Open'] - rango2.iloc[0]['Open']) / rango2.iloc[0]['Open']) * 100

    if crrango1 > crrango2:
        mayorrango = 'Mayor: ' + rango1.iloc[0]['Ticker'] + ' ' + str(crrango1) + ' %'
        menorrango = 'Menor: ' + rango2.iloc[0]['Ticker'] + ' ' + str(crrango2) + ' %'
    else:
        mayorrango = 'Mayor: ' + rango2.iloc[0]['Ticker'] + ' ' + str(crrango2) + ' %'
        menorrango = 'Menor: ' + rango1.iloc[0]['Ticker'] + ' ' + str(crrango1) + ' %'

    archivoexcel = input('Seleccione un nombre para el archivo excel de crecimiento: ')

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter("/content/drive/My Drive/proyecto_integrador/" + archivoexcel + '.xlsx',
                            engine='xlsxwriter')
    datoscrecimiento = pd.DataFrame({'Crecimiento entre fechas': [mayorrango, menorrango]})
    datoscrecimiento.to_excel(writer, sheet_name='Tabla crecimiento')
    rango1.to_excel(writer, sheet_name='Rango ' + str(rango1.iloc[0]['Ticker']))
    rango2.to_excel(writer, sheet_name='Rango ' + str(rango2.iloc[0]['Ticker']))

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

    print('Crecimiento entre ' + fecha_inicio + ' y ' + fecha_fin)
    print(mayorrango)
    print(menorrango)
    print()


# Preparamos los datos para graficar
def graficar():
    label1 = ticker1['Ticker'][0]
    label2 = ticker2['Ticker'][0]
    Xg = ticker1['Date']
    Yg = ticker1['Open']
    Xa = ticker2['Date']
    Ya = ticker2['Open']
    Xc = list(cruces.keys())
    Yc = list(cruces.values())
    Xd = list(dd.keys())
    Yd = list(dd.values())
    Xd2 = list(dd2.keys())
    Yd2 = list(dd2.values())

    ancho = 20
    alto = 10
    ancho_alto = (ancho, alto)

    plt.figure(figsize=ancho_alto)
    plt.subplot(311)
    plt.plot(Xg, Yg, 'b-', label=label1)
    plt.plot(Xa, Ya, 'r-', label=label2)
    plt.plot(Xc, Yc, 'y+', label='Cruces: ' + str(len(cruces)))
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
               ncol=1, mode="", borderaxespad=0.)
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.subplot(312)
    plt.plot(Xd, Yd, 'b-', label='DD ' + label1)
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
               ncol=1, mode="", borderaxespad=0.)
    # plt.legend()
    plt.subplot(313)
    plt.plot(Xd2, Yd2, 'r-', label='DD ' + label2)
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
               ncol=1, mode="", borderaxespad=0.)
    plt.subplots_adjust(hspace=.3)
    plt.show()


menu()