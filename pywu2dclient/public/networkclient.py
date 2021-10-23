class INetworkClient:
    def __init__(self):
        pass

    def is_connected(self):
        '''
        Returns the current connection state of the network client
        '''
        raise NotImplementedError("INetworkClient.is_conneted needs to be implemented")

    def connect(self):
        '''
        Connect implementation that is called whenever is_connected returns False
        '''
        raise NotImplementedError("INetworkClient.connect needs to be implemented")

    def stop(self):
        '''
        Stop the network client.  After this is called, the expectation is that connect needs to be called again
        '''
        raise NotImplementedError("INetworkClient.stop needs to be implemented")

    def send(self, message):
        '''
        Sends message to the client.  Message should be preformatted.  Will fail if is_connected returns False
        '''
        raise NotImplementedError("INetworkClient.send needs to be implemented")

    def read(self):
        '''
        Read message from the remote.  Will only be called if is_connect returns True
        '''
        raise NotImplementedError("INetworkClient.read needs to be implemented")
