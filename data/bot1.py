import telebot
from telebot import types
from datetime import datetime
from EventService import get_events, get_event_detail, get_event_comments
from NewsService import get_news, get_news_comments, get_news_detail
from PlaceService import get_places, get_place_detail, get_place_comments

TOKEN = "7622174761:AAFwi7d4QXTAh6qjxy5sIzoxoPaih1vgJBs"
bot = telebot.TeleBot(TOKEN)

state = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Меню")
    markup.add(btn1)
    bot.send_message(message.chat.id, "Добро пожаловать! Нажмите кнопку 'Меню' для начала работы", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Меню")
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    btn_events = types.InlineKeyboardButton("События", callback_data="section:events")
    btn_news = types.InlineKeyboardButton("Новости", callback_data="section:news")
    btn_places = types.InlineKeyboardButton("Места", callback_data="section:places")
    markup.add(btn_events, btn_news, btn_places)
    bot.send_message(message.chat.id, "Выберите интересующий вас вариант", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: not call.data.startswith("more_comments"))
def callback_query(call):
    data = call.data.split(":")
    action = data[0]
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if action == "section":
        section = data[1]
        if section in ["events", "places"]:
            bot.send_message(chat_id, f"Введите код города для поиска (например, msk для Москвы):")
            state[chat_id] = f"waiting_for_location_{section}"
        elif section == "news":
            show_news(chat_id, 1)
    elif action in ["next", "prev"]:
        section = data[1]
        current_page = int(data[2])
        page = current_page + 1 if action == "next" else current_page - 1
        if page < 1:
            page = 1
        location = data[3] if len(data) > 3 else None
        if section == "events":
            show_events(chat_id, location, page, message_id)
        elif section == "news":
            show_news(chat_id, page, message_id)
        elif section == "places":
            show_places(chat_id, location, page, message_id)
    elif action == "event":
        event_id = int(data[1])
        show_event_detail(chat_id, event_id)
    elif action == "news":
        news_id = int(data[1])
        show_news_detail(chat_id, news_id)
    elif action == "place":
        place_id = int(data[1])
        show_place_detail(chat_id, place_id)
    elif action == "comments":
        item_type = data[1]
        item_id = int(data[2])
        show_comments(chat_id, item_type, item_id)


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    chat_id = message.chat.id
    if chat_id in state:
        if state[chat_id].startswith("waiting_for_location_"):
            section = state[chat_id].split("_")[-1]
            location = message.text.strip().lower()
            if section == "events":
                show_events(chat_id, location, 1)
            elif section == "places":
                show_places(chat_id, location, 1)
            del state[chat_id]


def show_events(chat_id, location, page, message_id=None):
    events_data = get_events(location, page)
    events = events_data["results"]
    if not events:
        text = f"События в {location} не найдены."
    else:
        text = f"События в {location}, страница {page}:\n\n"
        for event in events:
            title = event["title"]
            date_str = datetime.now().strftime("%Y-%m-%d")  # Текущая дата
            text += f"<b>{title}</b> ({date_str})\n\n"
    markup = types.InlineKeyboardMarkup()
    for event in events:
        btn = types.InlineKeyboardButton(event["title"], callback_data=f"event:{event['id']}")
        markup.add(btn)
    if events_data["previous"]:
        markup.add(types.InlineKeyboardButton("Назад", callback_data=f"prev:events:{page}:{location}"))
    if events_data["next"]:
        markup.add(types.InlineKeyboardButton("Далее", callback_data=f"next:events:{page}:{location}"))
    if message_id:
        bot.edit_message_text(text, chat_id, message_id, parse_mode="HTML", reply_markup=markup)
    else:
        bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=markup)

def show_news(chat_id, page, message_id=None):
    news_data = get_news(page)
    news_list = news_data["results"]
    if not news_list:
        text = "Новости не найдены."
    else:
        text = f"Новости, страница {page}:\n\n"
        for news in news_list:
            title = news["title"]
            pub_date = datetime.fromtimestamp(news["publication_date"]).strftime("%Y-%m-%d")
            text += f"<b>{title}</b> ({pub_date})\n\n"
    markup = types.InlineKeyboardMarkup()
    for news in news_list:
        btn = types.InlineKeyboardButton(news["title"], callback_data=f"news:{news['id']}")
        markup.add(btn)
    if news_data["previous"]:
        markup.add(types.InlineKeyboardButton("Назад", callback_data=f"prev:news:{page}"))
    if news_data["next"]:
        markup.add(types.InlineKeyboardButton("Далее", callback_data=f"next:news:{page}"))
    if message_id:
        bot.edit_message_text(text, chat_id, message_id, parse_mode="HTML", reply_markup=markup)
    else:
        bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=markup)

