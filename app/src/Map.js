import React, { Component } from "react";
import {Map, TileLayer, Popup, Marker, withLeaflet} from "react-leaflet";



class MapExample extends Component {
  constructor(props) {
    super(props);
    this.state = {
      currentPos: null,
      currentAlt: null
    };
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(e){
    this.setState({ currentPos: e.latlng });
    console.log(this.state.currentPos)
    let query = "http://localhost/alti?lat="+this.state.currentPos.lat+"&long="+this.state.currentPos.lng
    console.log(query)
    fetch(query)
    .then((response) => response.json())
    .then((response) => console.log(response));
  }



  render() {
    return (
      <div>
        <Map center={this.props.center} zoom={this.props.zoom} onClick={this.handleClick}>
          <TileLayer
              url='https://{s}.tile.osm.org/{z}/{x}/{y}.png'
          />
          {this.state.currentPos && <Marker position={this.state.currentPos}></Marker>}
        </Map>
        <p>{JSON.stringify(this.state.currentPos, null, 2)}</p>
      </div>
    )
  }
}

export default MapExample;
