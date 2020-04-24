import json
import os
import subprocess
import sys
import time
import threading

list_room = []
list_total = []
log_jicofo = '/var/log/jitsi/jicofo.log'
jicofo_config = '/etc/jitsi/jicofo/config'
output_file = 'output.json'
domain = (subprocess.getoutput("cat {} | grep 'JICOFO_HOSTNAME'".format(jicofo_config))).split('=')[1]
YELLOW = "\033[0;33m"
GREEN = "\033[1;32m"
BLUE = "\033[1;34m"
CLEAR = "\033[0m"


def export_to_json(material, json_file):
    output = json.dumps(material, indent=4, ensure_ascii=False)
    op = open(json_file, 'w', encoding="utf-8")
    op.write(output)
    op.close()

def calculate_active_rooms(): 
    list_room = []
    list_total = []
    count = int(subprocess.getoutput("cat {} | wc -l".format(log_jicofo)))
    op = open(log_jicofo, 'r', encoding="utf-8")
    room_opened = []
    total_participants = 0
    for x in range (count):
        data = op.readline()
        if 'Created new focus for' in data:
            room_name = data.split(' ')[10].split('@')[0]
            room_opened.append(room_name)
        if 'Disposed conference' in data:
            room_name = data.split(' ')[10].split('@')[0]
            room_opened.remove(room_name)
    op.seek(0)
    for room_name in room_opened:
        participants = 0
        host = ''
        for x in range (count):
            data = op.readline()
            if ('Member {}@conference.{}'.format(room_name, domain) in data) and ('joined' in data):
                participants += 1
            elif ('Member {}@conference.{}'.format(room_name, domain) in data) and ('is leaving' in data):
                participants -= 1
            if ('Authenticated jid: ' in data) and ('R={}@conference.{}'.format(room_name, domain) in data):
                host = data.split(' ')[11].split('=')[1].split('@')[0]
        room = {"name": room_name, "participants": participants, "host": host}
        list_room.append(room)
        total_participants += participants
        op.seek(0)
    list_total.append({"total_room": len(list_room), "total_participants": total_participants})
    list_total.append(list_room)
    return list_total
    
def screen_output():
    for _ in range(10000000):
        lists = calculate_active_rooms()
        os.system('clear')
        print('--------------------ACTIVE ROOMS--------------------')
        print('----------------------------------------------------')
        print('Trạng thái domain {}{}{}'.format(BLUE, domain, CLEAR))
        print('------------------------')
        print('Số phòng đang mở: {}{}{}'.format(GREEN, lists[0]['total_room'], CLEAR))
        print('Số người tham dự: {}{}{}'.format(GREEN, lists[0]['total_participants'], CLEAR))
        print('------------------------')
        for x in lists[1]:
            print('       + {}{}{} [{}{}{}]  ->  {}{}{} người tham dự'.format(BLUE, x['name'], CLEAR, YELLOW, x['host'], CLEAR, GREEN, x['participants'], CLEAR))
        print('----------------------------------------------------')
        print('----------------(Ctrl + Z) for Quit-----------------')
        print("Updating...")
        time.sleep(2)

        
def realtime_update():
    syms = ['\\', '|', '/', '-']
    for _ in range(1000000000):
        for sym in syms:  
            syms = ['\\', '|', '/', '-']
            sys.stdout.write(("\b%s" % sym))
            sys.stdout.flush()
            time.sleep(.1) 

t1 = threading.Thread(target=screen_output)  
t2 = threading.Thread(target=realtime_update)  
t1.start()
t2.start()
