import re
import sys
import multiprocessing as mp
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QFileDialog)
from hashing import check_hash, algorithm_luna
import time
class Window(QMainWindow):
    def __init__(self) -> None:
        """
        Функция инициализации
        """
        super(Window, self).__init__()
        self.setWindowTitle('SEARCH OF BANK CARD')
        self.setFixedSize(600, 400)
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 600, 400)
        self.background.setPixmap(QPixmap("icon.jpg").scaled(600, 400))
        self.info = QLabel(self)
        self.info.setText("Выберите размер пула")
        self.info.setGeometry(225, 20, 500, 50)
        #self.message = QLabel(self)
       # self.message.setGeometry(225, 250, 200, 50)
        self.button_card = QPushButton('Найти карту', self)
        self.button_card.setGeometry(200, 100, 200, 50)
       # self.button_card.clicked.connect(self.on_activated)
        #self.button_card.hide()
       # self.key_size = QtWidgets.QComboBox(self)
        self.result = QLabel(self)
        self.result.setGeometry(200, 150, 200, 50)        
        '''
        self.key_size.addItems(["64 бит", "128 бит", "192 бит"])
        self.key_size.setGeometry(200, 50, 200, 50)
        self.key_size.activated[str].connect(self.on_activated)

        self.button_e.clicked.connect(self.encryption)
        self.button_e.hide()
        self.button_d = QPushButton('Дешифровать текст', self)
        self.button_d.setGeometry(200, 200, 200, 50)
        self.button_d.clicked.connect(self.decryption)
        self.button_d.hide()
        '''
        self.show()

    def on_activated(self, text: str) -> None:
        """
        Функция присвоения размера ключа
        """
       # self.prepare_pb()
        start = time.time()
        self.find_card(start)

    def hidden(self) -> None:
        """
        Функция показа кнопок для шифрования и дешифрования после генерации ключей
        """
        self.button_d.show()
        self.result.show()

    def find_card(self, start: float) -> None:
        """
        Функция нахождения ключа
        """
        with mp.Pool(self.value) as p:
            for i, result in enumerate(p.map(check_hash, range(99999, 10000000))):
                if result:
                    self.update_pb_on_success(start, result)
                    p.terminate()
                    break
                self.update_pb_on_progress(i)
            else:
                self.result_label.setText('Solution not found')
                self.pbar.setValue(100)





def application() -> None:
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()