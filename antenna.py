import openpyxl
import json
import pyproj
import warnings
from selenium import webdriver
from time import sleep
import csv
import pandas as pd
import requests

dict = {
    "site": "Site",
    "ui": 3,
    "network": "sernhac_MC1_GW3",
    "engine": "2",
    "transmitter": {
        "lat": "38.990511",
        "lon": "1.447991",
        "alt": "0.2",
        "frq": "2400",
        "txw": 0.00100145,
        "bwi": "0.1"
    },
    "receiver": {
        "lat": 0,
        "lon": 0,
        "alt": "1",
        "rxg": "2",
        "rxs": "-103"
    },
    "antenna": {
        "txg": "1.8",
        "txl": "0.1",
        "ant": "39",
        "azi": "165",
        "tlt": "33",
        "hbw": "0",
        "vbw": "0",
        "fbr": "1.8",
        "pol": "v"
    },
    "model": {
        "pm": "2",
        "pe": "2",
        "ked": "0",
        "rel": "95"
    },
    "environment": {
        "clm": "1",
        "cll": "2",
        "clt": "Minimal.clt"
    },
    "output": {
        "units": "m",
        "col": "RAINBOW.dBm",
        "out": "2",
        "ber": None,
        "mod": None,
        "nf": "-120",
        "res": "20",
        "rad": "2"
    }
}

def transform(x,y):
    inProj = pyproj.Proj(init='epsg:2154')
    outProj = pyproj.Proj(init='epsg:4326')
    x2, y2 = pyproj.transform(inProj, outProj, x, y)
    return [x2, y2]

def get_site_name(path):
    wb_obj = openpyxl.load_workbook(path)
    sheet_obj = wb_obj.active
    for i in range(sheet_obj.max_row):
        cell_obj = sheet_obj.cell(row=i + 1, column=1)
        if cell_obj.value == "solar_park_name":
            return sheet_obj.cell(row=i + 1, column=2).value

#vérifier que la chaine correspond bien à un réseau
def isNetwork(string) :
    if string is not None:
        mc = str(string).find("MC")
        gw = str(string).find("GW")
        return gw != -1 and mc != -1

#liste des réseaux et la coordonnée de leur GW
def list_network(path):
    network = dict()
    wb_obj = openpyxl.load_workbook(path)
    sheet_obj = wb_obj.active
    for i in range(sheet_obj.max_row):
        cell_obj = sheet_obj.cell(row=i + 1, column=1)
        if isNetwork(cell_obj.value):
            dict.update({"Name": get_site_name(path) + str(cell_obj.value).split('_')[0] })
            dict.update({"lat" : str(sheet_obj.cell(row=i + 1, column=5).value).split(',')[1]})
            dict.update({"lon": str(sheet_obj.cell(row=i + 1, column=5).value).split(',')[0]})
    return network

def post(json):
        headers = {
            "key"  : "47474-8f9ffce24b48f4dca92bfe201421a5e3f601989d",
            "content-Type" : "application/json, text/javascript, */*; q=0.01"
        }
        req = requests.post(url = "https://api.cloudrf.com/area",json= json,headers=headers)
        print(req.status_code)

def get(json):
        pass
       # req = requests.get(url = "https://api.cloudrf.com/area",json= json,)

def post_all_TC():
    pass
def post_TC(MC, GW, TC_id, lat, long, site):
    TC = {
        "site": "TC" + str(TC_id),
        "ui": 3,
        "network": str(site)+"_"+str(MC)+"_"+str(GW),
        "engine": "2",
        "transmitter": {
            "lat": str(lat),
            "lon": str(long),
            "alt": "0.2",
            "frq": "2400",
            "txw": 0.00100145,
            "bwi": "0.1"
        },
        "receiver": {
            "lat": 0,
            "lon": 0,
            "alt": "1",
            "rxg": "2",
            "rxs": "-103"
        },
        "antenna": {
            "txg": "1.8",
            "txl": "0.1",
            "ant": "39",
            "azi": "165",
            "tlt": "33",
            "hbw": "0",
            "vbw": "0",
            "fbr": "1.8",
            "pol": "v"
        },
        "model": {
            "pm": "2",
            "pe": "2",
            "ked": "0",
            "rel": "95"
        },
        "environment": {
            "clm": "1",
            "cll": "2",
            "clt": "Minimal.clt"
        },
        "output": {
            "units": "m",
            "col": "RAINBOW.dBm",
            "out": "2",
            "ber": None,
            "mod": None,
            "nf": "-120",
            "res": "20",
            "rad": "2"
        }
    }
    post(TC)

#post(mon_json)
#print(list_network('config_gargenville.xlsx'))
# wb_obj = openpyxl.load_workbook("config_sernhac.xlsx")
# sheet_obj = wb_obj.active
#print(wb_obj.sheetnames[0])
print(get_site_name("config_sernhac.xlsx"))
