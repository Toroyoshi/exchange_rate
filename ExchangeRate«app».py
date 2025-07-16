import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt, QLocale
from PyQt6.QtGui import QDoubleValidator

class CurrencyConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.language = "en"  # Default language
        self.translations = {
            "en": {
                "window_title": "Currency Converter",
                "amount_placeholder": "Enter amount to convert",
                "from_label": "From:",
                "to_label": "To:",
                "convert_btn": "Convert",
                "swap_btn": "Swap Currencies",
                "invalid_amount": "Please enter a valid number",
                "api_error": "Failed to get exchange rates",
                "connection_error": "Check your internet connection"
            },
            "pt": {
                "window_title": "Conversor de Moedas",
                "amount_placeholder": "Digite o valor para converter",
                "from_label": "De:",
                "to_label": "Para:",
                "convert_btn": "Converter",
                "swap_btn": "Inverter Moedas",
                "invalid_amount": "Digite um número válido",
                "api_error": "Erro ao obter taxas de câmbio",
                "connection_error": "Verifique sua conexão com a internet"
            }
        }
        
        self.currency_symbols = {
            "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥", 
            "BRL": "R$", "CAD": "C$", "AUD": "A$", "CNY": "¥"
        }
        
        self.init_ui()
        self.set_language("en")  # Set default language

    def init_ui(self):
        # Main layout
        layout = QVBoxLayout()
        self.setGeometry(100, 100, 400, 300)

        # Language selection
        lang_layout = QHBoxLayout()
        self.pt_btn = QPushButton("Português")
        self.en_btn = QPushButton("English")
        self.pt_btn.clicked.connect(lambda: self.set_language("pt"))
        self.en_btn.clicked.connect(lambda: self.set_language("en"))
        lang_layout.addWidget(self.pt_btn)
        lang_layout.addWidget(self.en_btn)
        layout.addLayout(lang_layout)

        # Amount input
        self.amount_input = QLineEdit()
        validator = QDoubleValidator()
        validator.setBottom(0)
        self.amount_input.setValidator(validator)
        layout.addWidget(self.amount_input)

        # Currency selection
        self.from_currency = QComboBox()
        self.to_currency = QComboBox()
        currencies = ["USD", "EUR", "BRL", "JPY", "GBP", "CAD", "AUD", "CNY"]
        self.from_currency.addItems(currencies)
        self.to_currency.addItems(currencies)
        self.to_currency.setCurrentText("BRL")

        self.from_label = QLabel()
        self.to_label = QLabel()
        
        layout.addWidget(self.from_label)
        layout.addWidget(self.from_currency)
        layout.addWidget(self.to_label)
        layout.addWidget(self.to_currency)

        # Buttons
        self.convert_button = QPushButton()
        self.convert_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.convert_button.clicked.connect(self.convert_currency)
        
        self.swap_button = QPushButton()
        self.swap_button.clicked.connect(self.swap_currencies)
        
        layout.addWidget(self.convert_button)
        layout.addWidget(self.swap_button)

        # Result display
        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def set_language(self, lang):
        """Update UI text based on selected language"""
        self.language = lang
        trans = self.translations[lang]
        
        self.setWindowTitle(trans["window_title"])
        self.amount_input.setPlaceholderText(trans["amount_placeholder"])
        self.from_label.setText(trans["from_label"])
        self.to_label.setText(trans["to_label"])
        self.convert_button.setText(trans["convert_btn"])
        self.swap_button.setText(trans["swap_btn"])

    def swap_currencies(self):
        from_idx = self.from_currency.currentIndex()
        to_idx = self.to_currency.currentIndex()
        self.from_currency.setCurrentIndex(to_idx)
        self.to_currency.setCurrentIndex(from_idx)

    def convert_currency(self):
        try:
            amount_text = self.amount_input.text().strip().replace(",", ".")
            if not amount_text or not self.is_float(amount_text):
                QMessageBox.warning(self, 
                                  self.translations[self.language]["window_title"],
                                  self.translations[self.language]["invalid_amount"])
                return

            amount = float(amount_text)
            if amount <= 0:
                QMessageBox.warning(self,
                                   self.translations[self.language]["window_title"],
                                   self.translations[self.language]["invalid_amount"])
                return

            from_curr = self.from_currency.currentText()
            to_curr = self.to_currency.currentText()

            url = f"https://api.exchangerate-api.com/v4/latest/{from_curr}"
            response = requests.get(url)
            
            if response.status_code != 200:
                QMessageBox.critical(self,
                                   self.translations[self.language]["window_title"],
                                   self.translations[self.language]["api_error"])
                return

            data = response.json()
            rates = data.get("rates", {})
            
            if to_curr not in rates:
                QMessageBox.critical(self,
                                   self.translations[self.language]["window_title"],
                                   f"Currency {to_curr} not found")
                return

            rate = rates[to_curr]
            result = amount * rate
            
            from_symbol = self.currency_symbols.get(from_curr, from_curr)
            to_symbol = self.currency_symbols.get(to_curr, to_curr)
            
            self.result_label.setText(
                f"{from_symbol} {amount:,.2f} {from_curr} = "
                f"{to_symbol} {result:,.2f} {to_curr}\n"
                f"{self.translations[self.language]['from_label']} 1 {from_curr} = {rate:.4f} {to_curr}"
            )

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self,
                               self.translations[self.language]["window_title"],
                               self.translations[self.language]["connection_error"])
        except Exception as e:
            QMessageBox.critical(self,
                               self.translations[self.language]["window_title"],
                               f"Error: {str(e)}")

    def is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
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