import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QFrame
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculator")
        self.init_ui()
        self.current_operator = None
        self.should_clear_display = False
        self.first_operand = None  # Сохраняет первый операнд

    def init_ui(self):
        # Основной макет
        layout = QVBoxLayout()  # Основной вертикальный макет

        # Поле для отображения операндов (маленький экран)
        self.operator_display = QLineEdit()
        self.operator_display.setAlignment(Qt.AlignRight)
        self.operator_display.setReadOnly(True)
        self.operator_display.setFixedHeight(40)
        self.operator_display.setFixedWidth(50)  # Устанавливаем ширину немного больше символа
        self.operator_display.setStyleSheet("font-size: 25px; color: gray;")
        layout.addWidget(self.operator_display)

        # Поле для отображения результатов (большой экран)
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(100)
        self.display.setStyleSheet("font-size: 40px;")
        self.display.setText('0')
        layout.addWidget(self.display)

        # Сетка для кнопок
        grid = QGridLayout()

        # Стили для кнопок
        button_style = """
        QPushButton {
            background-color: lightgray;
            border: 2px solid gray;
            border-radius: 30px;
            padding: 20px;
            font-size: 36px;
        }
        QPushButton:pressed {
            background-color: darkgray;
        }
        """

        # Кнопки с цифрами и запятой
        buttons = {
            '7': (1, 0), '8': (1, 1), '9': (1, 2),
            '4': (2, 0), '5': (2, 1), '6': (2, 2),
            '1': (3, 0), '2': (3, 1), '3': (3, 2),
            ',': (4, 0), '0': (4, 1, 1, 2)  # Кнопка 0 занимает две ячейки
        }

        # Добавляем кнопки на сетку
        for btn_text, pos in buttons.items():
            button = QPushButton(btn_text)
            button.setStyleSheet(button_style)
            button.setFixedSize(120, 120)
            button.clicked.connect(self.on_click)
            if btn_text == '0':
                button.setFixedSize(250, 120)
            if len(pos) == 2:
                grid.addWidget(button, *pos)
            else:
                grid.addWidget(button, *pos)

        # Вертикальная линия-разделитель
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setFixedWidth(20)
        grid.addWidget(separator, 1, 3, 4, 1)

        # Кнопки операций и очистки
        operations = {
            'C': (1, 4), 'AC': (1, 5, 1, 2),
            '+': (2, 4), '*': (2, 5),
            '-': (3, 4), '/': (3, 5),
            '=': (4, 4, 1, 2), '%': (4, 6)
        }

        for op_text, pos in operations.items():
            button = QPushButton(op_text)
            button.setStyleSheet(button_style)
            button.setFixedSize(120, 120)
            if op_text == '=' or op_text == 'AC':
                button.setFixedSize(250, 120)

            button.clicked.connect(self.on_click)
            if len(pos) == 2:
                grid.addWidget(button, *pos)
            else:
                grid.addWidget(button, *pos)

        # Добавляем сетку в основной макет
        layout.addLayout(grid)

        # Устанавливаем основной макет
        self.setLayout(layout)

    def on_click(self):
        button = self.sender()
        text = button.text()

        if text.isdigit() or text == ',':
            self.input_number(text)
        elif text in ['+', '-', '*', '/', '%']:
            self.set_operator(text)
        elif text == '=':
            self.calculate_result()
        elif text == 'C':
            self.clear_entry()
        elif text == 'AC':
            self.clear_all()

    def input_number(self, text):
        if self.should_clear_display:
            self.display.setText('0')
            self.should_clear_display = False

        current_text = self.display.text()
        if current_text == '0':
            current_text = ''

        self.display.setText(current_text + text)

    def set_operator(self, operator):
        if self.first_operand is None:
            self.first_operand = float(self.display.text().replace(',', '.'))
        else:
            self.calculate_result()

        self.current_operator = operator
        self.operator_display.setText(operator)
        self.should_clear_display = True

    def calculate_result(self):
        if self.current_operator is None or self.first_operand is None:
            return

        second_operand = float(self.display.text().replace(',', '.'))

        result = 0
        if self.current_operator == '+':
            result = self.first_operand + second_operand
        elif self.current_operator == '-':
            result = self.first_operand - second_operand
        elif self.current_operator == '*':
            result = self.first_operand * second_operand
        elif self.current_operator == '/':
            if second_operand != 0:
                result = self.first_operand / second_operand
            else:
                self.display.setText('Error')
                return
        elif self.current_operator == '%':
            result = self.first_operand % second_operand

        if result.is_integer():
            self.display.setText(str(int(result)))
        else:
            self.display.setText(str(result))
        self.operator_display.clear()
        self.first_operand = result
        self.current_operator = None
        self.should_clear_display = True

    def clear_entry(self):
        self.display.setText('0')

    def clear_all(self):
        self.display.setText('0')
        self.operator_display.clear()
        self.first_operand = None
        self.current_operator = None
        self.should_clear_display = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())
