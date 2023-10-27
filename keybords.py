from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


# *************users part *************

def menu_main():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("🎁 Бонус за отзыв", callback_data="bonus"),
        InlineKeyboardButton("🏷 Акционные товары", callback_data="akcii"),                       
    )
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("❔ Faq", callback_data="faq"),
        InlineKeyboardButton("📍 Наши ресурсы", callback_data='resurce'),                             
                    
    )
    markup.row_width = 1
    markup.add(                             
        InlineKeyboardButton("🆘 Помощь", url='https://t.me/Mr_OYRusin'),                         
    )
    return markup

def choice_category():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Одежда", callback_data="category::Одежда"),
        InlineKeyboardButton("Аксессуары", callback_data="category::Аксессуары"),   
        InlineKeyboardButton("Иное", callback_data="category::Иное"),                               
    )

    return markup

def attention_otziv():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("✅ Я оставил(-а) отзыв", callback_data="otziv_screen_push"),
        InlineKeyboardButton("Назад", callback_data="back"),                           
    )

    return markup
def voronka(question, step):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    if step == 0:
        markup.add(
            InlineKeyboardButton("1", callback_data="voronka::1"),
            InlineKeyboardButton("2", callback_data="voronka::2"),
            InlineKeyboardButton("3", callback_data="voronka::3"),
            InlineKeyboardButton("4", callback_data="voronka::4"),                       
                
    )
    elif '4️⃣' not in question:
        markup.add(
            InlineKeyboardButton("1", callback_data="voronka::1"),
            InlineKeyboardButton("2", callback_data="voronka::2"),
            InlineKeyboardButton("3", callback_data="voronka::3"),
                    
                
    )
    else:
        markup.add(
            InlineKeyboardButton("1", callback_data="voronka::1"),
            InlineKeyboardButton("2", callback_data="voronka::2"),
            InlineKeyboardButton("3", callback_data="voronka::3"),
            InlineKeyboardButton("4", callback_data="voronka::4"),                    
                
    )

    return markup

def back():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Назад", callback_data="back"),
                      
    )

    return markup


# *************admin part *************

def admin_board():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Отчет по клиентам", callback_data="report"),
        InlineKeyboardButton("Отчет по админам", callback_data="report_admin"),
        InlineKeyboardButton("Отправить не по лидам", callback_data="no_lid"),
        InlineKeyboardButton("Отправить всем", callback_data="all"),        
                           
                      
    )

    return markup

