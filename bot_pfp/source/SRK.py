# En este programa obtendre todo lo necesario para la resolución de problemas
from source.metodoLin import lin


def m(x):
    return 0.480 + (1.574*x) - (0.176*pow(x, 2))
# EL metodo recibe los datos, la fracción mol, la presión y la temperatura


def SRK(dt, y, T=460, n=0, vc=0, mc=0, P=0):
    R = 10.732  # Constante
    deltam = 0  # delta del mezclado
    atm = 0  # declaración de atm
    # Datos para las raices
    raicesPositivas = []  # delcarar las raices positivas
    z1 = 0
    z2 = 0

    # Componentes de tabla
    nombre = list(map(lambda x: x["Componente"], dt))
    # Masa molar de la mezcla
    masa = list(map(lambda x: x["Masa molar"], dt))
    # Presión critica
    pc = list(map(lambda x: x["Presión Critica"], dt))
    # Temperatura critica
    tc = list(map(lambda x: x["Temperatura Critica"]+460, dt))
    # Factor acéntrico
    w = list(map(lambda x: x["Factor acéntrico"], dt))
    ############# __Metodo para at__#############
    # Metodo tr
    tr = list(T/tc for tc in tc)
    # Metodo alpha
    alpha = list(pow(1 + (m(w)*(1 - pow(tr, 0.5))), 2) for tr, w in zip(tr, w))
    # metodo de ac
    ac = list((0.42748*pow(R, 2)*pow(tc, 2))/pc for tc, pc in zip(tc, pc))

    at = list(alpha*ac for alpha, ac in zip(alpha, ac))

    ############# __Metodo para b__#############
    b = list((0.08664*R*tc)/pc for tc, pc in zip(tc, pc))

    ############# __Metodo para la regla de mezclado__#############

    for i in range(0, n):
        for j in range(0, n):
            atm += (y[i]*y[j])*pow(at[i]*at[j], 0.5)*(1-deltam)

    bt = sum(b*y for b, y in zip(b, y))

    ############# __Metodo para A y B__#############
    A = (atm*P)/(pow(10.732*T, 2))

    B = (bt*P)/(10.732*T)
    
    #Calculo de mc masa del hidrocarburo
    if mc == 0: 
        mc = sum(y*masa for y, masa in zip(y, masa))
    #Procedimiento del problema de densidad
    if(P!=0):
        ############# __Metodo para obtener raices__#############
        raices = lin(A-B-pow(B, 2), -(A*B))
        print(type(raices))
        if (type(raices) == list):
            raices.sort()
            print(raices)
            for raiz in raices:
                if (raiz < 0):
                    print("Hay una raíz negativa\n")
                else:
                    raicesPositivas.append(raiz)
            if (len(raicesPositivas == 2)):
                z1 = raicesPositivas[0]  # Raíz del liquido
                z2 = raicesPositivas[1]  # Raíz del gas
            elif (len(raicesPositivas == 3)):
                z1 = raicesPositivas[0]  # Raíz del liquido
                z2 = raicesPositivas[2]  # Raíz del gas
            else:
                z = raicesPositivas
        else:
            z = raices
        
        ############# __Metodo para obtener la densidad__#############
        if (z1 == 0):
            densidad = (P*mc)/(z*R*T)
            return round(densidad, 5)
        
        else:
            densidadL = (P*mc)/(z1*R*T)  # densidad del liquido
            densidadG = (P*mc)/(z2*R*T)  # densidad del gas
            return list(round(densidadL, 5), round(densidadG, 5))
            
    ############# __Metodo para obtener la presión__#############
    else:
        vm = vc/mc
        presion = ((R*T)/(vm-bt))-((atm)/(vm*(vm+bt)))
        return round(presion, 5)
