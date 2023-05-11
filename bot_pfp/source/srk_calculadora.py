import config as con  # Importa el bot
import decimal
# lib para crear botones y para contestar un mensaje
from telebot.types import ForceReply, ReplyKeyboardMarkup
from source.conexion import conect1
from source.srk_metodo import SRK
import time
"--------------------------------------------------------------------------------"

# Declaración de variables globales
# variables
lista = []
dic = dict
y = []
contador = 0
numeroDeElementos = int
temperatura = float
volumenCelda = float
mc = float
presion = float
temperatura = float
eleccion = str
densidadl = float
densidadg = float
densidad = float
chatId = int


class ValueHolder:
    def __init__(self, value):
        self.value = value


numeroDeElementos = 5
mmh7p = ValueHolder(None)
tch7p = ValueHolder(None)
pch7p = ValueHolder(None)
fah7p = ValueHolder(None)
yh7p = ValueHolder(None)

eleccion = str

"--------------------------------------------------------------------------------"
#!SECTION Funciones auxiliares


def resetVariables():
    global lista, dic, y, contador, numeroDeElementos, temperatura, volumenCelda, mc, presion, eleccion, densidadl, densidadg, densidad, mmh7p, tch7p, pch7p, fah7p, yh7p
    lista = []
    dic = {}
    y = []
    contador = 0
    numeroDeElementos = 0
    temperatura = 0.0
    volumenCelda = 0.0
    mc = 0.0
    presion = 0.0
    temperatura = 0.0
    densidadl = 0.0
    densidadg = 0.0
    densidad = 0.0
    mmh7p.value = 0.0
    tch7p.value = 0.0
    pch7p.value = 0.0
    fah7p.value = 0.0
    yh7p.value = 0.0

# NOTE - Función para conexión a la base de datos


def aux(a):
    # Lista cuyo sera el directorio
    encabezado = ('Número', 'Componente', 'Formula', 'Masa molar',
                  'Temperatura Critica', 'Presión Critica', 'Factor acéntrico')
    lista = []
    # Metodos para la conexion con la base de datos
    conexion = conect1()
    cursor = conexion.cursor()
    # Query de consulta
    query = f'''SELECT * FROM svk_datos 
    where if((select count(*) from svk_datos where componente = '{a}') > 0,
    componente = '{a}', componente like '%{a}%');'''
    # Metodo para hacer consultas
    cursor.execute(query)
    data = cursor.fetchall()
    # print(data)
    if (len(data) == 0):
        # Devuelve un mesaje al usuario para que pueda volver a insertar el elemento
        print("""El elemento solicitado no se encuentra en la base de datos\n
              Intente de nuevo""")
        return None
    else:
        # Metodo por el cual obtenemos los datos en orden
        for dt in data:
            for d in dt:
                if (isinstance(d, decimal.Decimal)):
                    lista.append(float(d))
                else:
                    print(d)
                    lista.append(d)
            break
        datos = {encabezado: lista for encabezado,
                 lista in zip(encabezado, lista)}
        return datos
    cursor.close()
    conexion.close()


def get_float_input(message, bot, set_variable, next_step):
    try:
        value = float(message.text)
        set_variable(value)
        next_step(message, bot)
    except ValueError:
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id, "ERROR: Debes ingresar un número.\nIntenta nuevamente.", reply_markup=markup)
        bot.register_next_step_handler(
            msg, lambda m: get_float_input(m, bot, set_variable, next_step))


def reiniciar(message, bot):
    bot.reply_to(message, "¡Proceso reiniciado!")
    bot.clear_step_handler(message.chat.id)
    # Aquí puedes agregar cualquier código adicional que necesites para reiniciar el proceso


"--------------------------------------------------------------------------------"
# SECTION - Preguntar el volumen si se trata de la presión y la presión si se trata de la densidad


