import React, {Component} from 'react';
import 'react-tippy/dist/tippy.css';
import {Tooltip,} from 'react-tippy';

class ProfileForm extends Component {

        constructor(props){
            super(props)
            this.state = {
                day: '',
                mode: 'Daily',
                transformer: 'TG-VNG072A-2'
            }

            this.transformers = ['TG-LGR017A-1', 'TG-LGR017A-2', 'TG-LGR046A-1', 'TG-LGR046A-2', 'TG-LGR054A-1',
                'TG-LGR054A-2', 'TG-LGR080A-1', 'TG-PNR104A-1', 'TG-PNR104A-2', 'TG-PNR105A-1', 'TG-PNR120A-1',
                      'TG-PNR120A-2','TG-VNG072A-2','TG-PNR128A-1', 'TG-PNR161A-1', 'TG-PNR189A-1','TG-VNG046A-1', 'TG-VNG046A-2' ]
                      
                      
                    // , 'TG-VNG058A-1', 'TG-VNG071A-1', 'TG-VNG071A-2', 'TG-VNG071A-3',
                    //    'TG-VNG072A-1', 'TG-VNG072A-2', 'TG-VNG075A-1', 'TG-VNG075A-2', 'TG-VNG103A-1', 'TG-VNG103A-2',
                    //     'TG-VNG103A-3', 'TG-VNG107A-1', 'TG-PNR121A-1','TG-PNR120A-3']
        }

        handleChange = (event) => {
            this.setState({
                [event.target.name]: event.target.value
            })
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

            fetch('http://127.0.0.1:5000/profile',options)
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
                        <Tooltip title="Choose a DT for profile disaggregation" 
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

                    
                <Tooltip title="Submit the form to re-render the graphics." 
                                    size='small' position="right" arrow={true} >
                    <button type="submit" className="btn btn-primary mt-3 ml-5 mb-5">Submit</button>
                </Tooltip>
            

                </form>
            )
        }

}

export default ProfileForm;