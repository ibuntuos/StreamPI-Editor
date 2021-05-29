#!/usr/bin/env python3
# (c) 2021 Rick Sanchez

import time, sys, os, pathlib, subprocess
from conf.config import *
from conf.auth import *

WorkPath=os.path.dirname(os.path.realpath(__file__))+'/conf'
try:
    import PySimpleGUI as sg
    import paramiko
    import scp
    import cryptography

except Exception as e:
    print(e)
    os.system("python "+os.path.join(WorkPath, "dependencies.py"))
    import PySimpleGUI as sg
    import paramiko
    import scp

sg.theme('LightBrown')   # Add a touch of color
winicon=WorkPath+'/favicon.ico'
WIN_W = 150
WIN_H = 30

#Delete old rtmp-config
filename = pathlib.Path(WorkPath+'/rtmp.conf')
if filename.is_file():
 os.remove(filename)

frame_layout = [
    [sg.Text('Host         '), sg.InputText(key='hname'), sg.T('                     ')],
    [sg.Text('Port          '), sg.InputText(key='portn'), sg.T('                     ')],
    [sg.Text('User         '), sg.InputText(key='uname'), sg.T('                     ')],
    [sg.Text('Passwort  '), sg.InputText('', key='pwdu', password_char="*"), sg.T('                     ')],
    [sg.Text('Key          '), sg.InputText(key='kfile'), sg.Button("Suche")],
    [sg.T('                     ')],
    [sg.Button('Speichern', key='SettingSave'), sg.Button('Verbinden')]
]
colHeader = [[sg.Image(r''+WorkPath+'/nginx-logo.png'), sg.Text('StreamPI Konfigurations Editor', font=("Helvetica", 25))]]

layout = [  [sg.Column(colHeader),sg.T('                                                                  '), sg.Frame('Zugangsdaten zur StreamPI', frame_layout, font='Any 9', title_color='blue')],
            [sg.Text('')],
            [sg.HorizontalSeparator()],
            [sg.Text('Programm zum direkten Bearbeiten der RTMP-Konfiguration der StreamPI')],
            [sg.HorizontalSeparator()],
            #[sg.Text('Bitte Key eingeben'), sg.InputText(key='input')],
            #[sg.Text('')],
            [sg.Multiline(font=('Consolas', 12), size=(WIN_W, WIN_H), key='_BODY_')],
            [sg.Button('Speichern', disabled=True), sg.Button('Beenden')],
            [sg.Text(size=(40,1), key='-LINE-OUTPUT-')]]

# Create the Window
window = sg.Window('StreamPI Konfigurations Editor 1.0 ©2021 Rick Sanchez', layout=layout, icon=winicon, margins=(0, 0), resizable=True, return_keyboard_events=True, finalize=True)
window['_BODY_'].expand(expand_x=True, expand_y=True)
window['hname'].update(hostname)
window['uname'].update(usrname)
window['portn'].update(p)
window['kfile'].update(k)
window['pwdu'].update(passwd)


while True:
    event, values = window.read()
    if event == 'Speichern':
        filename.write_text(values.get('_BODY_'))
        sg.popup("StreamPI Konfiguration wird upgedatet ...      ", button_type=sg.POPUP_BUTTONS_NO_BUTTONS, auto_close=True,auto_close_duration=3, non_blocking=True, title="Bitte warten", keep_on_top=True )
        scp.put(WorkPath+'/rtmp.conf', '/home/'+usrname)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo mv /home/'+usrname+'/rtmp.conf /etc/nginx/')
        time.sleep(5)
        sg.popup("StreamPI Server wird neu gestartet ...", button_type=sg.POPUP_BUTTONS_NO_BUTTONS, auto_close=True,auto_close_duration=3, non_blocking=True, title="Bitte warten", keep_on_top=True )
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo systemctl restart nginx")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("ls -a")
        time.sleep(5)
        window['-LINE-OUTPUT-'].update("StreamPI Konfiguration upgedatet!")

    if event == 'Suche':
        filename= sg.popup_get_file('Open', no_window=True)
        window['kfile'].update(filename)

    if event == 'Verbinden':
        try:
            sg.popup("Verbindung zur StreamPI wird hergestellt...", button_type=sg.POPUP_BUTTONS_NO_BUTTONS, auto_close=True,auto_close_duration=4, non_blocking=True, title="Bitte warten", keep_on_top=True)
            hostname= values['hname']
            usrname= values['uname']
            p= values['portn']
            k= values['kfile']
            passw=values['pwdu']
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if k == '':
                ssh.connect(hostname, port=p, username=usrname, password=passw)
            else:
                kf = paramiko.RSAKey.from_private_key_file(k)
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname, port=p, username=usrname, pkey = kf)

            time.sleep(4)
            window['-LINE-OUTPUT-'].update("Verbindung mit StreamPI hergestellt.")
            scp = scp.SCPClient(ssh.get_transport())
            scp.get('/etc/nginx/rtmp.conf', WorkPath)
            time.sleep(2)
            filename = pathlib.Path(WorkPath+'/rtmp.conf')
            window['_BODY_'].update(value=filename.read_text())
            window['Speichern'].update(disabled=False)
        except Exception as e:
            print(e)
            window['-LINE-OUTPUT-'].update("Keine Verbindung zur StreamPI möglich!")
            window['Speichern'].update(disabled=True)

    if event == 'SettingSave':
        hostname= values['hname']
        p= values['portn']
        usrname= values['uname']
        passw=values['pwdu']
        k= values['kfile']
        writestuff(keyID, WorkPath, hostname, p, usrname, passw, k)
        window['-LINE-OUTPUT-'].update("Zugangsdaten gespeichert!")
    if event == sg.WINDOW_CLOSED or event == 'Beenden':
        break


window.close()
