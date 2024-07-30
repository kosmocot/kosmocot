import telebot
from telebot import types
import openpyxl
from openpyxl import Workbook

TOKEN = 'You Token'
bot = telebot.TeleBot(TOKEN)

wb = Workbook()
ws = wb.active
ws.append(['Chat ID', 'Возраст', 'Гражданство', 'Город', 'Торговый центр', 'Бренд', 'Позиция', 'Опыт', 'Ожидания',
           'Расписание', 'Детальное расписание', 'Номер телефона'])


def save_data_to_excel(user_data):
    ws.append([
        user_data.get('chat_id', ''),
        user_data.get('age', ''),
        user_data.get('citizenship', ''),
        user_data.get('city', ''),
        user_data.get('shopping_center', ''),
        user_data.get('brand', ''),
        user_data.get('vacancy', ''),
        user_data.get('experience', ''),
        user_data.get('money', ''),
        user_data.get('sched', ''),
        user_data.get('time', ''),
        user_data.get('phone_number', '')
    ])
    wb.save('user_data.xlsx')


user_data = {}

shopping_malls = {
    "Москва": ["Охотный ряд", "Авиапарк", "Вегас Крокус", "Европейский", "Мега Белая Дача",
               "Вегас на Каширском", "Колумбус", "Метрополис", "Мега Теплый Стан", "Весна",
               "Ривьера", "Океания", "Саларис", "Европолис", "Вегас Кунцево", "Мега Химки"],
    "Новосибирск": ["Галерея", "Мега", "Аура"],
    "Новокузнецк": ["Планета"],
    "Самара": ["Космопорт", "Мега"],
    "Санкт-Петербург": ["Европолис", "Мега Дыбенко", "Лето", "Галерея", "Сити Молл"],
    "Уфа": ["Планета", "Мега"],
    "Тюмень": ["Кристалл"],
    "Смоленск": ["Макси"],
    "Мурманск": ["Мурманск Молл"],
    "Астрахань": ["Ярмарка"],
    "Пенза": ["Коллаж"],
    "Сочи": ["Море Молл"],
    "Волгоград": ["Ворошиловский"],
    "Ярославль": ["Аура"],
    "Челябинск": ["Алмаз", "Родник"],
    "Красноярск": ["Планета"],
    "Екатеринбург": ["Гринвич", "Мега", "Веер Молл"],
    "Калининград": ["Европа"],
    "Н.Новгород": ["Фантастика"],
    "Краснодар": ["Галерея", "Ред Сквер", "ОЗ Молл", "Мега Адыгея"],
    "Омск": ["Мега"],
    "Тольятти": ["Парк Хаус"],
    "Казань": ["Парк Хаус", "Мега"],
    "Владимир": ["Мегаторг"],
    "Сургут": ["Аура"],
    "Саратов": ["Триумф"],
    "Саранск": ["СитиПарк"],
    "Иркутск": ["Сильвер Молл"],
    "Набережные Челны": ["Санрайз Сити"],
    "Ставрополь": ["Космос"],
    "Барнаул": ["Галактика"],
    "Владивосток": ["Калина Молл"],
    "Новороссийск": ["Ред Сквер"],
    "Хабаровск": ["Броско Молл"],
    "Пермь": ["Планета"],
    "Киров": ["Макси"]
}

brands = ["MAAG", "ECRU", "DUB", "VILET"]

schedule = ["В будние и в выходные ", "Только будни ", "Только выходные"]

vacancy = ["Консультант - кассир", "Администратор", "Операционный специалист", "Визуальный мерчандайзер",
           "Менеджер магазина", "Директор магазина"]

working_time = ["Только утром", "Только вечером", "В любое время"]


# Bot started
@bot.message_handler(commands=['start'])
def start(message):
    start_menu(message)


# First message
def start_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_start = types.KeyboardButton('Начать')
    markup.add(item_start)
    bot.send_message(message.chat.id,
                     "Привет " + message.from_user.first_name + "! \nЯ чат-бот компании RMixed (Новая Мода) бренды MAAG, ECRU, DUB, VILET. \n\nСпасибо за проявленный интерес к нашим вакансиям. \n\n Нажми, чтобы начать😉",
                     reply_markup=markup)


