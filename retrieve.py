## AUTHOR: BRIAN SMITH
## CREATED: 25/01/2024
## Adapted from:
##      SLTrack.py
##      (c) 2019 Andrew Stokes  All Rights Reserved
##      https://www.space-track.org/documentation#howto
##
##
##  Simple Python script to retreive and visualise mean altitude data for the ISS in the year 2023
##
##
##  Copyright Notice:
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  For full licencing terms, please refer to the GNU General Public License
##  (gpl-3_0.txt) distributed with this release, or see
##  http://www.gnu.org/licenses/.
##

import requests
import json
import configparser
from datetime import datetime
import pandas as pd

class MyError(Exception):
    def __init___(self,args):
        Exception.__init__(self,"my exception was raised with arguments {0}".format(args))
        self.args = args

# See https://www.space-track.org/documentation for details on REST queries
# the "Gp_HistISS" retrieves historical gp data for NORAD CAT ID=25544 (ISS) in the year 2023, JSON format.
uriBase                = "https://www.space-track.org"
requestLogin           = "/ajaxauth/login"
requestCmdAction       = "/basicspacedata/query" 
requestGp_HistISS      = "/class/gp_history/NORAD_CAT_ID/25544/EPOCH/%3E2023-01-01%2C%3C2024-01-01/orderby/EPOCH%20asc/format/json"

# Use configparser package to pull in the ini file (pip install configparser)
config = configparser.ConfigParser()
config.read("./SLTrack.ini")
configUsr = config.get("configuration","username")
configPwd = config.get("configuration","password")
configOut = config.get("configuration","output")
siteCred = {'identity': configUsr, 'password': configPwd}

altData = {'date': [], 'meanAltitude': [], 'apogee': [], 'perigee': []} # dict of lists for storing altitude data

# use requests package to drive the RESTful session with space-track.org
with requests.Session() as session:
    print("Started space-track.org session...") 
    # run the session in a with block to force session to close if we exit

    # need to log in first. note that we get a 200 to say the web site got the data, not that we are logged in
    resp = session.post(uriBase + requestLogin, data = siteCred)
    if resp.status_code != 200:
        raise MyError(resp, "POST fail on login")

    # this query picks up ISS gp data from 2023. Note - a 401 failure shows you have bad credentials 
    resp = session.get(uriBase + requestCmdAction + requestGp_HistISS)
    if resp.status_code != 200:
        print(resp)
        raise MyError(resp, "GET fail on request for Starlink satellites")

    # use the json package to break the json formatted response text into a Python structure
    retData = json.loads(resp.text)
    for gp_item in retData:
        datetimeObject = datetime.strptime(gp_item['EPOCH'], '%Y-%m-%dT%H:%M:%S.%f') # map date format given by gp to expected datetime object.
        altData['date'].append(datetimeObject.date())
        altData['apogee'].append(float(gp_item['APOAPSIS']))
        altData['perigee'].append(float(gp_item['PERIAPSIS']))
        meanAltitude = (float(gp_item['APOAPSIS']) + float(gp_item['PERIAPSIS']))/2.0 # Determine mean altitude, mean of apogee and perigee
        altData['meanAltitude'].append(meanAltitude)

    # pickle data to file, no need to request everytime a plot is made or changed.
    altData = pd.DataFrame(altData)
    altData.to_pickle('altData.pkl')
    session.close()

print("Completed session.")