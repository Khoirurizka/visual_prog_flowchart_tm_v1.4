import re
from flask import Flask, jsonify
import requests
import threading
import time

#app = Flask(__name__)
#url_update_graph = "http://localhost:6000/update_graph"

output_pddl_str = "\n(find red_wire)\n(pickup arm1 red_wire table)\n(insert arm1 red_wire power_supply_5)\n(putdown arm1 red_wire power_supply_5)\n(lock arm2 red_wire power_supply_5)"

robots_list=["arm1","arm2"]
actions_list=["pickup","lock", "insert", "putdown","find"]
object_item_list=["red_wire","blue_wire", "yellow_wire", "white_wire","green_wire"]
location_list=["table","power_supply_5"]

extacted_commands=[]

class PDDL_line:
    def __init__(self, command_keypharse):
        self.action="-"
        self.robot="-"
        self.object_item="-"
        self.location="-"

        for ck in command_keypharse:
            for al in actions_list:
                if ck==al:
                    self.action = ck
                    break
            for rl in robots_list:
                if ck==rl:
                    self.robot = ck
                    break

            for oi in object_item_list:
                if ck==oi:
                    self.object_item = ck
                    break
            for ll in location_list:
                if ck==ll:
                    self.location = ck
                    break

    def __str__(self):
        return f"{self.robot}->{self.action} obj:{self.object_item} on:{self.location})"

def extract_pddl_lines(text):
    lines = re.findall(r'\((.*?)\)', text)
    # print(lines)
    return lines

def extract_basic_keyPharse(text):
    command_keypharse = text.strip('()').split()
    # print(command_keypharse)
    return PDDL_line(command_keypharse)


def convert_PDDL_line_to_jsonGraph(extacted_commands):
    node = []
    link = []
    executable=[]
    robot={'-':{'start':0,'end':0}} #to prevert null value
    last_key_id_on_each_robot={'-':-1}
    has_robot=True

    ### Initialize robot start-end node
    for i in range(len(extacted_commands)):
        has_robot=True
        for rb in robot:
            if extacted_commands[i].robot == rb:
                has_robot=False

        if has_robot:
            start_robot_node=-(2*len(robot)-1)
            end_robot_node=-(2*len(robot))
            # print(start_robot_node,end_robot_node)
            node_entry = {
            "key": start_robot_node,
            "robot": str(extacted_commands[i].robot),
            "command": "Start_"+str(extacted_commands[i].robot),
            "color": "lightblue",
            "category": "StartEnd"
            }
            node.append(node_entry)
            node_entry = {
            "key": end_robot_node,
            "robot": str(extacted_commands[i].robot),
            "command": "End_"+str(extacted_commands[i].robot),
            "color": "lightblue",
            "category": "StartEnd"
            }
            node.append(node_entry)
            robot.update({str(extacted_commands[i].robot):{'start':start_robot_node,'end':end_robot_node}})
            last_key_id_on_each_robot.update({str(extacted_commands[i].robot):-1})
    # print(robot)
    give_key_id=0
    prev_robot_active="-"
    # print(last_key_id_on_each_robot)
   
    for i in range(len(extacted_commands)):
        # Draw node
        if (i==0):
            # print(list(robot.keys())[1])
            prev_robot_active=list(robot.keys())[1]
        elif(i>0 and extacted_commands[i].robot!=prev_robot_active):
            ### add wait node for switch robot
            # print(extacted_commands[i].robot)
            node_entry = {
            "key": give_key_id,
            "robot": str(extacted_commands[i].robot),
            "command": "wait another",
            "color": "white",
            "category": "Process"
            }
            node.append(node_entry)
            # add link from start robot node to node
            if last_key_id_on_each_robot[extacted_commands[i].robot]<0:
                last_key_id_on_each_robot[extacted_commands[i].robot]=robot[extacted_commands[i].robot]["start"]

                link_entry = {
                    "key": str(-give_key_id-1)+"s", 
                    "from": last_key_id_on_each_robot[extacted_commands[i].robot], 
                    "to": give_key_id
                }
                
                last_key_id_on_each_robot[extacted_commands[i].robot]=give_key_id
                link.append(link_entry)

            # add link from previous process node to node
            link_entry = {
                    "key": -give_key_id-1, 
                    "from": last_key_id_on_each_robot[extacted_commands[i-1].robot], 
                    "to": give_key_id
                }
                
            last_key_id_on_each_robot[extacted_commands[i].robot]=give_key_id
            link.append(link_entry)
            give_key_id=give_key_id+1

            prev_robot_active=extacted_commands[i].robot
            # print(prev_robot_active)

        ### add main node
        node_entry = {
            "key": give_key_id,
            "robot": str(extacted_commands[i].robot),
            "command": extacted_commands[i].action,
            "color": "white",
            "category": "Process"
        }
        node.append(node_entry)
        

        ### Draw link main process
        # draw link on initial
        if (i==0):
            link_entry = {
                "key": str(-give_key_id-1)+"s", 
                "from": robot[list(robot.keys())[1]]["start"], 
                "to": give_key_id
            }
            last_key_id_on_each_robot[extacted_commands[1].robot]=give_key_id
            link.append(link_entry)
        # draw link on each step
        else:
            link_entry = {
                "key": -give_key_id-1, 
                "from": last_key_id_on_each_robot[extacted_commands[i].robot], 
                "to": give_key_id
            }
            last_key_id_on_each_robot[extacted_commands[i].robot]=give_key_id
            link.append(link_entry)

        give_key_id=give_key_id+1
        ### Draw terminator link, node each robot to the end
    for i in range(1,len(last_key_id_on_each_robot)):
        link_entry = {
            "key": str(-give_key_id-1)+"e", 
            "from": last_key_id_on_each_robot[list(last_key_id_on_each_robot.keys())[i]], 
            "to": robot[list(last_key_id_on_each_robot.keys())[i]]["end"]
        }
        link.append(link_entry)

        give_key_id=give_key_id+1
    for i in range(len(robots_list)):
        executable.append({'robot':robots_list[i], 'cmd_list': []})
    #print(executable)

    for item_link in link:
        cmd_appear=False

        node_key=""
        for item_node in node:
            if item_node['key']==item_link['to']:
                node_key=item_node['robot']
                if node_key=='-':
                    node_key='arm2'
                # print(node_key)
                for executable_item in executable:
                    if executable_item['robot']== node_key:
                        executable_item['cmd_list'].append([item_node['command'],'0','1'])
                        cmd_appear=True
                        break
                if cmd_appear:
                    break

    for robot in executable:
        cmd_list = robot['cmd_list']
        cleaned_list = []
        for i, cmd in enumerate(cmd_list):
            # Add the command if it is not a duplicate of the previous command
            if i == 0 or cmd != 'wait another' or cmd_list[i - 1] != 'wait another':
                cleaned_list.append(cmd)
        robot['cmd_list'] = cleaned_list
    print(f"executable:{executable}")
    return node,link, executable
