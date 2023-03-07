import React, { useEffect, useState } from "react";
import "./App.css";
import { Component1 } from "../Component1/Component1";

export const App: React.FunctionComponent = () => {
    const [ currentNumber, setCurrentNumber ] = useState( 0 );

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
            </header>
        </div>
    );
};
