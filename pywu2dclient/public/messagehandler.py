class IMessageHandler:
    def on_connect(self):
        """
        Will be called once on client connection.  When invoked, all communication with the server is valid.
        Prior to being called, a sync request will have been made.  There is no reason for the IMessageHandler implementor to
        manually request sync
        """

        raise NotImplementedError("MessageHandler.on_connect needs to be implemented")

    def on_disconnect(self):
        """
        Will be called once on disconnect.
        """

        raise NotImplementedError(
            "MessageHandler.on_disconnect needs to be implemented"
        )

    def on_read(self, type, id, data):
        """
        Will be called once per game message or custom message

        @params
            type - message type
            id - message id
            data - the data associated with the message
        """

        raise NotImplementedError("MessageHandler.on_read needs to be implemented")

    def on_handshake(self):
        """
        Will be called once per handshake message received from the server
        """

        raise NotImplementedError("MessageHandler.on_handshake needs to be implemented")

    def on_sync(self, message):
        """
        Will be called once per sync message received from the server
        """

        raise NotImplementedError("MessageHandler.on_handshake needs to be implemented")

    def on_client_config(self, config):
        """
        Will be called once per client config message from the server
        """

        raise NotImplementedError(
            "MessageHandler.on_client_config needs to be implemented"
        )