'''
@app.route('/')
def home():
    return jsonify({"status": "Flask app running", "message": "Automatic data sending to Electron enabled"})

# Function to send data automatically
def send_data_to_electron(data):
    while True:
        try:
            response = requests.post(url_update_graph, json=data)
            print(f"Data sent: {response.status_code}, Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending data: {e}")
        time.sleep(10)  # Wait 10 seconds before sending data again

def convert_pddl_and_send_to_electron():
    while True:
        pddl_lines=extract_pddl_lines(output_pddl_str)
        for pddl_line in pddl_lines:
            extacted_command=extract_basic_keyPharse(pddl_line)
            extacted_commands.append(extacted_command)
        node,link=convert_PDDL_line_to_jsonGraph(extacted_commands)

        print(node)
        print("\n")
        print(link)
        post_data = {
            'linkDataArray': link,
            'nodeDataArray': node
            }
        print("\njson")
        print(post_data)
        break
        # send_data_to_electron(post_data)

def start_main():
    thread = threading.Thread(target=convert_pddl_and_send_to_electron)
    thread.daemon = True
    thread.start()
'''
if __name__ == "__main__":
    pddl_lines=extract_pddl_lines(output_pddl_str)
    for pddl_line in pddl_lines:
        extacted_command=extract_basic_keyPharse(pddl_line)
        extacted_commands.append(extacted_command)
    node,link,executable=convert_PDDL_line_to_jsonGraph(extacted_commands)

    print(node)
    print("\n")
    print(link)
    post_data = {
        'linkDataArray': link,
        'nodeDataArray': node
        }
    print("\njson")
    print(post_data) 
    # start_main()
    #app.run(port=5000, debug=True)

