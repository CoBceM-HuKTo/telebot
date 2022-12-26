import telebot, os
from telebot import types

list_of_niknames = {}
list_of_events_to_be_held = ['Мотивационные встречи', 'Футбол', 'Силовые упражнения', 'ГТО', 'Баскетбол',
                             'Волейбол',
                             'Шахматы', 'Лазертаг', 'Рыбалка', 'Туристические походы', 'Моржевание', 'Эстафета',
                             'Настольные игры', 'Профориентация',
                             'Лыжи', 'Настольный теннис', 'Бадминтон', 'Патриотика', 'НВП', 'Дартс',
                             'Актёрское мастерство', 'Боулинг', 'Бильярд', 'PR-реклама', 'Школьный лагерь',
                             'Конкурс талантов', 'КВН',
                             'Видеомонтаж', 'Парашютный прыжок', 'Тир', 'Хоккей', 'Муз. группа', 'Фотосьемка', 'SMM',
                             'Дискуссии', 'Вело-тур', 'Cамозащитa',
                             'Эстафеты', 'Зарядка', 'Субботник']  # список мероприятий для проведения

dictionary_of_upcoming_events = {'ПримерФутбол': '14.06.2023', 'ПримерХоккей': '20.12.2022',
                                 'ПримерЛазертаг': '28.12.2022'}  # словарь ближайших мероприятий
dictionary_of_regular_events = {'ПримерМоржевание': 'Суббота - 9:00, позвонить: 89220062234',
                                'ПримерЗарядка': 'Суббота - 9:00, позвонить: 89220062234',
                                'ПримерГТО': 'Суббота - 9:00, позвонить: 89220062234'}  # словарь ближайших мероприятий

list_of_events_to_participate_in = list_of_events_to_be_held  # список мероприятий для участия

# list_of_events_to_participate_in.append('❗Я закончил выбирать❗')
list_of_events_to_be_held.append('❗Я закончил выбирать❗')
p = 1
about_me = ''
name_for_event = ''
quantity_for_event = ''
phone_for_event = ''

questionnaire_father_full_name = ''  # ФИО пользователя
questionnaire_father_age = ''  # Возраст пользователья
questionnaire_father_scope_of_work = ''  # Сфера работы пользователя
questionnaire_father_hobby = []  # Увлечения пользователя
questionnaire_father_can_hold_events = []  # Какие мероприятия может проводить пользователь
questionnaire_father_want_to_participate_in_events = []  # В каких мероприятиях пользователь хочет учавствовать
questionnaire_inventory = []  # инвентарь пользователья
questionnaire_number_of_children = 0
questionnaire_children_full_names = []  # ФИО детей пользователя
questionnaire_children_dates_of_birth = []  # дата рождения детей пользователя
questionnaire_children_age = []  # возраст детей пользователя
questionnaire_children_classes = []  # класс детей пользователя
questionnaire_children_clubs = []  # секции детей пользователя
questionnaire_children_interests = []  # интересы детей пользователя
questionnaire_ideas = ''  # идеи
questionnaire_user_id = ''  # id пользователя
counter_for_entering_id = 0  # счетчик дя одноразового получения id пользователя
main_questions = ['Назад', 'Узнать список ближайших мероприятий', 'Записаться на мероприятие', 'Начать заново',
                  'Добавиться в группу совета надёжных отцов - ВК/Телеграм', 'Познакомиться с участниками Совета Отцов',
                  'Наше вИдение']  # список основных вопросов бота
q = 'False'  # флаг для разных случаев
message_glob = None
counter_of_children = 0

bot = telebot.TeleBot('')  # подключаемся к боту
my_id = ''
name_event_reg = ''


