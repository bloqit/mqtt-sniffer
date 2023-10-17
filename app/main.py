from logger import Logger
import signal
import sys
import time
from mqtt_client import MQTTClient
import ssl

log_dir = "logs"
sniffer_log_file = 'sniffer_log_file.json'
sniffer_app_log_file = 'sniffer_app_log_file.json'

sniffer_logger = Logger("sniffer_log", log_dir, sniffer_log_file)
sniffer_app_logger = Logger("sniffer_app", log_dir, sniffer_app_log_file)

def set_exit_handler(func):
    signal.signal(signal.SIGTERM, func)

def on_exit(sig, func=None):
    # Log
    sniffer_app_logger.info("Application has been stopped.")
    mqtt_client.disconnect()
    sys.exit(1)

def on_message(client, userdata, msg):
    sniffer_app_logger.info("Message received on topic={0} qos={1}.".format(msg.topic, msg.qos))
    sniffer_logger.info('Message Received', extra={'topic': msg.topic, 'payload': msg.payload.decode()})

if __name__ == "__main__":
    # Log
    sniffer_app_logger.info("Application has been started.")

    # Exit Handler
    set_exit_handler(on_exit)

    # MQTT client
    
    mqtt_client = MQTTClient(        
        hostname= "a3bb627xnif6gp-ats.iot.eu-central-1.amazonaws.com",
        port = 8883,
        keep_alive = 60,        
        tls = {
            "ca_certs" : "certificate/ca_cert.pem", 
            "certfile" : "certificate/certificate.pem.crt", 
            "keyfile" : "certificate/key.pem.key", 
            "cert_reqs" : ssl.CERT_REQUIRED, 
            "tls_version" : ssl.PROTOCOL_TLSv1_2,
            "ciphers" : None,
            "keyfile_password" : None
        },
        logger = sniffer_app_logger,
        qos = 1,
        client_id = "sniffer")
    
    subscribed_topic = "#"
    mqtt_client.subscribed_topics = [subscribed_topic]
    mqtt_client.add_message_callback(subscribed_topic, on_message)
    mqtt_client.connect()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            # Log
            sniffer_app_logger.info("Application has been interrupted.")
            mqtt_client.disconnect()         
            sys.exit(0)
