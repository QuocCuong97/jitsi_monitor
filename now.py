import json
import os
import subprocess

list_room = []
list_total = []
log_jicofo = '/var/log/jitsi/jicofo.log'
jicofo_config = '/etc/jitsi/jicofo/config'
output_file = 'output.json'
domain = (subprocess.getoutput("cat {} | grep 'JICOFO_HOSTNAME'".format(jicofo_config))).split('=')[1]

def export_to_json(material, json_file):
    output = json.dumps(material, indent=4, ensure_ascii=False)
    op = open(json_file, 'w', encoding="utf-8")
    op.write(output)
    op.close()

def caculate_active_rooms(): 
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
    print('--------------------ACTIVE ROOMS--------------------')
    print('----------------------------------------------------')
    print('Trạng thái domain {}'.format(domain))
    print('------------------------')
    print('Số phòng đang mở: {}'.format(list_total[0]['total_room']))
    print('Số người tham dự: {}'.format(list_total[0]['total_participants']))

    for x in list_total[1]:
        print('       + {} [{}]  ->  {} người tham dự'.format(x['name'], x['host'], x['participants']))
    print('----------------------------------------------------')

os.system("clear")
caculate_active_rooms()
screen_output()
export_to_json(list_total, output_file)
