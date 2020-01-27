import sys
import os
import subprocess
import re
import json

def get_active_window():
    root = subprocess.Popen(
        ['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()

    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    if m != None:
        window_id = m.group(1)
        window = subprocess.Popen(
            ['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE)
        stdout, stderr = window.communicate()
    else:
        return None

    match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", stdout)
    if match != None:
        ret = match.group("name")
        # print(type(ret))
        ret = str(ret)
        return ret.split("b'")[1].replace('"','').replace("'",'')
    return None

def run():
    act = data['activity']
    new_window = None
    current_window = get_active_window()
    while(True):
        if new_window != current_window:
            print(str(current_window).split(" - "))
            task = str(current_window).split(" - ")
            if len(task)>2:
                if task[-1] not in act:
                    act[task[-1]]={}
                if task[-2] not in act[task[-1]]:
                    act[task[-1]][task[-2]]=[]
                act[task[-1]][task[-2]].append(task[-3])
            current_window = new_window
        new_window = get_active_window()
        

def count_down():
    count = 0
    act = data['activity']
    if 'Google Chrome' in act:
        chrome = act['Google Chrome']
    if 'Mozilla Firefox' in act:
        fox = act['Mozilla Firefox']
    if 'Wikipedia' in chrome:
        count+=len(chrome['Wikipedia'])
    if 'Wikipedia' in fox:
        count+=len(fox['Wikipedia'])
    return count
    
try:
    data={}
    data['activity']={}    
    run()
except KeyboardInterrupt:
    with open('activity.json','w') as outfile:
        json.dump(data,outfile)
    print("\nTotal links hopped:"+str(count_down()))
