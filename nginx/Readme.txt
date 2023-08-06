23:30 06.08.2023

Docker muss auf Streampi installiert sein.
Am besten auch Portainer installieren. Und Deunhealth und Watchtower für Auto-Updates:

curl -fsSL https://get.Docker.com -o get-Docker.sh
sudo sh get-Docker.sh
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
docker volume create portainer_data
docker run -d -p 8000:8000 -p 9443:9443 --name portainer  -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data cr.portainer.io/portainer/portainer-ce:latest


Stack für deunhealth:
version: "3.7"
services:
  deunhealth:
    image: qmcgaw/deunhealth
    container_name: deunhealth
    network_mode: "none"
    environment:
      - LOG_LEVEL=info
      - HEALTH_SERVER_ADDRESS=127.0.0.1:9999
      - TZ=Europe/Berlin
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

Label: deunhealth.restart.on.unhealthy  true


Command für Watchtower

docker run --detach  --name watchtower --volume /var/run/docker.sock:/var/run/docker.sock containrrr/watchtower


dann den Ordner nginx nach /etc/  kopieren. 
Chmod 777 


