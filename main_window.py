import re
import sys
import multiprocessing as mp
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QPushButton, QProgressBar)
from hashing import check_hash, algorithm_luna, SETTING
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
        self.info.setText("Выберите начало карты")
        self.info.setGeometry(225, 0, 500, 50)
        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        self.progress.setGeometry(100, 230, 400, 50)
        self.progress.hide()
        self.button_card = QPushButton('Найти карту', self)
        self.button_card.setGeometry(200, 100, 200, 50)
        self.button_card.clicked.connect(self.find_card)
        self.button_card.hide()
        self.result = QLabel(self)
        self.result.setGeometry(200, 150, 400, 100)
        self.pool_size = QtWidgets.QComboBox(self)
        self.pool_size.addItems(["Выберите размер пула", "1", "2", "3", "4", "5", '6', '7', '8'])
        self.pool_size.setGeometry(200, 50, 200, 50)
        self.pool_size.hide()
        self.number = QtWidgets.QComboBox(self)
        self.number.addItems(SETTING["begin_digits"])
        self.number.setGeometry(200, 20, 200, 50)
        self.number.activated[str].connect(self.on_activated)
        self.show()

    def on_activated(self, text: str) -> None:
        """
        Функция присвоения размера пула
        """
        self.pool_size.show()
        try:
            self.number = int(re.findall('(\d+)', text)[0])
        except:
            self.number = SETTING['begin_digits'][0]
        self.pool_size.activated[str].connect(self.choose_pool)

    def choose_pool(self, text: str):
        """
        Функция присвоения размера пула
        """
        try:
            self.size = int(re.findall('(\d+)', text)[0])
        except:
            self.size = 0
        self.button_card.show()

    def find_card(self, start: float) -> None:
        """
        Функция нахождения карты
        """
        items = [(i, self.number) for i in range(99999, 10000000)]
        #print(items)
        start = time.time()
        self.progress.show()
        QApplication.processEvents()
        with mp.Pool(self.size) as p:
            for i, result in enumerate(p.starmap(check_hash, items)):
                if result:
                    self.success(start, result)
                    break
                self.progress.setValue(int((i)/9900000*100))
                QApplication.processEvents()
            else:
                self.result.setText('НЕ НАЙДЕНО')
                self.progress.setValue(0)

    def success(self, start: float, result: float):
        """Функция вывыда информации о карте
        """
        self.progress.setValue(100)
        end = time.time() - start
        result_text = f'Расшифрованный номер: {result}\n'
        result_text += f'Проверка на алгоритм Луна: {algorithm_luna(result)}\n'
        result_text += f'Время: {end:.2f} секунд'
        self.result.setText(result_text)

def application() -> None:
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
  #  cores = mp.cpu_count() # 8
 #   print(cores)
    application()
