from django.shortcuts import render
from .models import Tejidos, Grafo
from django_pandas.io import read_frame
from math import sqrt

def home(request):
    return render(request, 'app/home.html')


def datos(request):
    datos = Tejidos.objects.all()
    procesado = procesa_tabla(datos)
    return render(request, 'app/datos.html', {'misTejidos': datos, 'proceso': procesado})


def procesa_tabla(qs):
    df = read_frame(qs)
    return df


def resultados(request):
    tejido = Tejidos.objects.all()
    print('longitud: ' + str(len(tejido)))
    df = read_frame(tejido)

    mediaTemperatura = df['temperatura'].mean()

    mediaColor = df['color'].mean()
    
    mediaInflamacion = df['inflamacion'].mean()

    m = df.iloc[0, 2:5].mean()
   
    lista = [{'r1: ': df['id'][j], 'r2: ': df['id'][i], 'distancia': sqrt((abs(df.iloc[j, 2:5]-df.iloc[i, 2:5]).sum())*2)} for j in range(0, len(tejido)-1) for i in range(j+1, len(tejido))]
    lista2 = [{'r1: ': df['id'][j], 'r2: ': df['id'][i], 'conectado: ': True if sqrt((abs(df.iloc[j, 2:5]-df.iloc[i, 2:5]).sum())*2)<5 else False} for j in range(0, len(tejido)-1) for i in range(j+1, len(tejido))]
    
    listafinal = [{'nodo': Grafo.objects.create(origen=Tejidos.objects.get(pk=df.iloc[j,0:1]), destino=Tejidos.objects.get(pk=df.iloc[i,0:1]), conectado= True if sqrt((abs(df.iloc[j, 2:5]-df.iloc[i, 2:5]).sum())*2)<5 else False).save() }for j in range(0, len(tejido)-1) for i in range(j+1, len(tejido))]

    diccionario = {'mediaT': mediaTemperatura, 'mediaC': mediaColor, 'm': m, 'mediaI': mediaInflamacion}
    diccionario['lista2']=lista2
    diccionario['lista']=lista
    diccionario['max'] = df.iloc[0, 2:5].max()
    return render(request, 'app/resultados.html', diccionario)