@bot.message_handler(content_types=['text'])
def start(message):
    global questionnaire_user_id, counter_for_entering_id, dictionary_of_upcoming_events, message_glob, list_of_niknames
    bot.send_message(my_id, f'@{message.from_user.username} пишет боту прямо сейчас')
    if counter_for_entering_id == 0:
        questionnaire_user_id = message.chat.id
        message_glob = message
        counter_for_entering_id += 1
    else:
        pass
    if message.from_user.username not in list_of_niknames:
        list_of_niknames[str(message.from_user.username)] = questionnaire_user_id
    if message.text == '/start' or message.text == 'Начать заново' or message.text == 'Назад':
        main_keyboard = types.ReplyKeyboardMarkup()
        button_restart = types.KeyboardButton('Начать заново')
        button_check_events_list = types.KeyboardButton('Узнать список ближайших мероприятий')
        button_register_to_group = types.KeyboardButton('Добавиться в группу совета надёжных отцов - ВК/Телеграм')
        button_register_to_event = types.KeyboardButton('Записаться на мероприятие')
        button_vision = types.KeyboardButton('Наше вИдение')
        button_get_to_know_the_participants = types.KeyboardButton('Познакомиться с участниками Совета Отцов')
        main_keyboard.row(button_restart, button_vision)
        main_keyboard.row(button_register_to_group)
        main_keyboard.row(button_check_events_list)
        main_keyboard.row(button_register_to_event, button_get_to_know_the_participants)
        bot.send_message(questionnaire_user_id,
                         'Привет, вместе с нами, Советом Надёжных Отцов 94 школы, Вы можете организовывать и проводить мероприятия для своего ребенка, участвовать с ребенком в мероприятиях, проводимых другими отцами в нашей школе, а также найти единомышленников в деле восптания характера у детей. Меню ниже поможет Вам в этом.',
                         reply_markup=main_keyboard)
    elif message.text == 'Записаться на мероприятие':
        markup = types.InlineKeyboardMarkup()
        for i in dictionary_of_upcoming_events:
            markup.row(types.InlineKeyboardButton(f'{i}', callback_data=f'{i} registration_for_the_event'))
        bot.send_message(questionnaire_user_id, 'Выберите мероприятие:', reply_markup=markup)
    elif message.text == 'Добавиться в группу совета надёжных отцов - ВК/Телеграм':
        networks_keyboard = types.InlineKeyboardMarkup()
        networks_keyboard.row(types.InlineKeyboardButton(f'ВКонтакте', callback_data=f'ВК'))
        networks_keyboard.row(types.InlineKeyboardButton(f'Телеграм', callback_data=f'ТГ'))
        bot.send_message(questionnaire_user_id,
                         f'Телеграм - группа СНО 94 школы, создана для организации и прилашения отцов на мероприятия.\n'
                         f'ВКонтакте - сообщество повествующее об уже проведённых мероприятиях СНО 94',
                         reply_markup=networks_keyboard)
    elif message.text == 'Узнать список ближайших мероприятий':
        s = 1
        bot.send_message(questionnaire_user_id, '❗Ближайшие планируемые мероприятия:')
        for i in dictionary_of_upcoming_events:
            bot.send_message(questionnaire_user_id, f'{s}) {i} - {dictionary_of_upcoming_events[i]}')
            s += 1
        bot.send_message(questionnaire_user_id, '❗Регулярные мероприятия:')
        s = 1
        for i in dictionary_of_regular_events:
            bot.send_message(questionnaire_user_id, f'{s}) {i} - {dictionary_of_regular_events[i]}')
            s += 1
        bot.send_message(questionnaire_user_id,
                         '❗Чтобы записаться на мероприятие нажмите кнопку ниже: "Записаться на мероприятие"')
    elif message.text == 'Наше вИдение':
        selection_keyboard = types.InlineKeyboardMarkup()
        vision_video = types.InlineKeyboardButton('СНО г.Тюмень', callback_data='vision_video')
        vision_photo = types.InlineKeyboardButton('СНО 94 школа', callback_data='vision_photo')
        selection_keyboard.row(vision_video)
        selection_keyboard.row(vision_photo)
        bot.send_message(questionnaire_user_id, 'Наше вИдение:', reply_markup=selection_keyboard)
    elif message.text == 'Познакомиться с участниками Совета Отцов':
        bot.send_message(questionnaire_user_id,
                         'Чтобы узнать больше о других участниках Совета Надёжных Отцов, рассказжите о себе поподробнее:')
        bot.register_next_step_handler(message, to_learn_more)
    # elif message.text == 'Назад':
        # start(message)
    else:
        # nikname = message.from_user.username
        # if nikname in list_of_niknames:
        #     idd = list_of_niknames[nikname]
        # else:
        #     idd = questionnaire_user_id
        # bot.send_message(my_id, f'{message.text}\n@{message.from_user.username}')
        # if str(message.from_user.id) == my_id:
        #     bot.send_message(idd, f"🎧 Оператор: {message.text}")
        # else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Назад']])
        bot.send_message(questionnaire_user_id,
                             f"Используйте меню внизу ↓↓↓ или дождитесь пока вам ответит оператор 🎧 (в течении суток).",
                             reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def ans(call, *types):
    global questionnaire_father_can_hold_events, questionnaire_father_want_to_participate_in_events, counter_of_children, name_event_reg
    if str(types) == '()':
        if str(call.data) == 'vision_video':
            bot.send_message(questionnaire_user_id, 'https://vk.com/video-214384206_456239075')
        elif str(call.data) == 'vision_photo':
            img = open('photo.jpg', 'rb')
            bot.send_message(questionnaire_user_id, "Загрузка...")
            bot.send_message(questionnaire_user_id, "⌛")
            bot.send_photo(questionnaire_user_id, img)
        elif str(call.data) == 'ТГ':
            bot.send_message(questionnaire_user_id,
                             'Для вступления в группу Совета Надёжных Отцов просим пройти небольшой опрос для того, чтобы добиться лучшего результата в проводимых для детей мероприятиях.')
            bot.send_message(questionnaire_user_id, 'Ваши ФИО:')
            bot.register_next_step_handler(call, anketa_to_group_father_name)
        elif str(call.data) == 'ВК':
            bot.send_message(questionnaire_user_id, 'https://vk.com/sno_94')
        elif 'registration_for_the_event' in str(call.data):
            name_event_reg = str((str(call.data).replace(" registration_for_the_event", '')))
            bot.send_message(questionnaire_user_id,
                             f'Чтобы зарегестрироваться на мероприятие "{str(call.data).replace(" registration_for_the_event", "")}", введите свои ФИО:')
            bot.register_next_step_handler(call.data, registration_to_event_name)
        elif 'held' in str(call.data):
            if 'Я закончил выбирать' not in str(call.data):
                questionnaire_father_can_hold_events.append(str(call.data).replace(' held', ''))
            else:
                anketa_to_group_father_arrange(call.data)
        elif 'participate' in str(call.data):
            if 'Я закончил выбирать' not in str(call.data):
                questionnaire_father_want_to_participate_in_events.append(
                    str(call.data).replace(' participate', ''))
            else:
                anketa_to_group_father_participate(call.data)
    elif 'anketa_to_group_father_name' in str(types):
        if 'few_words' in str(types):
            bot.send_message(questionnaire_user_id,
                             'Нужно ввести ТРИ слова: Фамилия, Имя, Отчество. Попробуйте еще раз:')
            bot.register_next_step_handler(call, anketa_to_group_father_name)
        elif 'few_letters' in str(types):
            bot.send_message(questionnaire_user_id,
                             'Каждое из вводимых слов должно быть не менее 2 символов, попробуйте ещё раз:')
            bot.register_next_step_handler(call, anketa_to_group_father_name)
    elif 'anketa_to_group_father_age' in str(types):
        if 'not_int' in str(types):
            bot.send_message(questionnaire_user_id, 'Возраст указан неверно, укажите числом:')
            bot.register_next_step_handler(call, anketa_to_group_father_age)
        elif 'too_young' in str(types):
            bot.send_message(questionnaire_user_id, 'Зарегестрироваться может только совершеннолетний:')
            bot.register_next_step_handler(call, anketa_to_group_father_age)
        elif 'too_old' in str(types):
            bot.send_message(questionnaire_user_id, 'Неправдоподобно много лет, повторите попытку:')
            bot.register_next_step_handler(call, anketa_to_group_father_age)
    elif 'count_of_children' in str(types):
        if 'not_int' in str(types):
            bot.send_message(questionnaire_user_id, 'Будьте добры, укажите числом:')
            bot.register_next_step_handler(call, anketa_to_group_count_of_children)
        elif 'more_8' in str(types):
            bot.send_message(questionnaire_user_id,
                             'Приносим свои извенения, но у Вас не может быть более 8 детей. Пожалуйста используйте цифру от 0 до 7:')
            bot.register_next_step_handler(call, anketa_to_group_count_of_children)
    elif 'anketa_to_group_names_of_children' in str(types):
        if 'few_words' in str(types):
            bot.send_message(questionnaire_user_id,
                             'Нужно ввести ТРИ слова: Фамилия, Имя, Отчество. Попробуйте еще раз:')
            if 'one' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_names_of_children_one)
            elif 'two' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_names_of_children_two)
            elif 'three' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_names_of_children_three)
            elif 'four' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_names_of_children_four)
            elif 'five' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_names_of_children_five)
            elif 'six' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_names_of_children_six)
            elif 'seven' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_names_of_children_seven)
        elif 'few_letters' in str(types):
            bot.send_message(questionnaire_user_id,
                             'Каждое из вводимых слов должно быть не менее 2 символов, попробуйте ещё раз:')
            if 'one' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_names_of_children_one)
            elif 'two' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_names_of_children_two)
            elif 'three' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_names_of_children_three)
            elif 'four' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_names_of_children_four)
            elif 'five' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_names_of_children_five)
            elif 'six' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_names_of_children_six)
            elif 'seven' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_names_of_children_seven)
    elif 'anketa_to_group_birthday' in str(types):
        if 'few_simbols' in str(types):
            bot.send_message(questionnaire_user_id, 'Введите только год числом, например: 2022')
            if 'one' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_birthday_one)
            elif 'two' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_birthday_two)
            elif 'three' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_birthday_three)
            elif 'four' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_birthday_four)
            elif 'five' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_birthday_five)
            elif 'six' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_birthday_six)
            elif 'seven' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_birthday_seven)
        elif 'not_int' in str(types):
            bot.send_message(questionnaire_user_id, 'Введите год числом, например: 2022')
            if 'one' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_birthday_one)
            elif 'two' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_birthday_two)
            elif 'three' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_birthday_three)
            elif 'four' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_birthday_four)
            elif 'five' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_birthday_five)
            elif 'six' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_birthday_six)
            elif 'seven' in str(types):
                bot.register_next_step_handler(call, anketa_to_group_birthday_seven)
    elif 'registration_to_event_name' in str(types):
        if 'few_words' in str(types):
            bot.send_message(questionnaire_user_id,
                             'Нужно ввести ТРИ слова: Фамилия, Имя, Отчество. Попробуйте еще раз:')
            bot.register_next_step_handler(call, registration_to_event_name)
        elif 'few_letters' in str(types):
            bot.send_message(questionnaire_user_id,
                             'Каждое из вводимых слов должно быть не менее 2 символов, попробуйте ещё раз:')
            bot.register_next_step_handler(call, registration_to_event_name)
    elif 'registration_to_event_quantity' in str(types):
        if 'not_int' in str(types):
            bot.send_message(questionnaire_user_id,
                             'Вводите цифрой:')
            bot.register_next_step_handler(call, registration_to_event_quantity)
        elif 'very_much' in str(types):
            bot.send_message(questionnaire_user_id, 'Нельзя приглашать более 20 человек:')
            bot.register_next_step_handler(call, registration_to_event_quantity)
    elif 'registration_to_event_phone' in str(types):
        if 'not_int' in str(types):
            bot.send_message(questionnaire_user_id,
                             'Используйте цифры для ввода номера телефона, например: 89220062243. Попробуйте:')
            bot.register_next_step_handler(call, registration_to_event_phone)
        elif 'short' in str(types):
            bot.send_message(questionnaire_user_id,
                             'Слишком мало символов, должно быть 11, например: 89220062243. Попробуйте:')
            bot.register_next_step_handler(call, registration_to_event_phone)
        elif 'long' in str(types):
            bot.send_message(questionnaire_user_id,
                             'Слишком много символов, должно быть 11, например: 89220062243. Попробуйте:')
            bot.register_next_step_handler(call, registration_to_event_phone)
    elif 'to_learn_more_name' in str(types):
        if 'few_words' in str(types):
            bot.send_message(questionnaire_user_id,
                             'Нужно ввести ТРИ слова: Фамилия, Имя, Отчество. Попробуйте еще раз:')
            bot.register_next_step_handler(call, to_learn_more_name)
        elif 'few_letters' in str(types):
            bot.send_message(questionnaire_user_id,
                             'Каждое из вводимых слов должно быть не менее 2 символов, попробуйте ещё раз:')
            bot.register_next_step_handler(call, to_learn_more_name)


