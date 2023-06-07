import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from scrap_info import scrape_fii_info, save_to_excel

class StockInfoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Info App")
        self.setWindowIcon(QIcon("icon.png"))  # Replace "icon.png" with your desired icon file

        self.fii_codes = []

        self.initUI()

    def initUI(self):
        # Create the label
        self.label = QLabel("Enter FII codes:")
        self.label.setAlignment(Qt.AlignCenter)

        # Create the text box
        self.text_box = QLineEdit()
        self.text_box.setPlaceholderText("Enter FII codes")
        self.text_box.setClearButtonEnabled(True)
        self.text_box.returnPressed.connect(self.add_fii_code)

        # Create the layout for chips
        self.chips_layout = QHBoxLayout()

        # Create the button
        self.button = QPushButton("Get Information")
        self.button.clicked.connect(self.get_stock_info)

        # Create the layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(self.chips_layout)
        layout.addWidget(self.text_box)
        layout.addWidget(self.button)

        # Set the main layout
        self.setLayout(layout)

    def add_fii_code(self):
        entered_code = self.text_box.text().strip().upper()

        if entered_code != "" and entered_code not in self.fii_codes:
            self.fii_codes.append(entered_code)

            chip_label = QLabel(entered_code)
            chip_label.setObjectName("chip")
            chip_label.setFixedHeight(self.text_box.height())

            close_button = QPushButton("x")
            close_button.setObjectName("closeButton")
            close_button.clicked.connect(lambda: self.remove_fii_code(entered_code))

            chip_layout = QHBoxLayout()
            chip_layout.addWidget(chip_label)
            chip_layout.addWidget(close_button)
            chip_layout.setSpacing(2)
            chip_layout.setContentsMargins(0, 0, 0, 0)

            chip_widget = QWidget()
            chip_widget.setLayout(chip_layout)
            chip_widget.setObjectName("chipWidget")

            self.chips_layout.addWidget(chip_widget)

        self.text_box.clear()

    def remove_fii_code(self, code):
        self.fii_codes.remove(code)

        for i in range(self.chips_layout.count()):
            chip_widget = self.chips_layout.itemAt(i).widget()
            chip_label = chip_widget.layout().itemAt(0).widget()
            if chip_label.text() == code:
                self.chips_layout.removeWidget(chip_widget)
                chip_widget.deleteLater()
                break

    def get_stock_info(self):
        if len(self.fii_codes) > 0:
            # Scrape data for each FII and store it in a list
            fii_data = []
            for code in self.fii_codes:
                stock_info = scrape_fii_info(code)
                if stock_info:
                    fii_data.append(stock_info)

            # Save the data in an Excel file
            save_to_excel(fii_data, 'stock_info.xlsx')

            self.show_message_box("Stock Info", "Data saved to stock_info.xlsx")
        else:
            self.show_message_box("Stock Info", "Please enter FII codes")

    def show_message_box(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()

if __name__ == '__main__':
    # Create the application
    app = QApplication(sys.argv)

    # Create the main window
    window = StockInfoApp()
    window.show()

    # Execute the application
    sys.exit(app.exec_())