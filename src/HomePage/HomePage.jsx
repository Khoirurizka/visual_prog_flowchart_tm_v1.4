import React, { useState, memo } from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import * as ReactDOM from 'react-dom';
import * as FlexLayout from 'flexlayout-react';
import 'flexlayout-react/style/light.css';
import './HomePage.css';

import Chatbot from 'react-chatbot-kit'
import '../ChatBot/ChatBot.css'
import config from '../ChatBot/config.js';
import MessageParser from '../ChatBot/MessageParser.js';
import ActionProvider from '../ChatBot/ActionProvider.js';
import GraphPanel from '../GraphConstruct/GraphPanel.js';
import FrameRender from '../FrameRender/FrameRender.js';
import BEV_FrameRender from '../FrameRender/BEV_FrameRender.js';
import GripperFrameRender from '../FrameRender/GripperFrameRender.js';
import ScrewDriverFrameRender from '../FrameRender/ScrewDriverFrameRender.js';
import VLM_FrameRender from '../FrameRender/VLM_FrameRender.js';

var json = {
  global: { tabEnableClose: false },
  borders: [
    {
      "type": "border",
      "location": "top",
      "size": 100,
      "children": [
        {
          "type": "tab",
          "name": "Toolbar",
          "component": "toolbar"
        }, {
          "type": "tab",
          "name": "Preferences",
          "component": "preferences"
        }
      ]
    },
    {
      "type": "border",
      "location": "left",
      "size": 100,
      "children": []
    }
  ],
  layout: {
    "type": "row",
    "weight": 100,
    "children": [
      {
        "type": "column",
        "weight": 30,
        "children": [
          {
            "type": "tabset",
            "weight": 50,
            "selected": 0,
            "children": [
              {
                "type": "tab",
                "name": "Action-function Library",
                "component": "Action-function Library"
              },
            ]
          },
          {
            "type": "tabset",
            "weight": 50,
            "selected": 0,
            "children": [
              {
                "type": "tab",
                "name": "Gripper Cam",
                "component": "GripperFrameRender"
              },
              {
                "type": "tab",
                "name": "Screw Driver Cam",
                "component": "ScrewDriverFrameRender"
              },
              {
                "type": "tab",
                "name": "BEV Cam",
                "component": "BEV_FrameRender"
              },
              {
                "type": "tab",
                "name": "VLM capture",
                "component": "VLM_FrameRender"
              }
            ]
          },
        ]
      },
      {
        "type": "tabset",
        "weight": 50,
        "selected": 0,
        "children": [
          {
            "type": "tab",
            "name": "Flowchart Program",
            "component": "graph"
          }
        ]
      },
      {
        "type": "tabset",
        "weight": 30,
        "selected": 0,
        "children": [
          {
            "type": "tab",
            "name": "Hucenrotia Assistant",
            "component": "chat_bot"
          }
        ]
      },
    ]
  }
};

const Preferences = memo(({ layerspacing, columnSpacing, onLayerSpacingChange, onColumnSpacingChange }) => (
  <div className="preferences">
    <Container fluid>
      <Col>
        <Col sm={8}>
          <label id="layerspacing_label">Layer Spacing:</label>
          <input type="button" value="-" onClick={() => onLayerSpacingChange(layerspacing - 1)} />
          <input
            id="layerspacing"
            type="text"
            style={{ textAlign: 'right' }}
            value={layerspacing}
            onChange={(e) => onLayerSpacingChange(Number(e.target.value))}
          />
          <input type="button" value="+" onClick={() => onLayerSpacingChange(layerspacing + 1)} />
        </Col>
        <Col>
          <label id="columnspacing_label">Column Spacing:</label>
          <input type="button" value="-" onClick={() => onColumnSpacingChange(columnSpacing - 1)} />
          <input
            id="columnspacing"
            type="text"
            style={{ textAlign: 'right' }}
            value={columnSpacing}
            onChange={(e) => onColumnSpacingChange(Number(e.target.value))}
          />
          <input type="button" value="+" onClick={() => onColumnSpacingChange(columnSpacing + 1)} />
        </Col>
      </Col>
    </Container>
  </div>
));

const HomePage = () => {
  const [layerspacing, setLayerSpacing] = useState(30);
  const [columnSpacing, setColumnSpacing] = useState(30);
  const [selectedOption, setSelectedOption] = useState('Option 1');

  const handleChange = (event) => {
    setSelectedOption(event.target.value);
  };

  const [layoutModel, setLayoutModel] = useState(FlexLayout.Model.fromJson(json));
  const resetLayout = () => {
    setLayoutModel(FlexLayout.Model.fromJson(json));
  };

  const factory = (node) => {
    var component = node.getComponent();
    switch (component) {

      case "GripperFrameRender":
        return (<div className="GripperFrameRender"><GripperFrameRender /></div>);
      case "ScrewDriverFrameRender":
        return (<div className="ScrewDriverFrameRender"><ScrewDriverFrameRender /></div>);
      case "BEV_FrameRender":
        return (<div className="BEV_FrameRender"><BEV_FrameRender /></div>);
      case "VLM_FrameRender":
        return (<div className="VLM_FrameRender"><VLM_FrameRender /></div>);
      case "graph":
        return (<div className="graph">
          <GraphPanel
            layerspacing={layerspacing}
            columnSpacing={columnSpacing} />
        </div>);
      case "chat_bot":
        return (<div className="chat_bot">
          <Chatbot
            config={config}
            messageParser={MessageParser}
            actionProvider={ActionProvider}
            placeholderText='Type your message or give a prompt...'
          />
        </div>
        );
      case "Action-function Library":
        return (<div className="Action-function Library">Action-function Library is under development</div>);
      case 'preferences':
        return (
          <Preferences
            layerspacing={layerspacing}
            columnSpacing={columnSpacing}
            onLayerSpacingChange={setLayerSpacing}
            onColumnSpacingChange={setColumnSpacing} />
        );
      case "toolbar":
        return (
          <div className="toolbar">
            <label id="dropdownlabel">Robot Name</label>
            <select id="dropdown" value={selectedOption} onChange={handleChange}>
              <option value="Option 1">Screw driver robot</option>
              <option value="Option 2">Gripper robot</option>
            </select>
          </div>
        );
      default:
        return (<div className="panel">Panel {node.getName()}</div>);

    }
  }
  return (
    <FlexLayout.Layout
      model={layoutModel}
      factory={factory} />
  );
}
export default HomePage;
