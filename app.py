import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QTextEdit, QLabel, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt
from LLM import ask_mistral_with_context

class RAGApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Docu-M8")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.input = QLineEdit()
        self.input.setPlaceholderText("your question …")
        layout.addWidget(self.input)

        self.button = QPushButton("push button to ask")
        self.button.clicked.connect(self.ask_question)
        layout.addWidget(self.button)

        self.response_box = QTextEdit()
        self.response_box.setReadOnly(True)
        layout.addWidget(self.response_box)

        self.links_label = QLabel("relevante documents:")
        layout.addWidget(self.links_label)

        self.doc_list = QListWidget()
        self.doc_list.itemClicked.connect(self.open_file)
        layout.addWidget(self.doc_list)

        self.setLayout(layout)

    def ask_question(self):
        query = self.input.text().strip()
        if not query:
            return

        self.response_box.setPlainText("searching …")
        QApplication.processEvents()

        answer = ask_mistral_with_context(query)
        parts = answer.split("relevant documents:\n")
        main_answer = parts[0].strip()
        doc_links = parts[1].strip().split("\n") if len(parts) > 1 else []

        self.response_box.setPlainText(main_answer)
        self.doc_list.clear()
        for link in doc_links:
            item = QListWidgetItem(link.replace("- ", ""))
            self.doc_list.addItem(item)

    def open_file(self, item):
        path = item.text()
        if os.path.exists(path):
            os.system(f"open '{path}'")  # öffnet Datei im macOS Finder
        else:
            self.response_box.append(f"[error] file not found: {path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RAGApp()
    window.show()
    sys.exit(app.exec())
