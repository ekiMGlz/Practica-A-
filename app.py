# -*- coding: utf-8 -*-

import numpy as np
import scipy.misc as misc
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import json
import imageio
import subprocess
import time
from tkinter import *
from tkinter.ttk import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def indexOfClosest(x, y, px, py):
     return np.argmin([(x-px[i])**2 + (y-py[i])**2 for i in range(len(px))])

pX = []
pY = []
nombres = []
MEX = imageio.imread("assets/mexico.gif")
MEX = misc.imresize(MEX,185)
cities = json.load(open("data/data.json", 'r'))
roads = json.load(open("data/connect5.json"))

#Inicializa puntos y nombres
tot = len(cities)
for i in range(tot):
    coorx, coory, nom = cities[str(i)]
    pX.append(coorx)
    pY.append(coory)
    nombres.append(nom)

#Crear matriz de conexiones para pintar

R = np.zeros((tot, tot))
for k in roads.keys():
    for j in roads[k].keys():
        if int(k)<int(j):
            R[int(k),int(j)] = 1
        else:
            R[int(j),int(k)] = 1    
            

class App:
    def __init__(self, master):
        self.frame = Frame()
        
        ##Inicializa cosas
        self.start = 0
        self.end = 1
        
        #Creacion del plot
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.imshow(MEX)
        self.sctr = self.ax.scatter(pX,pY,c=['b']*len(pX))
        
        #Crea las conexiones del grafo
        for i in range(tot):
            for j in range(i,tot):
                if R[i,j]==1:
                    self.ax.plot([ pX[i], pX[j] ], [ pY[i], pY[j] ], linewidth=0.5, c='k')
        
        
        
        #Elementos del GUI
        self.l1 = Label(master, text="Origen: ")
        self.l1.pack()
        
        self.dd1 = Combobox(master, state = "readonly")
        self.dd1['values']=nombres
        self.dd1.current(0)
        self.dd1.bind("<<ComboboxSelected>>", self.onOriginChange)
        self.dd1.pack()
        
        self.l2 = Label(master, text="Destino: ")
        self.l2.pack()
        
        self.dd2 = Combobox(master, state = "readonly")
        self.dd2['values']=nombres
        self.dd2.current(0)
        self.dd2.bind("<<ComboboxSelected>>", self.onDestinyChange)
        self.dd2.pack()
        
        self.b1 = Button(master, text="Calcular Ruta", command = self.onClickCalcula)
        self.b1.pack()
        
        self.b2 = Button(master, text="Borrar", command = onClickReset)
        self.b2.pack()
        
        self.canvas = FigureCanvasTkAgg(self.fig,master=root)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        
        self.canvas.mpl_connect('button_press_event', self.onClick)
    
    def onClick(self, event):
        
        if not event.inaxes != self.ax:
        
            X = event.xdata
            Y = event.ydata
            i = indexOfClosest(X, Y, pX, pY)

            if event.button == 1:
                self.dd1.current(i)
                if self.end!=self.start:
                    self.sctr._facecolors[self.start]=(0,0,1,1)
                self.start = i
                self.sctr._facecolors[self.start]=(0,1,0,1)
                self.canvas.draw()
            elif event.button == 3:
                self.dd2.current(i)
                if self.end!=self.start:
                    self.sctr._facecolors[self.end]=(0,0,1,1)
                self.end = i
                self.sctr._facecolors[self.end]=(1,0,0,1)
                self.canvas.draw()
    
    def onOriginChange(self, event):
        i = self.dd1.current()
        
        self.sctr._facecolors[self.start]=(0,0,1,1)
        self.start = i
        self.sctr._facecolors[self.start]=(0,1,0,1)
        self.canvas.draw()
    
    def onDestinyChange(self, event):
        i = self.dd2.current()
        
        self.sctr._facecolors[self.end]=(0,0,1,1)
        self.end = i
        self.sctr._facecolors[self.end]=(1,0,0,1)
        self.canvas.draw()
    
    def onClickCalcula(self):
        self.coorS = np.array([int(cities[str(self.start)][0]), int(cities[str(self.start)][1])])
        self.coorE = np.array([int(cities[str(self.end)][0]), int(cities[str(self.end)][1])])

        #Output para lisp
        f = open("data/in.txt", 'w')
        f.write("({0} nil {1} {2} {3} 0 {3})\n".format(self.start, self.coorS[0], self.coorS[1], np.linalg.norm(self.coorS-self.coorE))) 
        f.write("({0} nil {1} {2} 0 0 0)\n(".format(self.end, self.coorE[0], self.coorE[1]))

        #Guarda el resto de los nodos como (id x y h), hay q completarlos en lisp
        for i in cities.keys():
            self.coorN = [int(cities[i][0]), int(cities[i][1])]
            f.write("({0} {1} {2} {3})".format(i, self.coorN[0], self.coorN[1], np.linalg.norm(self.coorN-self.coorE)))
        f.write(")")
        f.close()
        
        subprocess.call(["clisp", "A-star.cl"])
        
        res = open("data/out.txt", 'r')
        self.ruta = res.read()[1:-1].split(' ')
        res.close()
        self.ruta = [int(i) for i in self.ruta]
        
        #Pintar ruta final
        for i in range(len(self.ruta)-1):
            self.ax.plot([pX[self.ruta[i]], pX[self.ruta[i+1]]], [pY[self.ruta[i]], pY[self.ruta[i+1]]], c='r')
            self.canvas.draw()
            time.sleep(0.5)

def onClickReset():
    global root
    global a
    root.destroy()
    root=Tk()
    root.title("A*")
    a = App(root)
    root.mainloop()

    
root=Tk()
root.title("A*")
a = App(root)
root.mainloop()