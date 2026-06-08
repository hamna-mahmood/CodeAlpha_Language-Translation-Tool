import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QTextEdit,
    QPushButton, QComboBox, QVBoxLayout,
    QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from deep_translator import GoogleTranslator


class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Language Translation Tool")
        self.resize(900, 650)

        self.languages = {
            "English": "en",
            "Urdu": "ur",
            "French": "fr",
            "Spanish": "es",
            "German": "de",
            "Arabic": "ar",
            "Hindi": "hi",
            "Chinese": "zh-CN"
        }

        self.setup_ui()

    def setup_ui(self):

        self.setStyleSheet("""
            QWidget {
                background-color: #48A860;
            }

            #card {
                background-color: white;
                border-radius: 20px;
            }

            QLabel {
                background: transparent;
            }

            QTextEdit {
                background-color: #F8F8F8;
                border: 2px solid #D9D9D9;
                border-radius: 15px;
                padding: 12px;
                font-size: 14px;
                color: black;
            }

            QComboBox {
                background-color: white;
                border: 2px solid #D9D9D9;
                border-radius: 12px;
                padding: 8px;
                min-width: 150px;
                font-size: 13px;
                color: black;
            }

            QPushButton {
                background-color: #00A86B;
                color: white;
                border: none;
                border-radius: 22px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
            }

            QPushButton:hover {
                background-color: #009961;
            }

            QPushButton:pressed {
                background-color: #007A50;
            }
        """)

        # Main Layout
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(40, 40, 40, 40)

        # White Card
        card = QWidget()
        card.setObjectName("card")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(20)

        # Heading
        heading = QLabel("Language Translation Tool")
        heading.setFont(QFont("Georgia", 24, QFont.Bold))
        heading.setAlignment(Qt.AlignCenter)
        heading.setStyleSheet("""
            color: #006B45;
            background: transparent;
        """)

        # Input Label
        input_label = QLabel("Enter Text")
        input_label.setFont(QFont("Georgia", 13, QFont.Bold))
        input_label.setStyleSheet("color:#333333;")

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Type text here...")

        # Language Selection
        language_layout = QHBoxLayout()

        self.source_combo = QComboBox()
        self.target_combo = QComboBox()

        self.source_combo.addItems(self.languages.keys())
        self.target_combo.addItems(self.languages.keys())

        self.source_combo.setCurrentText("English")
        self.target_combo.setCurrentText("Urdu")

        source_layout = QVBoxLayout()
        source_layout.addWidget(QLabel("Source Language"))
        source_layout.addWidget(self.source_combo)

        target_layout = QVBoxLayout()
        target_layout.addWidget(QLabel("Target Language"))
        target_layout.addWidget(self.target_combo)

        swap_btn = QPushButton("⇄")
        swap_btn.setFixedSize(50, 50)
        swap_btn.clicked.connect(self.swap_languages)

        language_layout.addLayout(source_layout)
        language_layout.addWidget(swap_btn)
        language_layout.addLayout(target_layout)

        # Translate Button
        translate_btn = QPushButton("Translate")
        translate_btn.setFixedSize(180, 45)
        translate_btn.clicked.connect(self.translate_text)

        translate_layout = QHBoxLayout()
        translate_layout.addStretch()
        translate_layout.addWidget(translate_btn)
        translate_layout.addStretch()

        # Output Label
        output_label = QLabel("Translated Text")
        output_label.setFont(QFont("Georgia", 13, QFont.Bold))
        output_label.setStyleSheet("color:#333333;")

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        # Copy Button
        copy_btn = QPushButton("Copy Text")
        copy_btn.setFixedSize(180, 45)
        copy_btn.clicked.connect(self.copy_text)

        copy_layout = QHBoxLayout()
        copy_layout.addStretch()
        copy_layout.addWidget(copy_btn)
        copy_layout.addStretch()

        # Add widgets to card
        card_layout.addWidget(heading)
        card_layout.addWidget(input_label)
        card_layout.addWidget(self.input_text)
        card_layout.addLayout(language_layout)
        card_layout.addLayout(translate_layout)
        card_layout.addWidget(output_label)
        card_layout.addWidget(self.output_text)
        card_layout.addLayout(copy_layout)

        outer_layout.addStretch()
        outer_layout.addWidget(card)
        outer_layout.addStretch()

        self.setLayout(outer_layout)

    def swap_languages(self):
        source = self.source_combo.currentText()
        target = self.target_combo.currentText()

        self.source_combo.setCurrentText(target)
        self.target_combo.setCurrentText(source)

    def translate_text(self):
        try:
            text = self.input_text.toPlainText().strip()

            if not text:
                QMessageBox.warning(
                    self,
                    "Warning",
                    "Please enter some text."
                )
                return

            source = self.languages[
                self.source_combo.currentText()
            ]

            target = self.languages[
                self.target_combo.currentText()
            ]

            translated = GoogleTranslator(
                source=source,
                target=target
            ).translate(text)

            self.output_text.setText(translated)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    def copy_text(self):
        QApplication.clipboard().setText(
            self.output_text.toPlainText()
        )

        QMessageBox.information(
            self,
            "Copied",
            "Translated text copied successfully!"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TranslatorApp()
    window.show()

    sys.exit(app.exec_())