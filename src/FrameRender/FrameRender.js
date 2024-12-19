import React, {Component} from 'react';
import localImage from '../assets/Cover Icon 500x500px.png';

//import {View, StyleSheet, Animated, Easing} from 'react-native';

function FrameRender() {
    return (
        <div className="FrameRender" >
            <div>
                <iframe width="500"
                        height="500"
                        src={localImage} >
                </iframe>
            </div>
        </div>
);
}

export default FrameRender;