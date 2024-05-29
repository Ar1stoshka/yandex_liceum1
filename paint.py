import sys
import hashlib
import sqlite3
import res
import res1
import res2
import res3
import res4
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction,\
    QFileDialog, QColorDialog, QInputDialog, QWidget, QLineEdit
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtCore import Qt


global_var = globals()  # место, где будем хранить имя пользователя, для отображения аккаунта
con = sqlite3.connect("users.db")  # подключаем базу данных
cursor = con.cursor()
a = ord('а')
rus_alphabet = ''.join([chr(i) for i in range(a, a + 6)] + [chr(a + 33)] + [chr(i) for i in range(a + 6, a + 32)])

cursor.execute('''CREATE TABLE IF NOT EXISTS users_data(
    id INTEGER primary key autoincrement,
    username TEXT,
    password TEXT
)''')  # создаем таблицу в бд, если она не существует
con.commit()


class NewUsername(QWidget):  # класс, отвечающий за смену никнейма пользователя
    def __init__(self):
        super().__init__()
        self.setFixedSize(380, 280)
        self.setWindowTitle('Picasso in your pocket')
        uic.loadUi('change_username.ui', self)
        self.pushButton_3.setStyleSheet("appearance: none;"
                                        "border: 0;"
                                        "border-radius: 5px;"
                                        "background: #61948c;"
                                        "color: #fff;"
                                        "padding: 8px 16px;")
        self.pushButton_3.clicked.connect(self.new_username)

    def new_username(self):  # метод, переписывающий данные в бд, если соблюдены условия
        username = self.lineEdit_3.text()  # получаем никнейм,
        # на который пользователь хочет поменять свой текущий никнейм
        if len(username) == 0:
            self.label_9.setText("Required fields are missing")
            return
        data = list(cursor.execute("SELECT username, password FROM users_data").fetchall())
        for i in data:
            if i[0] == username and i[-1] != hashlib.md5(PaintApp().pw.encode()).hexdigest():
                self.label_9.setText("This username is taken")
                return
        query = "UPDATE users_data SET username = ? WHERE password = ?"
        s = (username, hashlib.md5(PaintApp().pw.encode()).hexdigest())
        cursor.execute(query, s)
        con.commit()  # перезаписываем данные
        self.label_9.setText("Username successfully updated")  # оповещаем пользователя, что все прошло успешно


class CheckPassword(QWidget):  # класс, отвечающий за проверку пароля, при входе в настройки аккаунта
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 270)
        self.setWindowTitle('Picasso in your pocket')
        uic.loadUi('check_password.ui', self)
        self.lineEdit_3.setEchoMode(QLineEdit.Password)
        self.pushButton_4.clicked.connect(self.checker)
        self.pushButton_3.clicked.connect(self.show_hide_password)
        self.c = 1
        self.pushButton_4.setStyleSheet("appearance: none;"
                                        "border: 0;"
                                        "border-radius: 5px;"
                                        "background: #61948c;"
                                        "color: #fff;"
                                        "padding: 8px 16px;")

    def show_hide_password(self):  # метод, отвечающий за скрытие пароля
        if self.c % 2 != 0:
            self.lineEdit_3.setEchoMode(QLineEdit.Normal)
            self.c += 1
            return
        if self.c % 2 == 0:
            self.lineEdit_3.setEchoMode(QLineEdit.Password)
            self.c += 1

    def checker(self):  # метод проверки введенного пароля
        data = list(cursor.execute("SELECT password FROM users_data WHERE username = ?",
                                   (PaintApp().user_name, )))
        password = self.lineEdit_3.text()
        if data[0][0] == hashlib.md5(password.encode()).hexdigest():
            self.w1 = Settings()
            self.w1.show()
            self.close()
        self.label_14.setText("Wrong password")  # оповещение пользователя, что пароль неверный


class Settings(QWidget):  # класс, отвечающий за настройки аккаунта
    def __init__(self):
        super().__init__()
        self.setFixedSize(478, 478)
        self.setWindowTitle('Picasso in your pocket')
        uic.loadUi('settings.ui', self)
        self.c = 1
        self.pushButton.setStyleSheet("appearance: none;"
                                      "border: 0;"
                                      "border-radius: 5px;"
                                      "background: #4a5d8b;"
                                      "color: #fff;"
                                      "padding: 8px 16px;")
        self.lineEdit_2.setEchoMode(QLineEdit.Password)  # устанавливаем мод пароля, чтобы введенные данные
        # отображались скрытно
        self.lineEdit.setText(PaintApp().user_name)
        self.lineEdit_2.setText(PaintApp().pw)
        self.pushButton_2.clicked.connect(self.show_hide)
        self.pushButton.clicked.connect(self.change_username)
        self.label_7.setText(PaintApp().user_name)

    def show_hide(self):  # метод, отвечающий за скрытие пароля
        if self.c % 2 != 0:
            self.lineEdit_2.setEchoMode(QLineEdit.Normal)
            self.c += 1
            return
        if self.c % 2 == 0:
            self.lineEdit_2.setEchoMode(QLineEdit.Password)
            self.c += 1

    def change_username(self):  # метод, вызывающий окно другого класса
        self.w = NewUsername()
        self.w.show()
        self.close()


