# -*- coding: utf-8 -*-
from datetime import datetime
from xat_ecu.legacy.common.logger import logger

final_mid = 0


def gen_client_id(prefix="jd-robot-"):
    return prefix + str(int(datetime.timestamp(datetime.utcnow())))


def on_connect(mqttc, user_data, flags, rc):
    if user_data is True:
        logger.debug("rc: " + str(rc))

    else:
        logger.debug("rc: " + str(rc))


def on_message(mqttc, user_data, msg):
    logger.debug("topic: %s, dup: %d, mid: %d, qos: %d, payload: %s" % (
        msg.topic,
        msg.dup,
        msg.mid,
        msg.qos,
        msg.payload,
    ))
    global final_mid
    if msg.retain == 0:
        pass  # sys.exit()
    else:
        if user_data is True:
            logger.debug("Clearing topic " + msg.topic)
        (rc, final_mid) = mqttc.publish(msg.topic, None, 1, True)


def on_publish(mqttc, user_data, mid):
    global final_mid
    if mid == final_mid:
        logger.debug("duplicate message: " + str(mid))
    logger.debug("published mid: " + str(mid))


def on_message_tbox(mqttc, user_data, msg):
    global final_mid
    if msg.retain == 0:
        pass
        # sys.exit()
    else:
        if user_data is True:
            logger.debug("Clearing topic " + msg.topic)
        (rc, final_mid) = mqttc.publish(msg.topic, None, 1, True)
    logger.debug(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    logger.debug("on_message_tbox")


def on_subscribe(mqttc, user_data, mid, granted_qos):
    logger.debug("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    logger.debug(string)
