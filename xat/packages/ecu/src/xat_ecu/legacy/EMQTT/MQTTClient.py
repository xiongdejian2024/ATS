import six
from xat_ecu.legacy.utils.utils import *
from xat_ecu.legacy.common.logger import logger
from paho.mqtt.client import Client
from xat_ecu.legacy.EMQTT.Callbacks import gen_client_id, on_connect, on_message, on_publish, on_subscribe, on_message_tbox


@six.add_metaclass(SingleMeta)
class MQTTClient(object):

    def __init__(self, client_id=None, clean_session=True, user_data=None, protocol=4, transport="tcp", func_obj=on_message):
        self.clean_session = clean_session
        self.user_data = user_data
        self.protocol = protocol
        self.transport = transport
        self._conn = None
        self._client = None
        self._client_id = None
        self.setup_client(client_id, func_obj=func_obj)

    @property
    def client_id(self):
        if not self._client_id:
            raise AssertionError("invalid client id, use keyword *setup_client* first.")
        return self._client_id

    def setup_client(self, client_id=None, func_obj=on_message):
        self._client_id = str(client_id) if client_id else gen_client_id()
        self._client = Client(client_id=self._client_id,
                              clean_session=self.clean_session,
                              userdata=self.user_data,
                              protocol=self.protocol,
                              transport=self.transport)
        self._client.enable_logger(logger)
        self._client.on_connect = on_connect
        self._client.on_message = func_obj
        self._client.on_publish = on_publish
        self._client.on_subscribe = on_subscribe
        logger.debug("*Initialized instance: %s*" % str(id(self._client)))

    def connect(self, hostname, port=1883, keep_alive=60, bind_address=""):
        if not hostname:
            logger.info("hostname is not specified. exit!")
            raise AssertionError("hostname missed.")
        self._conn = self._client.connect(host=hostname,
                                          port=int(port),
                                          keepalive=keep_alive,
                                          bind_address=bind_address)
        self.start()

    def disconnect(self):
        self._client.disconnect()
        self.stop()
        logger.info("disconnected by " + self._client_id)
        logger.info("*terminated instance: %s*" % str(id(self._client)))

    def is_connected(self):
        return self._client.is_connected()

    def subscribe(self, topic_name):
        if not isinstance(topic_name, list):
            topic_name_list = [topic_name]
        else:
            topic_name_list = topic_name
        for name in topic_name_list:
            self._client.subscribe(topic=str(name))

    def add_subscribe(self, topic_name, call_back=on_message_tbox):
        if topic_name:
            self._client.message_callback_add(str(topic_name), call_back)

    def start(self):
        self._client.loop_start()

    def stop(self):
        self._client.loop_stop()

    def publish(self, topic_name, payload, qos=2):
        self._client.publish(topic=topic_name, payload=payload, qos=qos)

    @property
    def client(self):
        return self._client
