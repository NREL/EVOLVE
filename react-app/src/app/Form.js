import React, {Component} from 'react';
import 'react-tippy/dist/tippy.css';
import {Tooltip,} from 'react-tippy';

class Form extends Component {

        constructor(props){
            super(props)
            this.state = {
                pvcapacity: 20,
                batteryenergy: 100,
                batterypower:50,
                batterystrategy: 'Time Based',
                sweep: true,
                chargethreshold: '3,4,5',
                dischargethreshold:'9,10,11,12',
                autocapacity:true, 
                optimizecapacity: false,
                evnumber:0,
                respercentage: 25,
                kwchargerate: 0.8,
                kwdischargerate: 0.6,
                feeder: 'Hargovind Enclave',
                dtorfeeder: 'Feeder',
                day: '',
                mode: 'Daily',
                transformer: 'TG-VNG072A-2'
            }



            this.transformers = ['TG-LGR017A-1', 'TG-LGR017A-2', 'TG-LGR046A-1', 'TG-LGR046A-2', 'TG-LGR054A-1',
                'TG-LGR054A-2', 'TG-LGR080A-1', 'TG-PNR104A-1', 'TG-PNR104A-2', 'TG-PNR105A-1', 'TG-PNR120A-1',
                      'TG-PNR120A-2','TG-VNG072A-2','TG-PNR128A-1', 'TG-PNR161A-1', 'TG-PNR189A-1','TG-VNG046A-1', 'TG-VNG046A-2' ]

            //this.feeders = ['Hargovind Enclave','Sohan Singh', 'Vishkarma Park']
            this.feeders = ['Feeder1', 'Feeder2', 'Feeder3']

            this.boolean_states = ['sweep','autocapacity','optimizecapacity']
                      
                    // , 'TG-VNG058A-1', 'TG-VNG071A-1', 'TG-VNG071A-2', 'TG-VNG071A-3',
                    //    'TG-VNG072A-1', 'TG-VNG072A-2', 'TG-VNG075A-1', 'TG-VNG075A-2', 'TG-VNG103A-1', 'TG-VNG103A-2',
                    //     'TG-VNG103A-3', 'TG-VNG107A-1', 'TG-PNR121A-1','TG-PNR120A-3']
        }

        handleChange = (event) => {
            
            if (this.boolean_states.includes(event.target.name) ) {
                this.setState({
                    [event.target.name]: event.target.checked
                })
            }
            else {
                this.setState({
                    [event.target.name]: event.target.value
                })
            }
            
        }

        submitHandler = (event) => {
            event.preventDefault()
            
            // Let's make a post request

            const options = {
                method: 'POST',
                body: JSON.stringify(this.state),
                headers: new Headers({
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                })
            }

            fetch('http://127.0.0.1:5000/getdata',options)
                .then(response => 
                    response.json())
                .then((response)=>{
                    console.log(response)
                    this.props.change_data(response)
                })
                .catch(error=>{
                    console.log('error')
                    console.log(error);
                 });
                
        }