def to_learn_more(message):
    global questionnaire_user_id, about_me, main_questions
    about_me = message.text
    if about_me not in main_questions:
        if len(about_me.split()) < 15:
            bot.send_message(questionnaire_user_id,
                             f'Слишком мало слов, необходимо не менее 15 слов. У Вас всего: {len(about_me.split())}')
            bot.register_next_step_handler(message, to_learn_more)
        else:
            bot.send_message(questionnaire_user_id,
                             f'Введите Ваши ФИО: ')
            bot.register_next_step_handler(message, to_learn_more_name)
    else:
        start(message)


def to_learn_more_name(message):
    global questionnaire_user_id, main_questions
    name = message.text
    q = ''
    if name not in main_questions:
        if len(name.split()) == 3:
            s = True
            for i in name.split():
                if len(i) < 2:
                    q += 'False'
                else:
                    q += 'True'
        else:
            q += 'False'
            s = False
        if 'False' not in q:
            f = open('about_fathers.csv', 'a')
            f.write(f'\n{name};{about_me}')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['Назад']])
            bot.send_message(questionnaire_user_id,
                             f'Супер, чуть позже я отправлю Вам файл с информацией о других отцах.',
                             reply_markup=keyboard)
        else:
            if s is False:
                ans(message, 'to_learn_more_name', 'few_words')
            else:
                ans(message, 'to_learn_more_name', 'few_letters')
    else:
        bot.register_next_step_handler(message, start)


def registration_to_event_name(message):
    global name_for_event, phone_for_event, quantity_for_event, questionnaire_user_id, message_glob
    name_for_event = ''
    phone_for_event = ''
    quantity_for_event = ''
    name = message
    message = message_glob
    message.text = name
    q = ''
    if len(name.split()) == 3:
        s = True
        for i in name.split():
            if len(i) < 2:
                q += 'False'
            else:
                q += 'True'
    else:
        q += 'False'
        s = False
    if 'False' not in q:
        name_for_event = name
        bot.send_message(questionnaire_user_id, 'Количество человек:')
        bot.register_next_step_handler(message, registration_to_event_quantity)
        q = 'False'
    else:
        if s is False:
            ans(message, 'registration_to_event_name', 'few_words')
        else:
            ans(message, 'registration_to_event_name', 'few_letters')


def registration_to_event_quantity(message):
    global quantity_for_event, questionnaire_user_id
    try:
        int(message.text)
        if int(message.text) <= 20:
            quantity_for_event = message.text
            bot.send_message(questionnaire_user_id, 'Ваш номер телефона:')
            bot.register_next_step_handler(message, registration_to_event_phone)
        else:
            ans(message, 'registration_to_event_quantity', 'very_much')
    except ValueError or KeyError:
        ans(message, 'registration_to_event_quantity', 'not_int')


def registration_to_event_phone(message):
    global phone_for_event, questionnaire_user_id, name_event_reg
    if len(message.text) == 11:
        try:
            int(message.text)
            phone_for_event = message.text
            if os.path.isfile(f'{name_event_reg}.csv'):
                f = open(f'{name_event_reg}.csv', 'a')
                f.write(f'\n{name_for_event};{quantity_for_event};{phone_for_event};')
            else:
                f = open(f'{name_event_reg}.csv', 'w')
                f.write('ФИО;Количество человек;Номер телефона;')
                f.write(f'\n{name_for_event};{quantity_for_event};{phone_for_event};')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['Назад']])
            bot.send_message(questionnaire_user_id,
                             f'Отлично, вы записаны на мероприятие "{name_event_reg}". За 3 дня мы напомним Вам о нём.',
                             reply_markup=keyboard)

        except ValueError or KeyError:
            ans(message, 'registration_to_event_phone', 'not_int')
    elif len(message.text) < 11:
        ans(message, 'registration_to_event_phone', 'short')
    else:
        ans(message, 'registration_to_event_phone', 'long')


