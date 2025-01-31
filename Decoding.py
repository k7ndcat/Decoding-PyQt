import sys
import sqlite3
from PyQt6.QtWidgets import QVBoxLayout, QStackedWidget, QMessageBox
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QLineEdit, QFileDialog, QLabel
from PyQt6.QtGui import QIntValidator, QImage, QColor
import random

crypt_path = ""
ref_path = ""
text_path = ""
image_crypt = None
mode = 1


def make_key(start, factor, len_of_text):
    return [start + factor * i for i in range(len_of_text)]


def text_to_bin(symbol, keys=1):  # перевод в бинарный код, с расчётом на замену в rgb
    global text_bin
    for i in symbol:
        text_bin.append(format(ord(i) + keys, '12b').replace(' ', '0'))


def create_data_base(self, login, password, database='Login_Password.db'):
    conn = sqlite3.connect(database)
    cr = conn.cursor()
    cr.execute('''
         CREATE TABLE IF NOT EXISTS users (
              Id INTEGER PRIMARY KEY AUTOINCREMENT,
              Name TEXT
         )
     ''')
    cr.execute('''
              CREATE TABLE IF NOT EXISTS passwords (
                  Id INTEGER PRIMARY KEY AUTOINCREMENT,
                  Password TEXT
              )
          ''')
    cr.execute('INSERT INTO Users (Name) VALUES (?)', (login,))
    cr.execute('INSERT INTO passwords (Password) VALUES (?)', (password,))
    conn.commit()
    conn.close()


class TextInImageApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # Инициализация интерфейса
    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('k1ndcat')

        # Создаем QStackedWidget
        self.stacked_widget = QStackedWidget()

        # Создаем слой входа
        self.login_layer = self.create_login_layer()
        # Создаем второй слой (основной интерфейс)
        self.main_layer = self.create_main_layer()

        # Добавляем слои в стек
        self.stacked_widget.addWidget(self.login_layer)
        self.stacked_widget.addWidget(self.main_layer)

        # Устанавливаем стек как центральный виджет
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    def create_login_layer(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.username_label = QLabel('Username:', self)
        layout.addWidget(self.username_label)

        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_input)

        self.password_label = QLabel('Password:', self)
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit(self)

        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Скрыть ввод пароля

        layout.addWidget(self.password_input)

        self.login_button = QPushButton('Sign up', self)
        self.login_check = QPushButton('Sign in', self)
        self.login_button.clicked.connect(self.handle_login)
        self.login_check.clicked.connect(self.chek_login)

        layout.addWidget(self.login_button)
        layout.addWidget(self.login_check)

        widget.setLayout(layout)
        return widget

    def handle_login(self):
        login = self.username_input.text()
        password = self.password_input.text()
        create_data_base(self, login, password)

        # Здесь можно добавить проверку имени пользователя и пароля
        if login and password:  # Простейшая проверка
            self.stacked_widget.setCurrentIndex(1)  # Переход к основному слою

    def chek_login(self):
        login = self.username_input.text()
        password = self.password_input.text()
        create_data_base(self, login, password)

    def create_main_layer(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.load_ref_btn = QPushButton('LOAD IMAGE', self)
        self.load_ref_btn.clicked.connect(self.load_ref)
        layout.addWidget(self.load_ref_btn)

        self.load_text_btn = QPushButton('LOAD TEXT', self)
        self.load_text_btn.clicked.connect(self.load_text)
        layout.addWidget(self.load_text_btn)

        self.load_crypt_btn = QPushButton('LOAD CRYPT IMAGE', self)

        self.load_crypt_btn.clicked.connect(self.load_crypt)
        layout.addWidget(self.load_crypt_btn)

        self.key_field = QLineEdit(self)
        self.key_field.setPlaceholderText("Enter key")
        layout.addWidget(self.key_field)

        # Поле для ввода номера режима с ограничением на ввод целых чисел
        self.mode_input = QLineEdit(self)
        self.mode_input.setPlaceholderText("Enter mode number (1 or 2)")

        # Устанавливаем валидатор для ввода только чисел от 1 до 2
        validator = QIntValidator(1, 2, self.mode_input)
        self.mode_input.setValidator(validator)

        layout.addWidget(self.mode_input)

        # Кнопка для выбора режима
        self.select_mode_btn = QPushButton('SELECT MODE', self)
        self.select_mode_btn.clicked.connect(self.select_mode)
        layout.addWidget(self.select_mode_btn)

        self.encrypt_btn = QPushButton('ENCRYPT AND SAVE', self)
        layout.addWidget(self.encrypt_btn)

        self.encrypt_btn.clicked.connect(self.encrypt)

        self.decrypt_btn = QPushButton('DECRYPT AND SAVE', self)
        layout.addWidget(self.decrypt_btn)
        self.decrypt_btn.clicked.connect(self.decrypt)

        # Текстовое поле для вывода информации
        self.debug_area = QTextEdit(self)
        self.debug_area.setReadOnly(True)
        layout.addWidget(self.debug_area)

        widget.setLayout(layout)
        return widget

    def encrypt(self):
        if mode == 1:
            self.encrypt1()
        else:
            self.encrypt2()

    def decrypt(self):
        if mode == 1:
            self.decrypt1()
        else:
            self.decrypt2()

    def select_mode(self):
        global mode
        mode_number = self.mode_input.text()
        if mode_number in ["1", "2"]:
            mode_number = int(mode_number)
            # Здесь можно добавить логику для обработки выбранного режима
            QMessageBox.information(self, "Mode Selected", f"You selected mode {mode_number}.")
            # Вы можете добавить дополнительную логику в зависимости от номера режима
            if mode_number == 1:
                self.debug_area.append("Mode 1 selected: Perform action A.")
                mode = 1
            elif mode_number == 2:
                self.debug_area.append("Mode 2 selected: Perform action B.")
                mode = 2
            else:
                self.debug_area.append("Invalid mode selected.")
        else:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number (1 or 2) for the mode.")

    def get_seed(self):
        this_key = self.key_field.text()
        key_seed = 1
        for i in range(len(this_key) - 1):
            key_seed *= ord(this_key[i]) * (ord(this_key[i]) - ord(this_key[i + 1]))
        return key_seed

        # Кнопка шифровки

    def encrypt1(self):
        global image_crypt, ref_path, text_path
        if ref_path and text_path:
            # Загружаем изображение и вычисляем его размер
            image_crypt = QImage(ref_path)
            img_size = image_crypt.width() * image_crypt.height()

            # Загружаем текст и вычисляем его размер
            with open(text_path, 'r', encoding="utf-8") as file:
                lines = file.readlines()
            text_size = sum(len(line) + 1 for line in lines)  # +1 на перенос

            # Проверки ошибок
            if text_size == 0:
                self.debug_area.setText("Empty text file")
                return
            if text_size * 3 >= img_size:
                self.debug_area.setText("Image is too small")
                return

            # Добавляем ноль в самый конец текста
            lines[-1] += '\0'
            text_size += 1

            random.seed(self.get_seed())

            # Массив для отслеживания занятых пикселей
            pixs = []
            counter = 0

            # Цикл шифрования
            for line in lines:
                for j in range(len(line) + 1):
                    # Поиск свободного пикселя
                    while True:
                        this_pix = random.randint(0, img_size - 1)
                        if this_pix not in pixs:
                            pixs.append(this_pix)
                            break

                    # Получаем текущий символ
                    this_char = ord(line[j]) if j < len(line) else ord('\n')

                    # Костыль для русских букв
                    if this_char > 1000:
                        this_char -= 890

                    # Пакуем данные в RGB
                    x, y = this_pix % image_crypt.width(), this_pix // image_crypt.width()
                    color = QColor(image_crypt.pixel(x, y))
                    new_color = QColor(
                        (color.red() & 0xF8) | ((this_char & 0xE0) >> 5),
                        (color.green() & 0xFC) | ((this_char & 0x18) >> 3),
                        (color.blue() & 0xF8) | (this_char & 0x07)
                    )
                    image_crypt.setPixel(x, y, new_color.rgb())

            image_crypt.save("crypt_image.png")
            self.debug_area.setText("Finished")
        else:
            self.debug_area.setText("Image is not selected")

        # Кнопка дешифровки

    def encrypt2(self):
        global image_crypt, ref_path, text_path, text_bin
        key = self.key_field.text()

        if ref_path and text_path:
            # Загружаем изображение и вычисляем его размер
            image_crypt = QImage(ref_path)
            img_size = image_crypt.width() * image_crypt.height()

            with open(text_path, 'r', encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:  # загружаем массив двоичных символов
                    text_to_bin(line, keys=int(key))
            key_take_pixel = make_key(int(key), int(key) + 2, len(text_bin))

            # Проверки ошибок
            if len(text_bin) == 0:
                self.debug_area.setText("Empty text file")
                return
            if len(text_bin) * 3 >= img_size:
                self.debug_area.setText("Image is too small")
                return

            for i in range(len(key_take_pixel)):
                x_pix = key_take_pixel[i] % image_crypt.width()
                y_pix = key_take_pixel[i] // image_crypt.width()
                text_pix = text_bin[i]
                r, g, b = [int(text_pix[j:j + 4], 2) for j in range(0, 12, 4)]
                color = QColor(255 - r, 255 - g, 255 - b).rgb()  # Создаем цвет
                image_crypt.setPixel(x_pix, y_pix, color)

            image_crypt.save("crypt_image.png")
            self.debug_area.setText("Finished")
        else:
            self.debug_area.setText("Image is not selected")

    def decrypt2(self):
        pass

    def decrypt1(self):
        global image_crypt, crypt_path
        if crypt_path:
            image_crypt = QImage(crypt_path)
            img_size = image_crypt.width() * image_crypt.height()

            random.seed(self.get_seed())

            pixs = []
            decrypt_text = ""
            counter = 0

            # Цикл дешифровки
            while True:
                # Поиск свободного пикселя
                while True:
                    this_pix = random.randint(0, img_size - 1)
                    if this_pix not in pixs:
                        pixs.append(this_pix)
                        break

                # Извлечение символа
                x, y = this_pix % image_crypt.width(), this_pix // image_crypt.width()
                color = QColor(image_crypt.pixel(x, y))

                # Распаковка
                this_char = ((color.red() & 0x07) << 5) | ((color.green() & 0x03) << 3) | (color.blue() & 0x07)

                # Костыль для русских букв
                if this_char > 130:
                    this_char += 890
                if this_char == 0:  # Конец текста
                    break
                decrypt_text += chr(this_char)

            self.debug_area.setText(decrypt_text)

            # Сохранение в файл
            with open("decrypt_text.txt", "w", encoding="utf-8") as file:
                file.write(decrypt_text)
        else:
            self.debug_area.setText("Crypted image is not selected")

    def load_ref(self):
        global ref_path
        ref_path, _ = QFileDialog.getOpenFileName(self, "Select Reference Image", "", "Images (*.png *.jpg *.bmp)")
        self.debug_area.setText(ref_path or "Image is not selected")

    def load_crypt(self):
        global crypt_path
        crypt_path, _ = QFileDialog.getOpenFileName(self, "Select Crypted Image", "", "Images (*.png *.jpg *.bmp)")
        self.debug_area.setText(crypt_path or "Crypted image is not selected")

    def load_text(self):
        global text_path
        text_path, _ = QFileDialog.getOpenFileName(self, "Select Text File", "", "Text Files (*.txt)")
        self.debug_area.setText(text_path or "Text file is not selected")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = TextInImageApp()
    main_window.show()
    sys.exit(app.exec())
