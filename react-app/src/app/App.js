// imports

import React, {Component} from "react"
import {withRouter} from 'react-router-dom'
import LineChart from './LineChart';
import LineChart2 from './LineChart2';
import TextBlock from './TextBlock';
import DonutChart from './DonutChart';
import Table from './Table';
import NavBar from './NavBar';
import Form from './Form';
import './custom.css';
import { faLeaf, faSolarPanel, faCarBattery, faChargingStation } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import 'react-tippy/dist/tippy.css';
import {Tooltip,} from 'react-tippy';


// App is the root !!!
class App extends Component {

    constructor() {
      
      super()
      this.state = {
              'date': {
                'format': 'month',
                'data':['2018-1-1 1:15:0','2018-1-1 5:15:0','2018-3-1 1:15:0','2018-4-1 1:15:0','2018-12-1 1:15:0']
              },
              'xarray': {
                'data': [1,2,3,4,5]
              },
              'number_by_group' : [1,1,1],
              'sweepmessage':'',
              'autocapacitymessage': '',
              'optimizedbatterymessage': '',
              'dt_metric' : {'peakpower':0,'energy':0,'ramp':0,'avg2peak':0},
              'dt_metric_new': {'peak_r':'0%','energy_r': '0%','ramp': '0%','avg2peak': '0%'},
              'dt_metric_new_isneg': {'peak_r': true,'energy_r': true,'ramp': true,'avg2peak': true},
              'dt_profile': [
                // {'key':'Net load', 'data': [0,0,0,0,0],'color': 'rgba(255,0,0,1)'},
                {'key':'Base load', 'data':[0,0,0,0,0],'color': 'rgba(0,255,0,1)'},
                {'key':'New load', 'data': [0,0,0,0,0],'color': 'rgba(0,0,255,1)'}
              ],
              'dt_ldc': [
                // {'key':'Net LDC', 'data': [0,0,0,0,0],'color': 'rgba(255,0,0,1)'},
                {'key':'Base LDC', 'data':[0,0,0,0,0],'color': 'rgba(0,255,0,1)'},
                {'key':'New LDC', 'data': [0,0,0,0,0],'color': 'rgba(0,0,255,1)'}
              ],
              'solar_metric': {'energy': 0, 'power_at_peak':0, 'peak_power': 0},
              'ev_metric': {'energy': 0, 'power_at_peak':0, 'peak_power': 0},
              'battery_metric': {'c_energy': 0, 'd_energy':0, 'cd_cycle': 0},
              'solar_output': [{'key':'solar_output', 'data': [0,0,0,0,0],'color': '#dc3545'}],
              'battery_output': [
                {'key':'storage_energy', 'data': [0,0,0,0,0],'color': '#007bff'},
                {'key':'charging_power', 'data': [0,0,0,0,0],'color': 'rgba(0,255,0,1)'},
                {'key':'discharging_power', 'data': [0,0,0,0,0],'color': 'rgba(255,0,0,1)'},
              ],
              'ev_output': [{'key':'ev_output', 'data': [0,0,0,0,0],'color': '#17a2b8'}],
              'feeders': [],
              'transformers': []
            }
            // this.transformers = transformers
            // this.feeders = feeders

            fetch('http://127.0.0.1:5000/gettransformers')
                .then(response => 
                     response.json())
                .then((data)=>{
                    console.log(data)
                    this.setState({"transformers": data.transformers})
                })
                .catch(error=>{
                    console.log('error')
                    console.log(error);
                 });

            fetch('http://127.0.0.1:5000/getfeeders')
                 .then(response => 
                      response.json())
                 .then((data)=>{
                     console.log('my', data.feeders)
                     this.setState({"feeders": data.feeders})
                 })
                 .catch(error=>{
                     console.log('error')
                     console.log(error);
                  });
           
    }


    changeState (new_data) {
      this.setState(new_data);
      console.log(this.state)
    }

