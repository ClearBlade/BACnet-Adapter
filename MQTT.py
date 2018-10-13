

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
        messaging_client = Messaging.Messaging(device)
        messaging_client.InitializeMQTT()
        return messaging_client

    def PublishTopic(self, topic, message):
        self.messaging_client.publishMessage(topic, message, 0)

    def SubscribeToTopic(self, topic, callback):
        self.messaging_client.subscribe(topic, 0, callback)