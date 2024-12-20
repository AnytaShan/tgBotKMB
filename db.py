from aiogram.types import InlineKeyboardButton
import mysql.connector as con

connection = con.connect(
    host='localhost',
    user='root',
    password='q1w2e3r4t5y6',
    database='STYDENTS'
)


cursor = connection.cursor(buffered=True)


def get_groups():
      # Выводим из бд список всех групп
      groups = []
      cursor.execute("SELECT GroupsName, GroupsId FROM `Groups`")
      for row in cursor.fetchall():
            group_name = row[0]
            group_id = str(row[1])
            groups.append(InlineKeyboardButton(text = group_name, callback_data = f"group_{group_id}")) # добавиль текст для поиска
      return groups


def get_students(group_id):
      # Выводим список студентов из выбранной группы
      student = []
      cursor.execute(f"SELECT CONCAT(StudentLastName, ' ', StudentName) AS FullName FROM Students WHERE GroupsID = {group_id}")
      for row in cursor.fetchall():
            student_name = row[0]
            student.append(InlineKeyboardButton(text = student_name, callback_data = f"student_{student_name}"))
      student.append(InlineKeyboardButton(text='Назад⬅', callback_data='student_000'))
      return student

 
def telegram_id(telegram_id, student_name):
      # присваеваем TelegramId выбраннаму студенту
      cursor.execute(f"UPDATE Students SET TelegramId = {telegram_id} WHERE CONCAT(StudentLastName,' ',StudentName) = '{student_name}'")
      connection.commit()

def group_id(student_name):
      #возвращаем id группы студента, от подтверждения которого отказались
      cursor.execute(f"select GroupsId from `Students` WHERE CONCAT(StudentLastName,' ',StudentName) = '{student_name}'")
      for row in cursor.fetchall():
           return row[0]

def get_menu(DayOfTheWeekId):
      # Выводим список блюд на сегодняшний день
      dishes = []
      cursor.execute(f"""SELECT Dishes.DishesName, Dishes.DishesId AS DishesId, Menu.DishesId AS MenuDishesId FROM `Menu` 
      JOIN Dishes ON Dishes.DishesId = Menu.DishesId WHERE DayOfTheWeekId = {DayOfTheWeekId}""")
      for row in cursor.fetchall():
            dishes_name = row[0]
            dishes_id = int(row[1])
            dishes.append(InlineKeyboardButton(text = dishes_name, callback_data = f"dishes_{dishes_id}"))

      return dishes

def chat_id():
      # Достаём список зарегестрированных в базе данных ID для рассылки
      chat_id = []
      cursor.execute("SELECT TelegramId FROM `Students` WHERE TelegramId IS NOT NULL'")
      for row in cursor.fetchall():
            chat_id.append(row[0])
  
      return chat_id

def get_selection(student_id, dishes_id, DayOfTheWeek_id):
      # записываем выбранное студентом блюдо
      cursor.execute(f"INSERT INTO Selection (StudentsId, DishesId, DayOfTheWeekId) VALUES ({student_id}, {dishes_id}, {DayOfTheWeek_id})")
      connection.commit()


def chat_student_id(telegram_id):
      # находим индекс студента исходя из его Telegram Id
      cursor.execute(f"Select StudentId From `Students` Where TelegramId = {telegram_id}")
      for row in cursor.fetchall():
           return row[0]

      
def examination_start(user_id):
      # проверяем, нет ли этого TelegramId в бд
      cursor.execute(f"SELECT EXISTS(SELECT TelegramId FROM `Students` WHERE TelegramId = {user_id})")
      for row in cursor.fetchall():
            return row[0]


def examination_student(student_name):
      # проверяем, нет ли этого студента уже в бд
      cursor.execute(f"select EXISTS(SELECT TelegramId FROM Students WHERE CONCAT(StudentLastName,' ',StudentName) = '{student_name}' And TelegramId IS Null)")
      for row in cursor.fetchall():
            return row[0]  
        

def delete_old_selections(DayOfTheWeek_id):
    # Удаляем записи, которым больше двух дней
      if DayOfTheWeek_id == 1:
          cursor.execute(f"DELETE FROM Selection WHERE DayOfTheWeekId != {DayOfTheWeek_id} AND DayOfTheWeekId != 10")
          
      elif DayOfTheWeek_id == 6:
          cursor.execute(f"DELETE FROM Selection WHERE DayOfTheWeekId != {DayOfTheWeek_id} AND DayOfTheWeekId != {DayOfTheWeek_id}-1")
