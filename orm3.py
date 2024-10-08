import tkinter as tk
import random
import math
import sqlite3
import json


#zona declarativa

personas=[]

class colorAleatorio():
    def colorRandom():
         r=random.randint(0,255)
         g=random.randint(0,255)
         b=random.randint(0,255)
         hexadecimal="#{:02x}{:02x}{:02x}".format(r,g,b)
         return hexadecimal  

class Recoger ():
    def __init__(self):
        self.posx=random.randint(0,768)
        self.posy=random.randint(0,768)
        self.color=colorAleatorio.colorRandom()

    def inventarioSerializado(self):
        return{
            "posicionX":self.posx,
            "posiciony":self.posy,
            "color":self.color,
            }
    
    
class Comida():
    def __init__(self):
        self.desayuno=random.randint(0,1)
        self.almuerzo=random.randint(0,1)
        self.cena=random.randint(0,1)
       
class Persona ():
    def __init__(self):
        self.posx=random.randint(0,768)
        self.posy=random.randint(0,768)
        self.size=10
        self.direccion=random.randint(0,360)
        self.color=colorAleatorio.colorRandom()
        self.identificador=""
        self.energia=100
        self.descanso=100
        self.cantidadEnergia=""
        self.cantidadDescanso=""
        self.edad=random.randint(0,99)
        self.inventario=[]
        for i in range (0,10):
            self.inventario.append(Recoger())
        self.desayuno=random.randint(0,1)
        self.almuerzo=random.randint(0,1)
        self.cena=random.randint(0,1)
        self.comida=[]
        for i in range(0,3):
            self.comida.append(Comida())
    
    def dibujar (self):
        self.identificador=lienzo.create_rectangle(
            self.posx-self.size/2,
            self.posy-self.size/2,
            self.posx+self.size/2,
            self.posy+self.size/2,
            fill=self.color
        )
        self.cantidadEnergia=lienzo.create_rectangle(
            self.posx-self.size/2,
            self.posy-self.size/2-10,
            self.posx-self.size/2,
            self.posy-self.size/2-8,
            fill="green"
        )
        self.cantidadDescanso=lienzo.create_rectangle(
            self.posx-self.size/2,
            self.posy-self.size/2-16,
            self.posx-self.size/2,
            self.posy-self.size/2,
            fill="red"
        )

        

    def mover(self):
        if self.energia>0:
            self.energia-=0.2
        if self.descanso>0:
            self.descanso-=0.3

        lienzo.move(
             self.identificador,
             math.cos(self.direccion),
             math.sin(self.direccion)
             )
        
        anchoEnergia=(self.energia/100)*self.size
        lienzo.coords(
             self.cantidadEnergia,
             self.posx-self.size/2,
             self.posy-self.size/2-10,
             self.posx-self.size/2+anchoEnergia,
             self.posy-self.size/2-8
             )
        
        anchoDescanso=(self.descanso/100)*self.size
        lienzo.coords(
             self.cantidadDescanso,
             self.posx-self.size/2,
             self.posy-self.size/2-16,
             self.posx-self.size/2+anchoDescanso,
             self.posy-self.size/2-14
             )
        
        self.paredes()
        #actualizar posicion del objeto
        self.posx+=math.cos(self.direccion)
        self.posy+=math.sin(self.direccion)


    #rebotar paredes de la ventana
    def paredes(self):
         if self.posx < 0 or self.posx>768 or self.posy<0 or self.posy>768:
              self.direccion+=math.pi

    def crearDiccionario(self):
        serializar={
            "posicionX":self.posx,
            "posiciony":self.posy,
            "tamano":self.size,
            "direccion":self.direccion,
            "color":self.color,
            "identidad":self.identificador,
            "energia":self.energia,
            "descanso":self.descanso,
            "edad":self.edad,
            "inventario":[vars(item) for item in self.inventario],
            "comida":[vars(item) for item in self.comida]
        }
        return(serializar)


