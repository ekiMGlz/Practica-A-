import numpy as np
import scipy.misc as misc
import matplotlib.pyplot as plt
import json
import imageio
from tkinter import *
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
        frame = Frame()
        
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
        
        
        
        #Botones
        b1 = Button(master, text="Calcular Ruta")
        b1.pack()
        b2 = Button(master, text="Borrar")
        b2.pack()
        self.canvas = FigureCanvasTkAgg(self.fig,master=root)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        
        self.canvas.mpl_connect('button_press_event', self.onClick)
    
    def onClick(self, event):
        
        print("Botton: " + str(event.button))
        if event.inaxes != self.ax:
            print("No")
        else:
            print("Si")

            X = event.xdata
            Y = event.ydata
            i = indexOfClosest(X, Y, pX, pY)

            if event.button == 1:
                print(i)
                self.sctr._facecolors[self.start]=(0,0,1,1)
                self.start = i
                self.sctr._facecolors[self.start]=(0,1,0,1)
                self.canvas.draw()
            elif event.button == 3:
                print(i)
                self.sctr._facecolors[self.end]=(0,0,1,1)
                self.end = i
                self.sctr._facecolors[self.end]=(1,0,0,1)
                self.canvas.draw()
                
root=Tk()
a = App(root)
root.mainloop()