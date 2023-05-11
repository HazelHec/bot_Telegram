"""----------------------------------------------------------------------------"""
#!SECTION Imports clasicos
import config as con  # Importa el bot
import telebot   # es la api para manejar el bot
import callback
# lib para crear botones
# Lib para contestar un mensaje
from telebot.types import ForceReply, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telebot.types import ReplyKeyboardMarkup
import os
import importlib

"""----------------------------------------------------------------------------"""
#SECTION - Importar modulos de las archivos
# Obtener el listado de archivos en la carpeta\
source = {}   
archivos = os.listdir(con.modulosPath)

# Importar cada módulo
for archivo in archivos:
    # Verificar si es un archivo Python
    if archivo.endswith('.py'):
        # Obtener el nombre del módulo sin la extensión .py
        nombre_modulo = archivo[:-3]
        # Importar el módulo usando importlib
        source[nombre_modulo] = importlib.import_module(f'source.{nombre_modulo}')
        # print(f'\nsource.{nombre_modulo}')

"""----------------------------------------------------------------------------"""

# Declarando bot
bot = telebot.TeleBot(con.TOKEN)

"""----------------------------------------------------------------------------"""
# Zona de variables
global OPCION
msg = []

"""----------------------------------------------------------------------------"""
#!SECTION Commands


@bot.message_handler(commands=["start"])
def cmd_start(message):
    """Da la bienvenida al bot"""
    delet = ReplyKeyboardRemove()
    bot.reply_to(message, con.msgStart, reply_markup=delet)


@bot.message_handler(commands=["opciones"])
def cmd_opciones(message):
    markup = InlineKeyboardMarkup(row_width=3)
    btn_calcular = InlineKeyboardButton("Calcular", callback_data="op_cal")
    btn_ejercicios = InlineKeyboardButton("Ejercicios", callback_data="op_exa")
    btn_libreria = InlineKeyboardButton("Libreria", callback_data="op_lib")
    markup.add(btn_calcular, btn_ejercicios, btn_libreria)
    msn = bot.send_message(
        message.chat.id,
        "Escoge una opción",
        reply_markup=markup
    )


@ bot.message_handler(commands=["datos_srk"])
def cmd_pruebas(message):
    rt_datos = open('./resource/SRK.pdf', 'rb')
    bot.send_document(message.chat.id, document=rt_datos,
                      caption="Los elementos utilizados vienen en este documento")
    rt_datos.close()


@ bot.message_handler(commands=["codigo_srk"])
def cmd_pruebas(message):
    rt_datos = open('./resource/codigoPrueba.zip', 'rb')
    bot.send_document(message.chat.id, document=rt_datos,
                      caption="Este es el codigo de prueba para el metodo SRK")
    rt_datos.close()



"""----------------------------------------------------------------------------"""
#!SECTION CAll BACK


@bot.callback_query_handler(func=lambda call: True)
def call_opciones(call):
    cid = call.from_user.id
    mid = call.message.id

    if call.data == "op_cal":
        callback.calcular(cid, bot)

    elif call.data == "op_exa":
        bot.send_message(
            cid,
            con.mxm
        )
    elif call.data == "op_lib":
        bot.send_message(
            cid,
            con.mxm
        )
    elif call.data == "cal_srk":

        callback.srk(cid, bot)

    elif call.data == "cal_rk":
        bot.send_message(
            cid,
            con.mxm
        )

    elif call.data == "cal_pr":
        bot.send_message(
            cid,
            con.mxm
        )
    elif call.data == "srk_presion":
        source['srk_calculadora'].procesar_opcion(call.data, cid, bot)

    elif call.data == "srk_densidad":
        source['srk_calculadora'].procesar_opcion(call.data, cid, bot)
    
    
    # Forma para borrar todos los botones una vez leidos
    bot.edit_message_reply_markup(cid, mid, reply_markup=None)
    bot.delete_message(cid, mid)


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
        telebot.types.BotCommand(
            "/opciones", "Opciones de las acciones del bot"),
        telebot.types.BotCommand(
            "/datos_srk", "Datos utilizados para los calculos"),
        telebot.types.BotCommand("/codigo_srk", "codigo de SRK")
    ])
    print("iniciando el bot")
    recibir_Mensajes()
    print("fin")
