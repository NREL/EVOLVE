
import React, { Component } from 'react'
import axios from 'axios';
import { Redirect } from 'react-router-dom';

export default class Login extends Component {

    constructor(props) {
        super(props)
    
        this.state = {
            email: '',
            password: '',
            registrationErrors: '',
            isLogged: false
        }

        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    
    handleSubmit(event){
        console.log("sign in submitted");
        event.preventDefault();

        const options = {
            method: 'POST',
            body: JSON.stringify(this.state),
            headers: new Headers({
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            })
        }
        
        fetch('http://127.0.0.1:5000/authenticate',options)
            .then(response => 
                response.json())
            .then((response)=>{
                console.log(response)
                this.setState(response)
                if (response.isLogged){
                    this.props.handleAuthenticate(response)
                }
            })
            .catch(error=>{
                console.log('error')
                console.log(error);
            });
    }

    handleChange(event){
        this.setState({[event.target.name]:event.target.value})
    }

    render() {
        return (
            <div className='col-6 shadow p-3 mb-5 bg-white rounded'>
                <h3 style={{color:'tomato', textAlign:"center"}}> Sign In !</h3>
                <form onSubmit={this.handleSubmit}>
                    <div className='form-group'>
                        <label>Email Address</label>
                        <input 
                            type='email' 
                            name='email' 
                            className='form-control' 
                            value={this.state.email} 
                            onChange={this.handleChange}
                            placeholder='Enter email'
                            required
                            />
                        <small className='form-text text-muted'>Your email address will 
                        not be used for other purposes.</small>
                    </div>

                    <div className='form-group'>
                        <label>Password</label>
                        <input 
                            type='password'
                            name = "password" 
                            placeholder = "Password"
                            value = {this.state.password}
                            onChange = {this.handleChange}
                            className='form-control'
                            required
                        />
                    </div>

                    <button type='submit' className='btn btn-primary'>Sign In</button>
                    <small className='form-text text-muted'>{this.state.registrationErrors}</small>

                </form>
            </div>
            )
    }
}
