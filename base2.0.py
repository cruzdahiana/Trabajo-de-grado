# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 15:39:43 2020

@author: DAHIANA
"""
import cv2
import psycopg2
import numpy as np
from datetime import datetime

conexion1 = psycopg2.connect(database="Tg", user="postgres", password="123")
cursor1=conexion1.cursor()
cursor2=conexion1.cursor()

def agregar(nombre):
    nom=""
    nom+=nombre
    im= cv2.resize(cv2.imread(nom,1),(70,70))
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    fot=[]
    r,c=im.shape
    for i in range(r):
        for j in range(c):
            #print(im[i,j],end=",")
            fot.append(str(im[i,j]))
    return fot    

def sortA(a,b):
    n=len(a)
    for i in range(n):
        for j in range(n - i - 1):
            if a[j] < a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                b[j], b[j + 1] = b[j + 1], b[j]    
    return a,b

def guardarBd():      
    archivo = open("nuevosp.txt", "r")
    sql="insert into perro(tamano,sexo,raza,lugar,pelaje,cola,descripcion,fecha,posicion,estado,foto) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    for linea in archivo.readlines():
        a=linea.split(",")
        print(a)
        tamaño=a[0]
        sexo=a[1][:9]    
        raza=a[2]
        lugar=a[3]
        pelaje=a[4]
        cola=a[5]
        descripcion=a[6]
        fecha=a[7]
        posicion=a[8]
        estado=a[9]
        print(a[10][:-1])
        foto=agregar(a[10][:-1])
        datos=(tamaño,sexo,raza,lugar,pelaje,cola,descripcion,fecha,posicion,estado,foto)
        cursor1.execute(sql,datos)
    conexion1.commit()

def compararR(per,todos,parecids):
    tamaño=["pequeno","mediano","grande","muy grande"]
    sexo=["macho","hembra","no se con"]
    raza=["golden retriver","braco de weimar","chihuahua","bulldog",
          "yorkshire terrier","pastor aleman","french poodle","pug","labrador",
          "schnauzer","pincher","shih tzu","pitbull","bull terrier","beagle",
          "american bully","chow chow","husky siberiano","dalmata","otra"]
    #lugar=["a","b","c","d","e","f","g","h"]
    pelaje=["corto","medio","largo"]
    cola=["corta","larga"]
    #fecha=["1","2","3","4","5","6","7"]
    #tipoFoto=["frente","perfil"]
    #estado=["perdido","encontrado"]
    diff=(todos[8]-per[8]).days
    punt=0
    if(tamaño.index(per[1])==tamaño.index(todos[1])):punt+=30
    if(abs(tamaño.index(per[1])-tamaño.index(todos[1])) == 1):punt+=10
    if(sexo.index(per[2])==sexo.index(todos[2])):punt+=5
    if(sexo.index(todos[2])==2):punt+=3
    if(raza.index(per[3])==raza.index(todos[3])):punt+=50
    #if(lugar.index(per[4])==lugar.index(todos[4])):punt+=10
    if(pelaje.index(per[5])==pelaje.index(todos[5])):punt+=5
    if(abs(pelaje.index(per[5])-pelaje.index(todos[5])) == 1):punt+=3
    if(cola.index(per[6])==cola.index(todos[6])):punt+=14
    #if(descripcion.index(per[7])==descripcion.index(todos[7])):punt+=5
    if(diff<0):punt-=500
    if(diff<60 and diff>=0):punt+=10
    if(diff>=60):punt+=4
    parecids.append(round(punt*100/104, 2))#Cambiar el 94 por la suma mayor de las punt
    
def compararF(perro,comp,parecidos):
    im = perro[11]
    r=70
    c=70
    perros=[]
    ids=[]
    for fila in comp:
        perros.append(fila[11])
        ids.append(fila[0])
    posid=-1
    for p in perros:

        pxy=-1
        posid+=1
        cont=0
        comp=r*c +1
        for i in range(r):
            for j in range(c):
                pxy+=1
                if(int(im[pxy])<15 or int(p[pxy])<15):
                    comp-=1
                    continue
                elif(int(p[pxy])>240 or int(im[pxy])>240):
                    comp-=1
                    continue
                elif(abs(int(im[pxy])-int(p[pxy]))<100):
                    cont+=1
        if(comp==0):continue
        #print("Parecido entre ",perro[0]," y ",ids[posid]," es de: ",cont*100/(comp),"%")
        parecidos.append(round(cont*100/(comp) , 2))        
    return parecidos

def principal(identrada):
    parecidos=[]
    mejoresR=[]
    data=[]
    cursor1.execute("select * from perro  where idperro="+str(identrada))
    cursor2.execute("select * from Perro where estado='encontrado'")
    #compara el perro de identrada con los que se han encontrado
    for p in cursor1:
        for fila in cursor2:
            data.append(fila)#datos de todos los perros encontrados
            compararR(p,fila,parecidos)#modifica la lista parecidos para que tenga lo que se compara
        #print(fila)
        #print(parecidos)
    #print(parecidos)
#    for i in data:
#        print(i[0],end=",")
    sortA(parecidos,data)
#    print("\ndespues de organizar\n")
    print("SR",parecidos[:10])

    for i in range(10):
        mejoresR.append(data[i])
        print(data[i][0],end=",")
    #data=data[:10].copy()
#    for i in mejoresR:
#        print(i[3],end=",")
    resultF=[]
    data1=data[:10].copy()
    cursor1.execute("select * from perro  where idperro= 1")
    for p in cursor1:
        compararF(p,mejoresR,resultF)
    print("\n")
#    print(resultF)
    sortA(resultF,data1)
#    print("\ndespues de organizar\n")
    print("FOTOS",resultF)
    for i in data1:
        print(i[0],end=",")
    salida=[]
    print("\n")
    for i in range(len(mejoresR)):
        salida.append(round(parecidos[i]*0.5+resultF[data1.index(mejoresR[i])]*0.5,1))        
    print(salida)
    sortA(salida,data)
    print("FINAL")
    print(salida)
    for i in data[:10]:
        print(i[0],end=",")
    print("SALIDA")
    print("SEÑOR USUARIO")
    print("Para su mascota perdida",end=" ")
    cursor1.execute("select * from perro  where idperro="+str(identrada))
    for p in cursor1:
        print(p[0:9])
    print("Los perrros similares que se han encontrado son:")
    for i in data[:5]:
        print(i[0:9])
    
#    print(data[1][8], data[0][8])
#    print(data[0][8]- data[1][8])
        
#    sortA(data[:][0],parecidos)
#    sortA(data1[:][0],resultF)
#    for i in data:
#        print(i[0],end=",")
#    print("::::::")
#    for i in data1:
#        print(i[0],end=",")
#    final=[]
#    for i in range(len(data)):
#        final.append(parecidos[i]+resultF[i])
#    print("AL FINAL SE TIENE QUE")
#    print(final)
#    print(data)
    
principal(326)#346   326   331   313
#guardarBd()   
