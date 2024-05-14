import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog
import speech_recognition as sr

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.statements = []
        self.recognizer = sr.Recognizer()

    def initUI(self):
        layout = QVBoxLayout()

        self.text_input = QLineEdit()
        layout.addWidget(QLabel("Введіть текстові заяви:"))
        layout.addWidget(self.text_input)
        self.text_input.returnPressed.connect(self.add_statement)

        voice_input_button = QPushButton("Голосове введення")
        voice_input_button.clicked.connect(self.voice_input)
        layout.addWidget(voice_input_button)

        load_file_button = QPushButton("Завантажити файл")
        load_file_button.clicked.connect(self.load_file)
        layout.addWidget(load_file_button)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(QLabel("Результати:"))
        layout.addWidget(self.output)

        calculate_button = QPushButton("Обчислити")
        calculate_button.clicked.connect(self.calculate)
        layout.addWidget(calculate_button)

        self.setLayout(layout)
        self.setWindowTitle("Задача про Брауна, Джонса і Сміта")

    def add_statement(self):
        statement = self.text_input.text()
        self.statements.append(statement)
        self.text_input.clear()

    def voice_input(self):
        with sr.Microphone() as source:
            print("Говоріть...")
            audio = self.recognizer.listen(source)

        try:
            statement = self.recognizer.recognize_google(audio, language="uk-UA")
            self.statements.append(statement)
            print("Ви сказали:", statement)
        except sr.UnknownValueError:
            print("Не вдалося розпізнати голос")
        except sr.RequestError as e:
            print(f"Виникла помилка сервісу розпізнавання голосу: {e}")

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Відкрити файл", "", "Текстові файли (*.txt)")
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                statements = file.readlines()
                self.statements.extend([statement.strip() for statement in statements])

    def calculate(self):
        # Перевірка коректності введених даних
        if len(self.statements) != 6:
            self.output.setText("Некоректні вхідні дані. Очікується 6 заяв.")
            return

        # Логічне виведення результатів
        brown_statements = [self.statements[0], self.statements[1]]
        jones_statements = [self.statements[2], self.statements[3]]
        smith_statements = [self.statements[4], self.statements[5]]

        if self.is_culprit(brown_statements, jones_statements, smith_statements):
            culprit = "Браун"
        elif self.is_culprit(jones_statements, brown_statements, smith_statements):
            culprit = "Джонс"
        else:
            culprit = "Сміт"

        self.output.setText(f"Злочин вчинив {culprit}.")

    def is_culprit(self, suspect_statements, other1_statements, other2_statements):
        suspect_lies = sum(1 for s in suspect_statements if self.is_lie(s))
        other1_lies = sum(1 for s in other1_statements if self.is_lie(s))
        other2_lies = sum(1 for s in other2_statements if self.is_lie(s))

        if suspect_lies == 1 and other1_lies == 2 and other2_lies == 2:
            return True
        elif suspect_lies == 2 and other1_lies == 1 and other2_lies == 2:
            return True
        elif suspect_lies == 2 and other1_lies == 2 and other2_lies == 1:
            return True
        else:
            return False

    def is_lie(self, statement):
        if "Браун" in statement and "не робив" in statement:
            return False
        elif "Джонс" in statement and "не робив" in statement:
            return False
        elif "Сміт" in statement and "зробив" in statement:
            return False
        else:
            return True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())