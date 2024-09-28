class LinkedListItem:
    """Класс, представляющий узел двусвязного кольцевого списка.

    Атрибуты:
        _data (любой тип): Данные, хранящиеся в узле.
        _next_item (LinkedListItem): Ссылка на следующий узел.
        _previous_item (LinkedListItem): Ссылка на предыдущий узел.
    """

    def __init__(self, data=None):
        """
        Инициализирует узел связного списка с переданными данными.

        Аргументы:
            data (любой тип): Данные, хранящиеся в узле. По умолчанию None.
        """
        self._data = data
        self._next_item = None
        self._previous_item = None

    @property
    def data(self):
        """
        Возвращает данные узла.

        Возвращает:
            data (любой тип): Данные узла.
        """
        return self._data

    @property
    def next_item(self):
        """
        Возвращает ссылку на следующий узел.

        Возвращает:
            LinkedListItem: Следующий узел списка.
        """
        return self._next_item

    @next_item.setter
    def next_item(self, value):
        """
        Устанавливает ссылку на следующий узел.

        Аргументы:
            value (LinkedListItem): Новый узел, на который будет указывать текущий.
        """
        self._next_item = value
        if value is not None:
            value._previous_item = self

    @property
    def previous_item(self):
        """
        Возвращает ссылку на предыдущий узел.

        Возвращает:
            LinkedListItem: Предыдущий узел списка.
        """
        return self._previous_item

    @previous_item.setter
    def previous_item(self, value):
        """
        Устанавливает ссылку на предыдущий узел.

        Аргументы:
            value (LinkedListItem): Новый узел, который будет предыдущим по отношению к текущему.
        """
        self._previous_item = value
        if value is not None:
            value._next_item = self

    def __repr__(self):
        """
        Возвращает строковое представление узла списка.

        Возвращает:
            str: Строковое представление узла в формате LinkedListItem(data).
        """
        return f"LinkedListItem({self._data})"


class LinkedList:
    """Класс для работы с двусвязным кольцевым списком.

    Атрибуты:
        first_item (LinkedListItem): Ссылка на первый узел списка.
    """

    def __init__(self, first_item=None):
        """
        Инициализирует новый связный список.

        Аргументы:
            first_item (LinkedListItem, опционально): Первый узел списка. По умолчанию None.
        """
        self.first_item = first_item

    @property
    def last(self):
        """
        Возвращает последний узел списка.

        Возвращает:
            LinkedListItem: Последний узел списка или None, если список пуст.
        """
        if not self.first_item:
            return None
        current = self.first_item
        while current.next_item and current.next_item != self.first_item:
            current = current.next_item
        return current

    def append_left(self, item):
        """
        Добавляет новый узел с данными item в начало списка.

        Аргументы:
            item (любой тип): Данные, которые будут добавлены в узел.
        """
        new_item = LinkedListItem(item)
        if not self.first_item:
            self.first_item = new_item
            new_item.next_item = new_item
            new_item.previous_item = new_item
        else:
            last = self.last
            new_item.next_item = self.first_item
            new_item.previous_item = last
            last.next_item = new_item
            self.first_item.previous_item = new_item
            self.first_item = new_item

    def append_right(self, item):
        """
        Добавляет новый узел с данными item в конец списка.

        Аргументы:
            item (любой тип): Данные, которые будут добавлены в узел.
        """
        if not self.first_item:
            self.append_left(item)
        else:
            new_item = LinkedListItem(item)
            last = self.last
            new_item.next_item = self.first_item
            new_item.previous_item = last
            last.next_item = new_item
            self.first_item.previous_item = new_item

    def append(self, item):
        """
        Добавляет новый узел с данными item в конец списка (alias для append_right).

        Аргументы:
            item (любой тип): Данные, которые будут добавлены в узел.
        """
        self.append_right(item)

    def remove(self, item):
        """
        Удаляет первый узел с данными item из списка.

        Аргументы:
            item (любой тип): Данные, которые нужно удалить.

        Выбрасывает:
            ValueError: Если элемент не найден.
        """
        if not self.first_item:
            raise ValueError("Item not found")
        current = self.first_item
        found = False
        while True:
            if current.data == item:
                found = True
                break
            current = current.next_item
            if current == self.first_item:
                break
        if not found:
            raise ValueError("Item not found")

        if current == self.first_item and current.next_item == self.first_item:
            self.first_item = None
        else:
            current.previous_item.next_item = current.next_item
            current.next_item.previous_item = current.previous_item
            if current == self.first_item:
                self.first_item = current.next_item

    def insert(self, value, data):
        """
        Вставляет новый узел с данными data после узла со значением value.

        Аргументы:
            value (любой тип): Значение узла, после которого нужно вставить новый.
            data (любой тип): Данные для нового узла.

        Выбрасывает:
            ValueError: Если элемент со значением value не найден.
        """
        if self.first_item is None:
            raise ValueError("Список пуст")

        current = self.first_item
        found = False

        while True:
            if current.data == value:
                found = True
                break
            current = current.next_item
            if current == self.first_item:
                break

        if not found:
            raise ValueError(f"Элемент со значением {value} не найден в списке")

        new_node = LinkedListItem(data)
        new_node.next_item = current.next_item
        current.next_item = new_node

    def __len__(self):
        """
        Возвращает длину списка (количество узлов).

        Возвращает:
            int: Количество узлов в списке.
        """
        if not self.first_item:
            return 0
        count = 1
        current = self.first_item
        while current.next_item != self.first_item:
            count += 1
            current = current.next_item
        return count

    def __iter__(self):
        """
        Итерация по элементам списка.

        Возвращает:
            generator: Генератор для итерации по узлам списка.
        """
        current = self.first_item
        if current:
            while True:
                yield current
                current = current.next_item
                if current == self.first_item:
                    break

    def __getitem__(self, index):
        """
        Возвращает данные узла по его индексу.

        Аргументы:
            index (int): Индекс узла.

        Возвращает:
            любой тип: Данные узла.

        Выбрасывает:
            IndexError: Если индекс выходит за пределы списка.
        """
        if not self.first_item:
            raise IndexError("List index out of range")
        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError("List index out of range")

        current = self.first_item
        for _ in range(index):
            current = current.next_item
        return current.data

    def __contains__(self, item):
        """
        Проверяет, содержится ли элемент с данными item в списке.

        Аргументы:
            item (любой тип): Данные для проверки.

        Возвращает:
            bool: True, если элемент найден, иначе False.
        """
        for node in self:
            if node.data == item:
                return True
        return False

    def __reversed__(self):
        """
        Итерация по элементам списка в обратном порядке.

        Возвращает:
            generator: Генератор для обратной итерации по узлам списка.
        """
        if self.first_item is None:
            return
        current = self.last
        while True:
            yield current.data
            current = current.previous_item
            if current == self.last:
                break
