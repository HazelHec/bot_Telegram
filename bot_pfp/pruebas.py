# Funciones para procesar opciones

def procesar_opcion(opcion, cid, bot):
    if opcion == 'srk_presion':
        markup = ForceReply()
        msg = bot.send_message(cid, "Por favor, escribe la temperatura en Rankine.", reply_markup=markup)
        bot.register_next_step_handler(msg, procesar_temperatura, bot)
    elif opcion == 'srk_densidad':
        markup = ForceReply()
        msg = bot.send_message(cid, "Por favor, escribe la temperatura en Rankine.", reply_markup=markup)
        bot.register_next_step_handler(msg, procesar_temperatura, bot)

def procesar_temperatura(message, bot):
    try:
        temperatura = float(message.text)
        if message.reply_to_message.text == "Por favor, escribe la temperatura en Rankine.":
            markup = ForceReply()
            msg = bot.send_message(message.chat.id, "Escribe el volumen de la celda en ft^3", reply_markup=markup)
            bot.register_next_step_handler(msg, procesar_volumen, bot, temperatura)
        elif message.reply_to_message.text == "Por favor, escribe la presión en psia":
            bot.register_next_step_handler(message, procesar_densidad, bot, temperatura)
    except ValueError:
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "ERROR: Debes ingresar un número.\nPor favor, escribe la temperatura en Rankine.", reply_markup=markup)

def procesar_volumen(message, bot, temperatura):
    try:
        volumenCelda = float(message.text)
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Seleciona una opción", resize_keyboard=True)
        markup.add("Si", "No")
        msg = bot.send_message(message.chat.id, "¿Tienes el valor de mc?", reply_markup=markup)
        bot.register_next_step_handler(msg, procesar_mc, bot, temperatura, volumenCelda)
    except ValueError:
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "ERROR: Debes ingresar un número.\nEscribe el volumen de la celda en ft^3.", reply_markup=markup)

def procesar_mc(message, bot, temperatura, volumenCelda):
    if message.text.lower() == "si":
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "Introdusca el valor de mc", reply_markup=markup)
        bot.register_next_step_handler(msg, procesar_elementos, bot, temperatura, volumenCelda, 1)
    else:
        msg = bot.send_message(message.chat.id, "Escribe algo para continuar el calculo.")
        bot.register_next_step_handler(msg, procesar_elementos, bot, temperatura, volumenCelda)

def procesar_densidad(message, bot, temperatura):
    try:
        presion = float(message.text)
        bot.register_next_step_handler(message, procesar_elementos, bot, temperatura, presion)
    except ValueError:
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "ERROR: Debes ingresar un número.\nPor favor, escribe la presión en psia.", reply_markup=markup)
