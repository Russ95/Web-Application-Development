#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import requests
import json
import os
import psutil
import datetime
import time
from AppKit import NSWorkspace
import appscript
from urllib.parse import urlparse


#url for test
geturl = 'http://127.0.0.1:8000/'
posturl = 'http://127.0.0.1:8000/time_manage/add-item'
'''
geturl = 'http://18.222.252.3/'
posturl = 'http://18.222.252.3/time_manage/add-item'
'''

headers={
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',    #!!!
}


def getfrontname():
    
    app_name = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
    app_pid = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationProcessIdentifier']
    print(app_name)

    
    #return app_name

def getwindow():
    #get the name and pid of the frontmost app
    #active_app_name = NSWorkspace.sharedWorkspace().frontmostApplication().localizedName()
    #active_pid = NSWorkspace.sharedWorkspace().frontmostApplication().processIdentifier()
    active_app_name = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
    active_pid = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationProcessIdentifier']

    if active_app_name == "Google Chrome":
        print("chrome")
        totalurl = appscript.app("Google Chrome").windows[0].active_tab.URL()
        hosturl = urlparse(totalurl).netloc
        
        print(hosturl)
        print()
        
    elif active_app_name == "Safari":
        print("chrome")
        totalurl = appscript.app("Safari").windows.first.current_tab.URL()
        hosturl = urlparse(totalurl).netloc
        print(hosturl)
        print()


    #use psutil to get more info
    pidlist = psutil.pids()
    if active_pid in pidlist:
        process = psutil.Process(active_pid)
        
        try:
            p_time = datetime.datetime.fromtimestamp(process.create_time()).isoformat()
            
            print("name:",process.name())
            print("pid:",active_pid)
        except:
            print("error")

        if active_app_name == "Google Chrome" or active_app_name == "Safari":
            name = hosturl
        else:
            name = process.name()
            


        #print(datetime.datetime.now().isoformat())
        test_data = {"process_name":name,
                    "update_time":datetime.datetime.now().isoformat(),
                    "create_time":p_time,
                    "type":"data",
                    "username":"123"}

        #print(type(test_data))
        jsondata = json.dumps(test_data)

        #print(jsondata)
        return jsondata
    else:
        return None

def sendmsg(jsondata):
    #GET
    response = requests.get(geturl)
    #print(response.text)
    #print(response.headers)
    cookie_value = "mLEf68ArHFvgs8ewnY11sWBWpyXk2fpijbcS6XngiIrUgLzmFCRq8gwT63ypVxwu"
    headers['Cookie'] = 'csrftoken=' + cookie_value

    '''
    for key,value in response.cookies.items():
        cookie_value = value
        print("1")
    headers['Cookie'] = key + '=' + cookie_value
    print(response.text)
    print(response.status_code)
    '''

    #POST
    postdata = [('item', jsondata),
            ('csrfmiddlewaretoken', cookie_value),
             ]
    #print(postdata)

    response = requests.post(posturl, data = postdata, headers = headers)

    #print info
    #print(response.text)
    #print(response.status_code)


while True:
    #getfrontname()
    try:
        data = getwindow()
        sendmsg(data)
        time.sleep(10)
    except:
        print("error")
        time.sleep(10)
