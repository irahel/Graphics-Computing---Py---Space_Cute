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
        tams = 0
        for i in array:
            tams += 1
        return tams