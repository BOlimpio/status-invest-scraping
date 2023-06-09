import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QScrollArea, QSizePolicy, QProgressBar
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QScrollArea, QSizePolicy, QProgressBar, QFileDialog
from scrap_info import save_to_excel, scrape_fii_info

class Worker(QThread):
    progress_updated = pyqtSignal(int)
    data_scraped = pyqtSignal(list)

    def __init__(self, fii_codes):
        super().__init__()
        self.fii_codes = fii_codes

    def run(self):
        fii_data = []
        total_fii_codes = len(self.fii_codes)

        for index, code in enumerate(self.fii_codes):
            stock_info = scrape_fii_info(code)
            if stock_info:
                fii_data.append(stock_info)
            
            progress = (index + 1) * 100 // total_fii_codes
            self.progress_updated.emit(progress)

        self.data_scraped.emit(fii_data)


class StockInfoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FII Info App")
        self.setWindowIcon(QIcon("image/money-bag.ico"))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint) 
        self.fii_codes = []

        self.initUI()


    def initUI(self):
        # Create the label
        self.label = QLabel("Enter FII codes:")
        self.label.setObjectName("titleLabel")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMinimumHeight(40)
        self.label.setFont(QFont("Arial", 20, QFont.Bold))

        # Create the text box
        self.text_box = QLineEdit()
        self.text_box.setPlaceholderText("Enter FII codes")
        self.text_box.setClearButtonEnabled(True)
        self.text_box.returnPressed.connect(self.add_fii_code)
        self.text_box.setObjectName("textBox")
        self.text_box.setMinimumHeight(40)
        self.text_box.setFont(QFont("Arial", 14))

        # Create the scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Create the layout for chips
        self.chips_layout = QVBoxLayout()
        self.chips_layout.setSpacing(10)
        self.chips_layout.setAlignment(Qt.AlignTop)

        # Create the button
        self.button = QPushButton("Get Information")
        self.button.setObjectName("actionButton")
        self.button.clicked.connect(self.get_stock_info)
        self.button.setMinimumHeight(40)
        self.button.setFont(QFont("Arial", 16))

        # Create the loading bar
        self.loading_bar = QProgressBar()
        self.loading_bar.setObjectName("loadingBar")
        self.loading_bar.setTextVisible(True)
        self.loading_bar.setMinimum(0)
        self.loading_bar.setMaximum(100)
        self.loading_bar.hide()

        # Create the main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.text_box)
        layout.addWidget(self.button)
        layout.addWidget(self.loading_bar)
        layout.setContentsMargins(20, 20, 20, 20)

        # Set the chips layout as the scroll area's widget
        scroll_content = QWidget()
        scroll_content.setLayout(self.chips_layout)
        self.scroll_area.setWidget(scroll_content)

        # Apply styles
        self.setStyleSheet("""
            StockInfoApp {
                background-color: #f5f5f5;
            }

            #titleLabel {
                color: #333;
                margin-bottom: 20px;
            }

            QLineEdit#textBox {
                border: 2px solid #ccc;
                border-radius: 4px;
                padding: 10px;
            }

            QPushButton#actionButton {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #4caf50, stop: 1 #388e3c);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 12px;
            }

            QPushButton#actionButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #45a049, stop: 1 #388e3c);
            }

            QLabel#chipLabel {
                background-color: #e0e0e0;
                color: #333;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton#deleteButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px;
                font-size: 10px;
                width: 16px;
                height: 16px;
                margin-left: 4px;
            }

            QPushButton#deleteButton:hover {
                background-color: #d32f2f;
            }

            QProgressBar#loadingBar {
                color: #333;
                background-color: #e0e0e0;
                border-radius: 4px;
                height: 20px;
                text-align: center;
                font-size: 14px;
            }
        """)

        self.setFixedSize(600, 400)

    def add_fii_code(self):
        entered_code = self.text_box.text().strip().upper()

        if entered_code != "" and entered_code not in self.fii_codes:
            self.fii_codes.append(entered_code)

            chip_layout = QHBoxLayout()
            chip_layout.setSpacing(4)
            chip_layout.setAlignment(Qt.AlignLeft)

            chip_label = QLabel(entered_code)
            chip_label.setObjectName("chipLabel")
            chip_label.setFixedHeight(30)
            chip_label.setFont(QFont("Arial", 14))

            delete_button = QPushButton("x")
            delete_button.setObjectName("deleteButton")
            delete_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            delete_button.clicked.connect(lambda _, layout=chip_layout, code=entered_code: self.delete_fii_code(layout, code))

            chip_layout.addWidget(chip_label)
            chip_layout.addWidget(delete_button)

            current_line_layout = None
            if self.chips_layout.count() > 0:
                current_line_layout = self.chips_layout.itemAt(self.chips_layout.count() - 1).layout()

            if current_line_layout is None or current_line_layout.count() >= 4:
                line_layout = QHBoxLayout()
                self.chips_layout.addLayout(line_layout)
            else:
                line_layout = current_line_layout

            line_layout.addLayout(chip_layout)

        self.text_box.clear()

    def delete_fii_code(self, layout, code):
        self.fii_codes.remove(code)
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)
        if layout.count() == 0:
            line_layout = self.chips_layout.itemAt(self.chips_layout.count() - 1).layout()
            if line_layout.count() == 0:
                line_layout.setParent(None)

    def get_stock_info(self):
        if len(self.fii_codes) == 0:
            QMessageBox.warning(self, "No FII Codes", "Please enter at least one FII code.")
            return

        self.loading_bar.setValue(0)
        self.loading_bar.show()

        self.worker = Worker(self.fii_codes)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.data_scraped.connect(self.handle_data_scraped)

        self.worker.start()

    def update_progress(self, progress):
        self.loading_bar.setValue(progress)

    def handle_data_scraped(self, data):
        self.loading_bar.hide()

        if len(data) == 0:
            QMessageBox.warning(self, "No Data Found", "No data found for the entered FII codes.")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Excel Files (*.xlsx)")

        error_messages = []
        for stock_data in data:
            error_messages.extend(stock_data.pop('Messages', []))

        if len(error_messages) > 0:
            QMessageBox.warning(self, "Error Scraping Data", "\n".join(error_messages))

        if filename:
            try:
                save_errors = save_to_excel(data, f"{filename}.xlsx")
                if len(save_errors) > 0:
                    QMessageBox.warning(self, "Error Saving Data", "\n".join(save_errors))
                else:
                    QMessageBox.information(self, "Data Saved", "Data saved successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Error Saving Data", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockInfoApp()
    window.show()
    sys.exit(app.exec_())
