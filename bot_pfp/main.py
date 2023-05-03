import calculadora as c
import config as con  # Importa el bot
import telebot   # es la api para manejar el bot
# lib para crear botones
# Lib para contestar un mensaje
from telebot.types import ForceReply, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telebot.types import ReplyKeyboardMarkup


# Declarando bot
bot = telebot.TeleBot(con.TOKEN)
# Zona de variables


OPCION = ""
msg = []


@bot.message_handler(commands=["start"])
def cmd_start(message):
    """Da la bienvenida al bot"""
    delet = ReplyKeyboardRemove()
    bot.reply_to(message, con.msgStart, reply_markup=delet)


@bot.message_handler(commands=["opciones"])
def cmd_opciones(message):
    markup = InlineKeyboardMarkup(row_width=3)
    a = InlineKeyboardButton("Calcular", callback_data="op_cal")
    b = InlineKeyboardButton("Ejercicios", callback_data="op_exa")
    c = InlineKeyboardButton("Libreria", callback_data="op_lib")
    markup.add(a, b, c)
    bot.send_message(
        message.chat.id, "Escoge una opción", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('op_'))
def call_opciones(call):
    cid = call.from_user.id
    mid = call.message.id
    if call.data == "op_cal":
        bot.send_message(cid, "Para continuar favor de dar click /calcular")
    elif call.data == "op_exa":
        bot.send_message(
            cid, "Por el momento este comando no ha sido habilitado")
    elif call.data == "op_lib":
        bot.send_message(
            cid, "Por el momento este comando no ha sido habilitado")
    bot.edit_message_reply_markup(cid, mid, reply_markup=None)
    bot.delete_message(cid, mid)


@bot.message_handler(commands=["calcular"])
def calcular(message):
    markup = InlineKeyboardMarkup(row_width=2)
    a = InlineKeyboardButton("RK", callback_data="cal_rk")
    b = InlineKeyboardButton("SRK", callback_data="cal_srk")
    markup.add(a, b)
    bot.send_message(
        message.chat.id, "Escoge una opción", reply_markup=markup)
        


@bot.callback_query_handler(func=lambda call: call.data.startswith('cal_'))
def call_opciones(call):
    cid = call.from_user.id
    mid = call.message.id
    if call.data == "cal_srk":
        bot.send_message(cid, "Para continuar favor de dar click /srk")
        bot.edit_message_reply_markup(cid, mid, reply_markup=None)
        bot.delete_message(cid, mid)


@bot.message_handler(commands=["srk"])
def srk(message):
    markup = InlineKeyboardMarkup(row_width=2)
    a = InlineKeyboardButton("Presión", callback_data="presion")
    b = InlineKeyboardButton("Densidad", callback_data="densidad")
    markup.add(a, b)
    bot.send_message(
        message.chat.id, "Escoge una opción", reply_markup=markup)
    
@bot.callback_query_handler(func=lambda x: x.data == "presion" or x.data =="densidad")
def call_opciones(call):
    cid = call.from_user.id
    mid = call.message.id
    global OPCION
    OPCION = call.data
    c.procesar_opcion(call.data,cid,bot)
    bot.edit_message_reply_markup(cid, mid, reply_markup=None)
    bot.delete_message(cid, mid)



@bot.message_handler(commands=["prueba"])
def cmd_pruebas(message):
    global OPCION
    bot.send_message(message.chat.id, "La opción seleccionada es: " + OPCION)


"""----------------------------------------------------------------------------"""


def recibir_Mensajes():
    bot.infinity_polling()


def handle_telegram_errors(exception):
    print(exception)


"""----------------------------------------------------------------------------"""

"""El main del proyecto"""

if __name__ == '__main__':
    # Metodo para poner los comandos visibles en el bot
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Presentación del bot"),
        telebot.types.BotCommand("/opciones", "Opciones de las acciones del bot"),
        # telebot.types.BotCommand("/PFP", "Ejercicios y datos de PfP")
    ])
    print("iniciando el bot")
    recibir_Mensajes()
    print("fin")
