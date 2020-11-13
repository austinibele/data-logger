"""
MQTT client for sending measurements to a MQTT broker.
"""

__author__ = 'Holger Fleischmann'
__copyright__ = 'Copyright 2018, Holger Fleischmann, Bavaria/Germany'
__license__ = 'Apache License 2.0'

import logging
import json
from datetime import datetime
from functools import partial

import paho.mqtt.client as mqtt

from signalsources import SignalSource, SignalValue

logger = logging.getLogger().getChild(__name__) 


class MqttClient:
    """
    Sends all signal changes to a MQTT broker.
    """

    def __init__(self):
        self.broker_host = 'localhost'
        self.broker_user = ''
        self.broker_password = ''
        self.broker_base_topic = 'datalogger'
        self.client = mqtt.Client()
        # self.client.enable_logger(logger)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        self.__started = False
    
    def use_signals_config(self, signal_sources_config):
        self.broker_host = signal_sources_config['mqtt_broker_host']
        self.broker_user = signal_sources_config['mqtt_broker_user']
        self.broker_password = signal_sources_config['mqtt_broker_password']
        self.broker_base_topic = signal_sources_config['mqtt_broker_base_topic']
        for group in signal_sources_config['groups']:
            for source in group['sources']:
                topic = self.broker_base_topic + '/' + source.identifier
                source.add_callback(partial(self._publish_signal_value, source))
    
    def start(self):
        if not self.__started:
            if self.broker_host == '':
                logger.info("NOT starting MQTT client because of config with empty broker")
            else:
                logger.info("Starting MQTT client for broker " + self.broker_host)
                if self.broker_user != '':
                    self.client.username_pw_set(self.broker_user, self.broker_password)
                self.client.connect_async(self.broker_host)
                self.client.loop_start()
                self.__started = True
        
    def stop(self):
        if self.__started:
            logger.info("Stopping MQTT client for broker " + self.broker_host)
            self.__started = False
            self.client.disconnect()
            self.client.loop_stop(True)
    
    def _publish_signal_value(self, source, signal_value):
        if self.__started:
            topic = self.broker_base_topic + '/' + source.identifier
            json_value = json.dumps({
                'value':     signal_value.value,
                'status':    signal_value.status,
                'formatted': '---' if signal_value.status != SignalSource.STATUS_OK else source.format(signal_value.value),
                'timestamp': datetime.fromtimestamp(signal_value.timestamp).isoformat(),
                'unit':      source.unit
            })
            self.client.publish(topic, json_value, 0, True)
        
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT broker " + self.broker_host)
        else:
            logger.error("Failed to connect to MQTT broker " + self.broker_host + " rc=" + str(rc))
        # this would be the place to client.subscribe("#")
    
    def _on_disconnect(self, client, userdata, rc):
        if rc == 0:
            logger.info("Disconnected from MQTT broker " + self.broker_host)
        else:
            logger.error("Connection lost to MQTT broker " + self.broker_host + " rc=" + str(rc))
            
    def _on_message(self, client, userdata, message):
        # this would be the place to receive subscription messages
        pass

