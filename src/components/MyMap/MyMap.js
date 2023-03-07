import React, { useEffect, useRef } from 'react';
import './MyMap.css';

const MyMap = ({
  mapIsReadyCallback /* To be triggered when a map object is created */,
}) => {
  const mapContainer = useRef(null);

  useEffect(() => {
    console.log('This is called when the component is mounted!');
    mapIsReadyCallback('my map');
  }, [mapContainer.current]);

  return <div className="map-container" ref={mapContainer}></div>;
};

export default MyMap;