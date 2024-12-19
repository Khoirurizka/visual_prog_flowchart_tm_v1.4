import logo from './logo.svg';
//import './App.css';
import { useState } from 'react';
import HomePage from './HomePage/HomePage.jsx';

/*
const fs = window.require('fs');
const pathModule = window.require('path');
const { app } = window.require('@electron/remote')
*/

function App() {
 // const [path, setPath] = useState(app.getAppPath());
  return (
    <div>
      <div>     
         <HomePage/>
      </div>
    </div>
  );
}

export default App;