class ForgetPassword(QWidget):  # класс, отвечающий за смену пароля
    def __init__(self):
        super().__init__()
        self.setFixedSize(892, 559)
        self.setWindowTitle('Picasso in your pocket')
        uic.loadUi('forget_password.ui', self)
        self.c2 = 1
        self.c3 = 1  # счетчики, отвечающие за нажатие/отжатие кнопки скрытия/показа пароля
        self.pushButton_5.setStyleSheet("appearance: none;"
                                        "border: 0;"
                                        "border-radius: 5px;"
                                        "background: #619ea8;"
                                        "color: #fff;"
                                        "padding: 8px 16px;")
        self.pushButton_6.setStyleSheet("appearance: none;"
                                        "border: 0;"
                                        "border-radius: 5px;"
                                        "background: #ce9c5b;"
                                        "color: #fff;"
                                        "padding: 8px 16px;")
        self.pushButton_6.clicked.connect(self.back)
        self.pushButton_5.clicked.connect(self.update_password)
        self.pushButton_7.clicked.connect(self.show_hide_password1)
        self.pushButton_8.clicked.connect(self.show_hide_password2)  # присоединение методов к кнопкам
        self.lineEdit.setPlaceholderText('Username')
        self.lineEdit_2.setPlaceholderText('Password')
        self.lineEdit_3.setPlaceholderText('Confirm password')  # установили текстовые подсказки для пользователя
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.lineEdit_3.setEchoMode(QLineEdit.Password)
        # установили вид написания символов в lineEdit - пароль, чтобы данные отображались скрытно

    def show_hide_password1(self):  # метод, отвечающий за то, показывать или скрывать пароль для 1 строки
        if self.c2 % 2 != 0:
            self.lineEdit_2.setEchoMode(QLineEdit.Normal)
            self.c2 += 1
            return
        if self.c2 % 2 == 0:
            self.lineEdit_2.setEchoMode(QLineEdit.Password)
            self.c2 += 1

    def show_hide_password2(self):  # метод, отвечающий за то, показывать или скрывать пароль для 2 строки
        if self.c3 % 2 != 0:
            self.lineEdit_3.setEchoMode(QLineEdit.Normal)
            self.c3 += 1
            return
        if self.c3 % 2 == 0:
            self.lineEdit_3.setEchoMode(QLineEdit.Password)
            self.c3 += 1

    def back(self):  # метод, отвечающий за возварещние на страницу входа в аккаунт
        self.w1 = Entrance()
        self.w1.show()
        self.close()

    def update_password(self):  # метод, обновляющий пароль пользоваетля
        username = self.lineEdit.text()
        pw1 = self.lineEdit_2.text()
        pw2 = self.lineEdit_3.text()  # получаем данные, которые ввел пользователь
        data = cursor.execute("SELECT username FROM users_data").fetchall()
        if len(username) == 0 or len(pw1) == 0 or len(pw2) == 0:  # если какое либо поле не заполнено
            self.label_7.setText("Required fields are missing")
            return
        if (username, ) not in data:  # если нет аккаунта
            self.label_7.setText("No such user, create an account")
            return
        if pw1 != pw2:  # если пароль неверный
            self.label_7.setText("Passwords don't match")
            return
        for i in pw1:
            if i in rus_alphabet or i in "/@'><|%;`~":  # если пароль содержит недопустимые символы
                self.label_7.setText("Invalid characteres in the password")
                return
        if len(pw1) < 5:
            self.label_7.setText("Password is too short. Min: 5 symb.")
            return
        if (username, ) in data:  # если все успешно
            query = "UPDATE users_data SET password = ? WHERE username = ?"  # обновляем данные пользователя в БД
            s = (hashlib.md5(pw1.encode()).hexdigest(), username)
            cursor.execute(query, s)
            con.commit()
            self.label_7.setText("Password successfully updated")


