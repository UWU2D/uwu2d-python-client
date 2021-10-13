import pygame


class KeyStack(list):
    def press(self, id):
        if self.__len__() == 0 or self[-1] != id:
            self.append(id)

    def release(self, id):
        try:
            self.remove(id)
        except ValueError:
            pass

    def is_key_pressed(self):
        return self.__len__() > 0

    def active(self):
        return self[-1]
