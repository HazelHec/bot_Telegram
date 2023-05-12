import config as con  # Importa el bot
import decimal
# lib para crear botones y para contestar un mensaje
from telebot.types import ForceReply, ReplyKeyboardMarkup
from source.conexion import conect1
from source.pr_metodo import peng_r
"--------------------------------------------------------------------------------"
#!SECTION Zona de variables globales
# NOTE - Strings
eleccion = str

# NOTE - Flotantes y enteras
chatId = int
numeroDeElementos = int
temperatura = float
volumenCelda = float
mc = float
presion = float
temperatura = float
densidadl = float
densidadg = float
densidad = float

# NOTE - Diccionarios y listas
lista = []
dic = {}
y = []


# NOTE - Clases y objetos
class ValueHolder:
    def __init__(self, value):
        self.value = value


mmh7p = ValueHolder(0)
tch7p = ValueHolder(0)
pch7p = ValueHolder(0)
fah7p = ValueHolder(0)
yh7p = ValueHolder(0)

"--------------------------------------------------------------------------------"
#!SECTION Zona de funciones auxiliares

# NOTE - Esta función conecta a la base de datos


def aux(a):
    # Lista cuyo sera el directorio
    encabezado = ('Número', 'Componente', 'Formula', 'Masa molar',
                  'Temperatura Critica', 'Presión Critica', 'Factor acéntrico')
    lista = []
    # Metodos para la conexion con la base de datos
    conexion = conect1()
    cursor = conexion.cursor()
    # Query de consulta
    query = f'''SELECT * FROM {con.base}
    where if((select count(*) from {con.base} where componente = '{a}') > 0,
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
#!SECTION Zona de funciones para obtener datos del método
# NOTE - Función que inicia la calculadora


def ini(opcion, cid, bot):
    resetVariables()
    global eleccion, chatId
    # NOTE - Se agrega valor del chat id y del tipo de calculo
    eleccion = opcion
    chatId = cid

    if opcion == 'pr_presion':
        markup = ForceReply()
        msg = bot.send_message(
            cid, "Por favor, escribe la temperatura en Rankine.", reply_markup=markup)
        bot.register_next_step_handler(msg, presion_step1, bot)

    elif opcion == 'pr_densidad':
        markup = ForceReply()
        msg = bot.send_message(
            cid, "Por favor, escribe la temperatura en Rankine.", reply_markup=markup)
        bot.register_next_step_handler(msg, densidad_step1, bot)


"--------------------------------------------------------------------------------"
# SECTION - Obtener datos para presion


# NOTE - Guardamos temperatura en variable global y preguntamos por el valor de la celda
def presion_step1(message, bot):
    global temperatura
    # Metodo para reiniciar el calculo
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)

    # Excepción para saber si el dato introducido es flotante
    try:
        temperatura = float(message.text)
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id, "Escribe el volumen de la celda en ft^3", reply_markup=markup)
        bot.register_next_step_handler(msg, presion_step2, bot)
    except ValueError:
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id,
            "ERROR: Debes ingresar un número.\nPor favor, escribe la temperatura en Rankine.",
            reply_markup=markup)
        bot.register_next_step_handler(msg, presion_step1, bot)


# NOTE - Guardamos el volumen de la celda y preguntamos por el MC
def presion_step2(message, bot):
    global volumenCelda
    # Metodo para reiniciar el calculo
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)

    # Excepción para saber si el dato introducido es flotante
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
        bot.register_next_step_handler(msg, presion_step3, bot)

    except ValueError:
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id,
            "ERROR: Debes ingresar un número.\nEscribe el volumen de la celda en ft^3.",
            reply_markup=markup)
        bot.register_next_step_handler(msg, presion_step2, bot)


# NOTE - Este pasó resive la respuesta del si hay mc o no
def presion_step3(message, bot):
    # Metodo para reiniciar el calculo
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)

    # Variable que vale 1 si el usuario tiene el valor de mc
    mcsi = 1
    if message.text.lower() == "si":
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id, "Introduzca el valor de mc", reply_markup=markup)
        bot.register_next_step_handler(msg, presion_step4, bot, mcsi)
    else:
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True,
            input_field_placeholder="Seleccione una opción",
            resize_keyboard=True
        )
        markup.add("Continuar")
        msg = bot.send_message(
            message.chat.id, "Presiona continuar", reply_markup=markup)
        bot.register_next_step_handler(msg, presion_step4, bot)


# NOTE - Guardamos el valor de mc y pasamos a all_data
def presion_step4(message, bot, mcsi=0):
    global mc
    # Metodo para reiniciar el calculo
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)

    # Excepción para saber si el dato introducido es flotante
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
        bot.register_next_step_handler(msg, presion_step4, bot)

    print("Entrando a global data\n")
    msg = bot.send_message(message.chat.id, "¿Cuántos elementos necesitas?")
    bot.register_next_step_handler(msg, global_data, bot)


"--------------------------------------------------------------------------------"
# SECTION - Obtener datos para densidad


# NOTE - Guardanos el valor de temperatura y preguntamos la presión
def densidad_step1(message, bot):
    global temperatura
    # Metodo para reiniciar el calculo
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)

    # Excepción para saber si el dato introducido es flotante
    try:
        temperatura = float(message.text)
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id, "Escribe la presión en psia", reply_markup=markup)
        bot.register_next_step_handler(msg, densidad_step2, bot)
    except ValueError:
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id,
            "ERROR: Debes ingresar un número.\nPor favor, escribe la temperatura en Rankine.",
            reply_markup=markup)
        bot.register_next_step_handler(msg, densidad_step1, bot)


# NOTE - Guardanos el valor de presión y pasamos a all_data
def densidad_step2(message, bot):
    global presion
    # Metodo para reiniciar el calculo
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)

    # Excepción para saber si el dato introducido es flotante
    try:
        presion = float(message.text)
    except ValueError:
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id,
            "ERROR: Debes ingresar un número.\nPor favor, escribe la presión en psia.",
            reply_markup=markup)
        bot.register_next_step_handler(msg, densidad_step2, bot)

    print("Entrando a global data\n")
    msg = bot.send_message(message.chat.id, "¿Cuántos elementos necesitas?")
    bot.register_next_step_handler(msg, global_data, bot)


"--------------------------------------------------------------------------------"
# SECTION - Obtener datos para el uso de ambos problemas


# NOTE - Guardamos el número de elementos y preguntamos por h7
def global_data(message, bot):
    global numeroDeElementos
    # Metodo para reiniciar el calculo
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)

    # Metodo por el cual revisa si el número de elementos es un número
    if not message.text.isdigit():
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id,
            "ERROR: Debes ingresar un número.\nPor favor, escribe cuantos elementos necesitas.",
            reply_markup=markup)
        bot.register_next_step_handler(msg, global_data, bot)
    else:
        # Excepción para saber si el dato introducido es entero
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
        bot.register_next_step_handler(msg, global_data_h7, bot)


# NOTE - iniciamos proceso para obtener valores de h7 o pasar a la obtención de datos
def global_data_h7(message, bot):
    global numeroDeElementos, mmh7p, tch7p, pch7p, fah7p, yh7p
    # Metodo para reiniciar el calculo
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)

    # Forma para saber si hay h7
    if message.text.lower() == "si":
        numeroDeElementos = numeroDeElementos-1
        # Masa molar de h7+
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id, "Ingresa la masa molar del h7+ en lb/lb-mol:", reply_markup=markup)
        bot.register_next_step_handler(msg, lambda m: get_float_input(
            m, bot, lambda x: setattr(mmh7p, 'value', x), lambda m, b: get_tch7p_values(m, b)))
    else:
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True,
            input_field_placeholder="Seleccione una opción",
            resize_keyboard=True
        )
        markup.add("Continuar")
        msg = bot.send_message(
            message.chat.id, "Presiona continuar", reply_markup=markup)
        bot.register_next_step_handler(msg, global_data_tabular, bot)
        print("Salida de h7")


"--------------------------------------------------------------------------------"
# SECTION - Obtenemos los datos necesarios para h7


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
        m, bot, lambda x: setattr(yh7p, 'value', x), lambda m, b: global_data_tabular(m, b)))


"--------------------------------------------------------------------------------"
# SECTION - Procesos de recompilación de datos

# NOTE - Inicio de la tabulación, preguntar por el nombre
def global_data_tabular(message, bot):
    global contador, numeroDeElementos, dic, eleccion, densidadl, densidadg, densidad, presion
    # Metodo para reiniciar el calculo
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)

    # Mensaje informativo
    print("\nEntrada proceso de tabulación")

    # Ordenamiento del h7
    h7p = {
        "Número": '7+',
        "Componente": 'Heptano Plus',
        "Formula": 'H7+',
        "Masa molar": float(mmh7p.value),
        "Temperatura Critica": float(tch7p.value),
        "Presión Critica": float(pch7p.value),
        "Factor acéntrico": float(fah7p.value)
    }

    # proceso de tabulación
    if (contador < numeroDeElementos):
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id, f"Escribe el nombre del elemento {contador+1}: \n", reply_markup=markup)
        bot.register_next_step_handler(msg, global_data_tabular_name, bot, h7p)


# NOTE - Guardar nombre[datos] y preguntar por el porcentaje
def global_data_tabular_name(message, bot, h7p):
    # Metodo para reiniciar el calculo
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
            msg, global_data_tabular_percentage, nombre_elemento, bot, h7p)
    else:
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id,
            "ERROR: El elemento no se encuentra en la base de datos \nEscribe nuevamente un elemento",
            reply_markup=markup)
        bot.register_next_step_handler(
            msg, global_data_tabular_name, bot, h7p)


# NOTE - Guardar porcentaje y enviar información al método de salida
def global_data_tabular_percentage(message, nombre_elemento, bot, h7p):
    global dic, y, contador, lista
    # Metodo para reiniciar el calculo
    if message.text.lower() == "reiniciar":
        reiniciar(message, bot)

    porcentaje = message.text
    try:
        porcentaje = float(porcentaje)
        lista.append(aux(nombre_elemento))
        y.append(porcentaje)
        contador += 1
        markup = ForceReply()

        if (contador == numeroDeElementos):
            dic = lista
            markup = ReplyKeyboardMarkup(
                one_time_keyboard=True,
                input_field_placeholder="Seleccione una opción",
                resize_keyboard=True
            )
            markup.add("Continuar")
            msg = bot.send_message(
                message.chat.id, "Presiona continuar", reply_markup=markup)
            bot.register_next_step_handler(msg, return_result, bot, h7p)
        else:
            markup = ReplyKeyboardMarkup(
                one_time_keyboard=True,
                input_field_placeholder="Seleccione una opción",
                resize_keyboard=True
            )
            markup.add("Continuar")
            msg = bot.send_message(
                message.chat.id, "Presiona continuar", reply_markup=markup)
            bot.register_next_step_handler(msg, global_data_tabular, bot)

    except ValueError:
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id,
            "ERROR: Debes ingresar un número.\nEscribe el porcentaje del elemento:",
            reply_markup=markup)
        bot.register_next_step_handler(
            msg, global_data_tabular_percentage, nombre_elemento, bot, h7p)


# NOTE - Método de salida
def return_result(message, bot, h7p):
    global contador, numeroDeElementos, dic, eleccion, densidadl, densidadg, densidad, presion, temperatura, volumenCelda, mc, chatId
    if (mmh7p.value != 0):
        lista.append(h7p)
        y.append(float(yh7p.value))

    # Mensaje informativo
    print("Enviando informacion")

    if eleccion == "pr_presion":
        # Mensaje informativo
        print(eleccion+'\n')
        print(
            f'{lista}\n{y}\n{temperatura}\n{numeroDeElementos}\n{volumenCelda}\n{mc}\n')
        presion = peng_r(chatId, lista, y, temperatura,
                      numeroDeElementos, volumenCelda, mc)

        # Enviando Resultados al usuario
        bot.send_message(message.chat.id, f"La presión es {presion} psia")
        excel = open(f'./resource/datos{chatId}.xlsx', 'rb')
        bot.send_document(message.chat.id, excel, caption="Datos del proceso")
        resetVariables()
    else:
        # Mensaje informativo
        print(eleccion+'\n')
        print(
            f'{lista}\n{y}\n{temperatura}\n{numeroDeElementos}\n{volumenCelda}\n{mc}\n{presion}\n')

        # Enviando Resultados al usuario
        try:
            # Enviando respuesta
            densidadl, densidadg = peng_r(chatId, lista, y, temperatura, numeroDeElementos,
                                       volumenCelda, mc, presion)
            bot.send_message(
                message.chat.id, f"la densidad liquida es {densidadl} lb/ft3 y la densidad del gas es {densidadg} lb/ft3")

            # Enviando excel
            excel = open(f'./resource/datos{chatId}.xlsx', 'rb')
            bot.send_document(message.chat.id, excel, caption="Datos del proceso")

            # Reset de variables
            resetVariables()
        except TypeError:
            # Enviando respuesta
            densidad = peng_r(chatId, lista, y, temperatura, numeroDeElementos,
                           volumenCelda, mc, presion)
            bot.send_message(
                message.chat.id, f"la densidad es {densidad} lb/ft3")

            # Enviando excel
            excel = open(f'./resource/datos{chatId}.xlsx', 'rb')
            bot.send_document(message.chat.id, excel, caption="Datos del proceso")

            # Reset de variables
            resetVariables()