def anketa_to_group_father_name(message):
    global questionnaire_father_full_name, q, questionnaire_user_id, questionnaire_father_age, \
        questionnaire_father_scope_of_work, questionnaire_father_hobby, questionnaire_father_can_hold_events, \
        questionnaire_father_want_to_participate_in_events, questionnaire_inventory, questionnaire_number_of_children, \
        questionnaire_children_full_names, questionnaire_children_dates_of_birth, questionnaire_children_age, \
        questionnaire_children_classes, questionnaire_children_clubs, questionnaire_children_interests, questionnaire_ideas
    questionnaire_father_full_name = message.text
    questionnaire_father_age = ''  # Возраст пользователья
    questionnaire_father_scope_of_work = ''  # Сфера работы пользователя
    questionnaire_father_hobby = []  # Увлечения пользователя
    questionnaire_father_can_hold_events = []  # Какие мероприятия может проводить пользователь
    questionnaire_father_want_to_participate_in_events = []  # В каких мероприятиях пользователь хочет учавствовать
    questionnaire_inventory = []  # инвентарь пользователья
    questionnaire_number_of_children = 0
    questionnaire_children_full_names = []  # ФИО детей пользователя
    questionnaire_children_dates_of_birth = []  # дата рождения детей пользователя
    questionnaire_children_age = []  # возраст детей пользователя
    questionnaire_children_classes = []  # класс детей пользователя
    questionnaire_children_clubs = []  # секции детей пользователя
    questionnaire_children_interests = []  # интересы детей пользователя
    questionnaire_ideas = ''  # идеи
    name = message.text
    q = ''
    if len(name.split()) == 3:
        s = True
        for i in name.split():
            if len(i) < 2:
                q += 'False'
            else:
                q += 'True'
    else:
        q += 'False'
        s = False
    if 'False' not in q:
        bot.send_message(questionnaire_user_id, 'Ваш возраст:')
        bot.register_next_step_handler(message, anketa_to_group_father_age)
        q = 'False'
    else:
        if s is False:
            ans(message, 'anketa_to_group_father_name', 'few_words')
        else:
            ans(message, 'anketa_to_group_father_name', 'few_letters')


def anketa_to_group_father_age(message):
    global questionnaire_user_id, questionnaire_father_age
    questionnaire_father_age = message.text
    try:
        int(questionnaire_father_age)
        if int(questionnaire_father_age) < 18:
            ans(message, 'anketa_to_group_father_age', 'too_young')
        elif int(questionnaire_father_age) > 100:
            ans(message, 'anketa_to_group_father_age', 'too_old')
        else:
            bot.send_message(questionnaire_user_id, 'В какой сфере Вы работаете?')
            bot.register_next_step_handler(message, anketa_to_group_father_scope_of_work)
    except ValueError:
        ans(message, 'anketa_to_group_father_age', 'not_int')


def anketa_to_group_father_scope_of_work(message):
    global questionnaire_user_id, questionnaire_father_scope_of_work
    questionnaire_father_scope_of_work = message.text
    bot.send_message(questionnaire_user_id, 'Ваши увлечения ЧЕРЕЗ ЗАПЯТУЮ:')
    bot.register_next_step_handler(message, anketa_to_group_father_hobby)


def anketa_to_group_father_hobby(message):
    global questionnaire_user_id, questionnaire_father_hobby, list_of_events_to_be_held
    questionnaire_father_hobby = str(message.text).split(',')
    markup = types.InlineKeyboardMarkup()
    for i in list_of_events_to_be_held:
        markup.row(types.InlineKeyboardButton(f'{i}', callback_data=f'{i} held'))
    bot.send_message(questionnaire_user_id, 'Какие мероприятия хотели бы ОРГАНИЗОВАТЬ?', reply_markup=markup)


def anketa_to_group_father_arrange(message):
    global questionnaire_user_id, list_of_events_to_participate_in
    markup1 = types.InlineKeyboardMarkup()
    for i in list_of_events_to_participate_in:
        markup1.row(types.InlineKeyboardButton(f'{i}', callback_data=f'{i} participate'))
    bot.send_message(questionnaire_user_id, 'В каких мероприятиях хотели бы принять участие с ребенком?',
                     reply_markup=markup1)


def anketa_to_group_father_participate(message):
    global questionnaire_user_id, message_glob
    message_glob.text = message
    message = message_glob
    bot.send_message(questionnaire_user_id,
                     'Есть ли у Вас какой-либо инвентарь который вы можете предоставлять в пользование Совету Отцов? Перечислите ЧЕРЕЗ ЗАПЯТУЮ:')
    bot.register_next_step_handler(message, anketa_to_group_inventory)


def anketa_to_group_inventory(message):
    global questionnaire_inventory, questionnaire_user_id
    questionnaire_inventory = str(message.text).split(',')
    bot.send_message(questionnaire_user_id, 'Сколько у Вас детей? (от 0 до 7)')
    bot.register_next_step_handler(message, anketa_to_group_count_of_children)


def anketa_to_group_count_of_children(message):
    global questionnaire_user_id, questionnaire_number_of_children, counter_of_children
    try:
        int(message.text)
        questionnaire_number_of_children = int(message.text)
        counter_of_children = int(message.text) - 1
        if questionnaire_number_of_children == 0:
            bot.send_message(questionnaire_user_id, 'Есть ли у Вас какие либо идеи, пожалания?')
            bot.register_next_step_handler(message, anketa_to_group_ideas)
        elif questionnaire_number_of_children > 8:
            ans(message, 'count_of_children', 'more_8')
        else:
            questionnaire_number_of_children = int(message.text)
            bot.send_message(questionnaire_user_id, 'Введите ФИО первого ребенка:')
            bot.register_next_step_handler(message, anketa_to_group_names_of_children_one)
    except ValueError:
        ans(message, 'count_of_children', 'not_int')


def anketa_to_group_names_of_children_one(message):
    global questionnaire_user_id, questionnaire_children_full_names, counter_of_children, q
    name = message.text
    q = ''
    if len(name.split()) == 3:
        s = True
        for i in name.split():
            if len(i) < 2:
                q += 'False'
            else:
                q += 'True'
    else:
        q += 'False'
        s = False
    if 'False' not in q:
        if counter_of_children > 0:
            questionnaire_children_full_names.append(message.text)
            counter_of_children -= 1
            bot.send_message(questionnaire_user_id, 'Введите ФИО второго ребёнка:')
            bot.register_next_step_handler(message, anketa_to_group_names_of_children_two)
            q = 'False'
        else:
            questionnaire_children_full_names.append(message.text)
            bot.send_message(questionnaire_user_id,
                             f'{questionnaire_children_full_names[0].title()}. Введите его год рождения:')
            bot.register_next_step_handler(message, anketa_to_group_birthday_one)
    else:
        if s is False:
            ans(message, 'anketa_to_group_names_of_children', 'few_words', 'one')
        else:
            ans(message, 'anketa_to_group_names_of_children', 'few_letters', 'one')


def anketa_to_group_names_of_children_two(message):
    global questionnaire_user_id, questionnaire_children_full_names, counter_of_children, q
    name = message.text
    q = ''
    if len(name.split()) == 3:
        s = True
        for i in name.split():
            if len(i) < 2:
                q += 'False'
            else:
                q += 'True'
    else:
        q += 'False'
        s = False
    if 'False' not in q:
        if counter_of_children > 0:
            questionnaire_children_full_names.append(message.text)
            counter_of_children -= 1
            bot.send_message(questionnaire_user_id, 'Введите ФИО третьего ребёнка:')
            bot.register_next_step_handler(message, anketa_to_group_names_of_children_three)
            q = 'False'
        else:
            questionnaire_children_full_names.append(message.text)
            bot.send_message(questionnaire_user_id,
                             f'{questionnaire_children_full_names[0].title()}. Введите его год рождения:')
            bot.register_next_step_handler(message, anketa_to_group_birthday_one)
    else:
        if s is False:
            ans(message, 'anketa_to_group_names_of_children', 'few_words', 'two')
        else:
            ans(message, 'anketa_to_group_names_of_children', 'few_letters', 'two')


