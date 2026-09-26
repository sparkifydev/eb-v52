import time
import threading
import traceback

from Heart.Utils.ClientsManager import ClientsManager
from Heart.Utils.Player import Player
from Heart.Messaging import MessageManager
from Heart.Messaging import Messaging
from Heart.Utils.Friend import nOff
from Heart.Crypto import Crypto 


class Connection(threading.Thread):
    def __init__(self, socket, address):
        super().__init__()
        self.client = socket
        self.address = address
        self.player = Player()
        self.timeout = time.time()

    def recv(self, n):
        data = bytearray()
        while len(data) < n:
            packet = self.client.recv(n - len(data))
            if not packet:
                return b''
            data.extend(packet)
        return data

    def _cleanup(self):
        allSockets = ClientsManager.GetAll()
        if self.player.ID[1] in allSockets and allSockets[self.player.ID[1]]["Socket"] == self.client:
            ClientsManager.RemovePlayer(self.player.ID)
            nOff(self.player.ID)
        self.client.close()

    def run(self):
        cryptoInit = Crypto()
        self.client.settimeout(30)
        try:
            while True:
                try:
                    messageHeader = self.client.recv(7)
                except TimeoutError:
                    print(f"Client with ip: {self.address} timed out!")
                    self._cleanup()
                    break
                if not messageHeader:
                    print(f"Client with ip: {self.address} disconnected!")
                    self._cleanup()
                    break
                if len(messageHeader) >= 7:
                    headerData = Messaging.readHeader(messageHeader)
                    packetPayload = self.recv(headerData[1])
                    packetID = headerData[0]
                    decryptedPayload = cryptoInit.decryptClient(packetID, bytes(packetPayload))
                    MessageManager.receiveMessage(self, packetID, decryptedPayload, cryptoInit)

        except ConnectionError:
            print(f"Client with ip: {self.address} disconnected!")
            self._cleanup()

        except Exception:
            print(traceback.format_exc())
            self._cleanup()
