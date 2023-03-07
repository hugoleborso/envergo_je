import { describe, expect } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { Component1 } from "./Component1";

describe( "test suite Component 1", ()=>{
    render( <Component1/> );
    const textContent = screen.getByText( "Component 1" );
    it( "should contain text Component 1", () => {
        expect( textContent ).toBeTruthy();
    } );
} );
