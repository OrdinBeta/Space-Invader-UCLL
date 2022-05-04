class LoopingVariable:
    def __init__(self, max):
        self.__value = 0
        self.max = max

    @property
    def value(self):
        return self.__value

    def increase(self, amount):
        self.__value += amount
        if self.__value >= self.max:
            self.__value = self.__value % self.max
        else:
            self.__value = self.__value