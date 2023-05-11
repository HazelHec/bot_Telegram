import math

def cardano_newton_cubic(a, b, c, d, x0=0, tol=1e-6, maxiter=100):
    """
    Encuentra las tres raíces del polinomio cúbico ax^3 + bx^2 + cx + d utilizando la fórmula de Cardano.
    Retorna una lista con las tres raíces encontradas.
    """
    try:
        delta = (b**2 - 3*a*c) / (9*a**2)
        delta_0 = (2*b**3 - 9*a*b*c + 27*a**2*d) / (54*a**3)

        if delta > 0:
            # Tres raíces reales distintas
            theta = math.acos(delta_0 / math.sqrt(delta**3))
            x1 = -2 * math.sqrt(delta) * math.cos(theta/3) - b/(3*a)
            x2 = -2 * math.sqrt(delta) * \
                math.cos((theta+2*math.pi)/3) - b/(3*a)
            x3 = -2 * math.sqrt(delta) * \
                math.cos((theta-2*math.pi)/3) - b/(3*a)
            print(f"Envio\n{x1,x2,x3}")
            return [x1,x2,x3]
        elif delta == 0:
            # Tres raíces reales iguales
            x1 = -b / (3*a)
            x2 = -b / (3*a)
            x3 = -b / (3*a)
            print(f"Envio\n{x1,x2,x3}")
            return [x1, x2, x3]
        else:
            x = x0
            for i in range(maxiter):
                # Evaluamos la función y su derivada
                fx = a*x**3 + b*x**2 + c*x + d
                fpx = 3*a*x**2 + 2*b*x + c
                # Calculamos el siguiente punto utilizando la fórmula de Newton-Raphson
                x_new = x - fx/fpx
                # Verificamos si se alcanzó la tolerancia
                if abs(x_new - x) < tol:
                    return x_new
                # Actualizamos el valor de la variable x
                x = x_new
            # Si se llega al máximo de iteraciones, se devuelve el último valor obtenido
            print(f"Envio\n{x}")
            return x
    except ValueError:
        """Encuentra una raíz real del polinomio de grado 3 utilizando el método de Newton-Raphson."""
        x = x0
        for i in range(maxiter):
            # Evaluamos la función y su derivada
            fx = a*x**3 + b*x**2 + c*x + d
            fpx = 3*a*x**2 + 2*b*x + c
            # Calculamos el siguiente punto utilizando la fórmula de Newton-Raphson
            x_new = x - fx/fpx
            # Verificamos si se alcanzó la tolerancia
            if abs(x_new - x) < tol:
                return x_new
            # Actualizamos el valor de la variable x
            x = x_new
        # Si se llega al máximo de iteraciones, se devuelve el último valor obtenido
        print(f"Envio\n{x}")
        return x
    