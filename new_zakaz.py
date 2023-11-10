import telebot
from telebot import types
import db_helper



token = ''
owner = [686674950, 5699395851]
pysto = types.InlineKeyboardMarkup()
no_dost = "Постой-ка! У тебя нет доступа! Для покупки можно обратится к @elijist"
platforms = ['Авито', 'Яндекс Карты', 'Google Карты', '2GIS']
orders = 0
bot = telebot.TeleBot(token)

menu1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Создать набор")
btn2 = types.KeyboardButton("Закрыть набор")
btn3 = types.KeyboardButton("Информация")
menu1.add(btn1, btn2, btn3)

markup2 = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton(platforms[0], callback_data=platforms[0])
btn2 = types.InlineKeyboardButton(platforms[1], callback_data=platforms[1])
btn3 = types.InlineKeyboardButton(platforms[2], callback_data=platforms[2])
btn4 = types.InlineKeyboardButton(platforms[3], callback_data=platforms[3])
btn5 = types.InlineKeyboardButton("Другая Платформа", callback_data='any')
markup2.add(btn1, btn2, btn3, btn4, btn5)



@bot.message_handler(commands=["delbut"])
def delbut(message):
    bot.send_message(message.chat.id, "Кнопки успешно скрыты!", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=["getadmins"])
def get(message):
    bot.send_message(message.chat.id, text=db_helper.get_all_admins())

@bot.message_handler(commands=["addadmin"])
def get1(message):
    if message.from_user.id in owner:
        k = bot.send_message(message.chat.id, "Введите id нового админа:")
        bot.register_next_step_handler(k, report)
    else:
        bot.send_message(message.chat.id, "У мужлана нету прав")

@bot.message_handler(commands=["delete_admin"])
def get1(message):
    if message.from_user.id in owner:
        k = bot.send_message(message.chat.id, "Введите id админа для удаления из базы:")
        bot.register_next_step_handler(k, del_report)
    else:
        bot.send_message(message.chat.id, "У мужлана нету прав")

def report(message):
    i = int(message.text)
    db_helper.add_admin(i)

def del_report(message):
    i = int(message.text)
    db_helper.delete_admin(i)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'any':
            anys = bot.send_message(call.message.chat.id, "Пожалуйста, Введите платформу:")
            bot.register_next_step_handler(anys, any_plat)

        if call.data in platforms:
            otzservice = call.data
            db_helper.set_otzservice(call.message.chat.id, otzservice)
            nextys = bot.send_message(call.message.chat.id, f"Выбранная платформа: {otzservice}\nУкажите оплату:")
            bot.register_next_step_handler(nextys, oplata_za_otziv)

        if call.data == 'да':
            gotovi_text = db_helper.get_finish_text(call.message.chat.id)
            otkl = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("Откликнуться", url='https://t.me/'+db_helper.get_user_name(call.message.chat.id))
            otkl.add(button1)
            bot.send_message("@SHARDotz", gotovi_text, parse_mode="Markdown", reply_markup=otkl)
            bot.send_message(call.message.chat.id, "Будет сделано!".format(call.message.from_user),
                               reply_markup=menu1)

        if call.data == "нет":
              bot.send_message(call.message.chat.id, "Видимо, что-то пошло не по плану...\nПожалуй, я это удалю.",
                               reply_markup=menu1)

@bot.message_handler(commands=["myid"])
def satr(message):
    bot.send_message(message.chat.id, message.from_user.id)

@bot.message_handler(commands=["start"])
def satrt(message):
    if db_helper.equals_admin(message.from_user.id):
        db_helper.set_user_name(message.from_user.id, message.from_user.username)
        db_helper.set_chat_id(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id,
             "🤴Кабинет Администратора\nИспользуя кнопки ниже, Вы можете открывать и закрывать наборы".format(
             message.from_user), reply_markup=menu1)
    else:
        bot.send_message(message.chat.id, no_dost)

