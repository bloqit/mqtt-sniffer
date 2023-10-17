import paho.mqtt.client as mqtt

class MQTTClient():
    def __init__(self, 
                 hostname=None, 
                 port=None, 
                 keep_alive=None,
                 auth=None,
                 tls=None,
                 name = "MQTT Client",
                 qos = 0,
                 logger=None,
                 client_id=""):
        
        self.hostname = hostname
        self.port = port
        self.keep_alive = keep_alive
        self.auth = auth
        self.tls = tls        
        self.name = name
        self.qos = qos
        self.logger = logger
        self.client_id = client_id

        self.subscribed_topics = []
        
        self._client = mqtt.Client(client_id = client_id) 
        
        self.on_connect_sucessful = None
         
        self._client.on_connect = self._on_connect
        self._client.on_subscribe = self._on_subscribe
        self._client.on_message = self._on_message
        self._client.on_publish = self._on_publish
        self._client.on_disconnect = self._on_disconnect
         
    def connect (self):

        if self.auth is not None and self.auth["username"] is not None and self.auth["password"] is not None: 
            self._client.username_pw_set(self.auth["username"], self.auth["password"])
        else:
            if self.tls is None:
                raise Exception("tls connot be None")
        
            self._client.tls_set(ca_certs=self.tls["ca_certs"], 
                                 certfile=self.tls["certfile"],
                                 keyfile=self.tls["keyfile"], 
                                 cert_reqs=self.tls["cert_reqs"], 
                                 tls_version=self.tls["tls_version"], 
                                 ciphers=self.tls["ciphers"],
                                 keyfile_password=self.tls["keyfile_password"])   

        self._client.loop_start()
        
        self._try_connect()
      
    def disconnect (self):
        self._client.disconnect()
        self._client.loop_stop()
     
    def subscribe(self, topics):
        self.subscribed_topics = topics
        topics = []

        for t in self.subscribed_topics:
            if isinstance(t, tuple):
                topics = self.subscribed_topics

                if self.logger is not None:
                    # Log
                    self.logger.info("{0}: subscribing to {1} ...".format(self.name, t[0]))
            else:
                topics.append((t, self.qos))

                if self.logger is not None:
                    # Log
                    self.logger.info("{0}: subscribing to {1} ...".format(self.name, t))
            
        # Subscribe topic
        self._client.subscribe(topics)
    
    def add_message_callback(self, topic, method):
        self._client.message_callback_add(topic, method)

    def publish_message(self, topic, message):

        # Send message
        (result, mid) = self._client.publish(topic, message, self.qos)
        
        if self.logger is not None:
            # Log
            self.logger.info("{0}: publishing to {1} (mid = {2} message = {3}).".format(self.name, topic, mid, message))

        error = False

        if result == mqtt.MQTT_ERR_SUCCESS:
            error = False

            if self.logger is not None:
                # Log
                self.logger.info("{0}: message has been published (mid = {1}).".format(self.name, mid))
        else:
            error = True

            if self.logger is not None:
                # Log
                self.logger.info("{0}: message has not been published (mid = {1}).".format(self.name, mid))

        return error

    def enable_logger(self):
        self._client.enable_logger(self.logger.logger)

    def _try_connect(self):
        try:
            if self.logger is not None:
                # Log
                self.logger.info("{0}: connecting to {1} (Port = {2} Keep alive = {3}) ...".\
                        format(self.name, self.hostname, self.port, self.keep_alive))

            # Connect
            self._client.connect(self.hostname, self.port, self.keep_alive)
        except Exception as e:
            if self.logger is not None:
                # Log
                self.logger.exception(e)

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            if self.logger is not None:
                # Log
                self.logger.info("{0}: connected (rc = {1}).".format(self.name, rc))  # 0: Connection successful

            if self.on_connect_sucessful is not None:
                self.on_connect_sucessful(userdata)
               
            if len(self.subscribed_topics) > 0:
                self.subscribe(self.subscribed_topics)          
        else:
            # Log
            if self.logger is not None:
                self.logger.warning("{0}: not connected. Bad connection (rc = {1}).".format(self.name, rc))
                # 1: Connection refused : incorrect protocol version
                # 2: Connection refused : invalid client identifier
                # 3: Connection refused : server unavailable
                # 4: Connection refused : bad username or password
                # 5: Connection refused : not authorised
                # 6-255: Currently unused.

    def _on_subscribe(self, client, obj, mid, granted_qos):
        # Log
        if self.logger is not None:
            for i, topic in enumerate(self.subscribed_topics):                    
                if isinstance(topic, tuple):
                    # Log
                    self.logger.info("{0}: subscribed {1} (qos = {2}).".format(self.name, topic[0], granted_qos[i]))
                else:
                    # Log
                    self.logger.info("{0}: subscribed {1} (qos = {2}).".format(self.name, topic, granted_qos[i]))

    def _on_publish(self, client, obj, mid):
        # Log
        if self.logger is not None:
            self.logger.info("{0}: message has been sent (mid = {1}).".format(self.name, mid))
         
    def _on_message(self, client, userdata, msg):
        # Log
        if self.logger is not None:
            self.logger.info("{0}: message received from {1} qos={2} payload={3}".format(self.name, msg.topic, msg.qos, msg.payload))
  
    def _on_disconnect(self, client, userdata, rc):
        # Log
        if self.logger is not None:
            self.logger.info("{0}: disconnected. (rc = {1})".format(self.name, rc))