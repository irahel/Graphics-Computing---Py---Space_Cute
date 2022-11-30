class Queue_rotative():
    def __init__(self):
        self.dates = []

    def push(self, elemento):
        self.dates.append(elemento)
 
    def pop(self):
        # date =
        # self.push(date)
        return self.dates.pop(0)

    def empty(self):
        return len(self.dates) == 0

    def tam(self):
        return self.tamanho(self.dates)

    def tamanho(self, array):
        return sum(1 for _ in array)