def anketa_to_group_names_of_children_three(message):
    global questionnaire_user_id, questionnaire_children_full_names, counter_of_children, q
    name = message.text
    q = ''
    if len(name.split()) == 3:
        s = True
        for i in name.split():
            if len(i) < 2:
                q += 'False'
            else:
                q += 'True'
    else:
        q += 'False'
        s = False
    if 'False' not in q:
        if counter_of_children > 0:
            questionnaire_children_full_names.append(message.text)
            counter_of_children -= 1
            bot.send_message(questionnaire_user_id, 'Введите ФИО четвертого ребёнка:')
            bot.register_next_step_handler(message, anketa_to_group_names_of_children_four)
            q = 'False'
        else:
            questionnaire_children_full_names.append(message.text)
            bot.send_message(questionnaire_user_id,
                             f'{questionnaire_children_full_names[0].title()}. Введите его год рождения:')
            bot.register_next_step_handler(message, anketa_to_group_birthday_one)
    else:
        if s is False:
            ans(message, 'anketa_to_group_names_of_children', 'few_words', 'three')
        else:
            ans(message, 'anketa_to_group_names_of_children', 'few_letters', 'three')


def anketa_to_group_names_of_children_four(message):
    global questionnaire_user_id, questionnaire_children_full_names, counter_of_children, q
    name = message.text
    q = ''
    if len(name.split()) == 3:
        s = True
        for i in name.split():
            if len(i) < 2:
                q += 'False'
            else:
                q += 'True'
    else:
        q += 'False'
        s = False
    if 'False' not in q:
        if counter_of_children > 0:
            questionnaire_children_full_names.append(message.text)
            counter_of_children -= 1
            bot.send_message(questionnaire_user_id, 'Введите ФИО пятого ребёнка:')
            bot.register_next_step_handler(message, anketa_to_group_names_of_children_five)
            q = 'False'
        else:
            questionnaire_children_full_names.append(message.text)
            bot.send_message(questionnaire_user_id,
                             f'{questionnaire_children_full_names[0].title()}. Введите его год рождения:')
            bot.register_next_step_handler(message, anketa_to_group_birthday_one)
    else:
        if s is False:
            ans(message, 'anketa_to_group_names_of_children', 'few_words', 'four')
        else:
            ans(message, 'anketa_to_group_names_of_children', 'few_letters', 'four')


def anketa_to_group_names_of_children_five(message):
    global questionnaire_user_id, questionnaire_children_full_names, counter_of_children, q
    name = message.text
    q = ''
    if len(name.split()) == 3:
        s = True
        for i in name.split():
            if len(i) < 2:
                q += 'False'
            else:
                q += 'True'
    else:
        q += 'False'
        s = False
    if 'False' not in q:
        if counter_of_children > 0:
            counter_of_children -= 1
            questionnaire_children_full_names.append(message.text)
            bot.send_message(questionnaire_user_id, 'Введите ФИО шестого ребёнка:')
            bot.register_next_step_handler(message, anketa_to_group_names_of_children_six)
            q = ''
        else:
            questionnaire_children_full_names.append(message.text)
            bot.send_message(questionnaire_user_id,
                             f'{questionnaire_children_full_names[0].title()}. Введите его год рождения:')
            bot.register_next_step_handler(message, anketa_to_group_birthday_one)
    else:
        if s is False:
            ans(message, 'anketa_to_group_names_of_children', 'few_words', 'five')
        else:
            ans(message, 'anketa_to_group_names_of_children', 'few_letters', 'five')


def anketa_to_group_names_of_children_six(message):
    global questionnaire_user_id, questionnaire_children_full_names, counter_of_children, q
    name = message.text
    q = ''
    if len(name.split()) == 3:
        s = True
        for i in name.split():
            if len(i) < 2:
                q += 'False'
            else:
                q += 'True'
    else:
        q += 'False'
        s = False
    if 'False' not in q:
        if counter_of_children > 0:
            questionnaire_children_full_names.append(message.text)
            counter_of_children -= 1
            bot.send_message(questionnaire_user_id, 'Введите ФИО седьмого ребёнка:')
            bot.register_next_step_handler(message, anketa_to_group_names_of_children_seven)
            q = 'False'
        else:
            questionnaire_children_full_names.append(message.text)
            bot.send_message(questionnaire_user_id,
                             f'{questionnaire_children_full_names[0].title()}. Введите его год рождения:')
            bot.register_next_step_handler(message, anketa_to_group_birthday_one)
    else:
        if s is False:
            ans(message, 'anketa_to_group_names_of_children', 'few_words', 'six')
        else:
            ans(message, 'anketa_to_group_names_of_children', 'few_letters', 'six')


def anketa_to_group_names_of_children_seven(message):
    global questionnaire_user_id, questionnaire_children_full_names, counter_of_children, q
    name = message.text
    q = ''
    if len(name.split()) == 3:
        s = True
        for i in name.split():
            if len(i) < 2:
                q += 'False'
            else:
                q += 'True'
    else:
        q += 'False'
        s = False
    if 'False' not in q:
        questionnaire_children_full_names.append(message.text)
        bot.send_message(questionnaire_user_id,
                         f'{questionnaire_children_full_names[0].title()}. Введите его год рождения:')
        bot.register_next_step_handler(message, anketa_to_group_birthday_one)
    else:
        if s is False:
            ans(message, 'anketa_to_group_names_of_children', 'few_words', 'seven')
        else:
            ans(message, 'anketa_to_group_names_of_children', 'few_letters', 'seven')


def anketa_to_group_birthday_one(message):
    global questionnaire_children_dates_of_birth, questionnaire_user_id, questionnaire_number_of_children, counter_of_children, questionnaire_children_full_names
    birthday = message.text
    counter_of_children = questionnaire_number_of_children - 1
    if len(str(birthday)) != 4:
        ans(message, 'anketa_to_group_birthday', 'few_simbols', 'one')
    else:
        try:
            int(birthday)
            questionnaire_children_dates_of_birth.append(birthday)
            if counter_of_children > 0:
                counter_of_children -= 1
                bot.send_message(questionnaire_user_id,
                                 f'{questionnaire_children_full_names[1]}. Введите его год рождения:')
                bot.register_next_step_handler(message, anketa_to_group_birthday_two)
            else:
                bot.send_message(questionnaire_user_id,
                                 f'В каком классе обучается {questionnaire_children_full_names[0].title()}?')
                bot.register_next_step_handler(message, anketa_to_group_class_one)
        except ValueError:
            ans(message, 'anketa_to_group_birthday', 'not_int', 'one')