def procesar_opcion(opcion, cid, bot):
    global eleccion, chatId
    eleccion = opcion
    chatId = cid
    resetVariables()
    if opcion == 'srk_presion':
        markup = ForceReply()
        msg = bot.send_message(
            cid, "Por favor, escribe la temperatura en Rankine.", reply_markup=markup)
        bot.register_next_step_handler(msg, VolumenCelda, bot)
    elif opcion == 'srk_densidad':
        markup = ForceReply()
        msg = bot.send_message(
            cid, "Por favor, escribe la temperatura en Rankine.", reply_markup=markup)
        bot.register_next_step_handler(msg, setPresion, bot)


"--------------------------------------------------------------------------------"
# SECTION - Elementos para problema de presión


def VolumenCelda(message, bot):
    global temperatura
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)
    try:
        temperatura = float(message.text)
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id, "Escribe el volumen de la celda en ft^3", reply_markup=markup)
        bot.register_next_step_handler(msg, RespuestaMc, bot)
    except ValueError:
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id,
            "ERROR: Debes ingresar un número.\nPor favor, escribe la temperatura en Rankine.",
            reply_markup=markup)
        bot.register_next_step_handler(msg, VolumenCelda, bot)


def RespuestaMc(message, bot):
    global volumenCelda
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)
    try:
        volumenCelda = float(message.text)
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True,
            input_field_placeholder="Seleciona una opción",
            resize_keyboard=True
        )
        markup.add("Si", "No")
        msg = bot.send_message(
            message.chat.id, "¿Tienes el valor de mc?", reply_markup=markup)
        bot.register_next_step_handler(msg, setMc, bot)

    except ValueError:
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id,
            "ERROR: Debes ingresar un número.\nEscribe el volumen de la celda en ft^3.",
            reply_markup=markup)
        bot.register_next_step_handler(msg, RespuestaMc, bot)


def setMc(message, bot):
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)
    mcsi = 1
    if message.text.lower() == "si":
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id, "Introduzca el valor de mc", reply_markup=markup)
        bot.register_next_step_handler(msg, getElements, bot, mcsi)
    else:
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True,
            input_field_placeholder="Seleccione una opción",
            resize_keyboard=True
        )
        markup.add("Continuar")
        msg = bot.send_message(
            message.chat.id, "Presiona continuar", reply_markup=markup)
        bot.register_next_step_handler(msg, getElements, bot)


"--------------------------------------------------------------------------------"
# SECTION - Elementos para problema de densidad


def setPresion(message, bot):
    global temperatura
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)
    try:
        temperatura = float(message.text)
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id, "Escribe la presión en psia", reply_markup=markup)
        bot.register_next_step_handler(msg, getElements, bot)
    except ValueError:
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id,
            "ERROR: Debes ingresar un número.\nPor favor, escribe la temperatura en Rankine.",
            reply_markup=markup)
        bot.register_next_step_handler(msg, setPresion, bot)


"--------------------------------------------------------------------------------"
#!SECTION Metodos de tabulación y recopilación


def getElements(message, bot, mcsi=0):
    print("Entro correctamente getElement")
    global eleccion, mc, presion
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)
    if (eleccion == "srk_presion"):
        try:
            if mcsi == 1:
                mc = float(message.text)
            else:
                mc = 0
        except ValueError:
            markup = ForceReply()
            msg = bot.send_message(
                message.chat.id,
                "ERROR: Debes ingresar un número.\nPor favor, escribe el valor de mc.",
                reply_markup=markup)
            bot.register_next_step_handler(msg, getElements, bot)
    else:
        try:
            presion = float(message.text)
        except ValueError:
            markup = ForceReply()
            msg = bot.send_message(
                message.chat.id,
                "ERROR: Debes ingresar un número.\nPor favor, escribe la presión en psia.",
                reply_markup=markup)
            bot.register_next_step_handler(msg, getElements, bot)

    msg = bot.send_message(message.chat.id, "¿Cuántos elementos necesitas?")
    bot.register_next_step_handler(msg, get_h7p, bot)


"--------------------------------------------------------------------------------"
# SECTION - Recopilación de datos h7+


