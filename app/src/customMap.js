import React, { Component } from "react";
import {Map, TileLayer, Popup, Marker, LayersControl, WMSTileLayer} from "react-leaflet";


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
      t_p:"No selected position yet.",
      surroundings:[],
      t_s:"No surroundings checked yet"
    };
    
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(e){
    this.setState({ currentPos: e.latlng });
    this.fillInfoParag();
    this.askAlti();
    this.askSurroundings()
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

  handleSurroundingsResponse(response){
    if (response.status === 422){
      alert('Error in the surroundings query by status: see console')
      console.log(response,response.status);
    }
    else if (response.success != false){
      console.log(response.points)
      this.setState({ surroundings: response.points});
      this.fillSurroundingsParag();
    } 
    else {
      console.log('r',response.success, true)
      alert('Error in the surroundings query by success variable : see console')
      console.log(response);
    }
  }

  askAlti(){
    let query = "http://"+this.state.fetchURL+"/alti?lat="+this.state.currentPos.lat+"&long="+this.state.currentPos.lng
    fetch(query)
    .then((response) => response.json())
    .then((response) => {this.handleAltiResponse(response)});
  }

  askSurroundings(){
    let query = "http://"+this.state.fetchURL+"/surroundings?lat="+this.state.currentPos.lat+"&long="+this.state.currentPos.lng
    fetch(query)
    .then((response) => response.json())
    .then((response) => {this.handleSurroundingsResponse(response)});
  }

  fillInfoParag(){
    if (this.state.currentPos===null){this.setState({t_p:"No selected position yet."})}
    else {this.setState({t_p: "You selected a position with lat = "+this.state.currentPos.lat+" and long = "+this.state.currentPos.lng+"."})}

    if (this.state.currentAlt ===null){this.setState({t_a:"No altitude yet."})}
    else {this.setState({t_a:"This point has an elevation of "+this.state.currentAlt+"."})}
  }

  fillSurroundingsParag(){
    if (this.state.surroundings ===null){this.setState({t_s:"No surroundings checked yet"})}
    else {
      let maxAlti = Math.max(...this.state.surroundings.map(o => o.z))
      let minAlti = Math.min(...this.state.surroundings.map(o => o.z))
      this.setState({t_s:"This zone has an max elevation of "+maxAlti+" and a min elevation of "+minAlti+"."})
    }
  }

  render() {
    return (
      <>
      <h1>EnvErgo Front Test</h1>
      <h2>Recherche sur le calcul de bassin versant</h2>
      <div>
        <div className="grey-p">
        <label htmlFor="api">Choix de l'API altimétrie</label>&nbsp;
          <select name="api" id="api-choice">
              <option value="IGN">IGN</option>
              <option value="elevation">Elevation API</option>
          </select>
        </div>
        <Map center={this.props.center} zoom={this.props.zoom} onClick={this.handleClick}>
          <LayersControl collapsed={false}>
            <LayersControl.BaseLayer name="Street View" checked>
            <TileLayer url='https://{s}.tile.osm.org/{z}/{x}/{y}.png'/>
            </LayersControl.BaseLayer>
            <LayersControl.BaseLayer name="Topography">
              <WMSTileLayer layers="TOPO-WMS" url="http://ows.mundialis.de/services/service?"/>
            </LayersControl.BaseLayer>
          </LayersControl>
          {this.state.currentPos && <Marker position={this.state.currentPos}></Marker>}
          {this.state.surroundings.map((pt)=> (
            <Marker
            key={pt.lon+""+pt.lat}
            position={[pt.lat,pt.lon]}></Marker>)
          )}
        </Map>
        <div className="grey-p">
          <p>{this.state.t_p}</p>
          <p>{this.state.t_a}</p>
        </div>
        <div className="grey-p">
          <p>{this.state.t_s}</p>
        </div>
      </div>
      </>
    )
  }
}

export default CustomMap;
