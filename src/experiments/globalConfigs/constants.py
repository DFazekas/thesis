from __future__ import absolute_import
import os
import sys

PREFIX = "thesis"
PORT = 8883
SUMO_HOME = os.path.realpath(os.environ.get(
    "SUMO_HOME", os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))
sys.path.append(os.path.join(SUMO_HOME, "tools"))
try:
    from sumolib import checkBinary
except ImportError:
    def checkBinary(name):
        return name
NETCONVERT = checkBinary("netconvert")
SUMO = checkBinary("sumo")
SUMOGUI = checkBinary("sumo-gui")
HOUR = 3600
ER = "ER"
C_ER = "C_ER"
CIVILIAN = "Civilian"
C_CIVILIAN = "C_Civilian"
DETOUR = "detour"
SAFETY_TIME_HEADWAY = 20  # seconds
