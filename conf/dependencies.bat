@echo off
echo StreamPI Editor konnte nicht geladen werden. Es wird versucht fehlende
echo Abhaengigkeiten nachzuinstallieren.
echo ========================================================================
echo Es wird installiert: PySimpleGUI, paramiko, scp und cryptography
echo Danach startet der StreamPI Editor automatisch
pause
python -m pip install paramiko pysimplegui scp cryptography
echo ========================================================================
pause