class SignUp(QWidget):  # класс, отвечающий за регистрацию пользователя
    def __init__(self):
        super().__init__()
        self.setFixedSize(892, 559)
        uic.loadUi('signup.ui', self)
        self.c2 = 1
        self.c4 = 1  # счетчики для кнопок, отвечающих за показ пароля
        self.pushButton_4.clicked.connect(self.back_to_registration)
        self.pushButton_3.setStyleSheet("appearance: none;"
                                        "border: 0;"
                                        "border-radius: 5px;"
                                        "background: #b86d41;"
                                        "color: #fff;"
                                        "padding: 8px 16px;")
        self.pushButton_4.setStyleSheet("appearance: none;"
                                        "border: 0;"
                                        "border-radius: 5px;"
                                        "background: #8f3a24;"
                                        "color: #fff;"
                                        "padding: 8px 16px;")
        self.pushButton_3.clicked.connect(self.sign_up)
        self.lineEdit.setPlaceholderText('Username')
        self.lineEdit_2.setPlaceholderText('Password')  # подсказки для пользователей
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.lineEdit_4.setPlaceholderText('Confirm password')  # подсказкa для пользователей
        self.lineEdit_4.setEchoMode(QLineEdit.Password)
        self.pushButton.clicked.connect(self.show_hide_password1)
        self.pushButton_2.clicked.connect(self.show_hide_password2)

    def show_hide_password1(self):  # метод, отвечающий за показ/скрытие данных
        if self.c2 % 2 != 0:
            self.lineEdit_2.setEchoMode(QLineEdit.Normal)
            self.c2 += 1
            return
        if self.c2 % 2 == 0:
            self.lineEdit_2.setEchoMode(QLineEdit.Password)
            self.c2 += 1

    def show_hide_password2(self):  # метод, отвечающий за показ/скрытие данных
        if self.c4 % 2 != 0:
            self.lineEdit_4.setEchoMode(QLineEdit.Normal)
            self.c4 += 1
            return
        if self.c4 % 2 == 0:
            self.lineEdit_4.setEchoMode(QLineEdit.Password)
            self.c4 += 1

    def sign_up(self):  # метод, отвечающий за регистрацию пользователя
        self.user_name = self.lineEdit.text()
        self.pw1 = self.lineEdit_2.text()
        self.pw2 = self.lineEdit_4.text()  # получение данных от пользователя
        data = cursor.execute("SELECT username, password FROM users_data").fetchall()
        if len(self.user_name) == 0 or len(self.pw1) == 0 or len(self.pw2) == 0:  # если какое-либо из полей пропущено
            self.label_5.setText("Required fields are missing")
            return
        if (self.user_name, hashlib.md5(self.pw1.encode()).hexdigest(), ) in data:  # если пароль и никнейм уже в БД
            self.label_5.setText("You already have an account")
            return
        if len(self.pw1) < 5:
            self.label_5.setText("Password is too short. Min: 5 symb.")  # если пароль слишком короткий
            return
        if self.pw1 != self.pw2:
            self.label_5.setText("Passwords don't match")  # если пользователь не смог ввести два одинаковых пароля
            return
        for i in data:
            if i[0] == self.user_name and i[1] != hashlib.md5(self.pw1.encode()).hexdigest():
                self.label_5.setText("This username is already taken")  # если такой никнейм уже есть в БД
                return
        for i in self.pw1:
            if i in rus_alphabet or i in "/@'><|%;`~":  # если пароль содержит недопустимые символы
                self.label_5.setText("Invalid characteres in the password")
                return
        cursor.execute("INSERT INTO users_data (username, password) VALUES (?, ?)",
                       (self.user_name, hashlib.md5(self.pw1.encode()).hexdigest()))
        self.label_5.setText("Account successfully created")  # если все критерии по регистрации не вызвали нариканий
        con.commit()

    def back_to_registration(self):  # метод, отвечающий за возвращение на экран входа в аккаунт
        self.w2 = Entrance()
        self.w2.show()
        self.close()


