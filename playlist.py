from linked_list import *
import pygame
from PyQt5.QtCore import QThread


class MusicPlayerThread(QThread):
    """
    Класс потока для воспроизведения музыкальных треков.

    Атрибуты:
        track_item (LinkedListItem): Узел списка с данными трека.
        playlist (PlayList): Плейлист, содержащий текущий трек.
    """

    def __init__(self, track_item, playlist):
        """
        Инициализирует поток для воспроизведения трека.

        Аргументы:
            track_item (LinkedListItem): Узел списка с треком.
            playlist (PlayList): Текущий плейлист.
        """
        super().__init__()
        self.track_item = track_item
        self.playlist = playlist

    def run(self):
        """
        Метод, запускаемый при старте потока.
        Воспроизводит трек и проверяет, завершилось ли воспроизведение.
        """
        track = self.track_item.data
        pygame.mixer.music.load(track.path)
        pygame.mixer.music.play()

        # Ожидание завершения трека или команды остановки
        while pygame.mixer.music.get_busy():
            self.msleep(100)  # Проверка каждые 100 миллисекунд
            if self.playlist.is_stopped:
                break  # Прерываем воспроизведение, если был вызван stop

        # Переходим к следующему треку, если воспроизведение не было остановлено
        if not self.playlist.is_stopped:
            self.playlist.next_track()


class Composition:
    """
    Класс, представляющий музыкальную композицию.

    Атрибуты:
        title (str): Название трека.
        path (str): Путь к файлу с треком.
    """

    def __init__(self, title, path):
        """
        Инициализирует музыкальную композицию.

        Аргументы:
            title (str): Название композиции.
            path (str): Путь к файлу с композицией.
        """
        self.title = title
        self.path = path

    def __repr__(self):
        """
        Возвращает строковое представление композиции.

        Возвращает:
            str: Строковое представление в формате Composition(title, path).
        """
        return f"Composition(title='{self.title}', path='{self.path}')"

    def __str__(self):
        """
        Возвращает название композиции.

        Возвращает:
            str: Название трека.
        """
        return self.title


class PlayList(LinkedList):
    """
    Класс, представляющий музыкальный плейлист.

    Атрибуты:
        name (str): Название плейлиста.
        _current (LinkedListItem): Текущий трек.
        is_paused (bool): Флаг паузы.
        is_stopped (bool): Флаг остановки.
    """

    def __init__(self, name):
        """
        Инициализирует плейлист с заданным именем.

        Аргументы:
            name (str): Название плейлиста.
        """
        super().__init__()
        self.name = name
        self._current = None
        self.is_paused = False
        self.is_stopped = False
        pygame.mixer.init()  # Инициализация Pygame микшера

    def __str__(self):
        """
        Возвращает название плейлиста.

        Возвращает:
            str: Название плейлиста.
        """
        return self.name

    def play_all(self, item=None):
        """
        Проигрывает все треки в плейлисте начиная с указанного.

        Аргументы:
            item (LinkedListItem, optional): Узел списка с начальным треком.
        """
        if item is not None:
            self._current = item

        # Проверка, если трек доступен
        print(f"Начинаем проигрывать плейлист '{self.name}' с трека: {self._current.data}")
        self._play_track(self._current)

    def _play_track(self, track_item):
        """
        Проигрывает указанный трек.

        Аргументы:
            track_item (LinkedListItem): Узел списка с треком.
        """
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            return

        # Запуск нового потока для воспроизведения трека
        self.music_thread = MusicPlayerThread(track_item, self)
        self.music_thread.start()

    def next_track(self):
        """
        Переходит к следующему треку в плейлисте.
        """
        if not self._current:
            raise ValueError("Нет текущего трека.")
        self._current = self._current.next_item
        print(f"Сейчас проигрывается трек: {self._current.data}")
        self._play_track(self._current)

    def previous_track(self):
        """
        Переходит к предыдущему треку в плейлисте.
        """
        if not self._current:
            raise ValueError("Нет текущего трека.")
        self._current = self._current.previous_item
        print(f"Сейчас проигрывается трек: {self._current.data}")
        self._play_track(self._current)

    def stop(self):
        """
        Останавливает текущее воспроизведение.
        """
        pygame.mixer.music.stop()
        self.is_stopped = True
        print("Воспроизведение остановлено.")

    def pause(self):
        """
        Приостанавливает текущее воспроизведение.
        """
        pygame.mixer.music.pause()
        self.is_paused = True
        print("Воспроизведение поставлено на паузу.")

    @property
    def current(self):
        """
        Возвращает текущий трек.

        Возвращает:
            Composition: Текущий трек.
        """
        if self._current is None:
            raise ValueError("Нет текущего трека.")
        return self._current.data

    def __repr__(self):
        """
        Возвращает строковое представление плейлиста.

        Возвращает:
            str: Строковое представление в формате PlayList(name, tracks).
        """
        return f"PlayList(name='{self.name}', tracks=[{', '.join(str(node.data) for node in self)}])"

    def move(self, old_index, new_index):
        """
        Перемещает трек с позиции old_index на позицию new_index.

        Аргументы:
            old_index (int): Индекс перемещаемого трека.
            new_index (int): Индекс, на который нужно переместить трек.

        Выбрасывает:
            IndexError: Если индексы вне допустимого диапазона.
        """
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

        # Шаг 1: Найти элемент по старой позиции
        current = self.first_item
        for _ in range(old_index):
            current = current.next_item

        # Сохраняем данные для перемещаемого узла
        data_to_move = current.data

        # Шаг 2: Удалить элемент с его текущей позиции
        self.remove(data_to_move)

        # Шаг 3: Вставить элемент на новую позицию
        if new_index == 0:
            self.append_left(data_to_move)
        else:
            target = self.first_item
            for _ in range(new_index - 1):
                target = target.next_item
            self.insert(target.data, data_to_move)
