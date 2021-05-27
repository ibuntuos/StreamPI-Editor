#!/usr/bin/env python3
# (c) 2021 OJ
import os
print("RTMPIE Control could not load. We try to install missing dependencies")
print("After this window closes just open the app again.")
print("========================================================================")
print("Installing: PySimpleGUI, paramiko and scp")
input("Press any key to continue...")
os.system("python -m pip install paramiko pysimplegui scp")
print("========================================================================")
input("Press any key to start Program...")
