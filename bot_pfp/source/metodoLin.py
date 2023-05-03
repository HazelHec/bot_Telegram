#Programa del metodo de Lin
from sympy import *
import math
def lin(c,d):
#grado del polinomio
    n=3

    #Coeficientes
    a=[1,-1,c,d]


    #Condiciones iniciales
    p = 0
    q = 0

    #Incremento 
    deltaP = a[2]/a[1]
    deltaQ = a[3]/a[1]

    #Ecuaciones de recurrencia
    b0=0
    b1=0

    for i in range(20):
        p = p + deltaP
        q = q + deltaQ
        b0 = a[0]
        b1 = a[1]-p*b0
        R = a[2] - p*b1 - q*b0
        S = a[3] - q*b1
        deltaP = R/b1
        deltaQ = S/b1
        e = sqrt(pow(R,2)+pow(S,2))
        
    #Polinomio de grado 2
    # x^2 + px + q
    discriminante = p**2 - 4*1*q

    # Verificar si existen raíces reales
    if discriminante < 0:
        return -b1
    else:
        # Calcular las raíces
        x1 = (-p + math.sqrt(discriminante)) / (2*1)
        x2 = (-p - math.sqrt(discriminante)) / (2*1)
        #Se regresa menos b1, ya que al resolver el polinomio de grado 1 tiene 
        #La estructura b0x + b1 = 0
        return list(x1,x2,-b1)
        