def anketa_to_group_birthday_two(message):
    global questionnaire_children_dates_of_birth, questionnaire_user_id, questionnaire_number_of_children, counter_of_children, questionnaire_children_full_names
    birthday = message.text

    if len(str(birthday)) != 4:
        ans(message, 'anketa_to_group_birthday', 'few_simbols', 'two')
    else:
        try:
            int(birthday)
            questionnaire_children_dates_of_birth.append(birthday)
            if counter_of_children > 0:
                counter_of_children -= 1
                bot.send_message(questionnaire_user_id,
                                 f'{questionnaire_children_full_names[2]}. Введите его год рождения:')
                bot.register_next_step_handler(message, anketa_to_group_birthday_three)
            else:
                bot.send_message(questionnaire_user_id,
                                 f'В каком классе обучается {questionnaire_children_full_names[0].title()}?')
                bot.register_next_step_handler(message, anketa_to_group_class_one)
        except ValueError:
            ans(message, 'anketa_to_group_birthday', 'not_int', 'two')


def anketa_to_group_birthday_three(message):
    global questionnaire_children_dates_of_birth, questionnaire_user_id, questionnaire_number_of_children, counter_of_children, questionnaire_children_full_names
    birthday = message.text

    if len(str(birthday)) != 4:
        ans(message, 'anketa_to_group_birthday', 'few_simbols', 'three')
    else:
        try:
            int(birthday)
            questionnaire_children_dates_of_birth.append(birthday)
            if counter_of_children > 0:
                counter_of_children -= 1
                bot.send_message(questionnaire_user_id,
                                 f'{questionnaire_children_full_names[3]}. Введите его год рождения:')
                bot.register_next_step_handler(message, anketa_to_group_birthday_four)
            else:
                bot.send_message(questionnaire_user_id,
                                 f'В каком классе обучается {questionnaire_children_full_names[0].title()}?')
                bot.register_next_step_handler(message, anketa_to_group_class_one)
        except ValueError:
            ans(message, 'anketa_to_group_birthday', 'not_int', 'three')


def anketa_to_group_birthday_four(message):
    global questionnaire_children_dates_of_birth, questionnaire_user_id, questionnaire_number_of_children, counter_of_children, questionnaire_children_full_names
    birthday = message.text

    if len(str(birthday)) != 4:
        ans(message, 'anketa_to_group_birthday', 'few_simbols', 'four')
    else:
        try:
            int(birthday)
            questionnaire_children_dates_of_birth.append(birthday)
            if counter_of_children > 0:
                counter_of_children -= 1
                bot.send_message(questionnaire_user_id,
                                 f'{questionnaire_children_full_names[4]}. Введите его год рождения:')
                bot.register_next_step_handler(message, anketa_to_group_birthday_five)
            else:
                bot.send_message(questionnaire_user_id,
                                 f'В каком классе обучается {questionnaire_children_full_names[0].title()}?')
                bot.register_next_step_handler(message, anketa_to_group_class_one)
        except ValueError:
            ans(message, 'anketa_to_group_birthday', 'not_int', 'four')


def anketa_to_group_birthday_five(message):
    global questionnaire_children_dates_of_birth, questionnaire_user_id, questionnaire_number_of_children, counter_of_children, questionnaire_children_full_names
    birthday = message.text
    if len(str(birthday)) != 4:
        ans(message, 'anketa_to_group_birthday', 'few_simbols', 'five')
    else:
        try:
            int(birthday)
            questionnaire_children_dates_of_birth.append(birthday)
            if counter_of_children > 0:
                counter_of_children -= 1
                bot.send_message(questionnaire_user_id,
                                 f'{questionnaire_children_full_names[5]}. Введите его год рождения:')
                bot.register_next_step_handler(message, anketa_to_group_birthday_six)
            else:
                bot.send_message(questionnaire_user_id,
                                 f'В каком классе обучается {questionnaire_children_full_names[0].title()}?')
                bot.register_next_step_handler(message, anketa_to_group_class_one)
        except ValueError:
            ans(message, 'anketa_to_group_birthday', 'not_int', 'five')


def anketa_to_group_birthday_six(message):
    global questionnaire_children_dates_of_birth, questionnaire_user_id, questionnaire_number_of_children, counter_of_children, questionnaire_children_full_names
    birthday = message.text
    if len(str(birthday)) != 4:
        ans(message, 'anketa_to_group_birthday', 'few_simbols', 'six')
    else:
        try:
            int(birthday)
            questionnaire_children_dates_of_birth.append(birthday)
            if counter_of_children > 0:
                counter_of_children -= 1
                bot.send_message(questionnaire_user_id,
                                 f'{questionnaire_children_full_names[6]}. Введите его год рождения:')
                bot.register_next_step_handler(message, anketa_to_group_birthday_seven)
            else:
                bot.send_message(questionnaire_user_id,
                                 f'В каком классе обучается {questionnaire_children_full_names[0].title()}?')
                bot.register_next_step_handler(message, anketa_to_group_class_one)
        except ValueError:
            ans(message, 'anketa_to_group_birthday', 'not_int', 'six')


def anketa_to_group_birthday_seven(message):
    global questionnaire_children_dates_of_birth, questionnaire_user_id, questionnaire_number_of_children, counter_of_children, questionnaire_children_full_names
    birthday = message.text
    if len(str(birthday)) != 4:
        ans(message, 'anketa_to_group_birthday', 'few_simbols', 'seven')
    else:
        try:
            int(birthday)
            questionnaire_children_dates_of_birth.append(birthday)
            bot.send_message(questionnaire_user_id,
                             f'В каком классе обучается {questionnaire_children_full_names[0].title()}?')
            bot.register_next_step_handler(message, anketa_to_group_class_one)
        except ValueError:
            ans(message, 'anketa_to_group_birthday', 'not_int', 'seven')


