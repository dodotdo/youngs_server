from __future__ import print_function

import json

from app.helper.wrapper import wrap_data
from twisted.protocols.basic import LineReceiver

# ServerClientInfo = ['127.0.0.1', '192.168.10.3']
class ServerProtocol(LineReceiver):
    """
    Serve up Talk protocol
    """
    def __init__(self):
        self.setRawMode()

    def connectionMade(self):
        print('Server Connection made from %s' % self.transport.getPeer())
        print(self.transport.client)
        # if self.transport.client[0] not in ServerClientInfo:
        #     print('not server side connect')
        #
        self.sendLine('welcome server'.encode())
        self.factory.server = self

    @staticmethod
    def unzipServerData(data):
        try:
            data_json = json.loads(data.decode('utf-8'))
            namepace = data_json['namespace'] if data_json['namespace'] is not None else None
            payload = data_json['payload'] if data_json['payload'] is not None else None
            target = data_json['target'] if data_json['target'] is not None else None
            return namepace, payload, target
        except Exception as e:
            print(e)
            return None, None, None


    # TODO : get target device from the redis
    def rawDataReceived(self, data):
        namespace, payload, target = self.unzipServerData(data)
        print(namespace, payload, target)
        try:
            if 'inroom_data_clean' in namespace:
                wrapped_data = wrap_data('inroom_data_clean', b"")
                self.send_to_clients(self.factory.app.inroom_client_manager.inroom_clients, wrapped_data)
            if 'update_signage' in namespace:
                wrapped_data = wrap_data('update_signage', b"")
                self.send_to_clients(self.factory.app.inroom_client_manager.inroom_clients, wrapped_data)
            if 'update_attraction' in namespace:
                wrapped_data = wrap_data('update_attraction', b"")
                self.send_to_clients(self.factory.app.inroom_lient_manager.inroom_clients, wrapped_data)
            if 'update_service' in namespace:
                wrapped_data = wrap_data('update_service', b"")
                self.send_to_clients(self.factory.app.inroom_client_manager.inroom_clients, wrapped_data)
            if 'update_info' in namespace:
                wrapped_data = wrap_data('update_info', b"")
                self.send_to_clients(self.factory.app.inroom_client_manager.inroom_clients, wrapped_data)
            if 'update_faq' in namespace:
                wrapped_data = wrap_data('update_faq', b"")
                self.send_to_clients(self.factory.app.inroom_client_manager.inroom_clients, wrapped_data)
            if 'guest_requirement_survey' in namespace:
                dummy_data = b'{"surveys":[{"id":1, "title":"survey","max_point":5,"type":"requirement_complete"}],"guest_requirement_id":1}'
                wrapped_data = wrap_data('guest_requirement_survey', dummy_data)
                self.send_to_clients(self.factory.app.inroom_client_manager.inroom_clients, wrapped_data)
        except UnicodeDecodeError as e:
            print(e)

    def send_to_clients(self, clients, data):
        for client in clients:
            if client.protocol == self:
                continue
            if client.is_authorized is True:
                client.protocol.message(data)


    def connectionLost(self, reason):
        print('Server Connection lost from %s' % self.transport.getPeer())
        # self.factory.app.inroom_client_manager.clients.remove(self)

    def message(self, message):
        self.transport.write((message + '\n').encode())

