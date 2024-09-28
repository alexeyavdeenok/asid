from linked_list import *
import pygame
from PyQt5.QtCore import QThread


class MusicPlayerThread(QThread):
    def __init__(self, track_item, playlist):
        super().__init__()
        self.track_item = track_item
        self.playlist = playlist

    def run(self):
        """Проигрывание трека в отдельном потоке."""
        track = self.track_item.data
        pygame.mixer.music.load(track.path)
        pygame.mixer.music.play()

        # Ожидание завершения трека, пока не будет вызван stop
        while pygame.mixer.music.get_busy():
            self.msleep(100)  # Проверяем каждые 100 миллисекунд
            if self.playlist.is_stopped:
                break  # Останавливаем воспроизведение, если был вызван stop
        if not self.playlist.is_stopped:
            self.playlist.next_track()


class Composition:
    """Класс, представляющий музыкальную композицию"""
    def __init__(self, title, path):
        self.title = title
        self.path = path

    def __repr__(self):
        return f"Composition(title='{self.title}', path='{self.path}')"

    def __str__(self):
        return self.title


class PlayList(LinkedList):
    """Класс, представляющий плейлист"""
    def __init__(self, name):
        super().__init__()
        self.name = name
        self._current = None
        self.is_paused = False
        self.is_stopped = False  # Новый флаг для остановки
        pygame.mixer.init()  # Инициализация микшера Pygame

    def __str__(self):
        return self.name

    def play_all(self, item=None):
        """Начать проигрывать все треки, начиная с item."""
        if item is not None:
            self._current = item

        # if self._current is None:
        #     raise ValueError("Нет доступных треков для проигрывания.")

        print(f"Начинаем проигрывать плейлист '{self.name}' с трека: {self._current.data}")
        self._play_track(self._current)

    def _play_track(self, track_item):
        """Вспомогательный метод для проигрывания трека."""
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            return

        # Запуск нового потока для воспроизведения трека
        self.music_thread = MusicPlayerThread(track_item, self)
        self.music_thread.start()

    def next_track(self):
        """Перейти к следующему треку."""
        if not self._current:
            raise ValueError("Нет текущего трека.")
        self._current = self._current.next_item
        print(f"Сейчас проигрывается трек: {self._current.data}")
        self._play_track(self._current)

    def previous_track(self):
        """Перейти к предыдущему треку."""
        if not self._current:
            raise ValueError("Нет текущего трека.")
        self._current = self._current.previous_item
        print(f"Сейчас проигрывается трек: {self._current.data}")
        self._play_track(self._current)

    def stop(self):
        """Останавливаем текущий трек и поток."""
        pygame.mixer.music.stop()
        self.is_stopped = True  # Устанавливаем флаг остановки
        print("Воспроизведение остановлено.")

    def pause(self):
        """Поставить воспроизведение на паузу."""
        pygame.mixer.music.pause()
        self.is_paused = True
        print("Воспроизведение поставлено на паузу.")

    @property
    def current(self):
        """Получить текущий трек."""
        if self._current is None:
            raise ValueError("Нет текущего трека.")
        return self._current.data

    def __repr__(self):
        return f"PlayList(name='{self.name}', tracks=[{', '.join(str(node.data) for node in self)})])"

    def move(self, old_index, new_index):
        """Метод для перемещения элемента с позиции `old_index` на позицию `new_index`."""
        if not self.first_item:
            raise IndexError("Список пуст")

        length = len(self)

        # Обработка отрицательных индексов
        if old_index < 0:
            old_index += length
        if new_index < 0:
            new_index += length

        # Проверка допустимости индексов
        if old_index < 0 or old_index >= length or new_index < 0 or new_index >= length:
            raise IndexError("Индекс вне диапазона")

        # Шаг 1: Найдем элемент по старой позиции (old_index)
        current = self.first_item
        for _ in range(old_index):
            current = current.next_item

        # Сохраняем данные для перемещаемого узла
        data_to_move = current.data

        # Шаг 2: Удалим элемент с его текущей позиции
        self.remove(data_to_move)

        # Шаг 3: Вставим элемент на новую позицию
        if new_index == 0:
            # Если нужно вставить на первую позицию
            self.append_left(data_to_move)
        else:
            # Найдём элемент, перед которым будет вставка
            target = self.first_item
            for _ in range(new_index - 1):
                target = target.next_item
            # Вставляем новый элемент после найденного
            self.insert(target.data, data_to_move)