@bot.message_handler(content_types=["text"])
def unlock(message):
    if db_helper.equals_admin(message.from_user.id):
        chat_id = db_helper.get_chat_id(int(message.from_user.id))
        if message.text.lower() == "создать набор":
            pl = bot.send_message(chat_id,
                                  "Выберите платформу:".format(message.from_user), reply_markup=markup2)
        elif message.text.lower() == "закрыть набор":
            print(1111)
            z = bot.send_message(chat_id, "Ссылку на пост:")
            bot.register_next_step_handler(z, close)
        elif message.text.lower() == "информация":
            if db_helper.equals_admin(message.from_user.id):
                status = "Администратор"
            else:
                status = "Пользователь"
            bot.send_message(message.chat.id,
                             f"*Ваш Telegram ID:* {message.from_user.id}\n*Ваш Username:* @{message.from_user.username}\n"
                             f"*Вы:* {status}\n[*Канал*](t.me/SHARDotz)\n[*Выплаты*](t.me/shardopl)\n"
                             f"[*Отзывы*](t.me/repshard)", parse_mode="Markdown")

        elif '/addadmin' in message.text.lower():
            adminid = message.text.split(maxsplit=1)[1]
            if message.from_user.id in owner:
                db_helper.add_admin(int(adminid))
                bot.send_message(message.chat.id, "Успешно!")
        else:
            bot.send_message(message.chat.id, "Неизвестная команда!\nВозможно, Вы хотели открыть набор?",
                             reply_markup=menu1)

@bot.message_handler(func=lambda message: db_helper.equals_admin(message.from_user.id))
def close(message):
    chatik = db_helper.get_chat_id(message.from_user.id)
    link = message.text
    print(link[22:])
    bot.edit_message_text(chat_id = "@SHARDotz", message_id=link[22:], text= "🔒* Набор исполнителей закрыт, идёт выдача заданий... *",parse_mode="Markdown",reply_markup=pysto)
    bot.send_message(chatik, "Готово!", reply_markup=menu1)

@bot.message_handler(func=lambda message: db_helper.equals_admin(message.from_user.id))
def any_plat(message):
    db_helper.set_otzservice(message.from_user.id, message.text)
    opls = bot.send_message(db_helper.get_chat_id(message.from_user.id), "Укажите оплату:")
    bot.register_next_step_handler(opls, oplata_za_otziv)

@bot.message_handler(func=lambda message: db_helper.equals_admin(message.from_user.id))
def get_plat(message):
    opls = bot.send_message(message.chat.id, "Укажите оплату:")
    bot.register_next_step_handler(opls, oplata_za_otziv)

@bot.message_handler(func=lambda message: db_helper.equals_admin(message.from_user.id))
def oplata_za_otziv(message):
    db_helper.set_chels(message.from_user.id, message.text)
    comm = bot.send_message(db_helper.get_chat_id(message.from_user.id), "Отлично, введите описание к набору:".format(message.from_user),
                            reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(comm, com)

@bot.message_handler(func=lambda message: db_helper.equals_admin(message.from_user.id))
def com(message):
    comment = message.text
    global orders
    orders += 1
    data = db_helper.get_data_admin(message.from_user.id)
    potd = types.InlineKeyboardMarkup()
    da = types.InlineKeyboardButton("Отправить", callback_data="да")
    net = types.InlineKeyboardButton("Удалить", callback_data="нет")
    potd.add(da, net)
    text = f"*▸ Платформа: {data[0]}*\n*▸ Получите оплату: {data[1]}₽*\n*▸ Описание: {comment}*\n\n★ *Писать: @{data[2]}*\n☆ Наши выплаты: @SHARDopl"
    db_helper.set_finish_text(message.from_user.id, text)
    bot.send_message(message.chat.id, f"Отлично, я Вас правильно понял?\n{text}\n", parse_mode="Markdown", reply_markup=potd)


bot.infinity_polling()