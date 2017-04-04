from clearblade import auth
from clearblade import Client
from clearblade import Messaging


class MQTT:
    def __init__(self, credentials):
        self.systemKey = credentials['systemKey']
        self.systemSecret = credentials['systemSecret']
        self.username = credentials['deviceName']
        self.password = credentials['activeKey']
        self.platformURL = credentials['platformURL']

        #Connect to MQTT
        self.messaging_client = self.Connect()

    def Connect(self):
        cb_auth = auth.Auth()

        #Authenticate using device auth
        device = Client.DevClient(self.systemKey, self.systemSecret, self.username, self.password, self.platformURL)
        cb_auth.Authenticate(device)
        messaging_client = Messaging.Messaging(device)

        messaging_client.InitializeMQTT()
        return messaging_client

    def PublishTopic(self, topic, message):
        self.messaging_client.publishMessage(topic, message, 0)

    def SubscribeToTopic(self, topic, callback):
        self.messaging_client.subscribe(topic, 0, callback)