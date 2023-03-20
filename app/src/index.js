import React, { Component } from 'react';
import { render } from 'react-dom';
import Map from './customMap';
import './style.css';

const App = () => {
return <Map zoom={9} center={{ lat: 47.169177, lng: -1.766052246}} />
} 
render(<App />, document.getElementById('root'));
