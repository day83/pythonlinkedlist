class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return str(self.data)

    def copy(self):
        return Node(self.data)


class LinkedList:
    def __init__(self):
        self.head = None

    # Генератор последовательного перебора элементов
    # Флаг copy позволяет изменять значение next элемента не нарушая итерацию
    def walk(self, start: Node=False, end: Node=None, copy=False):
        node = start if start else self.head
        if copy:
            while node != end:
                next = node.next
                yield node
                node = next
        else:
            while node != end:
                yield node
                node = node.next

    # Длина списка
    def __len__(self):
        length = 0
        for node in self.walk():
            length += 1
        return length

    # Длина списка начиная с определённого элемента
    def length(self, start: Node=False):
        length = 0
        for node in self.walk(start=start):
            length += 1
        return length

    # Элемент по индексу
    def get(self, index, start=False):
        counter = 0
        if index >= 0:
            for node in self.walk(start=start):
                if counter == index:
                    return node
                counter += 1
        else:
            length = self.length(start=start)
            if abs(index) > length:
                return None
            return self.get(length + index, start=start)

    # Добавление элемента в конец списка
    def append(self, data):
        if self.head is None:
            self.head = Node(data)
            return

        *_, last_node = self.walk()
        last_node.next = Node(data)

    # Добавление элемента в начало списка
    def push(self, data):
        node = Node(data)
        node.next = next(self.walk())
        self.head = node

    # Добавление элемента после выбранного элемента
    def insert(self, after_data, insert_data, occurrence=1):
        new_node = Node(insert_data)
        for node in self.walk():
            if node.data == after_data:
                occurrence -= 1
                if occurrence == 0:
                    new_node.next = node.next
                    node.next = new_node
                    return True

    # Удаление элемента по значению
    def remove(self, remove_data, occurrence=1):
        previous = None
        for node in self.walk():
            if node.data == remove_data:
                occurrence -= 1
                if occurrence == 0:
                    node = node.next
                    if previous:
                        previous.next = node
                    else:
                        self.head = node
                    return True
            previous = node

    # Преобразование списка в обратном порядке
    def reverse(self):
        previous = None
        for node in self.walk(copy=True):
            node.next = previous
            previous = node
        self.head = previous

    # Подсчёт элементов списка по значению
    def count(self, data):
        counter = 0
        for node in self.walk():
            if node.data == data:
                counter += 1
        return counter

    # Создание копии списка
    def copy(self, start: Node=False):
        new = LinkedList()
        for node in self.walk(start=start):
            new.append(node.copy())
        return new

    # Слияние с другим списком
    def merge(self, second_list, on_index=False):
        merge_node = self.get(on_index) if on_index else -1
        tail = merge_node.next
        for second_list_node in second_list.walk():
            merge_node.next = second_list_node.copy()
            merge_node = merge_node.next
        merge_node.next = tail

    # Сортировка слиянием (merge sort)
    def sort(self, head=False, reverse=False) -> Node:
        def sorted_merge(left, right) -> Node:
            if left == None:
                return right
            if right == None:
                return left

            result = None
            if left.data <= right.data:
                result = left
                result.next = sorted_merge(left.next, right)
            else:
                result = right
                result.next = sorted_merge(left, right.next)
            return result

        if head == False:
            head = self.head

        if head.next == None:
            return head

        middle = self.get_middle(head)

        next_to_middle = middle.next

        middle.next = None

        left = self.sort(head)
        right = self.sort(next_to_middle)

        self.head = sorted_merge(left, right)

        if reverse == True:
            self.reverse()

        return self.head

    # Средний элемент списка
    def get_middle(self, head=False):
        length = self.length(head)
        return self.get(length // 2 - 1, start=head)

    # Вывод в одну строку в формате списка
    def __str__(self):
        res = ''
        for node in self.walk():
            res += str(node.data) + ', '
        return f'[{res[:-2]}]'

    # Вывод списка начиная с определённого элемена
    def print_from(self, start: Node=False):
        res = ''
        for node in self.walk(start=start):
            res += str(node.data) + ', '
        print(f'[{res[:-2]}]')

if __name__ == '__main__':

    a = LinkedList()
    print('Create List:', a)

    a.append(1)
    print('Append 1:', a)

    a.append(2)
    print('Append 2:', a)

    a.append(4)
    print('Append 4:', a)

    a.append(5)
    print('Append 5:', a)

    a.push(3)
    print('Push 3:', a)

    print('List length:', len(a))

    print('Insert after 4 1:', a.insert(4, 1), a)

    print('Insert after 2nd occurrence of 1 8:', a.insert(1, 8, 2), a)

    print('Remove 2nd occurrence of 1:', a.remove(1, 2), a)

    print('Get element on index 3:', a.get(3))

    print('Get element on index -2:', a.get(-2))

    print('Get middle element:', a.get_middle())

    print('Count 5-s:', a.count(5))

    a.reverse()
    print('List reverse:', a)

    print('Copy list:', a.copy())

    print()

    b = LinkedList()
    print('Create new linked list:', b)

    b.append(55)
    print('Append 55:', b)
    b.append(44)
    print('Append 44:', b)
    b.append(77)
    print('Append 77:', b)
    b.append(66)
    print('Append 66:', b)
    b.append(33)
    print('Append 33:', b)
    b.append(88)
    print('Append 88:', b)

    print('Merge second list to first list on index 4:')
    a.merge(b, on_index=2)
    print('List a:', a)
    print('List b:', b)
    print('Remove 55, 44, 66 from b list:')
    b.remove(55)
    b.remove(44)
    b.remove(66)
    print('List a:', a)
    print('List b:', b)
    print('Sort list a:', a.sort(), end=' ')
    print(a)