        render() {
            

            return (
                <form onSubmit={this.submitHandler}>

                     {/* Enter a settings for mode of analysis and choose a transformer to analyze*/}
                    
                    <h4><span className="badge badge-warning ml-5 mt-2 mb-3">Base Settings</span></h4>

                    <div className="form-group">
                        <Tooltip title="Select a date for analysis by clicking calendar button on right." 
                                    size='small' position="right" arrow={true} >
                            <label>Choose a Day</label>
                        </Tooltip>
                        <input type="date" className="form-control" name="day" value={this.state.day} onChange={this.handleChange}/>
                    </div>

                    <div className='form-group'>

                        <Tooltip title="Daily mode will results for a selected day only while Yearly mode will show the
                                result for entire year of selected day" 
                                    size='small' position="right" arrow={true} >
                            <label> Mode of time </label>
                        </Tooltip>
                        <div className="form-check">
                            <input className="form-check-input" type="radio" name="mode" value='Daily' defaultChecked={this.state.mode==='Daily'} onChange={this.handleChange}/>
                            <label className="form-check-label">Daily</label>
                        </div>
                        <div className="form-check">
                            <input className="form-check-input" type="radio" name="mode" value='Weekly' defaultChecked={this.state.mode==='Weekly'} onChange={this.handleChange}/>
                            <label className="form-check-label">Weekly</label>
                        </div>
                        <div className="form-check">
                            <input className="form-check-input" type="radio" name="mode" value='Yearly' defaultChecked={this.state.mode==='Yearly'} onChange={this.handleChange}/>
                            <label className="form-check-label">Yearly</label>
                        </div>
                    </div>

                    <div className='form-group'>

                        <Tooltip title="If you choose feeder transformer radio button will be ignored and vice-versa" 
                                    size='small' position="right" arrow={true} >
                            <label> Choose Feeder or DT </label>
                        </Tooltip>
                        <div className="form-check">
                            <input className="form-check-input" type="radio" name="dtorfeeder" value='Feeder' defaultChecked={this.state.dtorfeeder==='Feeder'} onChange={this.handleChange}/>
                            <label className="form-check-label">Feeder</label>
                        </div>
                        <div className="form-check">
                            <input className="form-check-input" type="radio" name="dtorfeeder" value='DT' defaultChecked={this.state.dtorfeeder==='DT'} onChange={this.handleChange}/>
                            <label className="form-check-label">DT</label>
                        </div>
                    </div>


                    <div className='form-group'>
                        <Tooltip title="Choose a feeder" 
                                    size='small' position="right" arrow={true} >
                            <label>Choose a feeder</label>
                        </Tooltip>


                        {this.feeders.map((name)=>{
                            return (<div className="form-check">
                                <input className="form-check-input" type="radio" name="feeder" value={name} defaultChecked={this.state.feeder===name} onChange={this.handleChange}/>
                                <label className="form-check-label">{name}</label>
                            </div>
                            )})}


                    </div>

                    <div className='form-group'>
                        <Tooltip title="Choose a DT for analysis" 
                                    size='small' position="right" arrow={true} >
                            <label>Choose a distribution transformer</label>
                        </Tooltip>


                        {this.transformers.map((name)=>{
                            return (<div className="form-check">
                                <input className="form-check-input" type="radio" name="transformer" value={name} defaultChecked={this.state.transformer===name} onChange={this.handleChange}/>
                                <label className="form-check-label">{name}</label>
                            </div>
                            )})}


                    </div>

                    
                    {/* Enter the settings for solar panels */}
                    <h4><span className="badge badge-warning ml-5 mt-2 mb-3">Solar Settings</span></h4>
                    <div className="form-group">
                        <Tooltip title="Enter total PV capacity in kW, negative values will be assumed zero." size='small' position="right" arrow={true} >
                            <label>Total Capacity (kW)</label>
                        </Tooltip>
                        <input type="number" className="form-control" name="pvcapacity" value={this.state.pvcapacity} onChange={this.handleChange}/>
                    </div>

                    
                    {/* Enter the settings for energy storage */}
                    <h4><span className="badge badge-warning ml-2 mt-2 mb-3">Energy Storage Settings</span></h4>
                    <div className="form-group">
                        <Tooltip title="Energy capacity of storage in kWh, default is 100 kWh, 0 will disable storage" size='small' position="right" arrow={true} >
                            <label>Energy Capacity (kWh)</label>
                        </Tooltip>
                        <input type="number" className="form-control" name="batteryenergy" value={this.state.batteryenergy} onChange={this.handleChange}/>

                        <Tooltip title="Rated capacity of storage in kW, default is 50 kW, 0 will disable storage" size='small' position="right" arrow={true} >
                            <label> Rated Capacity (kW) </label>
                        </Tooltip>

                        <input type="number" className="form-control" name="batterypower" value={this.state.batterypower} onChange={this.handleChange}/>

                        <div class="form-check form-check-inline mt-1">
                        <input class="form-check-input" type="checkbox" name="autocapacity" value='' checked={this.state.autocapacity} onChange={this.handleChange}/>
                        <label class="form-check-label text-danger">Check to find size utility scale battery</label>
                        </div>

                        <p className='text-primary'>{this.props.autocapacitymessage}</p>

                        <div class="form-check form-check-inline mt-1">
                        <input class="form-check-input" type="checkbox" name="optimizecapacity" value='' checked={this.state.optimizecapacity} onChange={this.handleChange}/>
                        <label class="form-check-label text-danger">Check to find size of behind the meter (BTM) battery</label>
                        </div>

                        <p className='text-primary'>{this.props.optimizedbatterymessage}</p>
                        
                        <Tooltip title="Time and power Based is implemented for now" size='small' position="right" arrow={true} >
                            <label> Charging/Discharging Strategy </label>
                        </Tooltip>
                        <select className="form-control" name="batterystrategy" value={this.state.batterystrategy} onChange={this.handleChange}>
                                <option>Time Based</option>
                                <option>Power Based</option>
                                <option>Price Based</option>
                        </select>

                        <Tooltip title="e.g. 10,11,12 for 'time-based' -- will charge the battery at hours 10, 11 and 12 only, 0.25 for 'power-based' 
                                will start charging battery after DT load falls 25% of it's peak." 
                                    size='small' position="right" arrow={true} >
                            <label> Charging Threshold </label>
                        </Tooltip>

                        <input type="text" className="form-control" name="chargethreshold" value={this.state.chargethreshold} onChange={this.handleChange}/>
                        

                        <Tooltip title="e.g. 3,4,5 for 'time-based' -- will discharge the battery at hours 3, 4 and 5 only, 0.8 for 'power-based' 
                                will start charging battery after DT load is above 80% of it's peak." 
                                    size='small' position="right" arrow={true} >
                        <label> Discharging Threshold </label>
                        </Tooltip>
                        
                        <input type="text" className="form-control" name="dischargethreshold" value={this.state.dischargethreshold} onChange={this.handleChange}/>
                    
                        
                        <div class="form-check form-check-inline mt-1">
                        <input class="form-check-input" type="checkbox" name="sweep" value='' checked={this.state.sweep} onChange={this.handleChange}/>
                        <label class="form-check-label text-danger">Sweep and find best thresholds</label>
                        </div>

                        <p className='text-primary'>{this.props.sweepmessage}</p>
                        
                        
                        <Tooltip title="e.g. 1.0, make sure to specify battery charging rate in per unit between 0 and 1" 
                                    size='small' position="right" arrow={true} >
                            <label> Charging Rate (0 - 1) </label>
                        </Tooltip>

                        <input type="number" className="form-control" name="kwchargerate" value={this.state.kwchargerate} onChange={this.handleChange}/>
                        
                        <Tooltip title="e.g. 1.0, make sure to specify battery discharging rate in per unit between 0 and 1" 
                                    size='small' position="right" arrow={true} >
                            <label> Discharging Rate (0 - 1) </label>
                        </Tooltip>

                        <input type="number" className="form-control" name="kwdischargerate" value={this.state.kwdischargerate} onChange={this.handleChange}/>
                        
                    
                    </div>

                    {/* Enter the settings for electric vehicle */}

                    <h4><span class="badge badge-warning ml-2 mt-1 mb-2">Electric Vehicle Settings</span></h4>
                    <div className="form-group">

                        <Tooltip title="Number of vehicles" 
                                    size='small' position="right" arrow={true} >
                        <label> Number of Vehicles </label>
                        </Tooltip>
                        <input type="number" className="form-control" name="evnumber" value={this.state.evnumber} onChange={this.handleChange}/>

                        <Tooltip title="Adoption percentage" 
                                    size='small' position="right" arrow={true} >
                        <label> Residential Percentage </label>
                        </Tooltip>
                        <input type="number" className="form-control" name="respercentage" value={this.state.respercentage} onChange={this.handleChange}/>
                    </div>

                    
                <Tooltip title="Submit the form to re-render the graphics." 
                                    size='small' position="right" arrow={true} >
                    <button type="submit" className="btn btn-primary mt-1 ml-5 mb-3">Submit</button>
                </Tooltip>
                
                {/* <div className='ml-2 mb-1'>
                    <img src={require('../assets/nrel-logo.jpg')} width="200" className='img-thumbnail'/>
                    <p className='mr-5 text-center'>National Renewable Energy Laboratory (NREL), 2020, Golden, CO, USA</p>
                </div> */}

                </form>
            )
        }

}

export default Form