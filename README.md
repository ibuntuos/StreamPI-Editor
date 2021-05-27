# StreamPI - Kostenlose Restreamlösung für Raspberry Pi
 Hier ist die Anleitung zur Einrichtung einer "StreamPI" auf einer RaspberryPI (3 oder höher).
 Das Programm "StreamPI Editor" dient dann zur Konfiguration

### Einrichtung der StreamPI
#### 1. RaspberryPI besorgen und Grundsystem installieren
  * RaspberryPI muss zunächst eingerichtet werden, am Besten mit dem Raspberry Pi Imager (https://www.raspberrypi.org/documentation/installation/installing-images/)

#### 2. Zugriff auf die RaspberryPI mittels Keyfile und SSH einrichten
  * Eine Gute Anleitung dazu findet sich hier: https://jankarres.de/2013/12/raspberry-pi-ssh-schluessel-erstellen-und-passwort-aendern/
  * Wichtig: Den "Private Key" unbedingt sichern, er wird später im "StreamPI Editor" benötigt.
  Der "StreamPI Editor" funktioniert ausschließlich mit Keyfiles, ein Verbindung zu einer nicht mit Keyfile gesicherter RaspberryPI ist nicht möglich.

#### 3. Installation und Einrichtung von NGINX
  * Um einen NGINX-RTMP Server einzurichten wird im Terminal der RaspberryPI folgendes eingegeben:
  ```
  sudo apt-get update
  sudo apt-get install nginx libnginx-mod-rtmp
  sudo nano /etc/nginx/rtmp.conf
  ```

  * In der sich dann öffnenden Datei gebt Ihr folgendes ein:

  ```
  rtmp {
  server {
    listen 1935;
    #listen [::]:1935 ipv6only=on;
    chunk_size 4096;
    allow play all;
    allow publish all;
    application live {
    live on;
    record off;

    #####################Direct Restream#########################

        #Restream
        #push rtmp://live.restream.io/live/{Streamkey};

        #DLive
        #push rtmp://stream.dlive.tv/live/{Streamkey};

    #############################################################
            }

        }
    }
  ```
  * Dies ist eine Beispieldatei die schon für das Streaming sowohl über IP4 als auch IPv6 (DS-Lite wie bei Deutscher Glasfaser oder Vodafone Kabel) eingerichtet ist.
  * Ebenfalls sind in dieser Datei schon mal Dummy-URLs für das Verteilen nach Restream oder direkt nach DLive.tv. Streaming-Einstellungen für z.B. Facebook kann im Internet finden.
  * Nach der Eingabe das ganze mit STRG+X speichern und bestätigen.
  * Danach die die NGINX-Konfigurationsdatei öffnen mit
  "sudo nano /etc/nginx/nginx.conf"

  Und dort dann als erste Zeile eingeben:

  ```
    include /etc/nginx/rtmp.conf;
  ```

  * Anschließend den Server neustarten:

  ```
    sudo systemctl restart nginx
  ```

  * Es gibt noch das Problem, das NGINX oft bei den RaspberryPIs aufgrund eines zu geringen Timeouts nicht beim Booten startet. Dies ist einfach zu beheben. Einfach folgende Datei editieren:

  ```
  sudo nano /lib/systemd/system/nginx.service
  ```
  Dort im Bereich "[Service]" folgende Zeile ergänzen:
  ```
  TimeoutStopSec=5
  ```

#### 4. Download und Installation von Python (min. 3.8)
  * Python kann man hier downloaden: https://www.python.org/downloads/
  * Der "StreamPI Editor" ist auf die Verwendung mit Windows optimiert, sollte aber auch unter Mac und Linux funktionieren

#### 5. Download des StreamPI Editors
  * Einfach das Repository hier als ZIP downloaden, entpacken und die "StreamPI Editor.pyw" Datei aufrufen.

### Verwendung
  * Nach dem Programmstart müssen im Bereicht der Zugangsdaten die konkreten Daten der RaspberryPI eingetragen werden, inkl. dem Pfad zum Private-Key.
  * Danach auf "Speichern" bei den Zugangsdaten klicken, damit die Daten beim nächsten Programmstart wieder verfügbar sind.
  * Abschließend auf "Verbinden" klicken - das Programm versucht sicht zur vorher konfigurierten RaspberryPI zu verbinden und lädt die dort hinterlegte RTMP-Konfiguration. Diese kann nun nach belieben geändert werden, Anleitungen dazu finden sich viele im Internet.
  * Am Ende den unteren "Speichern" Button benutzen, dann wird die Konfiguration auf die RaspberryPI zurückgeschrieben und der RTMP-Server wird durchgestartet.


So long und Danke für den vielen Fisch!
Kontakt: wochenschau@protonmail.com
