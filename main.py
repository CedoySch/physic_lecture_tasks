import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QFormLayout, \
    QMessageBox, QTextEdit, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


def cartesian_to_polar(x, y):
    r = math.sqrt(x ** 2 + y ** 2)
    theta = math.degrees(math.atan2(y, x))
    return r, theta


def polar_to_cartesian(r, theta):
    x = r * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(theta))
    return x, y


def cartesian_to_spherical(x, y, z):
    r = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    theta = math.degrees(math.atan2(y, x))
    phi = math.degrees(math.acos(z / r))
    return r, theta, phi


def spherical_to_cartesian(r, theta, phi):
    x = r * math.sin(math.radians(phi)) * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(phi)) * math.sin(math.radians(theta))
    z = r * math.cos(math.radians(phi))
    return x, y, z


def cartesian_to_cylindrical(x, y, z):
    r = math.sqrt(x ** 2 + y ** 2)
    theta = math.degrees(math.atan2(y, x))
    return r, theta, z


def cylindrical_to_cartesian(r, theta, z):
    x = r * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(theta))
    return x, y, z


class CustomSpinBox(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)
        self.spinbox = QLineEdit(self)
        self.spinbox.setText("2")
        self.spinbox.setAlignment(Qt.AlignCenter)
        self.spinbox.setFixedWidth(60)
        self.spinbox.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border-radius: 10px;
                border: 2px solid #E0E0E0;
                background-color: white;
                color: black;
            }
        """)

        self.up_button = QPushButton("▲", self)
        self.up_button.setFixedSize(30, 25)
        self.down_button = QPushButton("▼", self)
        self.down_button.setFixedSize(30, 25)

        button_style = """
            QPushButton {
                background-color: #E0E0E0;
                border-radius: 5px;
                margin: 0 3px;
            }
        """
        self.up_button.setStyleSheet(button_style)
        self.down_button.setStyleSheet(button_style)

        layout.addWidget(self.spinbox)
        layout.addWidget(self.up_button)
        layout.addWidget(self.down_button)

        self.up_button.clicked.connect(self.increment)
        self.down_button.clicked.connect(self.decrement)

    def increment(self):
        value = int(self.spinbox.text())
        if value < 10:
            self.spinbox.setText(str(value + 1))

    def decrement(self):
        value = int(self.spinbox.text())
        if value > 1:
            self.spinbox.setText(str(value - 1))

    def value(self):
        return int(self.spinbox.text())


class ModernConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Конвертер координат')
        self.setGeometry(100, 100, 450, 450)
        self.setStyleSheet("background-color: #F3F0FF;")

        layout = QVBoxLayout()

        title = QLabel("Конвертер координат")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Перевод между декартовыми, полярными, сферическими и цилиндрическими системами координат.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #666; margin-bottom: 20px;")

        self.inputXLabel = QLabel("X:")
        self.inputYLabel = QLabel("Y:")
        self.inputZLabel = QLabel("Z:")
        self.inputX = QLineEdit(self)
        self.inputY = QLineEdit(self)
        self.inputZ = QLineEdit(self)
        self.inputZ.setVisible(False)
        self.inputZLabel.setVisible(False)

        self.precisionSpinBox = CustomSpinBox()

        self.systemSelect = QComboBox(self)
        self.systemSelect.addItems([
            'Декартовы -> Полярные (2D)',
            'Полярные -> Декартовы (2D)',
            'Декартовы -> Сферические (3D)',
            'Сферические -> Декартовы (3D)',
            'Декартовы -> Цилиндрические (3D)',
            'Цилиндрические -> Декартовы (3D)'
        ])
        self.systemSelect.currentIndexChanged.connect(self.update_labels)

        convertButton = QPushButton('Конвертировать')
        convertButton.setStyleSheet("padding: 12px; font-size: 16px; background-color: #7F00FF; color: white; border-radius: 10px;")

        self.resultText = QTextEdit(self)
        self.resultText.setFont(QFont("Arial", 16))
        self.resultText.setReadOnly(True)
        self.resultText.setStyleSheet("background-color: #FFFFFF; padding: 10px; border-radius: 10px;")

        copyButton = QPushButton('Копировать')
        copyButton.setStyleSheet("padding: 8px; font-size: 14px; background-color: #7F00FF; color: white; border-radius: 10px;")
        copyButton.clicked.connect(self.copy_to_clipboard)

        resultLayout = QHBoxLayout()
        resultLayout.addWidget(self.resultText)
        resultLayout.addWidget(copyButton)

        input_style = """
            padding: 8px; 
            font-size: 14px; 
            border-radius: 10px; 
            border: 2px solid #E0E0E0; 
            background-color: white;
            color: black;
        """

        self.inputX.setPlaceholderText("Введите X")
        self.inputY.setPlaceholderText("Введите Y")
        self.inputX.setStyleSheet(input_style)
        self.inputY.setStyleSheet(input_style)
        self.inputZ.setPlaceholderText("Введите Z (опционально)")
        self.inputZ.setStyleSheet(input_style)

        self.systemSelect.setStyleSheet("""
                QComboBox {
                    padding-right: 30px; 
                    padding: 8px; 
                    font-size: 14px; 
                    border-radius: 10px; 
                    border: 2px solid #E0E0E0; 
                    background-color: white; 
                    color: black;
                }
                QComboBox::drop-down {
                    width: 0px;
                    height: 0px;
                    border: none;
                }
                QComboBox::down-arrow {
                    width: 0px;
                    height: 0px;
                }
            """)

        formLayout = QFormLayout()
        formLayout.addRow(self.inputXLabel, self.inputX)
        formLayout.addRow(self.inputYLabel, self.inputY)
        formLayout.addRow(self.inputZLabel, self.inputZ)
        formLayout.addRow('Точность:', self.precisionSpinBox)
        formLayout.addRow('Система координат:', self.systemSelect)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(formLayout)
        layout.addWidget(convertButton)
        layout.addLayout(resultLayout)

        self.setLayout(layout)

        convertButton.clicked.connect(self.convert_coordinates)

    def update_labels(self):
        selected_system = self.systemSelect.currentText()

        if 'Декартовы' in selected_system.split(' -> ')[0]:
            self.inputXLabel.setText("X:")
            self.inputYLabel.setText("Y:")
            self.inputX.setPlaceholderText("Введите X")
            self.inputY.setPlaceholderText("Введите Y")
            if '3D' in selected_system:
                self.inputZLabel.setText("Z:")
                self.inputZ.setPlaceholderText("Введите Z (опционально)")
                self.inputZ.setVisible(True)
                self.inputZLabel.setVisible(True)
            else:
                self.inputZ.setVisible(False)
                self.inputZLabel.setVisible(False)

        else:
            self.inputXLabel.setText("r:")
            self.inputYLabel.setText("θ:")
            self.inputX.setPlaceholderText("Введите r")
            self.inputY.setPlaceholderText("Введите θ")
            if '3D' in selected_system:
                self.inputZLabel.setText("φ:")
                self.inputZ.setPlaceholderText("Введите φ (опционально)")
                self.inputZ.setVisible(True)
                self.inputZLabel.setVisible(True)
            else:
                self.inputZ.setVisible(False)
                self.inputZLabel.setVisible(False)

    def format_number(self, number, precision):
        return f"{number:.{precision}f}"

    def convert_coordinates(self):
        try:
            x = float(self.inputX.text())
            y = float(self.inputY.text())
            z = float(self.inputZ.text()) if self.inputZ.isVisible() and self.inputZ.text() else 0.0
            precision = self.precisionSpinBox.value()

            conversion_type = self.systemSelect.currentText()

            if conversion_type == 'Декартовы -> Полярные (2D)':
                r, theta = cartesian_to_polar(x, y)
                result = f'r = {self.format_number(r, precision)}, θ = {self.format_number(theta, precision)}'
            elif conversion_type == 'Полярные -> Декартовы (2D)':
                r, theta = x, y
                x_res, y_res = polar_to_cartesian(r, theta)
                result = f'x = {self.format_number(x_res, precision)}, y = {self.format_number(y_res, precision)}'
            elif conversion_type == 'Декартовы -> Сферические (3D)':
                r, theta, phi = cartesian_to_spherical(x, y, z)
                result = f'r = {self.format_number(r, precision)}, θ = {self.format_number(theta, precision)}, φ = {self.format_number(phi, precision)}'
            elif conversion_type == 'Сферические -> Декартовы (3D)':
                r, theta, phi = x, y, z
                x_res, y_res, z_res = spherical_to_cartesian(r, theta, phi)
                result = f'x = {self.format_number(x_res, precision)}, y = {self.format_number(y_res, precision)}, z = {self.format_number(z_res, precision)}'
            elif conversion_type == 'Декартовы -> Цилиндрические (3D)':
                r, theta, z_res = cartesian_to_cylindrical(x, y, z)
                result = f'r = {self.format_number(r, precision)}, θ = {self.format_number(theta, precision)}, z = {self.format_number(z_res, precision)}'
            elif conversion_type == 'Цилиндрические -> Декартовы (3D)':
                r, theta, z_res = x, y, z
                x_res, y_res, z_res = cylindrical_to_cartesian(r, theta, z_res)
                result = f'x = {self.format_number(x_res, precision)}, y = {self.format_number(y_res, precision)}, z = {self.format_number(z_res, precision)}'
            else:
                result = 'Неверный выбор конверсии'

            self.resultText.setText(result)

        except ValueError as ve:
            QMessageBox.warning(self, "Ошибка", str(ve))
        except ZeroDivisionError:
            QMessageBox.warning(self, "Ошибка", "Произошла ошибка при вычислениях. Возможна ошибка деления на ноль.")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла неизвестная ошибка: {str(e)}")

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.resultText.toPlainText())
        QMessageBox.information(self, "Скопировано", "Результат скопирован в буфер обмена!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ModernConverter()
    window.show()
    sys.exit(app.exec_())
