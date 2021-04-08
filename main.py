#sudo service ntp stop && sudo ntpd -gq && sudo service ntp
import apiclient.discovery
import httplib2
# ------------------------------------------------------------
from oauth2client.service_account import ServiceAccountCredentials
import telebot
import datetime





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
usr = {}
day_schedule = []
data = 0
callback = []
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
schedule_change_mon_1 = telebot.types.InlineKeyboardMarkup()
schedule_change_mon_1.add(telebot.types.InlineKeyboardButton(text = "Изменить Пару", callback_data = 'change_pair6'))
schedule_change_tues_2 = telebot.types.InlineKeyboardMarkup()
schedule_change_tues_2.add(telebot.types.InlineKeyboardButton(text = "Изменить Пару", callback_data = 'change_pair7'))
schedule_change_wed_3 = telebot.types.InlineKeyboardMarkup()
schedule_change_wed_3.add(telebot.types.InlineKeyboardButton(text = "Изменить Пару", callback_data = 'change_pair8'))
schedule_change_thur_4 = telebot.types.InlineKeyboardMarkup()
schedule_change_thur_4.add(telebot.types.InlineKeyboardButton(text = "Изменить Пару", callback_data = 'change_pair9'))
schedule_change_fri_5 = telebot.types.InlineKeyboardMarkup()
schedule_change_fri_5.add(telebot.types.InlineKeyboardButton(text = "Изменить Пару", callback_data = 'change_pair10'))




#---------------------WORK_WITH_TIME--------------------------
dif = datetime.datetime.now() - datetime.datetime(2020, 9, 1)
dif = dif.days//7
today = datetime.datetime.now().weekday()


# --------------------CREATING_BOT----------------------------
bot = telebot.TeleBot('1795577258:AAGOp6HC5mfZfwQ5vd6jL5LxkHN-Py-pxiI')



