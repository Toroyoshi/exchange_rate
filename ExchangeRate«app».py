import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator

class CurrencyConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exchange rate")
        self.setGeometry(100, 100, 350, 250)
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Campo de valor com validação
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Digite o valor a converter")
        self.amount_input.setValidator(QDoubleValidator())
        layout.addWidget(self.amount_input)

        # Combobox com mais moedas
        self.from_currency = QComboBox()
        self.to_currency = QComboBox()
        currencies = ["USD", "EUR", "BRL", "JPY", "GBP", "CAD", "AUD", "CNY", "CHF", "INR"]
        
        self.from_currency.addItems(currencies)
        self.to_currency.addItems(currencies)
        self.to_currency.setCurrentText("BRL")  # Default para Real Brasileiro

        layout.addWidget(QLabel("Moeda de origem:"))
        layout.addWidget(self.from_currency)
        layout.addWidget(QLabel("Moeda de destino:"))
        layout.addWidget(self.to_currency)

        # Botão de conversão com estilo
        self.convert_button = QPushButton("Converter")
        self.convert_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.convert_button.clicked.connect(self.convert_currency)
        layout.addWidget(self.convert_button)

        # Resultado com formatação melhorada
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.result_label)

        # Botão para inverter moedas
        self.swap_button = QPushButton("Inverter Moedas")
        self.swap_button.clicked.connect(self.swap_currencies)
        layout.addWidget(self.swap_button)

        self.setLayout(layout)

    def swap_currencies(self):
        """Inverte as moedas selecionadas"""
        from_index = self.from_currency.currentIndex()
        to_index = self.to_currency.currentIndex()
        self.from_currency.setCurrentIndex(to_index)
        self.to_currency.setCurrentIndex(from_index)

    def convert_currency(self):
        try:
            amount_text = self.amount_input.text().strip().replace(",", ".")
            if not amount_text or not self.is_float(amount_text):
                QMessageBox.warning(self, "Valor inválido", "Digite um valor numérico válido.")
                return

            amount = float(amount_text)
            if amount <= 0:
                QMessageBox.warning(self, "Valor inválido", "O valor deve ser maior que zero.")
                return

            from_curr = self.from_currency.currentText()
            to_curr = self.to_currency.currentText()

            # Obter taxas de câmbio atualizadas
            url = f"https://api.exchangerate-api.com/v4/latest/{from_curr}"
            response = requests.get(url)
            
            if response.status_code != 200:
                QMessageBox.critical(self, "Erro de API", "Não foi possível obter as taxas de câmbio.")
                return

            data = response.json()
            rates = data.get("rates", {})
            
            if to_curr not in rates:
                QMessageBox.critical(self, "Erro", f"Moeda {to_curr} não encontrada.")
                return

            rate = rates[to_curr]
            result = amount * rate
            
            # Formatar o resultado com símbolos de moeda quando possível
            currency_symbols = {
                "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥", 
                "BRL": "R$", "CAD": "C$", "AUD": "A$", "CNY": "¥"
            }
            
            from_symbol = currency_symbols.get(from_curr, from_curr)
            to_symbol = currency_symbols.get(to_curr, to_curr)
            
            self.result_label.setText(
                f"{from_symbol} {amount:,.2f} {from_curr} = "
                f"{to_symbol} {result:,.2f} {to_curr}\n"
                f"Taxa: 1 {from_curr} = {rate:.4f} {to_curr}"
            )

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Erro de Conexão", "Verifique sua conexão com a internet.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro inesperado: {str(e)}")

    def is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Estilo geral da aplicação
    app.setStyleSheet("""
        QWidget {
            font-family: Arial;
            font-size: 14px;
        }
        QLineEdit {
            padding: 5px;
        }
        QComboBox {
            padding: 5px;
        }
    """)
    
    window = CurrencyConverter()
    window.show()
    sys.exit(app.exec())