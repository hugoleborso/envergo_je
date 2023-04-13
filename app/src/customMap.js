import React, { Component } from "react";
import {Map, TileLayer, ScaleControl, Marker, LayersControl, Circle} from "react-leaflet";


class CustomMap extends Component {
  constructor(props) {
    super(props);
    let fetchURL = "http://ec2-13-37-106-96.eu-west-3.compute.amazonaws.com"
    if (window.location.href.includes("localhost")){
      fetchURL = "http://localhost"
    }
    this.state = {
      fetchURL:fetchURL,
      currentPos: null,
      currentAlt:null,
      t_a:"",
      t_p:"No selected position yet.",
      t_s:"No surroundings checked yet",
      multiCircleRadii:[50,75,100,125],
      innerCircleRadii:25,
      slope:0.05,
      stats:null,
      estimatedSurface:null
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
      console.log(response)
      this.setState({ multiCircleRadii: response.radii});
      this.setState({ slope: response.slope});
      this.setState({ stats: response.stats});
      this.setState({ estimatedSurface: response.result});
      this.fillSurroundingsParag();
    }
    else {
      console.log('r',response.success, true)
      alert('Error in the surroundings query by success variable : see console')
      console.log(response);
    }
  }

  askAlti(){
    let api = document.getElementById("api-choice").value;
    let query = this.state.fetchURL+"/alti?lat="+this.state.currentPos.lat+"&long="+this.state.currentPos.lng+"&api="+api;
    fetch(query)
    .then((response) => response.json())
    .then((response) => {this.handleAltiResponse(response)});
  }

  askSurroundings(){
    this.setState({ stats: null});
    this.setState({ estimatedSurface: null});
    let radii = document.getElementById("radii").value
    let slope = document.getElementById("slope").value;
    
    let query = this.state.fetchURL+"/surroundings?lat="+this.state.currentPos.lat+"&long="+this.state.currentPos.lng+"&slope="+slope+"&strRadii=["+radii+"]"
    
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
    if (this.state.stats!==null){
      this.setState({t_s:"This zone has an max elevation of "+this.state.stats.max+" and a min elevation of "+this.state.stats.min+". "+
                          "The alti average is "+this.state.stats.mean+". "})
    }
    if (this.state.estimatedSurface !==null){
      this.setState({t_s:this.state.t_s+" The estimated surface is: "+this.state.estimatedSurface})
    }
    
  }

  render() {
    let redirectUrl = "https://fr-fr.topographic-map.com/map-r1xtp/France/";
    if (this.state.currentPos!==null){
      redirectUrl = "https://fr-fr.topographic-map.com/map-r1xtp/France/?center="+this.state.currentPos.lat+"%2C"+this.state.currentPos.lng+"&zoom=15&popup="+this.state.currentPos.lat+"%2C"+this.state.currentPos.lng;
    }
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
          </select>&nbsp;
          <label htmlFor="api">Rayons :</label>&nbsp;
          <input name="radii" defaultValue={this.state.multiCircleRadii} id = "radii"></input>&nbsp;
          <label htmlFor="slope">Pente :</label>&nbsp;
          <input name="slope" defaultValue={this.state.slope} id ="slope"></input>&nbsp;
          <a style={{float: 'right'}} href={redirectUrl} target="_blank" rel="noreferrer">Ouvrir dans la carto alti</a>
        </div>
        
        <Map center={this.props.center} zoom={this.props.zoom} onClick={this.handleClick}>
          
          <ScaleControl position="bottomleft" />
          
          <LayersControl collapsed={false}>
            <LayersControl.BaseLayer name="Street View" checked>
              <TileLayer url='https://{s}.tile.osm.org/{z}/{x}/{y}.png'/>
            </LayersControl.BaseLayer>
            <LayersControl.BaseLayer name="Topo IGN" >
              <TileLayer url='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png'/>
            </LayersControl.BaseLayer>
            <LayersControl.BaseLayer name="Topo 2" >
              <TileLayer url='http://{s}.tile3.opencyclemap.org/landscape/{z}/{x}/{y}.png'/>
            </LayersControl.BaseLayer>
          </LayersControl>

          {this.state.currentPos && <Marker position={this.state.currentPos}></Marker>}

          {this.state.estimatedSurface !== null && 
           <Circle center={[this.state.currentPos.lat,this.state.currentPos.lng]} 
                    radius={this.state.innerCircleRadii} 
                    pathOptions={{color:"#CC1034",fillColor: "#CC1034" }}/>
          }

          {this.state.estimatedSurface !== null && this.state.multiCircleRadii && this.state.multiCircleRadii.map((radius)=> (
            <Circle center={[this.state.currentPos.lat,this.state.currentPos.lng]} key={radius} radius={radius}/>
          ))}

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