@bot.message_handler(commands = ['start'])
def start_message(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Для выбора класса пропишите /choose и /show для показа рассписания. Нужно сменить класс, пиши /change. Если возникают вопросы, можно прописать /help")    



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
    

@bot.message_handler(commands = ['choose'])
def usr_choose(message):
    msg = bot.send_message(message.from_user.id,"Напишите номер класса в формате(*)")
    bot.register_next_step_handler(msg, usr_choice)

def usr_choice(message):
    global groups
    if message.text in groups:
        usr[str(message.from_user.id)] = message.text
        bot.send_message(message.from_user.id, "Вы успешно подключены")
    else:
        bot.send_message(message.from_user.id, "Проверьте правильность ввода номера класса")


@bot.message_handler(commands = ['show'])
def usr_showing(message):
    global usr, dif, today, groups , schedule, day_schedule
    if str(message.from_user.id) in usr.keys():
        if dif%2 == 0:
            k = 0
            days = ["Понедельник","Вторник","Среда","Четверг","Пятница"]
            for x in schedule[groups.index(usr[str(message.from_user.id)])][1:]:
                day_schedule.append(x.split(','))
            bot.send_message(message.from_user.id, "Рассписание на числитель")
            l = 0
            for x in days:
                if l == today:
                    bot.send_message(message.from_user.id, f"Сегодня\n\t1) {day_schedule[0][k]}\n\t2) {day_schedule[0][k+1]}\n\t3) {day_schedule[0][k+2]}\n\t4) {day_schedule[0][k+3]}\n\t5) {day_schedule[0][k+4]}\n\t6) {day_schedule[0][k+5]}\n\t7) {day_schedule[0][k+6]}\n\t8) {day_schedule[0][k+7]}")
                else:
                    bot.send_message(message.from_user.id, f"{x}\n\t1) {day_schedule[0][k]}\n\t2) {day_schedule[0][k+1]}\n\t3) {day_schedule[0][k+2]}\n\t4) {day_schedule[0][k+3]}\n\t5) {day_schedule[0][k+4]}\n\t6) {day_schedule[0][k+5]}\n\t7) {day_schedule[0][k+6]}\n\t8) {day_schedule[0][k+7]}")
                k+=8
            k = 0
        else:
            k = 0
            days = ["Понедельник","Вторник","Среда","Четверг","Пятница"]
            for x in schedule[groups.index(usr[str(message.from_user.id)])][1:]:
                day_schedule.append(x.split(','))
            bot.send_message(message.from_user.id, "Рассписание на числитель")
            l = 0
            for x in days:
                if l == today:
                    bot.send_message(message.from_user.id, f"Сегодня\n\t1) {day_schedule[1][k]}\n\t2) {day_schedule[1][k+1]}\n\t3) {day_schedule[1][k+2]}\n\t4) {day_schedule[1][k+3]}\n\t5) {day_schedule[1][k+4]}\n\t6) {day_schedule[1][k+5]}\n\t7) {day_schedule[1][k+6]}\n\t8) {day_schedule[1][k+7]}")
                else:
                    bot.send_message(message.from_user.id, f"{x}\n\t1) {day_schedule[1][k]}\n\t2) {day_schedule[1][k+1]}\n\t3) {day_schedule[1][k+2]}\n\t4) {day_schedule[1][k+3]}\n\t5) {day_schedule[1][k+4]}\n\t6) {day_schedule[1][k+5]}\n\t7) {day_schedule[1][k+6]}\n\t8) {day_schedule[1][k+7]}")
                k+=8
                l+=1
        l = 0
        k = 0
    else:
        bot.send_message(message.from_user.id, "Сначала нужно подключиться (/choose)")


@bot.message_handler(commands = ['change'])
def usr_changing(message):
    msg = bot.send_message(message.from_user.id,"Для смены напишите номер класса в формате(*)")
    bot.register_next_step_handler(msg, usr_change)

def usr_change(message):
    global groups
    if message.text in groups:
        usr[str(message.from_user.id)] = message.text
    else:
        bot.send_message(message.from_user.id, "Проверьте правильность ввода номера класса")



@bot.message_handler(commands = ['help'])
def start_message(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, "Помощь")



@bot.callback_query_handler(func=lambda call: True)
def callback_data(call):
    global callback, data
    if call.data == 'admin_creategroup':
        msg = bot.send_message(call.message.chat.id, "Введите номер(название класса)")
        bot.register_next_step_handler(msg, create_group)
    elif call.data == 'admin_chosegroup':
        msg = bot.send_message(call.message.chat.id, "Введите номер(название класса)")
        bot.register_next_step_handler(msg, chose_group)
    elif call.data == 'admin_deletegroup':
        print(1)
        msg = bot.send_message(call.message.chat.id, "Введите номер(название класса)")
        bot.register_next_step_handler(msg, delete_group)
    elif call.data == 'change_pair1':
        callback = [data, 1]
    elif call.data == 'change_pair2':
        callback = [data, 2]
    elif call.data == 'change_pair3':
        callback = [data, 3]
    elif call.data == 'change_pair4':
        callback = [data, 4]
    elif call.data == 'change_pair5':
        callback = [data, 5]
    elif call.data == 'change_pair6':
        callback = [data, 6]
    elif call.data == 'change_pair7':
        callback = [data, 7]
    elif call.data == 'change_pair8':
        callback = [data, 8]
    elif call.data == 'change_pair9':
        callback = [data, 9]
    elif call.data == 'change_pair10':
        callback = [data, 10]
    if callback:
        msg = bot.send_message(call.message.chat.id, "Введите Предметы через запятую для заполнения. В случае окна, поставьте пробел и запятую")
        bot.register_next_step_handler(msg, change)


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
    groups = service.spreadsheets().values().get(
        spreadsheetId = spreadsheet_id,
        range = "A1:A500",
        majorDimension = 'COLUMNS').execute()['values'][0]
    bot.send_message(message.from_user.id, "Группа была успешна добавлена")
    bot.register_next_step_handler(admin_message, admin_panel)

def delete_group(message):
    global groups, schedule
    z = 0
    if message.text not in groups:
        bot.send_message(message.from_user.id, "Проверьте правильность ввода номера группы")
    else:
        while z <len(groups):
            if message.text == groups[z]:
                schedule[z] = [""]
                print(schedule[z])
                groups.pop(z)
                service.spreadsheets().values().batchUpdate(
                    spreadsheetId = spreadsheet_id,
                    body = {
                    'valueInputOption':'USER_ENTERED',
                    'data': [
                    {'range': "A1:C500",
                    'majorDimension' : 'ROWS',
                    'values': schedule}]}).execute()
                print(schedule)
                bot.send_message(message.from_user.id, "Удаление успешно")
                break
            z+=1

def chose_group(message):
    global groups, admin_message, schedule, day_schedule, data
    day_schedule = []
    i = 0
    j = 0
    while i < len(groups):
        if groups[i] == message.text:
            data = i
            if len(schedule[i])<3:
                while j<2:
                    schedule[i].append(' , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ')
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
            k =0
            l =0
            days = ["Понедельник","Вторник","Среда","Четверг","Пятница"]
            markups = [schedule_change_mon, schedule_change_tues,schedule_change_wed,schedule_change_thur,schedule_change_fri,schedule_change_mon_1, schedule_change_tues_2,schedule_change_wed_3,schedule_change_thur_4,schedule_change_fri_5]
            for x in schedule[i][1:]:
                day_schedule.append(x.split(','))
            bot.send_message(message.from_user.id, "Рассписание на числитель")
            for x in days:
                bot.send_message(message.from_user.id, f"{x}\n\t1) {day_schedule[0][k]}\n\t2) {day_schedule[0][k+1]}\n\t3) {day_schedule[0][k+2]}\n\t4) {day_schedule[0][k+3]}\n\t5) {day_schedule[0][k+4]}\n\t6) {day_schedule[0][k+5]}\n\t7) {day_schedule[0][k+6]}\n\t8) {day_schedule[0][k+7]}",reply_markup = markups[l])
                k+=8
                l+=1
            k = 0
            bot.send_message(message.from_user.id, "Рассписание на знаментель")
            for x in days:
                bot.send_message(message.from_user.id, f"{x}\n\t1) {day_schedule[1][k]}\n\t2) {day_schedule[1][k+1]}\n\t3) {day_schedule[1][k+2]}\n\t4) {day_schedule[1][k+3]}\n\t5) {day_schedule[1][k+4]}\n\t6) {day_schedule[1][k+5]}\n\t7) {day_schedule[1][k+6]}\n\t8) {day_schedule[1][k+7]}",reply_markup = markups[l])
                k+=8
                l+=1
            k = 0 
            l = 0   
            break
        i+=1
    i=0
    if message.text not in groups:
        bot.send_message(message.from_user.id, "Проверьте правильность ввода номера группы")


def change(message):
    global callback, schedule, day_schedule, data
    messg_temp = message.text.strip(" ")
    messg_temp = messg_temp.split(',')
    print(messg_temp)
    if len(messg_temp)>8:
        bot.send_message("Слишком много уроков для 1 дня")
    else:
        while len(messg_temp)< 8:
            messg_temp.append(" ")
        if callback[1]>5:
            indexs = (callback[1]- 6)*8
        else:
            indexs = (callback[1]-1)*8
        print(messg_temp)
        day_schedule[callback[1]//6][indexs:indexs + 8]=messg_temp
        print(day_schedule[callback[1]//6][indexs:indexs + 8])
        print(" ,".join(day_schedule[callback[1]//6]))
        schedule[callback[0]][callback[1]//6+1] = " ,".join(day_schedule[callback[1]//6])
        service.spreadsheets().values().batchUpdate(
            spreadsheetId = spreadsheet_id,
            body = {
            'valueInputOption':'USER_ENTERED',
            'data': [
            {'range': "A1:C500",
            'majorDimension' : 'ROWS',
            'values': schedule}]}).execute()
        schedule = service.spreadsheets().values().get(
        spreadsheetId = spreadsheet_id,
        range = "A1:C500",
        majorDimension = 'ROWS').execute()['values']
        day_schedule= []
        callback =[]
        data = 0
        bot.send_message(message.from_user.id, "Изменения успешно внесены")
        


    






if __name__ == "__main__":
    bot.polling(none_stop = True)
