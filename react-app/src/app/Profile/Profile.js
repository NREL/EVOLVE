import React, { Component } from 'react'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faLeaf } from "@fortawesome/free-solid-svg-icons";
import NavBar from '../NavBar';
import ProfileForm from './ProfileForm';
import LineChart from '../LineChart';
import {Tooltip,} from 'react-tippy';

class Profile extends Component {


    constructor(props) {
        super(props)
    
        this.state = {

            'date': {
                'format': 'month',
                'data':['2018-1-1 1:15:0','2018-1-1 5:15:0','2018-3-1 1:15:0','2018-4-1 1:15:0','2018-12-1 1:15:0']
            },
            'weather_data' : [
                {'key':'Temperature', 'data': [0,0,0,0,0],'color': 'rgba(255,0,0,1)'},
                {'key':'Humidity', 'data':[0,0,0,0,0],'color': 'rgba(0,255,0,1)'},
            ],
            'date_data' : [
                {'key':'Month', 'data': [0,0,0,0,0],'color': 'rgba(255,0,0,1)'},
                {'key':'Day', 'data':[0,0,0,0,0],'color': 'rgba(0,255,0,1)'},
                {'key':'Hhindex', 'data': [0,0,0,0,0],'color': 'rgba(0,0,255,1)'},
                {'key':'Hday', 'data':[0,0,0,0,0],'color': 'rgba(255,255,0,1)'},
                {'key':'Domestic', 'data': [0,0,0,0,0],'color': 'rgba(255,0,255,1)'},
                {'key':'NonDomestic', 'data':[0,0,0,0,0],'color': 'rgba(0,255,255,1)'},
                {'key':'Industrial', 'data': [0,0,0,0,0],'color': 'rgba(255,125,125,1)'},
            ],
            'load_data' : [
                {'key':'DT_original', 'data': [0,0,0,0,0],'color': 'rgba(255,0,0,1)'},
                {'key':'DT_prediction', 'data':[0,0,0,0,0],'color': 'rgba(0,255,0,1)'},
                {'key':'Domestic_prediction', 'data': [0,0,0,0,0],'color': 'rgba(0,0,255,1)'},
                {'key':'Nondomestic_prediction', 'data':[0,0,0,0,0],'color': 'rgba(255,255,0,1)'},
                {'key':'Industrial_prediction', 'data':[0,0,0,0,0],'color': 'rgba(0,255,255,1)'},
            ]
        }
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
                            <p className='mb-0'>
                                Net load evolution</p>
                            <p className='mt-n1 ml-3'>
                                Dashboard
                            </p>
                        </div>
                        <div className='ml-3 mr-3'>
                            <ProfileForm change_data={this.changeState.bind(this)}/>
                        </div>
                    </div>
                </div>
                

                <div className='col-9 imageback'>
                            
                {/* Navbar for dashboard */}

                    <div className='row mb-3'>
                        <div className='col-12 shadow bg-primary rounded'>
                            <NavBar />
                        </div>
                    </div>

                {/* Input Data */}
                    <div className='row mt-2'>
                        <div className='col 12 shadow p-3 pl-0 mb-5 bg-white rounded'>
                        <Tooltip title="Weather parameters : Temperature in centigrade and humidity in percentage" 
                                            size='small' position="right" arrow={true} >
                            <h4><span className='badge badge-success'> Weather profile</span></h4>
                        </Tooltip>

                        <LineChart data={this.state.weather_data}
                                ylabel='load (kW)' date={this.state.date} height={20} width={100}/>
                        </div>
                    </div>

                    <div className='row mt-n4'>
                        <div className='col 12 shadow p-3 pl-0 mb-5 bg-white rounded'>
                        <Tooltip title="Month represnts month index from 1-12, day represents day index from 1 to last day,
                        Hhindex is half hourly index in a day from 0 to 47, Hday is 1 if holiday 0 otherwise, and Domestic,
                        Non Domestic Industrial monthly contribution to energy consumption" 
                                            size='small' position="right" arrow={true} >
                            <h4><span className='badge badge-success'> Date related data</span></h4>
                        </Tooltip>

                        <LineChart data={this.state.date_data}
                                ylabel='unitless number' date={this.state.date} height={21} width={100}/>
                        </div>
                    </div>

                    <div className='row mt-n4'>
                        <div className='col 12 shadow p-3 pl-0 mb-5 bg-white rounded'>
                        <Tooltip title="Self-explanatory" 
                                            size='small' position="right" arrow={true} >
                            <h4><span className='badge badge-success'> Load profile data</span></h4>
                        </Tooltip>

                        <LineChart data={this.state.load_data}
                                ylabel='load (kW)' date={this.state.date} height={25} width={100}/>
                        </div>
                    </div>

                </div>
            </div>
        )
    }
}

export default Profile;