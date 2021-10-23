import pywu2dclient.core.uwu2dservice as uwu2dservice
import pywu2dclient.core.network.websocketclient as websocketclient
import pywu2dclient.public.messagehandler as messaghandler

import signal


class Handler(messaghandler.IMessageHandler):
    def on_connect(self):
        print("on_connect")

    def on_disconnect(self):
        print("on_disconnect")

    def on_read(self, type, id, data):
        print("on_read: " + str(data))

    def on_handshake(self, clientId):
        print("on_handshake, clientId: " + clientId)


if __name__ == "__main__":

    service = uwu2dservice.UWU2DService(
        websocketclient.WebsocketClient("ws://localhost:41234"), Handler()
    )

    exit = False

    def ctrl_c_handler(sig, frame):
        global exit
        exit = True

    signal.signal(signal.SIGINT, ctrl_c_handler)
    while not exit:
        service.maintain()

    service.stop()
