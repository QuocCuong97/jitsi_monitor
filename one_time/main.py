import json
import subprocess

list_room = []
list_total = []
file_log = '/var/log/jitsi/jicofo.log'
domain = 'meeting2.cloud365.vn'
output_file = '../output.json'

def export_to_json(material, json_file):
    output = json.dumps(material, indent=4, ensure_ascii=False)
    op = open(json_file, 'w', encoding="utf-8")
    op.write(output)
    op.close()

def caculate_active_rooms():
    count = int(subprocess.getoutput("cat {} | wc -l".format(file_log)))
    op = open(file_log, 'r', encoding="utf-8")
    room_opened = []
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
            if ('Authenticated jid: ' in data) and (domain in data):
                host = data.split(' ')[11].split('=')[1].split('@')[0]
        room = {"name": room_name, "participants": participants, "host": host}
        list_room.append(room)
        op.seek(0)
    list_total.append({"total": len(list_room)})
    list_total.append(list_room)
    return list_total
    
def screen_output():
    print('--------------------ACTIVE ROOMS--------------------')
    print('----------------------------------------------------')
    print('Trạng thái domain {}'.format(domain))
    print('------------------------')
    print('Số phòng đang mở: {}'.format(list_total[0]['total']))
    for x in list_total[1]:
        print('       + {} [{}]  ->  {} người tham dự'.format(x['name'], x['host'], x['participants']))
    print('----------------------------------------------------')
    
caculate_active_rooms()
screen_output()
export_to_json(list_total, output_file)