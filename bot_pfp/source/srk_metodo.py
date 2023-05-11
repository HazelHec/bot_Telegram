from source.raicesp3 import cardano_newton_cubic
from source.creat_excel import creat_densidad, creat_presion
"""----------------------------------------------------------------------------"""
# SECTION - Función auxiliar m


def m(x):
    return 0.480 + (1.574*x) - (0.176*pow(x, 2))


def SRK(chatId, dt, y, T=460, n=0, vc=0, mc=0, P=0):
    """----------------------------------------------------------------------------"""
    # SECTION - Zona de variables
    R = 10.732
    # Delta del mezclado
    deltam = 0
    # Declaración de atm
    atm = 0
    # Datos para las raices
    raicesPositivas = []
    z1 = 0
    z2 = 0
    """----------------------------------------------------------------------------"""

    # SECTION - Zona de iterables
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
    # Metodo tr
    tr = list(T/tc for tc in tc)
    # Metodo alpha
    alpha = list(pow(1 + (m(w)*(1 - pow(tr, 0.5))), 2) for tr, w in zip(tr, w))
    # metodo de ac
    ac = list((0.42748*pow(R, 2)*pow(tc, 2))/pc for tc, pc in zip(tc, pc))
    at = list(alpha*ac for alpha, ac in zip(alpha, ac))
    b = list((0.08664*R*tc)/pc for tc, pc in zip(tc, pc))

    # Metodo para la regla de mezclado
    for i in range(0, n):
        for j in range(0, n):
            atm += (y[i]*y[j])*pow(at[i]*at[j], 0.5)*(1-deltam)
    bt = sum(b*y for b, y in zip(b, y))

    # Metodo para A y B
    A = (atm*P)/(pow(10.732*T, 2))
    B = (bt*P)/(10.732*T)

    # Calculo de mc masa del hidrocarburo
    if mc == 0:
        mc = sum(y*masa for y, masa in zip(y, masa))

    """----------------------------------------------------------------------------"""

    # SECTION - # Procedimiento del problema de densidad

    if (P != 0):
        # Metodo para obtener raices
        try:
            z, z1, z2 = cardano_newton_cubic(1, -1, A-B-pow(B, 2), -(A*B))
            print(f"valor de z: {z, z1, z2}")
            if z > 0 and z1 > 0 and z2 > 0:
                densidadL = (P*mc)/(z*R*T)  # densidad del liquido
                densidadG = (P*mc)/(z2*R*T)  # densidad del gas
                creat_densidad(chatId, dt, y, alpha, ac, at, b, atm,
                               bt, A, B, mc, densidadL, densidadG, 0, z, 0, z2)
                return [round(densidadL, 5), round(densidadG, 5)]
            elif z < 0 and z1 > 0 and z2 > 0:
                densidadL = (P*mc)/(z1*R*T)  # densidad del liquido
                densidadG = (P*mc)/(z2*R*T)  # densidad del gas
                creat_densidad(chatId, dt, y, alpha, ac, at, b, atm,
                               bt, A, B, mc, densidadL, densidadG, 0, 0, z1, z2)
                return [round(densidadL, 5), round(densidadG, 5)]
            elif z < 0 and z1 < 0 and z2 > 0:
                densidad = (P*mc)/(z2*R*T)
                creat_densidad(chatId, dt, y, alpha, ac, at, b,
                               atm, bt, A, B, mc, 0, 0, densidad, 0, 0, z2)
                return round(densidad, 5)
            else:
                densidad = (P*mc)/(z2*R*T)
                creat_densidad(chatId, dt, y, alpha, ac, at, b,
                               atm, bt, A, B, mc, 0, 0, densidad, 0, 0, z2)
                return round(densidad, 5)
        except TypeError:
            z = cardano_newton_cubic(1, -1, A-B-pow(B, 2), -(A*B))
            print(f"valor de z: {z}")
            densidad = (P*mc)/(z*R*T)
            # bt ya no es lista
            creat_densidad(chatId, dt, y, alpha, ac, at, b, atm,
                           bt, A, B, mc, 0, 0, densidad, z, 0, 0)

            return round(densidad, 5)
    # SECTION - # Procedimiento del problema de presión
    else:
        vm = vc/mc
        presion = ((R*T)/(vm-bt))-((atm)/(vm*(vm+bt)))
        creat_presion(chatId, dt, y, alpha, ac, at, b,
                      atm, bt, A, B, mc, vc, vm, presion)
        print(f"Valor de la presión: {presion}")
        return round(presion, 5)


if __name__ == "__main__":
    try:
        z, z1, z2 = cardano_newton_cubic(1, -1.044, 0.17, -0.00748)
        print(z, z1, z2)
    except TypeError:
        z = cardano_newton_cubic(1, -1.044, 0.17, -0.00748)
        print(z)