def anketa_to_group_class_one(message):
    global questionnaire_user_id, questionnaire_children_full_names, counter_of_children, questionnaire_number_of_children
    class_boy = message.text
    counter_of_children = questionnaire_number_of_children - 1
    if counter_of_children > 0:
        counter_of_children -= 1
        questionnaire_children_classes.append(class_boy)
        bot.send_message(questionnaire_user_id,
                         f'В каком классе обучается {questionnaire_children_full_names[1].title()}?')
        bot.register_next_step_handler(message, anketa_to_group_class_two)
    else:
        questionnaire_children_classes.append(class_boy)
        bot.send_message(questionnaire_user_id,
                         f'Какие секции посещает {questionnaire_children_full_names[0].title()}? (Если больше одной, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_clubs_one)


def anketa_to_group_class_two(message):
    global questionnaire_user_id, questionnaire_children_full_names, counter_of_children
    class_boy = message.text
    if counter_of_children > 0:
        counter_of_children -= 1
        questionnaire_children_classes.append(class_boy)
        bot.send_message(questionnaire_user_id,
                         f'В каком классе обучается {questionnaire_children_full_names[2].title()}?')
        bot.register_next_step_handler(message, anketa_to_group_class_three)
    else:
        questionnaire_children_classes.append(class_boy)
        bot.send_message(questionnaire_user_id,
                         f'Какие секции посещает {questionnaire_children_full_names[0].title()}? (Если больше одной, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_clubs_one)


def anketa_to_group_class_three(message):
    global questionnaire_user_id, questionnaire_children_full_names, counter_of_children
    class_boy = message.text
    if counter_of_children > 0:
        counter_of_children -= 1
        questionnaire_children_classes.append(class_boy)
        bot.send_message(questionnaire_user_id,
                         f'В каком классе обучается {questionnaire_children_full_names[3].title()}?')
        bot.register_next_step_handler(message, anketa_to_group_class_four)
    else:
        questionnaire_children_classes.append(class_boy)
        bot.send_message(questionnaire_user_id,
                         f'Какие секции посещает {questionnaire_children_full_names[0].title()}? (Если больше одной, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_clubs_one)


def anketa_to_group_class_four(message):
    global questionnaire_user_id, questionnaire_children_full_names, counter_of_children
    class_boy = message.text
    if counter_of_children > 0:
        counter_of_children -= 1
        questionnaire_children_classes.append(class_boy)
        bot.send_message(questionnaire_user_id,
                         f'В каком классе обучается {questionnaire_children_full_names[4].title()}?')
        bot.register_next_step_handler(message, anketa_to_group_class_five)
    else:
        questionnaire_children_classes.append(class_boy)
        bot.send_message(questionnaire_user_id,
                         f'Какие секции посещает {questionnaire_children_full_names[0].title()}? (Если больше одной, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_clubs_one)


def anketa_to_group_class_five(message):
    global questionnaire_user_id, questionnaire_children_full_names, counter_of_children
    class_boy = message.text
    if counter_of_children > 0:
        counter_of_children -= 1
        questionnaire_children_classes.append(class_boy)
        bot.send_message(questionnaire_user_id,
                         f'В каком классе обучается {questionnaire_children_full_names[5].title()}?')
        bot.register_next_step_handler(message, anketa_to_group_class_six)
    else:
        questionnaire_children_classes.append(class_boy)
        bot.send_message(questionnaire_user_id,
                         f'Какие секции посещает {questionnaire_children_full_names[0].title()}? (Если больше одной, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_clubs_one)


def anketa_to_group_class_six(message):
    global questionnaire_user_id, questionnaire_children_full_names, counter_of_children
    class_boy = message.text
    if counter_of_children > 0:
        counter_of_children -= 1
        questionnaire_children_classes.append(class_boy)
        bot.send_message(questionnaire_user_id,
                         f'В каком классе обучается {questionnaire_children_full_names[6].title()}?')
        bot.register_next_step_handler(message, anketa_to_group_class_seven)
    else:
        questionnaire_children_classes.append(class_boy)
        bot.send_message(questionnaire_user_id,
                         f'Какие секции посещает {questionnaire_children_full_names[0].title()}? (Если больше одной, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_clubs_one)


def anketa_to_group_class_seven(message):
    global questionnaire_user_id, questionnaire_children_full_names
    class_boy = message.text
    questionnaire_children_classes.append(class_boy)
    bot.send_message(questionnaire_user_id,
                     f'Какие секции посещает {questionnaire_children_full_names[0].title()}? (Если больше одной, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
    bot.register_next_step_handler(message, anketa_to_group_clubs_one)


def anketa_to_group_clubs_one(message):
    global questionnaire_children_clubs, questionnaire_user_id, questionnaire_children_full_names, counter_of_children, questionnaire_number_of_children
    questionnaire_children_clubs.append(message.text)
    counter_of_children = questionnaire_number_of_children - 1
    if counter_of_children > 0:
        counter_of_children -= 1
        bot.send_message(questionnaire_user_id,
                         f'Какие секции посещает {questionnaire_children_full_names[1].title()}? (Если больше одной, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_clubs_two)
    else:
        bot.send_message(questionnaire_user_id,
                         f'Чем увлекается {questionnaire_children_full_names[0].title()}? (Если больше одного увлечения, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_hobby_children_one)


def anketa_to_group_clubs_two(message):
    global questionnaire_children_clubs, questionnaire_user_id, questionnaire_children_full_names, counter_of_children
    questionnaire_children_clubs.append(message.text)
    if counter_of_children > 0:
        counter_of_children -= 1
        bot.send_message(questionnaire_user_id,
                         f'Какие секции посещает {questionnaire_children_full_names[2].title()}? (Если больше одной, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_clubs_three)
    else:
        bot.send_message(questionnaire_user_id,
                         f'Чем увлекается {questionnaire_children_full_names[0].title()}? (Если больше одного увлечения, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_hobby_children_one)


def anketa_to_group_clubs_three(message):
    global questionnaire_children_clubs, questionnaire_user_id, questionnaire_children_full_names, counter_of_children
    questionnaire_children_clubs.append(message.text)
    if counter_of_children > 0:
        counter_of_children -= 1
        bot.send_message(questionnaire_user_id,
                         f'Какие секции посещает {questionnaire_children_full_names[3].title()}? (Если больше одной, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_clubs_four)
    else:
        bot.send_message(questionnaire_user_id,
                         f'Чем увлекается {questionnaire_children_full_names[0].title()}? (Если больше одного увлечения, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_hobby_children_one)


def anketa_to_group_clubs_four(message):
    global questionnaire_children_clubs, questionnaire_user_id, questionnaire_children_full_names, counter_of_children
    questionnaire_children_clubs.append(message.text)
    if counter_of_children > 0:
        counter_of_children -= 1
        bot.send_message(questionnaire_user_id,
                         f'Какие секции посещает {questionnaire_children_full_names[4].title()}? (Если больше одной, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_clubs_five)
    else:
        bot.send_message(questionnaire_user_id,
                         f'Чем увлекается {questionnaire_children_full_names[0].title()}? (Если больше одного увлечения, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_hobby_children_one)


def anketa_to_group_clubs_five(message):
    global questionnaire_children_clubs, questionnaire_user_id, questionnaire_children_full_names, counter_of_children
    questionnaire_children_clubs.append(message.text)
    if counter_of_children > 0:
        counter_of_children -= 1
        bot.send_message(questionnaire_user_id,
                         f'Какие секции посещает {questionnaire_children_full_names[5].title()}? (Если больше одной, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_clubs_six)
    else:
        bot.send_message(questionnaire_user_id,
                         f'Чем увлекается {questionnaire_children_full_names[0].title()}? (Если больше одного увлечения, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_hobby_children_one)


def anketa_to_group_clubs_six(message):
    global questionnaire_children_clubs, questionnaire_user_id, questionnaire_children_full_names, counter_of_children
    questionnaire_children_clubs.append(message.text)
    if counter_of_children > 0:
        counter_of_children -= 1
        bot.send_message(questionnaire_user_id,
                         f'Какие секции посещает {questionnaire_children_full_names[6].title()}? (Если больше одной, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_clubs_seven)
    else:
        bot.send_message(questionnaire_user_id,
                         f'Чем увлекается {questionnaire_children_full_names[0].title()}? (Если больше одного увлечения, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_hobby_children_one)


def anketa_to_group_clubs_seven(message):
    global questionnaire_children_clubs, questionnaire_user_id, questionnaire_children_full_names, counter_of_children
    questionnaire_children_clubs.append(message.text)
    bot.send_message(questionnaire_user_id,
                     f'Чем увлекается {questionnaire_children_full_names[0].title()}? (Если больше одного увлечения, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
    bot.register_next_step_handler(message, anketa_to_group_hobby_children_one)


def anketa_to_group_hobby_children_one(message):
    global questionnaire_user_id, questionnaire_children_clubs, counter_of_children, questionnaire_number_of_children
    counter_of_children = questionnaire_number_of_children
    questionnaire_children_interests.append(message.text)
    if counter_of_children > 1:
        counter_of_children -= 1
        bot.send_message(questionnaire_user_id,
                         f'Чем увлекается {questionnaire_children_full_names[1].title()}? (Если больше одного увлечения, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_hobby_children_two)
    else:
        bot.send_message(questionnaire_user_id,
                         f'Есть ли у Вас идеи или предложения?')
        bot.register_next_step_handler(message, anketa_to_group_ideas)


def anketa_to_group_hobby_children_two(message):
    global questionnaire_user_id, questionnaire_children_clubs, counter_of_children
    questionnaire_children_interests.append(message.text)
    if counter_of_children > 1:
        counter_of_children -= 1
        bot.send_message(questionnaire_user_id,
                         f'Чем увлекается {questionnaire_children_full_names[2].title()}? (Если больше одного увлечения, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_hobby_children_three)
    else:
        bot.send_message(questionnaire_user_id,
                         f'Есть ли у Вас идеи или предложения?')
        bot.register_next_step_handler(message, anketa_to_group_ideas)


def anketa_to_group_hobby_children_three(message):
    global questionnaire_user_id, questionnaire_children_clubs, counter_of_children
    questionnaire_children_interests.append(message.text)
    if counter_of_children > 1:
        counter_of_children -= 1
        bot.send_message(questionnaire_user_id,
                         f'Чем увлекается {questionnaire_children_full_names[3].title()}? (Если больше одного увлечения, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_hobby_children_four)
    else:
        bot.send_message(questionnaire_user_id,
                         f'Есть ли у Вас идеи или предложения?')
        bot.register_next_step_handler(message, anketa_to_group_ideas)


def anketa_to_group_hobby_children_four(message):
    global questionnaire_user_id, questionnaire_children_clubs, counter_of_children
    questionnaire_children_interests.append(message.text)
    if counter_of_children > 1:
        counter_of_children -= 1
        bot.send_message(questionnaire_user_id,
                         f'Чем увлекается {questionnaire_children_full_names[4].title()}? (Если больше одного увлечения, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_hobby_children_five)
    else:
        bot.send_message(questionnaire_user_id,
                         f'Есть ли у Вас идеи или предложения?')
        bot.register_next_step_handler(message, anketa_to_group_ideas)


def anketa_to_group_hobby_children_five(message):
    global questionnaire_user_id, questionnaire_children_clubs, counter_of_children
    questionnaire_children_interests.append(message.text)
    if counter_of_children > 1:
        counter_of_children -= 1
        bot.send_message(questionnaire_user_id,
                         f'Чем увлекается {questionnaire_children_full_names[5].title()}? (Если больше одного увлечения, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_hobby_children_six)
    else:
        bot.send_message(questionnaire_user_id,
                         f'Есть ли у Вас идеи или предложения?')
        bot.register_next_step_handler(message, anketa_to_group_ideas)


def anketa_to_group_hobby_children_six(message):
    global questionnaire_user_id, questionnaire_children_clubs, counter_of_children
    questionnaire_children_interests.append(message.text)
    if counter_of_children > 1:
        counter_of_children -= 1
        bot.send_message(questionnaire_user_id,
                         f'Чем увлекается {questionnaire_children_full_names[6].title()}? (Если больше одного увлечения, вводите ЧЕРЕЗ ЗАПЯТУЮ):')
        bot.register_next_step_handler(message, anketa_to_group_hobby_children_seven)
    else:
        bot.send_message(questionnaire_user_id,
                         f'Есть ли у Вас идеи или предложения?')
        bot.register_next_step_handler(message, anketa_to_group_ideas)


def anketa_to_group_hobby_children_seven(message):
    global questionnaire_user_id, questionnaire_children_clubs, counter_of_children
    questionnaire_children_interests.append(message.text)
    bot.send_message(questionnaire_user_id,
                     f'Есть ли у Вас идеи или предложения?')
    bot.register_next_step_handler(message, anketa_to_group_ideas)


def anketa_to_group_ideas(message):
    global questionnaire_father_full_name, questionnaire_father_age, questionnaire_father_scope_of_work, \
        questionnaire_father_hobby, questionnaire_father_want_to_participate_in_events, questionnaire_father_can_hold_events, \
        questionnaire_children_full_names, questionnaire_children_age, questionnaire_children_classes, \
        questionnaire_children_dates_of_birth, questionnaire_children_clubs, questionnaire_children_interests, \
        questionnaire_ideas, questionnaire_user_id, questionnaire_inventory
    questionnaire_ideas = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Назад']])
    bot.send_message(questionnaire_user_id,
                     f"Вы записаны, в течение 2 дней Вашу заявку рассмотрят и свяжутся с Вами.",
                     reply_markup=keyboard)
    f = open('Questionnaire2.csv', 'a', encoding='utf-8-sig')
    f.write(
        f'\n{questionnaire_father_full_name};{questionnaire_father_age};{questionnaire_father_scope_of_work};'
        f'{" ".join(questionnaire_father_hobby)};{", ".join(questionnaire_father_can_hold_events)};'
        f'{", ".join(questionnaire_father_want_to_participate_in_events)};{" ".join(questionnaire_inventory)};')
    if len(questionnaire_children_full_names) != 0:
        f.write(
            f'{"".join(questionnaire_children_full_names[0])};{"".join(questionnaire_children_dates_of_birth[0])};'
            f';{"".join(questionnaire_children_classes[0])};{" ".join(questionnaire_children_clubs[0])};'
            f'{" ".join(questionnaire_children_interests[0])};{questionnaire_ideas}')
        if len(questionnaire_children_full_names) != 1:
            for i in questionnaire_children_full_names[1:]:
                name = i
                # num = questionnaire_children_full_names.index([i])
                try:
                    f.write(
                        f'\n;;;;;;;{" ".join(questionnaire_children_full_names[questionnaire_children_full_names.index(name)])};{"".join(questionnaire_children_dates_of_birth[questionnaire_children_full_names.index(name)])};'
                        f';{"".join(questionnaire_children_classes[questionnaire_children_full_names.index(name)])};{" ".join(questionnaire_children_clubs[questionnaire_children_full_names.index(name)])};'
                        f'{" ".join(questionnaire_children_interests[questionnaire_children_full_names.index(name)])}; {questionnaire_ideas}')
                except IndexError:
                    pass

        else:
            pass
    else:
        f.write(
            f';;;;;;{questionnaire_ideas};')


bot.polling(none_stop=True, interval=0)
