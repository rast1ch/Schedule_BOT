#sudo service ntp stop && sudo ntpd -gq && sudo service ntp
import apiclient.discovery
import httplib2
# ------------------------------------------------------------
import telebot
from oauth2client.service_account import ServiceAccountCredentials




# --------------------TOCKEN_SECTION--------------------------
CREDINTIALS_FILE = 'schedulebot-309820-d28d74e84bf5.json' #'digitaljournal-dfd2c8f6cfe1.json'
spreadsheet_id = '1LOqqZTEGSDfSDBfmxh32pmPwXOOlm-p0qiMtLlsoIFs'


# --------------------CREATING_APIS---------------------------
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDINTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

#----------------------CONTENT---------------------------------
groups = service.spreadsheets().values().get(
        spreadsheetId = spreadsheet_id,
        range = "A1:A500",
        majorDimension = 'COLUMNS').execute()['values'][0]
schedule = service.spreadsheets().values().get(
        spreadsheetId = spreadsheet_id,
        range = "A1:C500",
        majorDimension = 'ROWS').execute()['values']
day_schedule = []

#-------------------------------------------------------------
admin_flag = False
admin_code = '123'
admin_id = ''
admin_message = ''



#-------------------------MARKUPS-----------------------------
admin_keyboard = telebot.types.InlineKeyboardMarkup()
admin_keyboard.add(telebot.types.InlineKeyboardButton(text = "Создать группу", callback_data = 'admin_creategroup'))
admin_keyboard.add(telebot.types.InlineKeyboardButton(text = "Выбрать группу", callback_data = 'admin_chosegroup'))
admin_keyboard.add(telebot.types.InlineKeyboardButton(text = "Удалить группу", callback_data = 'admin_deletegroup'))
schedule_change_mon = telebot.types.InlineKeyboardMarkup()
schedule_change_mon.add(telebot.types.InlineKeyboardButton(text = "Изменить Пару", callback_data = 'change_pair1'))
schedule_change_tues = telebot.types.InlineKeyboardMarkup()
schedule_change_tues.add(telebot.types.InlineKeyboardButton(text = "Изменить Пару", callback_data = 'change_pair2'))
schedule_change_wed = telebot.types.InlineKeyboardMarkup()
schedule_change_wed.add(telebot.types.InlineKeyboardButton(text = "Изменить Пару", callback_data = 'change_pair3'))
schedule_change_thur = telebot.types.InlineKeyboardMarkup()
schedule_change_thur.add(telebot.types.InlineKeyboardButton(text = "Изменить Пару", callback_data = 'change_pair4'))
schedule_change_fri = telebot.types.InlineKeyboardMarkup()
schedule_change_fri.add(telebot.types.InlineKeyboardButton(text = "Изменить Пару", callback_data = 'change_pair5'))
# --------------------CREATING_BOT----------------------------
bot = telebot.TeleBot('1795577258:AAGOp6HC5mfZfwQ5vd6jL5LxkHN-Py-pxiI')



@bot.message_handler(commands = ['start'])
def start_message(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Выберите пожалуйста группу. Если возникают вопросы, можно прописать /help")    



@bot.message_handler(commands = ['admin'])
def admin_panel(message):
    global admin_code, admin_flag, admin_id, admin_message
    # Admin check
    if not admin_flag:
        try:
            if message.text.split()[1] == admin_code:
                admin_flag = True
                admin_id = str(message.from_user.id)
                admin_message = bot.send_message(message.from_user.id, "You are in", reply_markup = admin_keyboard)
                #bot.register_next_step_handler()
            else:
                bot.send_message(message.from_user.id, "Error, Wrong password")
        except IndexError:
            bot.send_message(message.from_user.id, "Error, wrong password")
    else:
        if admin_id == str(message.from_user.id):
            admin_message = bot.send_message(message.from_user.id, "You are in",reply_markup = admin_keyboard)
        else: 
            bot.send_message(message.from_user.id, "Admin is logged in")
    





@bot.message_handler(commands = ['help'])
def start_message(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, "Помощь")



@bot.callback_query_handler(func=lambda call: True)
def callback_data(call):
    if call.data == 'admin_creategroup':
        msg = bot.send_message(call.message.chat.id, "Введите номер(название группы)")
        bot.register_next_step_handler(msg, create_group)
    elif call.data == 'admin_chosegroup':
        msg = bot.send_message(call.message.chat.id, "Введите номер(название группы)")
        bot.register_next_step_handler(msg, chose_group)


def chose_group(message):
    global groups, admin_message, schedule
    i = 0
    j = 0
    while i < len(groups):
        if groups[i] == message.text:
            data = message.text
            if len(schedule[i])<3:
                while j<2:
                    schedule[i].append(" , , , , , , , , , , , , , , , , , , , ")
                    j+=1
                service.spreadsheets().values().batchUpdate(
                    spreadsheetId = spreadsheet_id,
                    body = {
                    'valueInputOption':'USER_ENTERED',
                    'data': [
                    {'range': "A1:C500",
                    'majorDimension' : 'ROWS',
                    'values': schedule}]}).execute()
                j=0
            bot.send_message(message.from_user.id, f"Группа номер {message.text}")
            if schedule[i][1] == " , , , , , , , , , , , , , , , , , , , ":
                bot.send_message(message.from_user.id, "На числитель пока расписания нет")
                if schedule[i][2] == " , , , , , , , , , , , , , , , , , , , ":
                    bot.send_message(message.from_user.id, "На знаменатель пока расписания нет")
            else:
                k =0
                l =0
                days = ["Понедельник","Вторник","Среда","Четверг","Пятница"]
                markups = [schedule_change_mon, schedule_change_tues,schedule_change_wed,schedule_change_thur,schedule_change_fri]
                for x in schedule[i][1:]:
                    day_schedule.append(x.split(','))
                for x in days:
                    bot.send_message(message.from_user.id, f"{x}\n\t1) {day_schedule[0][k]}\n\t2) {day_schedule[0][k+1]}\n\t3) {day_schedule[0][k+2]}\n\t4) {day_schedule[0][k+3]}",reply_markup = markups[k//4])
                    k+=4


            break
        i+=1
    if message.text not in groups:
        bot.send_message(message.from_user.id, "Проверьте правильность ввода номера группы")

def create_group(message):
    global groups, admin_message
    for i in groups:
        if i == '':
            i = message.text
            break
    if message.text not in groups:
        groups.append(message.text)
    service.spreadsheets().values().batchUpdate(
        spreadsheetId = spreadsheet_id,
        body = {
        'valueInputOption':'USER_ENTERED',
        'data': [
        {'range': "A1:A500",
        'majorDimension' : 'COLUMNS',
        'values': [groups]}]}).execute()
    bot.send_message(message.from_user.id, "Группа была успешна добавлена")
    bot.register_next_step_handler(admin_message, admin_panel)








if __name__ == "__main__":
    bot.polling(none_stop = True)