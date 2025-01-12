import re
from flask import Flask, request, jsonify
import requests
import threading
import time
import json

app = Flask(__name__)

url_LLM_server = "http://127.0.0.1:9000/AI_reciever_prompt_image" #Dummy LLM VLM API
#url_LLM_server = "https://gai.hucenrotia.ngrok.dev/AI_reciever_prompt_image" #Hucenrotia_LLM_server

LLM_message="" #"helo I am LLM tester"
output_pddl_str ="" # "\n(find red_wire)\n(pickup arm1 red_wire table)\n(insert arm1 red_wire power_supply_5)\n(putdown arm1 red_wire power_supply_5)\n(lock arm2 red_wire power_supply_5)"

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
            "command": "Start_"+str(extacted_commands[i].robot),
            "color": "lightblue",
            "category": "StartEnd"
            }
            node.append(node_entry)
            node_entry = {
            "key": end_robot_node,
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


    return node,link

# Function to send data automatically
def send_data_to_url(url,data):
    try:
        response = requests.post(url, json=data)
        print(f"Data sent: {response.status_code}, Response: {response.text}")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")
        return (f"Error sending data: {e}")
"""
def convert_pddl_and_send_to_electron():
    node = []
    link=[]
    pddl_lines=extract_pddl_lines(output_pddl_str)
    for pddl_line in pddl_lines:
        extacted_command=extract_basic_keyPharse(pddl_line)
        extacted_commands.append(extacted_command)
    node,link=convert_PDDL_line_to_jsonGraph(extacted_commands)
    message="okay"
    print(node)
    print("\n")
    print(link)
    post_data = {'message': message,
        'linkDataArray': link,
        'nodeDataArray': node
        }
    print("\njson")
    print(post_data)
    send_data_to_url(post_data)
"""

def process_data_from_AI(data_json):
    extacted_commands=[]
    node = []
    link=[]
    output_pddl_str=""
    try:
        data = data_json #request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Invalid data format'}), 400

        output_pddl_str = data['output_pddl']
        
        print(f"Received output_pddl: {output_pddl_str}")

        for command in output_pddl_str:
            # extract action, robot_id, object, position
            match = re.match(r"\((\w+)(?:\s+(\w+))?\s+(\w+)(?:\s+(\w+))?\)", command)
            if match:
                action = match.group(1)
                robot_id = match.group(2)
                obj = match.group(3)
                position = match.group(4)
                
                # extract terminal number if position contains 'power_supply_X'
                terminal = None
                if position and "power_supply" in position:
                    terminal_match = re.search(r"power_supply_(\d+)", position)
                    if terminal_match:
                        terminal = terminal_match.group(1)
                
                parsed_tasks.append({
                    "action": action,
                    "robot_id": robot_id,
                    "object": obj,
                    "position": position,
                    "terminal": terminal
                })

        print(parsed_tasks)

        # runt the robot
        # if robot_id == "arm1":
        #     controller_arm1(subtasks=[action], coords=[[0,0,0]])

        #put the action code here
        #if arm1 -->
        #    run
        # elif task == 'find':
        #     arm2.get_logger().info("Executing 'find' task.")
        #     if arm2.find():
        #         arm2.get_logger().info("Image successfully processed in 'find' task.")
        #     else:
        #         arm2.get_logger().error("Failed to process image in 'find' task.")
        #     scalled_frame = cv2.resize(arm2.image_frame, (480, 320))
        #     # Encode the frame into bytes (JPEG format)
        #     _, img_encoded = cv2.imencode('.jpg', scalled_frame)

        #     # Convert to bytes for sending
        #     base64_image = base64.b64encode(img_encoded)
        #     response = requests.post(url_update_screw_diver_capture, json={"image": base64_image})
        #     print(f"Server response: {response.text}")


# [1] Received output_pddl: 
# [1] (find blue_wire)
# [1] (pickup arm1 blue_wire table)
# [1] (insert arm1 blue_wire power_supply_5)
# [1] (putdown arm1 blue_wire power_supply_5)
# [1] (lock arm2 blue_wire power_supply_5)

        pddl_lines=extract_pddl_lines(output_pddl_str)
        for pddl_line in pddl_lines:
            extacted_command=extract_basic_keyPharse(pddl_line)
            extacted_commands.append(extacted_command)

        node,link=convert_PDDL_line_to_jsonGraph(extacted_commands)
        print(node)
        print("\n")
        print(link)
        post_data = {'message': data['message'],
                     'vlm_frame':data['vlm_frame'],
                     'linkDataArray': link,
                     'nodeDataArray': node
                     }
        print("\njson")
        print(post_data)
        
        return post_data
    except Exception as e:
        print(f"Error: {e}")
        return 'Error: An error occurred'

@app.route('/')
def home():
    return jsonify({"status": "Flask app running", "message": "Automatic data sending to Electron enabled"})

@app.route('/user_prompt_to_LLM_server', methods=['POST'])
def user_prompt_to_LLM_server():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Invalid data format'}), 400

        message = data['message']
        print(f"Received message: {message}")
        # post_data = {'message': message}
        # print(f"json :{post_data}")
        response =  send_data_to_url(url_LLM_server,data)
        response_json= json.loads(response)
        print(f"data_recieved: {response_json['data']}")

        result_from_AI= process_data_from_AI(response_json['data'])
        print(result_from_AI)
        return jsonify({'result_from_AI':result_from_AI,'status': 'success'}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred'}), 500

#def start_main():
   # thread = threading.Thread(target=convert_pddl_and_send_to_electron)
    #thread.daemon = True
   # thread.start()

if __name__ == "__main__":
   # start_main()
    app.run(host='127.0.0.2',port=8000, debug=True)

