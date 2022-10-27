import openpyxl
import json
import pyproj
import os
import warnings
from selenium import webdriver
from time import sleep
import csv
import pandas as pd
import re
import requests

query = {
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
def post_network_GW(path):
    warnings.filterwarnings("ignore")
    wb_obj = openpyxl.load_workbook(path)
    sheet_obj = wb_obj.active
    for i in range(sheet_obj.max_row):
        cell_obj = sheet_obj.cell(row=i + 1, column=1)
        if isNetwork(cell_obj.value):
            transf = transform(float(str(sheet_obj.cell(row=i + 1, column=5).value).split(',')[0]),float(str(sheet_obj.cell(row=i + 1, column=5).value).split(',')[1]))
            query.update({"site": "GW"})
            query.update({"network": get_site_name(path) + "_" + str(cell_obj.value)}),
            query.update(
                {"transmitter" : {
                    "lon": transf[0],
                    "lat" : transf[1],
                    "alt": "0.2",
                    "frq": "2400",
                    "txw": 0.00100145,
                    "bwi": "0.1"
                    }
                })
            print("posting " + get_site_name(path) + '_' + str(cell_obj.value) + "...")
            print(transf)
            try:
                os.mkdir("generation")
            except FileExistsError:
                pass
            with open('generation/geojson' + get_site_name(path) + str(cell_obj.value) + '.json', 'w') as mon_fichier:
                json.dump(query, mon_fichier, indent=4)
            post(query)

def post_network_TC():
    pass
def post(json):
        headers = {
            "key"  : "47474-8f9ffce24b48f4dca92bfe201421a5e3f601989d",
            "content-Type" : "application/json, text/javascript, */*; q=0.01"
        }
        req = requests.post(url = "https://api.cloudrf.com/area",json= json,headers=headers)
        print(req.status_code)

def delete(elt):
    headers = {
        "key": "47474-8f9ffce24b48f4dca92bfe201421a5e3f601989d",
        "content-Type": "application/json, text/javascript, */*; q=0.01"
    }
    print("deleting " + elt + "...")
    req = requests.get(url="https://api.cloudrf.com/archive/delete?nid=" + elt, headers=headers)
    print("code : " + str(req.status_code) + " message : " + str(req._content))

def nettoyer(list,string):
    for el in list:
        string.replace(el,'')
    return string
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

truc = {
    "site": "GW",
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
#post(mon_json)
#print(list_network('config_gargenville.xlsx'))
# wb_obj = openpyxl.load_workbook("config_sernhac.xlsx")
# sheet_obj = wb_obj.active
#print(wb_obj.sheetnames[0])
#print(get_site_name("config_sernhac.xlsx"))
#post_network_GW("config_gargenville.xlsx")
delete("Gargenville_MC3_GW2")
#post(truc)