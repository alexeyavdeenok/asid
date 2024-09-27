class LinkedListItem:
    """Узел связного списка"""
    def __init__(self, data=None):
        self._data = data
        self._next_item = None
        self._previous_item = None

    @property
    def data(self):
        return self._data

    @property
    def next_item(self):
        """Следующий элемент"""
        return self._next_item

    @next_item.setter
    def next_item(self, value):
        self._next_item = value
        if value is not None:
            value._previous_item = self

    @property
    def previous_item(self):
        """Предыдущий элемент"""
        return self._previous_item

    @previous_item.setter
    def previous_item(self, value):
        self._previous_item = value
        if value is not None:
            value._next_item = self

    def __repr__(self):
        return f"LinkedListItem({self._data})"


class LinkedList:
    """Связный список"""
    def __init__(self, first_item=None):
        self.first_item = first_item

    @property
    def last(self):
        """Последний элемент"""
        if not self.first_item:
            return None
        current = self.first_item
        while current.next_item and current.next_item != self.first_item:
            current = current.next_item
        return current

    def append_left(self, item):
        """Добавление слева"""
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
        """Добавление справа"""
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
        """Добавление справа (alias для append_right)"""
        self.append_right(item)

    def remove(self, item):
        """Удаление"""
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
        """Вставить новый узел с данными `data` после узла со значением `value` в кольцевом списке."""
        if self.first_item is None:
            raise ValueError("Список пуст")

        current = self.first_item
        found = False

        # Проходим по списку и ищем узел со значением `value`
        while True:
            if current.data == value:
                found = True
                break
            current = current.next_item
            # Если вернулись в начало списка, значит обошли весь список
            if current == self.first_item:
                break

        if not found:
            raise ValueError(f"Элемент со значением {value} не найден в кольцевом списке")

        # Создаем новый узел
        new_node = LinkedListItem(data)

        # Вставляем новый узел после найденного
        new_node.next_item = current.next_item
        current.next_item = new_node

    def __len__(self):
        if not self.first_item:
            return 0
        count = 1
        current = self.first_item
        while current.next_item != self.first_item:
            count += 1
            current = current.next_item
        return count

    def __iter__(self):
        current = self.first_item
        if current:
            while True:
                yield current
                current = current.next_item
                if current == self.first_item:
                    break

    def __getitem__(self, index):
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
        for node in self:
            if node.data == item:
                return True
        return False

    def __reversed__(self):
        """Итерация по списку в обратном порядке"""
        if self.first_item is None:
            return
        current = self.last  # Начинаем с последнего элемента
        while True:
            yield current.data
            current = current.previous_item  # Двигаемся к предыдущему элементу
            if current == self.last:  # Останавливаемся, когда снова попадаем на последний элемент
                break