class Entrance(QMainWindow):  # класс, отвечающий за вход в аккаунт
    def __init__(self):
        super().__init__()
        self.setFixedSize(900, 570)
        uic.loadUi('entrance.ui', self)
        self.counter = 1

        self.pushButton.setStyleSheet("appearance: none;"
                                      "border: 0;"
                                      "border-radius: 5px;"
                                      "background: #5d7b74;"
                                      "color: #fff;"
                                      "padding: 8px 16px;")

        self.pushButton_2.setStyleSheet("appearance: none;"
                                        "border: 0;"
                                        "border-radius: 5px;"
                                        "background: #69a9bd;"
                                        "color: #fff;"
                                        "padding: 8px 16px;")

        self.pushButton_3.setStyleSheet("appearance: none;"
                                        "border: 0;"
                                        "border-radius: 5px;"
                                        "background: #a56352;"
                                        "color: #fff;"
                                        "padding: 8px 16px;")  # дизайн кнопок
        self.lineEdit.setPlaceholderText('Username')
        self.lineEdit_2.setPlaceholderText('Password')  # подсказки для пользователя
        self.lineEdit_2.setEchoMode(QLineEdit.Password)  # делаем вводимые данные скрытыми
        self.pushButton_2.clicked.connect(self.signin)
        self.pushButton.clicked.connect(self.log_in)
        self.pushButton.setShortcut("Return")
        self.pushButton_5.clicked.connect(self.hide_show_password)
        self.pushButton_3.clicked.connect(self.forget_password)

    def forget_password(self):  # метод, вызывающий класс, которые реализует смену пароля
        self.w4 = ForgetPassword()
        self.w4.show()
        self.close()

    def hide_show_password(self):  # метод, отвечающий за показ/скрытие пароля
        if self.counter % 2 != 0:
            self.lineEdit_2.setEchoMode(QLineEdit.Normal)
            self.counter += 1
            return
        if self.counter % 2 == 0:
            self.lineEdit_2.setEchoMode(QLineEdit.Password)
            self.counter += 1

    def signin(self):  # метод, вызывающий класс регистрации
        self.w3 = SignUp()
        self.w3.show()
        self.close()

    def log_in(self):  # метод, отвечающий за вход в аккаунт
        self.username = self.lineEdit.text()
        self.password = self.lineEdit_2.text()  # получение данных пользователя
        if len(self.username) == 0 or len(self.password) == 0:
            self.label_4.setText("required fields are missing")  # если какое либо поле пропущено
            return
        data = cursor.execute("SELECT username, password FROM users_data").fetchall()
        if (self.username, hashlib.md5(self.password.encode()).hexdigest(), ) in data:
            global_var['hackish_global_var'] = (self.username, self.password)  # если все успешно, переходим в окно
            # рисования
            self.w2 = PaintApp()
            self.w2.show()
            self.close()
            return
        data = cursor.execute("SELECT password FROM users_data WHERE username = ?",
                              (self.username,)).fetchall()
        if not data:  # если никнейм не найдет в ДБ
            self.label_4.setText("No such user, create an account")
            return
        for i in data:
            if i[0] != hashlib.md5(self.password.encode()).hexdigest():
                self.label_4.setText("Wrong password")  # если пароль не совпадает с верным


