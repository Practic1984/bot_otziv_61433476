# -*- coding: utf-8 -*-
import telebot
from telebot import types, logger
import sys
import logging
import msg
import os
import datetime
import keybords
from config import TOKEN, GROUP_SPEC, ADMIN_LIST
from sqliteormmagic import SQLiteDB
import sqliteormmagic as som
import pytz
import pandas as pd
import time

bot = telebot.TeleBot(token=TOKEN, parse_mode='HTML', skip_pending=True)    
bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("start", "Запуск бота"),
    ],)
db_users = SQLiteDB('users.db')

def get_msk_time() -> datetime:
    time_now = datetime.datetime.now(pytz.timezone("Europe/Moscow"))
    time_now = time_now.strftime('%Y-%m-%d %H:%M:%S')
    return time_now

def cr_table_users(message):
    db_users.create_table('users', [
            ("from_user_id", 'INTEGER UNIQUE'), 
            ("from_user_username", 'TEXT'), 
            ("reg_time", 'TEXT'), 
            ("bonus_time", 'TEXT'), 
            ("faq_time", 'TEXT'), 
            ("akcii_time", 'TEXT'),     
            ("resurce_time", 'TEXT'),               
            ("category", 'TEXT'),  
            ("phone", 'TEXT'),                            
            ("lid", 'TEXT'),   
            ])
            
    db_users.ins_unique_row('users', [
            ("from_user_id", message.from_user.id), 
            ("from_user_username", message.from_user.username), 
            ("reg_time", get_msk_time()), 
            ("bonus_time", '0'), 
            ("faq_time", '0'), 
            ("akcii_time", '0'),     
            ("resurce_time", '0'),               
            ("category", '0'),  
            ("phone", '0'),                            
            ("lid", 'false'),   
            ])
    
def cr_table_admin(message):
    db_users.create_table('admins', [
            ("from_user_id", 'INTEGER UNIQUE'), 
            ("from_user_username", 'TEXT'), 
            ("reg_time", 'TEXT'), 
            ("type_push", 'TEXT'),         
            ("push_msg", 'TEXT'),                         
            ])
            
    db_users.ins_unique_row('admins', [
            ("from_user_id", message.from_user.id), 
            ("from_user_username", message.from_user.username), 
            ("reg_time", get_msk_time()), 
            ("type_push", '0'),         
            ("push_msg", '0'),    
            ])
    
