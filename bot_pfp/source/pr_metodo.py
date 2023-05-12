from source.raicesp3 import cardano_newton_cubic
from source.creat_excel import creat_densidad, creat_presion

#!SECTION Función de apoyo m
def m(x):
    return 0.37464 + (1.54556*x) - (0.26992*pow(x, 2))

def peng_r(chatId, dt, y, T=460, n=0, vc=0, mc=0, P=0):
    """----------------------------------------------------------------------------"""
    # SECTION - Zona de variables y constantes
    R = 10.732
    # Delta del mezclado
    deltam = 0
    # Declaración de atm
    am = 0
    # Datos para las raices
    raicesPositivas = []
    z1 = 0
    z2 = 0
    # parámetros de las sustancias puras adimensionales
    omega_a = 0.457234
    omega_b = 0.077796
    """----------------------------------------------------------------------------"""
    # SECTION - Zona de iterables

    # Masa molar de la mezcla
    masa = list(map(lambda x: x["Masa molar"], dt))
    # Presión critica
    pc = list(map(lambda x: x["Presión Critica"], dt))
    # Temperatura critica
    tc = list(map(lambda x: x["Temperatura Critica"]+460, dt))
    # Factor acéntrico
    w = list(map(lambda x: x["Factor acéntrico"], dt))
    # Metodo tr
    tr = list(T/tc for tc in tc)
    # Obtener alpha
    alpha = list(pow(1 + (m(w)*(1 - pow(tr, 0.5))), 2) for tr, w in zip(tr, w))
    # calculo de ac
    ac = list(omega_a*((pow(R, 2)*pow(tc, 2))/pc) for tc, pc in zip(tc, pc))
    # Calculo de at
    at = list(ac*alpha for ac, alpha in zip(ac, alpha))
    # Calculo de b
    bt = list(omega_b*((R*tc)/pc) for tc, pc in zip(tc, pc))
    # Metodo para la regla de mezclado
    for i in range(0, n):
        for j in range(0, n):
            am += (y[i]*y[j])*pow(at[i]*at[j], 0.5)*(1-deltam)
    bm = sum(b*y for b, y in zip(bt, y))
    # Calculo de A y B
    A = (am*P)/(pow(R*T, 2))
    B = (bm*P)/(R*T)
    # Calculo de mc masa del hidrocarburo
    if mc == 0:
        mc = sum(y*masa for y, masa in zip(y, masa))
    """----------------------------------------------------------------------------"""
    # SECTION - Zona de calculos finales y devolución de solución

    if (P != 0):
        # Metodo para obtener raices
        try:
            z, z1, z2 = cardano_newton_cubic(
                1, (B-1), A-2*B-3*pow(B, 2), -(A*B-pow(B, 2)-pow(B, 3)))
            if(z>0):
                raicesPositivas.append(z)
            if(z1>0):
                raicesPositivas.append(z1)
            if(z2>0):
                raicesPositivas.append(z2)
            raicesPositivas.sort()
            
            if(len(raicesPositivas)==2):
                densidadL = (P*mc)/(raicesPositivas[0]*R*T)  # densidad del liquido
                densidadG = (P*mc)/(raicesPositivas[1]*R*T)  # densidad del gas
                creat_densidad(chatId, dt, y, alpha, ac, at, bt, am,
                               bm, A, B, mc, densidadL, densidadG, 0, raicesPositivas[0], raicesPositivas[1], 0)
                print(f"valor de z: {raicesPositivas[0], raicesPositivas[1]}")
                return [round(densidadL, 5), round(densidadG, 5)]
            elif(len(raicesPositivas)==3):
                densidadL = (P*mc)/(raicesPositivas[0]*R*T)  # densidad del liquido
                densidadG = (P*mc)/(raicesPositivas[2]*R*T)  # densidad del gas
                creat_densidad(chatId, dt, y, alpha, ac, at, bt, am,
                               bm, A, B, mc, densidadL, densidadG, 0, raicesPositivas[0], raicesPositivas[2], 0)
                print(f"valor de z: {raicesPositivas}")
                return [round(densidadL, 5), round(densidadG, 5)]
            else:
                densidad = (P*mc)/(raicesPositivas[0]*R*T)
                # bt ya no es lista
                creat_densidad(chatId, dt, y, alpha, ac, at, bt, am,
                           bm, A, B, mc, 0, 0, densidad, raicesPositivas[0], 0, 0)

            return round(densidad, 5)
            
        except TypeError:
            z =  cardano_newton_cubic(
                1, (B-1), A-2*B-3*pow(B, 2), -(A*B-pow(B, 2)-pow(B, 3)))
            print(f"valor de z: {z}")
            densidad = (P*mc)/(z*R*T)
            # bt ya no es lista
            creat_densidad(chatId, dt, y, alpha, ac, at, bt, am,
                           bm, A, B, mc, 0, 0, densidad, z, 0, 0)

            return round(densidad, 5)
    else:
        #Método de vm
        vm = vc/mc
        presion = ((R*T)/(vm-bm))-(am/(vm*(vm+bm)+bm*(vm-bm)))
        creat_presion(chatId, dt, y, alpha, ac, at, bt,
                      am, bm, A, B, mc, vc, vm, presion)
        print(f"Valor de la presión: {presion}")
        return round(presion, 5)