def show_places(chat_id, location, page, message_id=None):
    places_data = get_places(location, page)
    places = places_data["results"]
    if not places:
        text = f"Места в {location} не найдены."
    else:
        text = f"Места в {location}, страница {page}:\n\n"
        for place in places:
            title = place["title"]
            subway = place.get("subway", "N/A")
            if subway:
                text += f"<b>{title}</b> (Метро: {subway})\n\n"
            else:
                text += f"<b>{title}</b>\n\n"
    markup = types.InlineKeyboardMarkup()
    for place in places:
        btn = types.InlineKeyboardButton(place["title"], callback_data=f"place:{place['id']}")
        markup.add(btn)
    if places_data["previous"]:
        markup.add(types.InlineKeyboardButton("Назад", callback_data=f"prev:places:{page}:{location}"))
    if places_data["next"]:
        markup.add(types.InlineKeyboardButton("Далее", callback_data=f"next:places:{page}:{location}"))
    if message_id:
        bot.edit_message_text(text, chat_id, message_id, parse_mode="HTML", reply_markup=markup)
    else:
        bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=markup)

def show_event_detail(chat_id, event_id):
    event = get_event_detail(event_id)
    title = event["title"]
    description = event["description"].replace("<p>", "").replace("</p>", "") if event["description"] else ""
    images = event["images"]
    if images:
        bot.send_photo(chat_id, images[0]["image"], caption=title)
    else:
        bot.send_message(chat_id, title)
    if description:
        bot.send_message(chat_id, description)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Комментарии", callback_data=f"comments:event:{event_id}"))
    bot.send_message(chat_id, "Подробнее:", reply_markup=markup)

def show_news_detail(chat_id, news_id):
    news = get_news_detail(news_id)
    title = news["title"]
    description = news["description"].replace("<p>", "").replace("</p>", "") if news["description"] else ""
    images = news["images"]
    if images:
        bot.send_photo(chat_id, images[0]["image"], caption=title)
    else:
        bot.send_message(chat_id, title)
    if description:
        bot.send_message(chat_id, description)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Комментарии", callback_data=f"comments:news:{news_id}"))
    bot.send_message(chat_id, "Подробнее:", reply_markup=markup)

def show_place_detail(chat_id, place_id):
    place = get_place_detail(place_id)
    title = place["title"]
    description = place["description"].replace("<p>", "").replace("</p>", "") if place["description"] else ""
    images = place["images"]
    if images:
        bot.send_photo(chat_id, images[0]["image"], caption=title)
    else:
        bot.send_message(chat_id, title)
    if description:
        bot.send_message(chat_id, description)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Комментарии", callback_data=f"comments:place:{place_id}"))
    bot.send_message(chat_id, "Подробнее:", reply_markup=markup)


def show_comments(chat_id, item_type, item_id):
    if item_type == "event":
        comments_data = get_event_comments(item_id)
    elif item_type == "news":
        comments_data = get_news_comments(item_id)
    elif item_type == "place":
        comments_data = get_place_comments(item_id)

    comments = comments_data["results"]
    total_count = comments_data["count"]

    if not comments:
        bot.send_message(chat_id, "Комментариев пока нет.")
        return

    bot.send_message(chat_id, f"Комментарии (всего: {total_count}):")
    for comment in comments:
        user = comment["user"]["name"]
        text_comment = comment["text"].strip()
        if not text_comment:
            continue
        if comment["is_deleted"]:
            text_comment = "[Удалённый комментарий]"
        message = f"{user}: {text_comment}"
        try:
            bot.send_message(chat_id, message)
        except telebot.apihelper.ApiTelegramException as e:
            if "message is too long" in str(e):
                bot.send_message(chat_id, f"{user}: {text_comment[:4000]}... (сообщение обрезано)")

    if total_count > 20:
        warning = f"Показано первые 20 из {total_count} комментариев."
        bot.send_message(chat_id, warning)


if __name__ == "__main__":
    bot.polling()