def get_h7p(message, bot):
    global numeroDeElementos
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)
    if not message.text.isdigit():
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id,
            "ERROR: Debes ingresar un número.\nPor favor, escribe los elementos necesitas.",
            reply_markup=markup)
        bot.register_next_step_handler(msg, get_h7p, bot)
    else:
        try:
            numeroDeElementos = int(message.text)
        except ValueError:
            numeroDeElementos = int(float(message.text))
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True,
            input_field_placeholder="Seleciona una opción",
            resize_keyboard=True
        )
        markup.add("Si", "No")
        msg = bot.send_message(
            message.chat.id, "¿Uno de los elementos es h7+?", reply_markup=markup)
        bot.register_next_step_handler(msg, get_mmh7p_values, bot)


def get_mmh7p_values(message, bot):
    global numeroDeElementos, mmh7p, tch7p, pch7p, fah7p, yh7p
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)
    if message.text.lower() == "si":
        numeroDeElementos = numeroDeElementos-1
        # Masa molar de h7+
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id, "Ingresa la masa molar del h7+ en lb/lb-mol:", reply_markup=markup)
        bot.register_next_step_handler(msg, lambda m: get_float_input(
            m, bot, lambda x: setattr(mmh7p, 'value', x), lambda m, b: get_tch7p_values(m, b)))
    else:
        # mmh7p.value = 0
        # tch7p.value = 0
        # pch7p.value = 0
        # fah7p.value = 0
        # yh7p.value = 0
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True,
            input_field_placeholder="Seleccione una opción",
            resize_keyboard=True
        )
        markup.add("Continuar")
        msg = bot.send_message(
            message.chat.id, "Presiona continuar", reply_markup=markup)
        bot.register_next_step_handler(msg, elementos, bot)
        print("Salida de h7")


def get_tch7p_values(message, bot):
    # Temperatura crítica de h7+
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)
    markup = ForceReply()
    msg = bot.send_message(
        message.chat.id, "Ingresa la temperatura crítica del h7+ en Farenheit:", reply_markup=markup)
    bot.register_next_step_handler(msg, lambda m: get_float_input(
        m, bot, lambda x: setattr(tch7p, 'value', x), lambda m, b: get_pch7p_values(m, b)))


def get_pch7p_values(message, bot):
    # Temperatura crítica de h7+
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)
    markup = ForceReply()
    msg = bot.send_message(
        message.chat.id, "Ingresa la presión critica del h7+:", reply_markup=markup)
    bot.register_next_step_handler(msg, lambda m: get_float_input(
        m, bot, lambda x: setattr(pch7p, 'value', x), lambda m, b: get_fah7p_values(m, b)))


def get_fah7p_values(message, bot):
    # Temperatura crítica de h7+
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)
    markup = ForceReply()
    msg = bot.send_message(
        message.chat.id, "Ingresa el factor acéntrico h7+:", reply_markup=markup)
    bot.register_next_step_handler(msg, lambda m: get_float_input(
        m, bot, lambda x: setattr(fah7p, 'value', x), lambda m, b: get_yh7p_values(m, b)))


def get_yh7p_values(message, bot):
    # Temperatura crítica de h7+
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)
    markup = ForceReply()
    msg = bot.send_message(
        message.chat.id, "Ingresa el porcentaje del h7+:", reply_markup=markup)
    bot.register_next_step_handler(msg, lambda m: get_float_input(
        m, bot, lambda x: setattr(yh7p, 'value', x), lambda m, b: elementos(m, b)))


"--------------------------------------------------------------------------------"
# SECTION - Conclusión del ciclo e impresión de resultados