class PaintApp(QMainWindow):  # класс, реализующий окно для рисования
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Picasso-in-your-pocket")
        self.setFixedSize(1000, 950)
        uic.loadUi('paint.ui', self)
        self.size = self.label.size()
        self.label_3 = self.label_3
        self.def_color = Qt.black
        self.prev_color = Qt.black  # устанавливаем цвета, которые пригодятся нам в работе с реализацией ластика
        self.counter = 1
        self.color = Qt.white
        canvas = QPixmap(self.size)  # создание места для рисования
        canvas.fill(self.color)
        self.label.setPixmap(canvas)
        self.last_x, self.last_y = None, None  # координаты мышки
        self.er = False
        self.user_name = global_var['hackish_global_var'][0]  # в переменные записываем текущие данные пользователя
        self.pw = global_var['hackish_global_var'][1]
        self.label_3.setText(self.user_name)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.brush_color = Qt.black
        self.brush_size = 6

        self.pushButton.setStyleSheet("appearance: none;"
                                      "border: 0;"
                                      "border-radius: 5px;"
                                      "background: #a83f48;"
                                      "color: #fff;"
                                      "padding: 8px 16px;")
        self.pushButton_2.setStyleSheet("appearance: none;"
                                        "border: 0;"
                                        "border-radius: 5px;"
                                        "background: #567ea2;"
                                        "color: #fff;"
                                        "padding: 8px 16px;")
        self.pushButton_2.clicked.connect(self.chose_color)
        self.pushButton_3.setStyleSheet("appearance: none;"
                                        "border: 0;"
                                        "border-radius: 5px;"
                                        "background: #6c9c83;"
                                        "color: #fff;"
                                        "padding: 8px 16px;")
        self.pushButton_3.clicked.connect(self.chose_size)
        self.pushButton_4.clicked.connect(self.eraser)
        self.pushButton_5.setStyleSheet("appearance: none;"
                                        "border: 0;"
                                        "border-radius: 5px;"
                                        "background: #66a7b0;"
                                        "color: #fff;"
                                        "padding: 8px 16px;")
        self.pushButton_6.setStyleSheet("background-color: #86c0c0;"
                                        "color: black;"
                                        "border-radius: 5px")
        self.pushButton_6.clicked.connect(self.select_photo)
        self.pushButton_7.setStyleSheet("background-color: #ea7761;"
                                        "color: black;"
                                        "border-radius: 5px")
        self.pushButton_7.clicked.connect(self.remove_photo)
        self.pushButton_5.clicked.connect(self.sheet_color)
        self.pushButton.clicked.connect(self.exit_from_account)
        self.pushButton_8.clicked.connect(self.settings)
        self.create_menu()

    def settings(self):  # открытие другого окна - настроек
        self.win1 = CheckPassword()
        self.win1.show()

    def exit_from_account(self):  # открытие другого окна, возвращение на страницу входа в аккаунт
        self.win = Entrance()
        self.win.show()
        self.close()

    def remove_photo(self):  # метод, привязанный к кнопке, убирающей фото для срисовывания
        self.label_5.clear()

    def select_photo(self):  # метод, привязанный к кнопке, отвечающей за выбор фото для срисовывания
        fname = QFileDialog.getOpenFileName(self, 'Select a photo', '')[0]
        self.pm = QPixmap(fname)
        self.label_5.setPixmap(self.pm)
        self.label_5.setScaledContents(True)

    def sheet_color(self):  # метод, привязанный к кнопке, отвечающей за смерну цвета листа
        new_color = QColorDialog.getColor()  # выбор нового цвета
        if new_color.isValid() and self.er:
            self.color = new_color  # установка этого цвета
            self.brush_color = self.color
            canvas = QPixmap(self.size)
            canvas.fill(self.color)
            self.label.setPixmap(canvas)
        if new_color.isValid() and not self.er:
            self.color = new_color
            self.brush_color = self.prev_color
            canvas = QPixmap(self.size)
            canvas.fill(self.color)
            self.label.setPixmap(canvas)

    def eraser(self):  # метод, привязанный к кнопке ластика
        self.er = True
        if self.counter % 2 != 0:
            self.brush_color = self.color  # меняем цвет кисти на цвет фона
            self.label_4.setText("Selected: eraser")
        else:
            self.er = False
            self.brush_color = self.def_color  # меняем цвет кисти на цвет, который был до нажатия на ластик
            self.label_4.setText("Selected: pen")
        self.counter += 1

    def chose_size(self):  # метод, привязанный к кнопке, отвечающей за выбор толщины кисти
        new_size, ok = QInputDialog.getInt(self, "Brush Size", "Enter the size:", self.brush_size,
                                           min=1, max=50)
        if ok:
            self.brush_size = new_size

    def chose_color(self):  # метод, привязанный к кнопке, отвечающей за выбор цвета кисти
        new_color = QColorDialog.getColor()
        if new_color.isValid():
            self.prev_color = new_color
            self.brush_color = new_color
            self.def_color = self.brush_color

    def create_menu(self):  # метод, создающий меню бар
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu("File")
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_image)
        file_menu.addAction(save_action)
        clear_action = QAction("Clear", self)
        clear_action.setShortcut("Ctrl+C")
        clear_action.triggered.connect(self.clear_image)
        file_menu.addAction(clear_action)  # добавление кнопок сохранить и очистить в меню

    def save_image(self):  # метод, сохраняющий нарисованное
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                   "PNG(*.png);;JPEG(*.jpg *.jpeg)")
        if file_path == "":
            return
        self.label.pixmap().save(file_path)

    def clear_image(self):  # метод, очищающий канву
        canvas = QPixmap(self.size)
        canvas.fill(self.color)
        self.label.setPixmap(canvas)

    def mouseMoveEvent(self, e):  # метод, отвечающий за передвижения мыши
        deltaX = self.centralWidget().x() + self.label.x()
        deltaY = self.centralWidget().y() + self.label.y()
        if self.last_x is None:
            self.last_x = e.x() - deltaX
            self.last_y = e.y() - deltaY
            return
        painter = QPainter(self.label.pixmap())  # создание пэинтера
        p = QPen(self.brush_color, self.brush_size, Qt.SolidLine)
        painter.setPen(p)  # установка кисти
        painter.drawLine(self.last_x, self.last_y, e.x() - deltaX, e.y() - deltaY)  # процесс рисования
        painter.end()
        self.update()
        self.last_x = e.x() - deltaX
        self.last_y = e.y() - deltaY  # вычисление координат остановки мыши

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Entrance()
    window.show()
    sys.exit(app.exec_())