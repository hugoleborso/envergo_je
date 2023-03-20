import React, { Component } from "react";
import {Map, TileLayer, Popup, Marker, withLeaflet} from "react-leaflet";


class CustomMap extends Component {
  constructor(props) {
    super(props);
    let fetchURL = "EC2urlAdress"
    if (window.location.href.includes("localhost")){
      fetchURL = "localhost"
    }
    this.state = {
      fetchURL:fetchURL,
      currentPos: null,
      currentAlt:null,
      t_a:"",
      t_p:"No selected position yet."
    };
    
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(e){
    this.setState({ currentPos: e.latlng });
    this.fillInfoParag();
    this.askAlti();
  }

  handleAltiResponse(response){
    if (response.status === 422){
      alert('Error in the altitude query by status: see console')
      console.log(response,response.status);
    }
    else if (response.success != false){
      this.setState({ currentAlt: response.alti});
      this.fillInfoParag();
    } 
    else {
      console.log('r',response.success, true)
      alert('Error in the altitude query by success variable : see console')
      console.log(response);
    }
  }

  askAlti(){
    let query = "http://"+this.state.fetchURL+"/alti?lat="+this.state.currentPos.lat+"&long="+this.state.currentPos.lng
    fetch(query)
    .then((response) => response.json())
    .then((response) => {this.handleAltiResponse(response)});
  }

  fillInfoParag(){
    if (this.state.currentPos===null){this.setState({t_p:"No selected position yet."})}
    else {this.setState({t_p: "You selected a position with lat = "+this.state.currentPos.lat+" and long = "+this.state.currentPos.lng+"."})}

    if (this.state.currentAlt ===null){this.setState({t_a:"No altitude yet."})}
    else {this.setState({t_a:"This point has an elevation of "+this.state.currentAlt+"."})}
  }

  render() {
    return (
      <>
      <h1>EnvErgo Front Test</h1>
      <h2>Je t'aime mon chat gros bisous</h2>
      <div>
        <Map center={this.props.center} zoom={this.props.zoom} onClick={this.handleClick}>
          <TileLayer
              url='https://{s}.tile.osm.org/{z}/{x}/{y}.png'
          />
          {this.state.currentPos && <Marker position={this.state.currentPos}></Marker>}
        </Map>
        <div id="info-p">
          <p>{this.state.t_p}</p>
          <p>{this.state.t_a}</p>
        </div>
      </div>
      </>
    )
  }
}

export default CustomMap;
