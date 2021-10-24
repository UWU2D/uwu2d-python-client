class IMessageHandler:
    def __init__(self):
        return

    def on_connect(self):
        raise NotImplementedError("MessageHandler.on_connect needs to be implemented")

    def on_disconnect(self):
        raise NotImplementedError(
            "MessageHandler.on_disconnect needs to be implemented"
        )

    def on_read(self, type, id, data):
        raise NotImplementedError("MessageHandler.on_read needs to be implemented")

    def on_handshake(self):
        raise NotImplementedError("MessageHandler.on_handshake needs to be implemented")

    def on_client_config(self, config):
        raise NotImplementedError(
            "MessageHandler.on_client_config needs to be implemented"
        )
