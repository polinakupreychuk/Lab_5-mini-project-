import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog
import speech_recognition as sr

# Interface для перевірки заяв
class StatementChecker:
    def check_statements(self, brown_statement, john_statement, smith_statement):
        pass

# Реалізація інтерфейсу для перевірки заяв детектива
class DetectiveStatementChecker(StatementChecker):
    def check_statements(self, brown_statement, john_statement, smith_statement):
        if (brown_statement == "Я не робив цього. Джонс не робив цього." and
            john_statement == "Сміт зробив це. Браун не робив цього." and
            smith_statement == "Я не робив це. Браун зробив це."):
            return ("Сміт", "Браун", "Джонс")
        else:
            return None

# Клас для запису аудіо
class AudioRecorder:
    @staticmethod
    def record_audio():
        recognizer = sr.Recognizer()

        # Налаштування чутливості мікрофона до шумів навколишнього середовища
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)

            print("Прослуховування...")
            audio = recognizer.listen(source)

        try:
            # Використання Google Web Speech API для розпізнавання мови
            statement = recognizer.recognize_google(audio, language="uk-UA")
            print("Аудіо записано:", statement)
            return statement
        except sr.UnknownValueError:
            print("Не вдалося розпізнати аудіо")
            return ""
        except sr.RequestError as e:
            print("Помилка при використанні Google Web Speech API: {0}".format(e))
            return ""

# Клас для вирішення головоломки
class PuzzleSolver:
    @staticmethod
    def solve(brown_statement, john_statement, smith_statement, statement_checker):
        return statement_checker.check_statements(brown_statement, john_statement, smith_statement)

# Клас для графічного інтерфейсу користувача
class DetectiveApp(QWidget):
    def __init__(self, statement_checker):
        super().__init__()
        self.setWindowTitle("Головоломка детектива")
        self.statement_checker = statement_checker
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Введіть заяви Брауна, Джонса і Сміта:")
        layout.addWidget(self.label)

        self.brown_input = QLineEdit()
        self.brown_input.setPlaceholderText("Заява Брауна")
        layout.addWidget(self.brown_input)

        self.john_input = QLineEdit()
        self.john_input.setPlaceholderText("Заява Джонса")
        layout.addWidget(self.john_input)

        self.smith_input = QLineEdit()
        self.smith_input.setPlaceholderText("Заява Сміта")
        layout.addWidget(self.smith_input)

        self.audio_button = QPushButton("Записати аудіо")
        self.audio_button.clicked.connect(self.record_audio)
        layout.addWidget(self.audio_button)

        self.solve_button = QPushButton("Вирішити")
        self.solve_button.clicked.connect(self.solve)
        layout.addWidget(self.solve_button)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(QLabel("Результат:"))
        layout.addWidget(self.output)

        self.setLayout(layout)

    def record_audio(self):
        statement = AudioRecorder.record_audio()
        if not self.brown_input.text():
            self.brown_input.setText(statement)
        elif not self.john_input.text():
            self.john_input.setText(statement)
        elif not self.smith_input.text():
            self.smith_input.setText(statement)

    def solve(self):
        brown_statement = self.brown_input.text().strip()
        john_statement = self.john_input.text().strip()
        smith_statement = self.smith_input.text().strip()

        if not brown_statement or not john_statement or not smith_statement:
            self.output.setText("Будь ласка, введіть заяви для всіх підозрюваних.")
            return

        result = PuzzleSolver.solve(brown_statement, john_statement, smith_statement, self.statement_checker)

        if result:
            self.output.setText(f"Злочин вчинив {result[0]}.")
        else:
            self.output.setText("Некоректні заяви. Будь ласка, введіть коректні заяви.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    statement_checker = DetectiveStatementChecker()
    window = DetectiveApp(statement_checker)
    window.show()
    sys.exit(app.exec_())