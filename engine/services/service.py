class Service:
    def __init__(self):
        pass

    def on_event(self, event):
        raise NotImplementedError("Implement Service.update")

    def on_update(self):
        pass
