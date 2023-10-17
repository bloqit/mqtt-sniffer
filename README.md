How to install the application on the machine?

1. Install Docker Engine following the instructions available [here](https://docs.docker.com/engine/install/ubuntu/).
2. Clone mqtt sniffer repository in ``/home/ubuntu/mqtt-sniffer`` folder:
```
    cd /home/ubuntu
    git clone https://github.com/bloqit/mqtt-sniffer.git
```
3. Create the ``certificate`` folder and include the certificates that should be used to establish the mqtt connection.
```
    mkdir /home/ubuntu/mqtt-sniffer/certificate
    mv <filename>.pem /home/ubuntu/mqtt-sniffer/certificate/ca_cert.pem
    mv <filename>.pem.key /home/ubuntu/mqtt-sniffer/certificate/key.pem.key
    mv <filename>.pem.crt /home/ubuntu/mqtt-sniffer/certificate/certificate.pem.crt
```
4. Create the ``logs`` folder.
```
    mkdir /home/ubuntu/mqtt-sniffer/logs
```
5. Run docker compose
```
    cd /home/ubuntu/mqtt-sniffer/
    sudo docker compose up -d
```