def main():
    @bot.message_handler(commands=['start'])
    def start_fnc(message):
        cr_table_users(message)
        bot.send_message(chat_id=message.from_user.id, text=msg.start_msg,reply_markup=keybords.menu_main())
        
    
    @bot.message_handler(commands=['admin'])
    def admin_fnc(message):
        
        if message.from_user.id in ADMIN_LIST:
            cr_table_admin(message)
            bot.send_message(chat_id=message.from_user.id, text=msg.admnin_start_msg,reply_markup=keybords.admin_board())
            
    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
       
        if call.data == 'bonus':
            db_users.upd_element_in_column(table_name='users', upd_par_name='bonus_time', key_par_name=get_msk_time(), upd_column_name='from_user_id', key_column_name=call.from_user.id)
            bot.send_message(chat_id=call.from_user.id, text=msg.bonus_start_msg, reply_markup=keybords.choice_category())
           
        elif 'category' in call.data:
            print(call.data)
            category = call.data.split('::')[1]
            db_users.upd_element_in_column(table_name='users', upd_par_name='category', key_par_name=category, upd_column_name='from_user_id', key_column_name=call.from_user.id)
            bot.send_message(chat_id=call.from_user.id, text=msg.bonus_rules_msg, reply_markup=keybords.attention_otziv())
        
        elif 'otziv_screen_push' in call.data:
            m = bot.send_message(chat_id=call.from_user.id, text=msg.otziv_screen_msg)
            bot.register_next_step_handler(m, get_otziv_screen)

        elif call.data == 'faq':
            db_users.upd_element_in_column(table_name='users', upd_par_name='faq_time', key_par_name=get_msk_time(), upd_column_name='from_user_id', key_column_name=call.from_user.id)
            bot.send_message(chat_id=call.from_user.id, text=msg.faq_msg, reply_markup=keybords.back())
        
        elif call.data == 'resurce':
            db_users.upd_element_in_column(table_name='users', upd_par_name='resurce_time', key_par_name=get_msk_time(), upd_column_name='from_user_id', key_column_name=call.from_user.id)
            bot.send_message(chat_id=call.from_user.id, text=msg.resurce_msg, reply_markup=keybords.back(), disable_web_page_preview=True)                        

        elif call.data == 'akcii':
            db_users.upd_element_in_column(table_name='users', upd_par_name='akcii_time', key_par_name=get_msk_time(), upd_column_name='from_user_id', key_column_name=call.from_user.id)
            bot.send_message(chat_id=call.from_user.id, text=msg.akcii_msg, reply_markup=keybords.back())  

        elif call.data == 'back':
            bot.send_message(chat_id=call.from_user.id, text=msg.start_msg,reply_markup=keybords.menu_main())
        
        elif call.data == 'report':   # admin callback
            connection = som.create_connection('users.db')
            query = f"""
            SELECT * FROM users 
            """
            all_records = pd.read_sql_query(query, connection)
            # new_records = all_records.drop(columns=['photo'])
            len_of_records = len(all_records['from_user_id'])
            all_records.to_excel('report.xlsx', index=False)
            connection.close()
            with open('report.xlsx', mode='rb') as filename:
                bot.send_document(call.from_user.id, document=filename, caption=f'Всего {len_of_records} пользователей. Отчет по статистике пользователей в прикрепленном файле')
        
        elif call.data == 'report_admin':   # admin callback
            connection = som.create_connection('users.db')
            query = f"""
            SELECT * FROM admins 
            """
            all_records = pd.read_sql_query(query, connection)
            # new_records = all_records.drop(columns=['photo'])
            len_of_records = len(all_records['from_user_id'])
            all_records.to_excel('report.xlsx', index=False)
            connection.close()
            with open('report.xlsx', mode='rb') as filename:
                bot.send_document(call.from_user.id, document=filename, caption=f'Всего {len_of_records} админов. Отчет по статистике админов в прикрепленном файле')
        


        elif call.data == 'no_lid':  # admin callback
            
            db_users.upd_element_in_column(table_name='admins', upd_par_name='type_push', key_par_name=call.data, upd_column_name='from_user_id', key_column_name=call.from_user.id)
            m = bot.send_message(chat_id=call.from_user.id, text=msg.admnin_push_msg)
            bot.register_next_step_handler(m, input_push)
        
        elif call.data == 'all':
            db_users.upd_element_in_column(table_name='admins', upd_par_name='type_push', key_par_name=call.data, upd_column_name='from_user_id', key_column_name=call.from_user.id)
            m = bot.send_message(chat_id=call.from_user.id, text=msg.admnin_push_msg)
            bot.register_next_step_handler(m, input_push)

    def get_phone(message):
        db_users.upd_element_in_column(table_name='users', upd_par_name='phone', key_par_name=message.text, upd_column_name='from_user_id', key_column_name=message.from_user.id)
        db_users.upd_element_in_column(table_name='users', upd_par_name='lid', key_par_name='true', upd_column_name='from_user_id', key_column_name=message.from_user.id)
        bot.send_message(chat_id=message.from_user.id, text=msg.success_voronka_msg,reply_markup=keybords.back())
        res = db_users.find_elements_in_column(table_name='users', key_name=message.from_user.id, column_name='from_user_id')
        res = res[0]
        text = f"""
Дата {get_msk_time()}
ID {res[0]}
Клиент @{res[1]}
Категория {res[7]}
Тел.: {res[8]}
"""
        bot.send_message(chat_id=GROUP_SPEC, text=text)
      
    
    def input_push(message):
        res = db_users.find_elements_in_column(table_name='admins', key_name=message.from_user.id, column_name='from_user_id')
        res = res[0]
        type_push = res[3]
        query = '111'
        connection = som.create_connection('users.db')
        if type_push == 'all':
            query = f"""
            SELECT from_user_id FROM users 
            """
        elif type_push == 'no_lid':
            query = f"""
            SELECT from_user_id FROM users WHERE lid = 'false'
            """
        print(query)
        all_records_users = pd.read_sql_query(query, connection)
        print(all_records_users)
        connection.close()
        list_of_users = []
        for i in all_records_users['from_user_id']:
            list_of_users.append(i)
        print(list_of_users)
        count = 0
        for user_id in list_of_users:
            try:
                bot.send_message(chat_id=user_id, text=message.text)
                time.sleep(0.15)
                count+=1
            except Exception as ex:
                
                bot.send_message(chat_id=message.from_user.id, text=f"{user_id} failed")
                time.sleep(0.15)
        bot.send_message(chat_id=message.from_user.id, text=f"Рассылка закончена, успешно отправлено {count} шт.")
        db_users.upd_element_in_column(table_name='admins', upd_par_name='push_msg', key_par_name=message.text, upd_column_name='from_user_id', key_column_name=message.from_user.id)
    
    def get_otziv_screen(message):    # пересылка скрина отзыва
        res = db_users.find_elements_in_column(table_name='users', key_name=message.from_user.id, column_name='from_user_id')
        res = res[0]
        foto = message.photo[len(message.photo) - 1].file_id
        file_info = bot.get_file(foto)
        photo = bot.download_file(file_info.file_path)
        text = f"""
Дата {get_msk_time()}
ID {res[0]}
Клиент @{res[1]}
Категория {res[7]}
Отправил скриншот отзыва
        """
        bot.send_photo(chat_id=GROUP_SPEC, photo=photo, caption=text)
        m = bot.send_message(chat_id=message.from_user.id, text=msg.kupon_screen_msg)
        bot.register_next_step_handler(m, get_kupon_screen)

    def get_kupon_screen(message):
        res = db_users.find_elements_in_column(table_name='users', key_name=message.from_user.id, column_name='from_user_id')
        res = res[0]
        foto = message.photo[len(message.photo) - 1].file_id
        file_info = bot.get_file(foto)
        photo = bot.download_file(file_info.file_path)
        text = f"""
Дата {get_msk_time()}
ID {res[0]}        
Клиент @{res[1]}
Категория {res[7]}
Отправил скриншот купона
        """
        bot.send_photo(chat_id=GROUP_SPEC, photo=photo, caption=text)
        m = bot.send_message(chat_id=message.from_user.id, text=msg.input_phone_msg)
        bot.register_next_step_handler(m, get_phone)
    bot.infinity_polling()

if __name__ == "__main__":
    main()

    