    render() {

      return (
        <div className='container-fluid row'>

          {/* Left pane of the dashboard, includes logo and form element */}

          <div className='col-3'>
              <div className='row shadow mr-2 bg-white rounded'>
                  <div className='col-1'></div>
                  <div className='mt-2 col-2'>
                      <FontAwesomeIcon icon={faLeaf} size='2x' color='#0275d8'/>
                  </div>
                  <div className='mt-2 col-8 font-weight-bold' style={{color:'#0275d8'}}>
                      <h3 className='mb-0 font-weight-bold'>
                          EVOLVE </h3>
                  </div>

                  <div className='ml-3 mr-3 text-center text-danger'>
                      <p>Developed by the National Renewable Energy Laboratory</p>
                  </div>
                  
                  <div className='ml-3 mr-3'>
                    <Form change_data={this.changeState.bind(this)} sweepmessage={this.state.sweepmessage} autocapacitymessage={this.state.autocapacitymessage} optimizedbatterymessage={this.state.optimizedbatterymessage} transformers={this.state.transformers} feeders={this.state.feeders}/>
                  </div>
              </div>
          </div>

          {/* Right pane of the dashboard */}
          
          <div className='col-9 imageback'>
              
              {/* Navbar for dashboard */}

              <div className='row mb-3'>
                <div className='col-12 shadow bg-primary rounded'>
                  <NavBar />
                </div>
              </div>

              {/* Donout chart and Table of DT metrics */}

              <div className='row'>
                  <div className='shadow p-3 mb-5 col-5 bg-white rounded'>
                    <DonutChart data={this.state.number_by_group}/>
                  </div>
                  <div className='col-7'>
                    <div className='shadow p-3 mb-5 bg-white ml-2 rounded row'>
                      <Tooltip title="Metrics shown will be displayed based on mode selected i.e. either daily or yearly" 
                                    size='small' position="right" arrow={true} >
                        <p className='text-center font-weight-bold'> Metrics for Distribution Transformer</p>
                      </Tooltip>
                      <Table data={this.state.dt_metric}/>
                    </div>
                  </div>
              </div>

              {/* Percentage Reduction in major metrics */}
              
              <div className='row mt-n4'>
                  <TextBlock heading='Peak Power Reduction' value={this.state.dt_metric_new.peak_r} 
                        isnegative={this.state.dt_metric_new_isneg.peak_r}/>
                  <TextBlock heading='Energy Reduction' value = {this.state.dt_metric_new.energy_r} 
                        isnegative={this.state.dt_metric_new_isneg.energy_r}/>
                  <TextBlock heading='Ramp Reduction' value = {this.state.dt_metric_new.ramp} 
                        isnegative={this.state.dt_metric_new_isneg.ramp}/>
                  <TextBlock heading='Avg2P Reduction' value = {this.state.dt_metric_new.avg2peak} 
                        isnegative={this.state.dt_metric_new_isneg.avg2peak}/>
              </div>

              
              {/* Effect of DERs in load profile */}
              
              <div className='row mt-n4'>
                <div className='col 12 shadow p-3 pl-0 mb-5 bg-white rounded'>
                  <Tooltip title="Base load : Native load profile without any DERs, Net load: Base load + the existing solar,
                    New load: Base load + mix of solar, storage, ev as specified by user." 
                                    size='small' position="right" arrow={true} >
                    <h4><span className='badge badge-success'> Effect of DERs on load profile</span></h4>
                  </Tooltip>

                  <LineChart data={this.state.dt_profile}
                           ylabel='load (kW)' date={this.state.date} height={30} width={100}/>
                </div>
              </div>

              {/* Solar panel results */}

              <div className='row mt-n4 shadow p-3 pl-0 mb-5 bg-white rounded'>
                
                <div className='col-4 border-right text-center'>
                  <FontAwesomeIcon icon={faSolarPanel} size='3x' color='#dc3545'/>
                  <h5><span className='badge badge-danger'> Solar Panel</span></h5>
                  <div className='row'>
                    <div className='col-4 border-right'>
                      <h2>{this.state.solar_metric.energy}</h2> <span className='badge badge-danger h6'>MWh</span>
                      <p className='mt-0 mb-0 pt-0 pb-0'>Energy Generation</p>
                    </div>
                    <div className='col-4 border-right'>
                      <h2>{this.state.solar_metric.power_at_peak}</h2> <span className='badge badge-danger h6'>kW</span>
                      <p className='mt-0 mb-0 pt-0 pb-0'>Generation at Peak</p>
                    </div>
                    <div className='col-4'>
                      <h2>{this.state.solar_metric.peak_power}</h2> <span className='badge badge-danger h6'>kW</span>
                      <p className='mt-0 mb-0 pt-0 pb-0'>Peak Generation</p>
                    </div>
                  </div>
                </div>

                <div className='col-8'>
                    <p><span className='badge badge-danger'> Solar Output</span></p>
                    <LineChart data={this.state.solar_output} ylabel='Generation (kW)' date={this.state.date} 
                        height={30} width={100}/>
                </div>
              </div>

              {/* Storage Panel */}

              <div className='row mt-n4 shadow p-3 pl-0 mb-5 bg-white rounded'>
                <div className='col-4 border-right text-center'>
                  <FontAwesomeIcon icon={faCarBattery} size='3x' color='#007bff'/>
                  <h5><span className='badge badge-primary'> Energy Storage</span></h5>
                  <div className='row'>
                    <div className='col-4 border-right'>
                      <h2>{this.state.battery_metric.c_energy}</h2> <span className='badge badge-primary h6'>MWh</span>
                      <p className='mt-0 mb-0 pt-0 pb-0'>Battery Energy (MWh)</p>
                    </div>
                    <div className='col-4 border-right'>
                      <h2>{this.state.battery_metric.d_energy}</h2> <span className='badge badge-primary h6'>MWh</span>
                      <p className='mt-0 mb-0 pt-0 pb-0'>Discharging Energy</p>
                    </div>
                    <div className='col-4'>
                      <h2>{this.state.battery_metric.cd_cycle}</h2> <span className='badge badge-primary h6'>cycle</span>
                      <p className='mt-0 mb-0 pt-0 pb-0'> C/D Cycle</p>
                    </div>
                  </div>

                </div>
                <div className='col-8'>
                    <p><span className='badge badge-primary'> Charging/Discharging profile</span></p>
                    <LineChart data={this.state.battery_output} ylabel='Energy/Power (kWh/kW)' date={this.state.date} 
                          height={30} width={100}/>
                </div>
              </div>

              {/* Electric Vehicle Panel */}

              <div className='row mt-n4 shadow p-3 pl-0 mb-5 bg-white rounded'>
                <div className='col-4 border-right text-center'>
                  <FontAwesomeIcon icon={faChargingStation} size='3x' color='#17a2b8'/>
                  <h5><span className='badge badge-info'> Electric Vehicle Charging Station</span></h5>
                
                  <div className='row'>
                    <div className='col-4 border-right'>
                      <h2>{this.state.ev_metric.energy}</h2> <span className='badge badge-info h6'>MWh</span>
                      <p className='mt-0 mb-0 pt-0 pb-0'>Energy Consumed</p>
                    </div>
                    <div className='col-4 border-right'>
                      <h2>{this.state.ev_metric.peak_power}</h2> <span className='badge badge-info h6'>kW</span>
                      <p className='mt-0 mb-0 pt-0 pb-0'>Max Power Consumed</p>
                    </div>
                    <div className='col-4'>
                      <h2>{this.state.ev_metric.power_at_peak}</h2> <span className='badge badge-info h6'>kW</span>
                      <p className='mt-0 mb-0 pt-0 pb-0'>Power Consumed at Peak</p>
                    </div>
                  </div>
                
                </div>
                <div className='col-8'>
                    <p><span className='badge badge-info'> Charging Station Profile</span></p>
                    <LineChart data={this.state.ev_output} ylabel='Consumption (kW)' date={this.state.date} 
                        height={30} width={100}/>
                </div>
              </div>

              {/* Effect of DERs in load duration curve */}
              
              <div className='row mt-n4'>
                <div className='col 12 shadow p-3 pl-0 mb-5 bg-white rounded'>
                  <Tooltip title="Base LDC: Native load duration curve without any DERs, Net LDC: Base LDC + the existing solar,
                    New LDC: Base LDC + mix of solar, storage, ev as specified by user." 
                                    size='small' position="right" arrow={true} >
                    <h4><span className='badge badge-success'> Effect of DERs on load duration curve</span></h4>
                  </Tooltip>

                  <LineChart2 data={this.state.dt_ldc}
                           ylabel='load (kW)' xarray={this.state.xarray} height={30} width={100}/>
                </div>
              </div>

          </div>
        </div>
      )
    }

}

export default withRouter(App)