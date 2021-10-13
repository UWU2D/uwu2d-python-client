from .service import Service


class SceneService(Service):
    def __init__(self, screen):
        super().__init__()

        self.__screen = screen
        self.__background_color = (0, 0, 0)

    @property
    def background(self):
        return self.__background_color

    @background.setter
    def background(self, color):
        self.__background_color = color

    def on_event(self, event):
        pass

    def on_update(self):
        self.__screen.fill(self.background)
