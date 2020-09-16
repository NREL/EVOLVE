
import React, { Component } from 'react'
import axios from 'axios';

export default class Registration extends Component {

    constructor(props) {
        super(props)
    
        this.state = {
            email: '',
            password: '',
            passwordConfirmation: '',
            registrationErrors: '',
            isLogged: false
        }

        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }
    
    handleSubmit(event){
        console.log("form submitted");
        event.preventDefault();

        const options = {
            method: 'POST',
            body: JSON.stringify(this.state),
            headers: new Headers({
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            })
        }

        // /127.0.0.1:5000
        
        fetch('http://127.0.0.1:5000/register',options) 
            .then(response => 
                response.json())
            .then((response)=>{
                console.log(response)
                this.setState(response)
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
                    <h3 style={{color:'tomato', textAlign:"center"}}> Register here !</h3>
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

                        <div className='form-group'>
                            <label>Confirm Password</label>
                            <input 
                                type='password' 
                                name = 'passwordConfirmation'
                                className='form-control' 
                                placeholder='Password'
                                value={this.state.passwordConfirmation}
                                onChange={this.handleChange}
                                required></input>
                        </div>

                        <button type='submit' className='btn btn-primary'>Register</button>
                        <small className='form-text text-muted'>{this.state.registrationErrors}</small>

                    </form>
                </div>
        )
    }
}
