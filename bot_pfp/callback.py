import source.srk_calculadora as c

from telebot.types import ForceReply, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

#NOTE - Estas son las funciones del callback
def calcular(cid, bot):
    markup = InlineKeyboardMarkup(row_width=2)
    btn_rk = InlineKeyboardButton("RK", callback_data="cal_rk")
    btn_srk = InlineKeyboardButton("SRK", callback_data="cal_srk")
    markup.add(btn_rk, btn_srk)
    bot.send_message(
        cid,
        "Escoge una opción",
        reply_markup=markup
    )
def srk(cid, bot):
    markup = InlineKeyboardMarkup(row_width=2)
    btn_presion = InlineKeyboardButton("Presión", callback_data="srk_presion")
    btn_densidad = InlineKeyboardButton("Densidad", callback_data="srk_densidad")
    markup.add(btn_presion, btn_densidad)
    bot.send_message(
        cid,
        "Escoge que deseas calcular",
        reply_markup=markup)
    
