class IUWU2DService:
    def __init__(self):
        return

    def is_connected(self):
        raise NotImplementedError("UWU2DService.is_connected should be implemented")

    def maintain(self):
        raise NotImplementedError("UWU2DService.maintain should be implemented")

    def stop(self):
        raise NotImplementedError("UWU2DService.stop should be implemented")

    def send_handshake(self):
        raise NotImplementedError("UWU2DService.send_handshake should be implemented")

    def send_sync(self):
        raise NotImplementedError("UWU2DService.send_sync should be implemented")

    def send_message(self, type, data):
        raise NotImplementedError("UWU2DService.send_message should be implemented")