def elementos(message, bot):
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)
    print("\nEntrada elementos")
    global contador, numeroDeElementos, dic, eleccion, densidadl, densidadg, densidad, presion
    h7p = {
        "Número": '7+',
        "Componente": 'Heptano Plus',
        "Formula": 'H7+',
        "Masa molar": float(mmh7p.value),
        "Temperatura Critica": float(tch7p.value),
        "Presión Critica": float(pch7p.value),
        "Factor acéntrico": float(fah7p.value)
    }
    if (contador < numeroDeElementos):
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id, f"Escribe el nombre del elemento {contador+1}: \n", reply_markup=markup)
        bot.register_next_step_handler(msg, get_element_name, bot)
    else:
        if (mmh7p.value != 0):
            lista.append(h7p)
            y.append(float(yh7p.value))
        print("Enviando informacion")
        if eleccion == "srk_presion":
            print(eleccion+'\n')
            print(
                f'{lista}\n{y}\n{temperatura}\n{numeroDeElementos}\n{volumenCelda}\n{mc}\n')
            presion = SRK(chatId, lista, y, temperatura,
                          numeroDeElementos, volumenCelda, mc)
            bot.send_message(message.chat.id, f"La presión es {presion} psia")
            excel = open(f'./resource/datos{chatId}.xlsx', 'rb')
            bot.send_document(message.chat.id,excel,"Datos del proceso")
            resetVariables()
        else:
            print(eleccion+'\n')
            print(
                f'{lista}\n{y}\n{temperatura}\n{numeroDeElementos}\n{volumenCelda}\n{mc}\n{presion}\n')
            try:
                densidadl, densidadg = SRK(chatId, lista, y, temperatura, numeroDeElementos,
                                           volumenCelda, mc, presion)
                bot.send_message(
                    message.chat.id, f"la densidad liquida es {densidadl} lb/ft3 y la densidad del gas es {densidadg} lb/ft3")
                excel = open(f'./resource/datos{chatId}.xlsx', 'rb')
                bot.send_document(message.chat.id,excel,"Datos del proceso")
                resetVariables()
            except TypeError:
                densidad = SRK(chatId, lista, y, temperatura, numeroDeElementos,
                               volumenCelda, mc, presion)
                bot.send_message(
                    message.chat.id, f"la densidad es {densidad} lb/ft3")
                excel = open(f'./resource/datos{chatId}.xlsx', 'rb')
                bot.send_document(message.chat.id,excel,"Datos del proceso")
                resetVariables()


def get_element_name(message, bot):
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)
    nombre_elemento = message.text
    if (aux(nombre_elemento) is not None):
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id,
            f"Escribe el porcentaje del elemento {contador+1}: ",
            reply_markup=markup)
        bot.register_next_step_handler(
            msg, get_element_percentage, nombre_elemento, bot)
    else:
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id,
            "ERROR: El elemento no se encuentra en la base de datos \nEscribe nuevamente un elemento",
            reply_markup=markup)
        bot.register_next_step_handler(
            msg, get_element_name, bot)


def get_element_percentage(message, nombre_elemento, bot):
    global dic, y, contador, lista
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)
    porcentaje = message.text
    try:
        porcentaje = float(porcentaje)
        lista.append(aux(nombre_elemento))
        y.append(porcentaje)
        contador += 1
        markup = ForceReply()

        if (contador+1 == numeroDeElementos):
            dic = lista
            markup = ReplyKeyboardMarkup(
                one_time_keyboard=True,
                input_field_placeholder="Seleccione una opción",
                resize_keyboard=True
            )
            markup.add("Continuar")
            msg = bot.send_message(
                message.chat.id, "Presiona continuar", reply_markup=markup)
            bot.register_next_step_handler(msg, elementos, bot)
        else:
            markup = ReplyKeyboardMarkup(
                one_time_keyboard=True,
                input_field_placeholder="Seleccione una opción",
                resize_keyboard=True
            )
            markup.add("Continuar")
            msg = bot.send_message(
                message.chat.id, "Presiona continuar", reply_markup=markup)
            bot.register_next_step_handler(msg, elementos, bot)

    except ValueError:
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id,
            "ERROR: Debes ingresar un número.\nEscribe el porcentaje del elemento:",
            reply_markup=markup)
        bot.register_next_step_handler(
            msg, get_element_percentage, nombre_elemento, bot)
