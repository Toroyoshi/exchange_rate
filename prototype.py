import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox
)
from PyQt6.QtCore import Qt

class CurrencyConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversor de Moedas")
        self.setGeometry(100, 100, 300, 200)

        # Layout principal
        layout = QVBoxLayout()

        # Campo de valor
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Valor a converter")
        layout.addWidget(self.amount_input)

        # Seleção de moedas
        self.from_currency = QComboBox()
        self.to_currency = QComboBox()
        currencies = ["USD", "EUR", "BRL", "JPY", "GBP"]

        self.from_currency.addItems(currencies)
        self.to_currency.addItems(currencies)

        layout.addWidget(QLabel("De:"))
        layout.addWidget(self.from_currency)
        layout.addWidget(QLabel("Para:"))
        layout.addWidget(self.to_currency)

        # Botão de conversão
        self.convert_button = QPushButton("Converter")
        self.convert_button.clicked.connect(self.convert_currency)
        layout.addWidget(self.convert_button)

        # Resultado
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def convert_currency(self):
        try:
            amount_text = self.amount_input.text().strip()
            if not amount_text or not amount_text.replace(".", "", 1).isdigit():
                self.result_label.setText("Digite um valor numérico válido.")
                return

            amount = float(amount_text)
            from_curr = self.from_currency.currentText()
            to_curr = self.to_currency.currentText()



            url = "https://open.er-api.com/v6/latest/USD"
            response = requests.get(url)
            print(response.json())


            if response.status_code != 200:
                self.result_label.setText("Erro ao acessar a API de câmbio.")
                return

            data = response.json()
            rate = data.get("rates", {}).get(to_curr)
            if rate is None:
                self.result_label.setText("Moeda não encontrada.")
                return

            result = amount * rate
            self.result_label.setText(f"{amount:.2f} {from_curr} = {result:.2f} {to_curr}")
        except Exception as e:
            self.result_label.setText(f"Erro inesperado: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CurrencyConverter()
    window.show()
    sys.exit(app.exec())
