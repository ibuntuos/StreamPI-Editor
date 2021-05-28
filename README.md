# StreamPI - Kostenlose Restreamlösung für Raspberry Pi
 Hier ist die Anleitung zur Einrichtung einer "StreamPI" auf einer RaspberryPI (3 oder höher).
 Das Programm "StreamPI Editor" dient dann zur Konfiguration

### Einrichtung der StreamPI
#### 1. RaspberryPI besorgen und Grundsystem installieren
  * RaspberryPI muss zunächst eingerichtet werden, am Besten mit dem Raspberry Pi Imager (https://www.raspberrypi.org/documentation/installation/installing-images/)

#### 2. Zugriff auf die RaspberryPI mittels Keyfile und SSH einrichten
  * Eine Gute Anleitung dazu findet sich hier: https://jankarres.de/2013/12/raspberry-pi-ssh-schluessel-erstellen-und-passwort-aendern/
  * Hierbei den "Public Key" nicht als Datei speichern sondern sich aus dem Textfeld von Puttygen in die Zwischenablage kopieren und dann auf der RaspberryPI unter "authorized_keys" wie in der Anleitung beschrieben kopieren.
  * Den "Private Key" als OpenSSH-Key exportieren.
  * Wichtig: Den "Private Key" unbedingt sichern, er wird später im "StreamPI Editor" benötigt.
  * Der "StreamPI Editor" funktioniert ausschließlich mit Keyfiles, eine Verbindung zu einer nicht mit Keyfile gesicherten RaspberryPI ist nicht möglich.
  * Wichtig: sollte man einen eigenen User zur besseren Absicherung der StreamPI einrichten wollen, so muss man diesem das Recht einräumen, ohne Passwort "sudo" Kommandos abzusetzen. Wie das geht ist hier beschrieben: https://www.cyberciti.biz/faq/linux-unix-running-sudo-command-without-a-password/

#### 3. Installation und Einrichtung von NGINX
  * Um einen NGINX-RTMP Server einzurichten wird im Terminal der RaspberryPI folgendes eingegeben:
  ```
  sudo apt-get update
  sudo apt-get install nginx libnginx-mod-rtmp
  sudo nano /etc/nginx/rtmp.conf
  ```

  * In der sich dann öffnenden Datei gebt ihr folgendes ein:

  ```
  rtmp {
  server {
    listen 1935;
    listen [::]:1935 ipv6only=on;
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
  * Dies ist eine Beispieldatei die schon für das Streaming sowohl über IPv4 als auch IPv6 (DS-Lite wie bei Deutscher Glasfaser oder Vodafone Kabel) eingerichtet ist.
  * Ebenfalls sind in dieser Datei schon mal Dummy-URLs für das Verteilen nach Restream oder direkt nach DLive.tv. Konkrete Streaming-Einstellungen für z.B. Facebook kann im Internet finden.
  * Nach der Eingabe das ganze mit STRG+X speichern und bestätigen.
  * Danach die die NGINX-Konfigurationsdatei öffnen mit:

  ```
  sudo nano /etc/nginx/nginx.conf
  ```  

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
  * Nach dem Programmstart müssen im oberen Bereich der Zugangsdaten die konkreten Daten der RaspberryPI eingetragen werden, inkl. dem Pfad zum Private-Key und dem SSH Port.
  * Danach auf "Speichern" bei den Zugangsdaten klicken, damit die Daten beim nächsten Programmstart wieder verfügbar sind.
  * Abschließend auf "Verbinden" klicken - das Programm versucht sich dann zur vorher konfigurierten RaspberryPI zu verbinden und lädt die dort hinterlegte RTMP-Konfiguration.
  * Diese kann nun nach belieben geändert werden, Anleitungen dazu finden sich viele im Internet.
  * Am Ende den unteren "Speichern" Button benutzen, dann wird die Konfiguration auf die RaspberryPI zurückgeschrieben und der RTMP-Server wird durchgestartet.
  * Im Streaming-Programm (z.B. OBS) dann einfach die URL der StreamPI eingeben (z.B: rtmp://localhost:1935/live)


So long und Danke für den vielen Fisch!
Kontakt: wochenschau@protonmail.com
