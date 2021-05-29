#!/usr/bin/env python3
# (c) 2021 Rick Sanchez
import os
print("RTMPIE Control could not load. We try to install missing dependencies")
print("After this window closes just open the app again.")
print("========================================================================")
print("Installing: PySimpleGUI, paramiko, scp and cryptography")
input("Press any key to continue...")
os.system("python -m pip install paramiko pysimplegui scp cryptography")
print("========================================================================")
input("Press any key to start Program...")
#streampi1#X
