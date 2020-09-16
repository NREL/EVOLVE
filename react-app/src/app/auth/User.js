import React, { Component } from 'react';
import Registration from './Registration';
import Login from './Login';


export default class User extends Component {
    
    constructor(props) {
        super(props)
    
        this.state = {
            isSignin : false,
            text: 'Sign In'
        }

        this.style = {
            height: '430px',
            width: '600px',
            marginTop: '100px',
            marginLeft: '350px'
        }

        this.changeState = this.changeState.bind(this);
    }

    handlePage(){
        if (!this.state.isSignin) {
            return <Registration handleAuthenticate={this.handleAuthenticate.bind(this)}/>
        }
        return <Login handleAuthenticate={this.handleAuthenticate.bind(this)}/>
    }

    handleAuthenticate(data) {
        this.props.history.push('./dashboard')
    }

    changeState(){

        var newstate = {};
        if (this.state.isSignin){
            newstate = {
                isSignin : false,
                text: 'Sign In'
            }
        }
        else {
            newstate = {
                isSignin : true,
                text: 'Register'
            }
        }
        this.setState(newstate);
    }
    
    
    render() {
        return (
            <div className='container row' style={this.style}>
                {this.handlePage()}
                <div className='col-6 p-3 mb-5 shadow' 
                    style={{background:'tomato',padding:'0px',margin:'0px'}}>
                    <h2 style={{
                        color:'white',
                        textAlign:'center',
                        alignItems: 'center',
                        marginTop: '100px'
                    }}> Welcome <br></br> click below to <br></br>{this.state.text} !!!</h2>
                    <button style={{marginLeft:'90px', marginTop:'20px'}} type='submit' 
                            className='btn btn-success' onClick={this.changeState}>{this.state.text}</button>
                </div>
            </div>
        )
    }
}