def guardarEstado():
    print("guardado")
    serializarJugador=[persona.crearDiccionario() for persona in personas]
    with open("practica8.json","w") as archivo:
        json.dumps(serializarJugador)

    #Guardar en SQLite
    conexion=sqlite3.connect("poblacion.sqlite3")
    cursor=conexion.cursor()
    #cursor.execute(" DELETE FROM poblacion")
    conexion.commit()
    for persona in personas:
        cursor.execute('''
                    INSERT INTO poblacion
                    VALUES (
                    NULL,
                    '''+str(persona.posx)+''',
                    '''+str(persona.posy)+''',
                    '''+str(persona.size)+''',
                    '''+str(persona.direccion)+''',
                    "'''+str(persona.color)+'''",
                    "'''+str(persona.identificador)+'''",
                    '''+str(persona.energia)+''',
                    '''+str(persona.descanso)+''',
                    '''+str(persona.edad)+''',
                    "'''+str(persona.inventario)+'''",
                    "'''+str(persona.comida)+'''"
                    )
                    ''')
    for elemento in persona.inventario:
        cursor.execute('''
                    INSERT INTO recogibles
                    VALUES (
                    NULL,
                    '''+str(persona.identificador)+''',
                    "'''+str(persona.posx)+'''",
                    "'''+str(persona.posy)+'''",
                    "'''+str(persona.color)+'''"
                    )
                    ''')
    for comida in persona.comida:
        cursor.execute('''
                    INSERT INTO comida
                    VALUES (
                    NULL,
                    '''+str(persona.identificador)+''',
                    '''+str(persona.desayuno)+''',
                    '''+str(persona.almuerzo)+''',
                    '''+str(persona.cena)+'''
                    )
                    ''')
    conexion.commit()
    conexion.close()

raiz=tk.Tk()

lienzo=tk.Canvas(raiz,width=768,height=768)
lienzo.pack()

boton=tk.Button(raiz,text="guardar",command=guardarEstado)
boton.pack()

#cargar desde SQL
try:
    conexion=sqlite3.connect("poblacion.sqlite3")
    cursor=conexion.cursor()
    cursor.execute('''
                   SELECT * 
                   FROM poblacion
                   ''')
    while True:
        fila=cursor.fetchone()
        if fila is None:
            break
        persona=Persona()
        persona.posx=fila[1]
        persona.posy=fila[2]
        persona.size=fila[3]
        persona.direccion=fila[4]
        persona.color=fila[5]
        persona.identificador=fila[6]
        persona.energia=fila[7]
        persona.descanso=fila[8]
        persona.edad=fila[9]

        cursor2=conexion.cursor()
        peticion2='''
            SELECT *
            FROM recogibles
            WHERE persona= '''+persona.identificador+'''
            '''
        cursor2.execute(peticion2)
        while True:
            fila2=cursor2.fetchone()
            if fila2 is None:
                break
            nuevoRecogible=Recoger()
            nuevoRecogible.posx=fila2[2]
            nuevoRecogible.posy=fila2[3]
            nuevoRecogible.color=fila2[4]
            persona.inventario.append(nuevoRecogible)  
            pass
        
        cursor3=conexion.cursor()
        peticion3='''
            SELECT *
            FROM comida
            WHERE persona= '''+persona.identificador+'''
            '''
        cursor3.execute(peticion3)
        while True:
            fila3=cursor3.fetchone()
            if fila3 is None:
                break
            nuevoComida=Comida()
            nuevoComida.desayuno=fila2[2]
            nuevoComida.almuerzo=fila2[3]
            nuevoComida.cena=fila2[4]
            persona.inventario.append(nuevoComida)  
            pass

        personas.append(persona)
    conexion.close()
    print("Cargado con exito")
except:
    print("error en recuperación")

#introduzco personas en la colección
if len(personas)==0:
    numeroPersonas=50
    for i in range (0, numeroPersonas):
        personas.append(Persona())


#para cada persona en colección las muestro en pantalla
for persona in personas:
    persona.dibujar()


#bucle para mover cada persona en colección
def bucle():
        for persona in personas:
            persona.mover()
        raiz.after(10,bucle)

bucle()



persona=Persona()
persona.dibujar()
raiz.mainloop()