# onPress Button "Начать" and get City list
@bot.message_handler(func=lambda message: message.text == 'Начать')
def send_city_selection(message):
    user_data[message.chat.id] = {'chat_id': message.chat.id}
    city_selection(message)


# function for City selection
def city_selection(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for city in sorted(shopping_malls.keys()):
        markup.add(types.KeyboardButton(city))
    markup.add(types.KeyboardButton('Назад'))
    msg = bot.send_message(message.chat.id, "Выбери свой город:", reply_markup=markup)
    bot.register_next_step_handler(msg, save_city_and_send_shopping_center_selection)


@bot.message_handler(func=lambda message: message.text in shopping_malls.keys())
def save_city_and_send_shopping_center_selection(message):
    if message.text == 'Назад':
        start_menu(message)
    else:
        user_data[message.chat.id]['city'] = message.text
        shopping_center_selection(message, user_data[message.chat.id]['city'])


def shopping_center_selection(message, city):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for center in shopping_malls.get(city, []):
        markup.add(types.KeyboardButton(center))
    markup.add(types.KeyboardButton('Назад'))
    msg = bot.send_message(message.chat.id, "Выбери торговый центр:", reply_markup=markup)
    bot.register_next_step_handler(msg, save_shopping_center_and_send_brand_selection)


# @bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('city') and message.text in shopping_malls.get(user_data[message.chat.id]['city'], []))
def save_shopping_center_and_send_brand_selection(message):
    if message.text == 'Назад':
        del user_data[message.chat.id]['city']
        city_selection(message)
    else:
        user_data[message.chat.id]['shopping_center'] = message.text
        brand_selection(message)


def brand_selection(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for brand in brands:
        markup.add(types.KeyboardButton(brand))
    markup.add(types.KeyboardButton('Назад'))
    msg = bot.send_message(message.chat.id, "Выбери бренд:", reply_markup=markup)
    bot.register_next_step_handler(msg, save_brand_and_ask_for_age)


@bot.message_handler(func=lambda message: message.text in brands)
def save_brand_and_ask_for_age(message):
    if message.text == 'Назад':
        del user_data[message.chat.id]['shopping_center']
        shopping_center_selection(message, user_data[message.chat.id]['city'])
    else:
        user_data[message.chat.id]['brand'] = message.text
        age_selection(message)


@bot.message_handler(func=lambda message: 'brand' in user_data.get(message.chat.id, {}))
def age_selection(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    age_buttons = ['18-25', '26-30', '31-35', '36-40', '41-45', '46-55', 'старше 55']
    for age in age_buttons:
        markup.add(types.KeyboardButton(age))
    markup.add(types.KeyboardButton('Назад'))
    msg = bot.send_message(message.chat.id, 'Выбери свой возраст:', reply_markup=markup)
    bot.register_next_step_handler(msg, save_age_and_send_citizenship_selection)


@bot.message_handler(
    func=lambda message: message.text in ['18-25', '26-30', '31-35', '36-40', '41-45', '46-55', 'старше 55'])
def save_age_and_send_citizenship_selection(message):
    if message.text == 'Назад':
        del user_data[message.chat.id]['brand']
        brand_selection(message)
    else:
        user_data[message.chat.id]['age'] = message.text
        citizenship_selection(message)


def citizenship_selection(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    countries = ['Россия', 'Белоруссия', 'Казахстан', 'Другие страны СНГ']
    for country in countries:
        markup.add(types.KeyboardButton(country))
    markup.add(types.KeyboardButton('Назад'))
    msg = bot.send_message(message.chat.id, 'Выбери свое гражданство:', reply_markup=markup)
    bot.register_next_step_handler(msg, save_citizenship_and_send_phone_input)


@bot.message_handler(func=lambda message: message.text in ['Россия', 'Белоруссия', 'Казахстан', 'Другие страны СНГ'])
def save_citizenship_and_send_phone_input(message):
    if message.text == 'Назад':
        user_data[message.chat.id]['age'] = ""
        age_selection(message)
    else:
        user_data[message.chat.id]['citizenship'] = message.text
        phone_number_input(message)


def phone_number_input(message):
    markup = types.ReplyKeyboardRemove()
    msg = bot.send_message(message.chat.id, "Теперь, пожалуйста, введите свой номер телефона:", reply_markup=markup)
    bot.register_next_step_handler(msg, save_phone_number)


def save_phone_number(message):
    user_data[message.chat.id]['phone_number'] = message.text
    vacancy_selection(message)


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('phone_number'))
def vacancy_selection(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for vacan in vacancy:
        markup.add(types.KeyboardButton(vacan))
    markup.add(types.KeyboardButton('Назад'))
    msg = bot.send_message(message.chat.id, "Выбери позицию:", reply_markup=markup)
    bot.register_next_step_handler(msg, save_vacancy_and_confirm)


@bot.message_handler(func=lambda message: message.text in vacancy)
def save_vacancy_and_confirm(message):
    if message.text == 'Назад':
        user_data[message.chat.id]['phone_number'] = ""
        user_data[message.chat.id]['citizenship'] = ""
        citizenship_selection(message)
    else:
        user_data[message.chat.id]['vacancy'] = message.text
        # bot.send_message(message.chat.id, message.text)
        confirm_vacancy(message)


def confirm_vacancy(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Продолжить'))
    markup.add(types.KeyboardButton('Назад'))
    # bot.send_message(message.chat.id, "Выбери позицию:", reply_markup=markup)
    if user_data[message.chat.id]['vacancy'] == 'Консультант - кассир':
        msg = bot.send_message(message.chat.id,
                               "Тебя ждёт:\n🕝️ Гибкий график работы и возможность совмещать с учебой;\n✅Полная или частичная занятость;\n💳️ Почасовая ставка + бонус от продаж;\n💸Премия за выполнение плана магазина;\n📈 Быстрый карьерный рост;\n🧥Дружная команда увлеченная модой;\n🛍️ Скидка сотрудника 25 % на все бренды  и стильная униформа;\n✅Скидки и предложения от компании партнеров;\n💝 ДМС после года Работы;\n✅ Официальное оформление по ТК.\n\nЧем занимаются наши сотрудники:\n\n✅ Консультируют покупателей и помогают в выборе модных образов;\n✅ Поддерживают порядка в зале;\n✅ Работают на примерочной, в зале, на кассе и на складе\n✅ Принимают и разбирают поставки;\n💯 Работают в команде профессионалов, развиваясь каждый день.\n\nОтветь на несколько вопросов и мы свяжемся с тобой 😊 \n\nЧто бы продолжить, нажми начать!",
                               reply_markup=markup)
    else:
        msg = bot.send_message(message.chat.id,
                               "Отлично!\nМы предлагаем :\n💸 Гарантированный доход и бонусы от продаж и превышение плана;\n🛍️Скидку 25 % на все бренды;\n📝 Официальное оформление по ТК;\n🚀 Быстрый карьерный рост;\n🌐 Международную корпоративную культуру;\n🌟 Программы благополучия сотрудников и заботы о здоровье, ДМС.\n\nТвои будущие задачи:\n✨ Достижение планов продаж, анализ ключевых показателей;\n🎯 Организация и контроль работы в магазине;\n🤝 Подбор, адаптация, обучение и развитие команды;\n🛍️ Поддержание стандартов визуального мерчандайзинга и высокого уровня обслуживания покупателей.\nЕсли тебе подходят условия, мы зададим тебе несколько уточняющих вопросов 😉",
                               reply_markup=markup)
    bot.register_next_step_handler(msg, continue_with_vacancy)


def continue_with_vacancy(message):
    if message.text == 'Продолжить':
        confirm_vacancy_and_go_next(message)
    elif message.text == 'Назад':
        del user_data[message.chat.id]['vacancy']
        vacancy_selection(message)


def confirm_vacancy_and_go_next(message):
    if user_data[message.chat.id]['vacancy'] == 'Консультант - кассир':
        schedule_selection_consult(message)
    else:
        schedule_selection_manager(message)


def schedule_selection_consult(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for sched in schedule:
        markup.add(types.KeyboardButton(sched))
    markup.add(types.KeyboardButton('Назад'))
    msg = bot.send_message(message.chat.id, "Какую занятость ты для себя рассматриваешь?", reply_markup=markup)
    bot.register_next_step_handler(msg, save_schedule)


def save_schedule(message):
    if message.text == 'Назад':
        confirm_vacancy(message)
    else:
        user_data[message.chat.id]['sched'] = message.text
        get_working_time(message)


def get_working_time(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for time in working_time:
        markup.add(types.KeyboardButton(time))
    markup.add(types.KeyboardButton('Назад'))
    msg = bot.send_message(message.chat.id, "В какую половину дня ты планируешь работать?", reply_markup=markup)
    bot.register_next_step_handler(msg, set_working_time)


def set_working_time(message):
    markup = types.ReplyKeyboardRemove()
    if message.text == 'Назад':
        del user_data[message.chat.id]['sched']
        schedule_selection_consult(message)
    else:
        user_data[message.chat.id]['time'] = message.text
        save_data_to_excel(user_data[message.chat.id])
        bot.send_message(message.chat.id,
                         "Спасибо! Мы свяжемся с тобой 😊 А пока предлагаем тебе посмотреть короткие ролики про работу с нами:) Работа в магазине https://disk.yandex.ru/i/kF7yXyLO_z2N4A Условия работы https://disk.yandex.ru/i/H2D9-DGNg6fGFw",
                         reply_markup=markup)


def schedule_selection_manager(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Да'))
    markup.add(types.KeyboardButton('Нет'))
    msg = bot.send_message(message.chat.id,
                           "Есть ли у тебя опыт работы в продажах, в сфере Fashion, на аналогичной должности или другой менеджерской позиции?",
                           reply_markup=markup)
    bot.register_next_step_handler(msg, get_experience)


def get_experience(message):
    if message.text == 'Назад':
        continue_with_vacancy(message)
    else:
        user_data[message.chat.id]['experience'] = message.text
        markup = types.ReplyKeyboardRemove()
        msg = bot.send_message(message.chat.id,
                               "Какие у тебя зарплатные ожидания (сумма совокупно на руки)?\nОтвет в свободной форме",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, set_experience)


def set_experience(message):
    if message.text == 'Назад':
        del user_data[message.chat.id]['experience']
        schedule_selection_manager(message)
    else:
        user_data[message.chat.id]['money'] = message.text
        save_data_to_excel(user_data[message.chat.id])
        bot.send_message(message.chat.id,
                         "Спасибо! Мы свяжемся с тобой 😊!\nА пока предлагаем посмотреть короткие ролики про работу наших команд!\nРабота в магазине https://disk.yandex.ru/i/kF7yXyLO_z2N4A \nУсловия работы https://disk.yandex.ru/i/H2D9-DGNg6fGFw")


# def save_phone_number(message):
#     user_data[message.chat.id]['phone_number'] = message.text
#     save_data_to_excel(user_data[message.chat.id])
#     bot.send_message(message.chat.id, "Спасибо! Мы свяжемся с тобой 😊 \nА пока предлагаем тебе посмотреть короткие ролики про работу с нами:) \nРабота в магазине \nhttps://disk.yandex.ru/i/kF7yXyLO_z2N4A \nУсловия работы https://disk.yandex.ru/i/H2D9-DGNg6fGFw", reply_markup=types.ReplyKeyboardRemove())


# @bot.message_handler(func=lambda message: message.text == 'Назад')
def go_back(message):
    if 'brand' in user_data[message.chat.id]:
        del user_data[message.chat.id]['brand']
        brand_selection(message)
    elif 'schedule' in user_data[message.chat.id]:
        del user_data[message.chat.id]['schedule']
        shopping_center_selection(message, user_data[message.chat.id]['city'])
    elif 'shopping_center' in user_data[message.chat.id]:
        del user_data[message.chat.id]['shopping_center']
        shopping_center_selection(message, user_data[message.chat.id]['city'])
    elif 'city' in user_data[message.chat.id]:
        del user_data[message.chat.id]['city']
        city_selection(message)
    elif 'citizenship' in user_data[message.chat.id]:
        del user_data[message.chat.id]['citizenship']
        citizenship_selection(message)
    elif 'age' in user_data[message.chat.id]:
        del user_data[message.chat.id]['age']
        age_selection(message)
    else:
        start_menu(message)


bot.infinity_polling()
