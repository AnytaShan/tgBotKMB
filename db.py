import sqlite3
from aiogram.types import InlineKeyboardButton

connection = sqlite3.connect('sqlite.db')
cursor = connection.cursor()


def get_groups():
      # Выводим из бд список всех групп
      groups = []
      for row in connection.execute("SELECT GroupsName, GroupsId FROM Groups"):
            group_name = row[0]
            group_id = str(row[1])
            groups.append(InlineKeyboardButton(text = group_name, callback_data = f"group_{group_id}")) # добавиль текст для поиска 
      return groups


def get_students(group_id):
      # Выводим список студентов из выбранной группы
      student = []
      for row in connection.execute(f"SELECT StudentLastName || ' ' || StudentName AS FullName FROM Students WHERE GroupsID = {group_id}"):
            student_name = row[0]
            student.append(InlineKeyboardButton(text = student_name, callback_data = f"student_{student_name}"))
      student.append(InlineKeyboardButton(text='Назад⬅', callback_data='student_000'))
      return student
 
def group_id(student_name):
      #возвращаем id группы студента, от подтверждения которого отказались
      cursor.execute(f"select GroupsId from Students WHERE StudentLastName || ' ' || StudentName = '{student_name}'")
      for row in cursor.fetchall():
           return row[0]

def telegram_id(telegram_id, student_name):
      # присваеваем TelegramId выбраннаму студенту
      cursor.execute(f"UPDATE Students SET TelegramId = {telegram_id} WHERE StudentLastName || ' ' || StudentName = '{student_name}'")
      connection.commit()


def get_menu(DayOfTheWeekId):
      # Выводим список блюд на сегодняшний день
      dishes = []
      for row in connection.execute(f"""SELECT Dishes.DishesName, Dishes.DishesId AS DishesId, Menu.DishesId AS MenuDishesId FROM Menu 
      JOIN Dishes ON Dishes.DishesId = Menu.DishesId WHERE DayOfTheWeekId = {DayOfTheWeekId}"""):
            dishes_name = row[0]
            dishes_id = int(row[1])
            dishes.append(InlineKeyboardButton(text = dishes_name, callback_data = f"dishes_{dishes_id}"))
      return dishes


def chat_id():
      # Достаём список зарегестрированных в базе данных ID для рассылки
      chat_id = []
      for row in connection.execute("SELECT TelegramId FROM Students WHERE TelegramId IS NOT NULL"):
            chat_id.append(row[0])
      return chat_id


def get_selection(student_id, dishes_id, DayOfTheWeek_id):
      # записываем выбранное студентом блюдо
      cursor.execute(f"INSERT INTO Selection (StudentsId, DishesId, DayOfTheWeekId) VALUES ({student_id}, {dishes_id}, {DayOfTheWeek_id})")
      connection.commit()


def chat_student_id(telegram_id):
      # находим индекс студента исходя из его Telegram Id
      for row in connection.execute(f"Select StudentId From Students Where TelegramId = {telegram_id}"):
           return row[0]
      
      
def examination_start(user_id):
      # проверяем, нет ли этого TelegramId в бд
      for row in connection.execute(f"SELECT EXISTS(SELECT TelegramId FROM Students WHERE TelegramId = {user_id})"):
            return row[0]


def examination_student(student_name):
      # проверяем, нет ли этого студента уже в бд
      for row in connection.execute(f"select EXISTS(SELECT TelegramId FROM Students WHERE StudentLastName || ' ' || StudentName = '{student_name}' And TelegramId IS Null)"):
            return row[0]       


def delete_old_selections(DayOfTheWeek_id):
    # Удаляем записи, которым больше двух дней
      if DayOfTheWeek_id == 1:
            cursor.execute(f"DELETE FROM Selection WHERE DayOfTheWeekId != {DayOfTheWeek_id} AND DayOfTheWeekId != 10")
      elif DayOfTheWeek_id == 6:
          cursor.execute(f"DELETE FROM Selection WHERE DayOfTheWeekId != {DayOfTheWeek_id} AND DayOfTheWeekId != {DayOfTheWeek_id}-1")
      connection.commit()


def get_admin(user_id):
      for row in connection.execute(f"select EXISTS(Select * From Admin where AdminId = {user_id})"):
            return row[0]


def admin_id():
      # Достаём список зарегестрированных в базе данных ID админов для рассылки
      admin_id = []
      for row in connection.execute("Select AdminId From Admin"):
            admin_id.append(row[0])
      return admin_id

def dish_coincidence(DayOfTheWeek_id, DishesName):
      for row in cursor.execute(f"SELECT COUNT(s.DishesId) FROM Selection s JOIN Dishes d ON s.DishesId = d.DishesId WHERE s.DayOfTheWeekId = {DayOfTheWeek_id} AND d.DishesName = '{DishesName}'"):
          return row[0]
      

def admin_info(group_id, data):
      # Выводим список студентов из выбранной группы
      group_admin = []
      for row in connection.execute(f"""SELECT 
                                          s.StudentLastName,
                                          CASE 
                                              WHEN sel.StudentsId IS NULL THEN 'не проголосовал❌'
                                              WHEN sel.DishesId = 0 THEN 'не будет обедать'
                                              ELSE 'проголосовал✅'
                                          END AS VoteStatus
                                    FROM 
                                          Students s
                                    LEFT JOIN 
                                          Selection sel ON s.StudentId = sel.StudentsId AND sel.DayOfTheWeekId = {data}
                                    WHERE 
                                          s.GroupsID = {group_id}
                                    ORDER BY 
                                          s.StudentLastName, s.StudentName;"""):
            group_name = str(row[0])
            group_status = str(row[1])
            group_admin.append(f"{group_name} --- {group_status}")  # Используем append вместо +=
      return group_admin
