#test
(find red_wire)
(pickup arm1 red_wire table)
(insert arm1 red_wire power_supply_5)
(putdown arm1 red_wire power_supply_5)
(lock arm2 red_wire power_supply_5)


#node result
 //[{ 'key': -1, 'command': 'Start_arm1', 'color': 'lightblue', 'category': 'StartEnd' }, { 'key': -2, 'command': 'End_arm1', 'color': 'lightblue', 'category': 'StartEnd' }, { 'key': -3, 'command': 'Start_arm2', 'color': 'lightblue', 'category': 'StartEnd' }, { 'key': -4, 'command': 'End_arm2', 'color': 'lightblue', 'category': 'StartEnd' }, { 'key': 0, 'command': 'find', 'color': 'white', 'category': 'Process' }, { 'key': 1, 'command': 'pickup', 'color': 'white', 'category': 'Process' }, { 'key': 2, 'command': 'insert', 'color': 'white', 'category': 'Process' }, { 'key': 3, 'command': 'putdown', 'color': 'white', 'category': 'Process' }, { 'key': 4, 'command': 'wait another', 'color': 'white', 'category': 'Process' }, { 'key': 5, 'command': 'lock', 'color': 'white', 'category': 'Process' }]
          /*Dummy node
          [
          { key: 0, command: 'Start_robot_1', color: 'lightblue', category: "StartEnd" },
          { key: 1, command: 'Pick', argument: '(3,2,0)', color: 'orange', category: "Process" },
          { key: 2, command: 'Does it grasp properly?', color: 'lightgreen', category: "Decision" },
          { key: 3, command: 'Place', argument: '(16,17,0)', color: 'pink', category: "Process" },
          { key: 4, command: 'End_robot_2', color: 'lightblue', category: "StartEnd" },
          { key: 5, command: 'Start_robot_2', color: 'lightblue', category: "StartEnd" },
          { key: 6, command: 'Pick', argument: '(3,2,0)', color: 'orange', category: "Process" },
          { key: 7, command: 'Does it grasp properly?', color: 'lightgreen', category: "Decision" },
          { key: 8, command: 'Place', argument: '(16,17,0)', color: 'pink', category: "Process" },
          { key: 9, command: 'End_robot_2', color: 'lightblue', category: "StartEnd" }
        ]*/

#unused
(pickup arm1 red_wire table)
(lock arm2 red_wirepower_supply_5)
(insert arm1 red_wire power_supply_5)
(putdown arm1 red_wire power_supply_5)
(find red_wire)
