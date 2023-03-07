import React, { useEffect, useState } from "react";
import "./App.css";
import { Component1 } from "../Component1/Component1";
import MyMap from "../MyMap/MyMap"

export const App: React.FunctionComponent = () => {
    const [ currentNumber, setCurrentNumber ] = useState( 0 );

    const mapIsReadyCallback = (map: any) => {
        console.log(map);
      };

    useEffect( () => {
        fetch( "api/number" ).then( res => res.json() ).then( data => {
            setCurrentNumber( data.number );
        } );
    }, [] );
    
    return (
        <div className="App">
            <header className="App-header">
                <Component1 />
                <p>
                  The current number is {currentNumber}
                </p>
                <MyMap mapIsReadyCallback={mapIsReadyCallback}/>
            </header>
        </div>
    );
};
