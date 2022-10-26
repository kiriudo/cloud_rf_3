import openpyxl
import json
import pyproj
import warnings
from selenium import webdriver
from time import sleep
import csv
import pandas as pd

mon_json ={"site":"Site","ui":3,"network":"sernhac_gw3","engine":"2","transmitter":{"lat":"38.990511","lon":"1.447991","alt":"0.2","frq":"2400","txw":0.00100145,"bwi":"0.1"},"receiver":{"lat":0,"lon":0,"alt":"1","rxg":"2","rxs":"-103"},"antenna":{"txg":"1.8","txl":"0.1","ant":"39","azi":"165","tlt":"33","hbw":"0","vbw":"0","fbr":"1.8","pol":"v"},"model":{"pm":"2","pe":"2","ked":"0","rel":"95"},"environment":{"clm":"1","cll":"2","clt":"Minimal.clt"},"output":{"units":"m","col":"RAINBOW.dBm","out":"2","ber":None,"mod":None,"nf":"-120","res":"20","rad":"2"}}


with open('antenna.json', 'w') as mon_fichier:
    json.dump(mon_json, mon_fichier, indent=4)