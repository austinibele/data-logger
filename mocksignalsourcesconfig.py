"""
Test configuration for development containing random test signals.
To be used as import in main.py for simulation.
"""

__author__ = 'Holger Fleischmann'
__copyright__ = 'Copyright 2021, Holger Fleischmann, Bavaria/Germany'
__license__ = 'Apache License 2.0'

from signalsources import TestSource

_sensor_1    = TestSource(       'sensor_1',              80,  1, label='Sensor 1',        unit='°C', value_format='{:.1f}',    color=[0.5, 0.5, 1.0, 1.0], z_order=1)
_sensor_2    = TestSource(       'sensor_2',              80,  1, label='Sensor 2',        unit='°C', value_format='{:.1f}',    color=[0.0, 0.2, 1.0, 1.0], z_order=2)
_sensor_3    = TestSource(       'sensor_3',              80,  1, label='Sensor 3',        unit='°C', value_format='{:.1f}',    color=[1.0, 0.0, 0.0, 1.0], z_order=2)
_sensor_4    = TestSource(       'sensor_4',              80,  1, label='Sensor 4',        unit='°C', value_format='{:.1f}',    color=[0.2, 0.3, 0.9, 1.0], z_order=0)

signal_sources_config = {
    'groups' : [
        {'label' : 'Chuck Temperature',
         'sources' : [
                _sensor_1,
                _sensor_2,
                _sensor_3,
                _sensor_4
        ]}
        ],
    
    'mqtt_broker_host' : '',
    'mqtt_broker_port' : 1883,
    'mqtt_broker_user' : '',
    'mqtt_broker_password' : '',
    'mqtt_broker_base_topic' : 'data-logger-test',
    'mqtt_use_ssl' : True,
    'mqtt_broker_ca_certs' : 'cacerts.pem'
}
