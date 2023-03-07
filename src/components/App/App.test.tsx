import { describe, expect } from "@jest/globals";

describe( "test suite", ()=>{
    it( "should return True when both texts are equal", () => {
        expect( "texte" ).toStrictEqual( "texte" );
    } );
} );
