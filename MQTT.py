from clearblade.ClearBladeCore import System, cbLogs, Developer



class MQTT:
    def __init__(self, credentials):
        print("MQTT __init__")
        self.systemKey = credentials['systemKey']
        self.systemSecret = 'system_secret_not_used'
        self.username = credentials['deviceName']
        self.password = credentials['activeKey']
        self.platformURL = credentials['platformURL']
        self.deviceName = credentials['deviceName']
        self.activeKey = credentials['activeKey']

        #Connect to MQTT
        self.messaging_client = self.Connect()

    def Connect(self):
        print("MQTT Connect")
        system = System(self.systemKey, 'system_secret_not_used', url=self.platformURL)

        #Authenticate using device auth
        device = system.Device(self.deviceName, self.activeKey)

        # Use device to access a messaging client
        messaging_client = system.Messaging(device)

        # Connect to MQTT
        messaging_client.connect()

        return messaging_client

    def PublishTopic(self, topic, message):
        self.messaging_client.publishMessage(topic, message, 0)

    def SubscribeToTopic(self, topic, callback):
        self.messaging_client.subscribe(topic, 0, callback)