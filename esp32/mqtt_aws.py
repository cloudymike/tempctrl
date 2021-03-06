from umqtt.simple import MQTTClient

MESSAGE = b''

def sub_cb(topic, msg):
    global MESSAGE
    MESSAGE = msg
    print((topic, MESSAGE))

class MQTTAWS:
    __slots__ = ('host', 'port', 'topic', 'client')

    def __init__(self, client_id, host, port, pub_topic, sub_topic, key_file, cert_file):
        self.client_id = client_id
        self.host = host
        self.port = port
        self.pub_topic = pub_topic
        self.sub_topic = sub_topic
        self.key_file = key_file
        self.cert_file = cert_file

        self.mqtt_client = None

        self.connect_mqtt()

        self.mqtt_client.set_callback(sub_cb)
        self.mqtt_client.subscribe(topic=self.sub_topic)

    def pub_msg(self, msg):
        try:
            self.mqtt_client.publish(self.pub_topic, msg, qos=0)
            print("Sent: " + msg)
        except Exception as e:
            print("Exception publish: " + str(e))
            raise

    def connect_mqtt(self):

        try:
            with open(self.key_file, "r") as f:
                key = f.read()
            print("Got Key")

            with open(self.cert_file, "r") as f:
                cert = f.read()
            print("Got Cert")

            self.mqtt_client = MQTTClient(
                client_id=self.client_id,
                server=self.host,
                port=self.port,
                keepalive=5000,
                ssl=True,
                ssl_params={"cert":cert, "key":key, "server_side":False})
            self.mqtt_client.connect()
            print('MQTT Connected')

        except Exception as e:
            print('Cannot connect MQTT: ' + str(e))
            raise

    def disconnect(self):
        self.mqtt_client.disconnect()

    # Checks whether a pending message from server is available.
    # If not, returns immediately with None. Otherwise, does
    # the same processing as wait_msg.
    def wait_msg(self):
        self.mqtt_client.wait_msg()

    # Wait for a single incoming MQTT message and process it.
    # Subscribed messages are delivered to a callback previously
    # set by .set_callback() method. Other (internal) MQTT
    # messages processed internally.
    def check_msg(self):
        self.mqtt_client.check_msg()

    # Behaves like wait_msg, but worse
    def subscribe(self):
        self.mqtt_client.subscribe(self.topic, 0)

    def last_msg(self):
        return(str(MESSAGE, 'utf-8'))
