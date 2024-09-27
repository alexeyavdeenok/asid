import sys
import pygame
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel


class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()

        # Инициализация Pygame для воспроизведения музыки
        pygame.mixer.init()

        self.initUI()

    def initUI(self):
        # Установка интерфейса
        self.setWindowTitle('MP3 Music Player')
        self.setGeometry(100, 100, 300, 200)

        # Создаем кнопку для выбора файла
        self.button = QPushButton('Выбрать MP3 файл', self)
        self.button.clicked.connect(self.open_file_dialog)

        # Метка для отображения выбранного файла
        self.label = QLabel('Выбранный файл: None', self)

        # Упаковка элементов в вертикальный layout
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def open_file_dialog(self):
        # Открытие диалога выбора файла
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите MP3 файл", "", "MP3 Files (*.mp3);;All Files (*)",
                                                   options=options)

        if file_path:
            self.label.setText(f'Выбранный файл: {file_path}')  # Отображаем выбранный файл
            self.play_music(file_path)  # Проигрывание выбранного файла

    def play_music(self, file_path):
        # Проигрывание музыки
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        print(f'Играет: {file_path}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())
