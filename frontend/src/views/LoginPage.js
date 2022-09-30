import { useRef, useState, useEffect } from 'react';
import useAuth from '../hooks/useAuth';
import { useNavigate, useLocation } from 'react-router-dom';
import React, { Component } from 'react';
import axios from 'axios';

class Login extends Component {
    constructor(props){
        super(props)
        
        this.state = {
                username: null,
                password: null
            }
    }

    handleLogin = (event) => {
        event.preventDefault();
        
        //  Validate username and password content
        // var username_re = new RegExp("^\\w[\\w.]{2,18}\\w$");
        // if (!username_re.test(this.state.username) {
        //     this.state.bad_username = true
        // }
        // can contain . or _ from 4 to 18 characters

        // var password_re = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");
        // if (!password_re.test(this.state.password)){
        //     this.state.bad_password = true
        // }
        // 1 lowercase, 1 uppercase, 1 numeric, 1 special character (!@#$%^&*), at least 8 characters long

       
       
        // Submit password 
        if (this.state.username && this.state.password) {

            let formBody = new FormData()
            
            formBody.append('username', this.state.username)
            formBody.append('password', this.state.password)

            axios.post('/token',formBody).then((response)=> {
                console.log(response)
                let user = this.state.username
                let accessToken = 'abcd'
                this.props.setauth({ user, accessToken})
                const from = this.props.location.state?.from?.pathname || "/";
                this.props.navigation(from, { replace: true });
                
            }).catch((error)=> {
                console.log(error)
                window.error("Login failed!")
            })
        }
    }

    handleInputChange = (event) => {
        this.setState({
            [event.target.name]: event.target.value
        })
    }

    handleErrorComponent = (err_text, variable) => {
        if (!variable && variable !== null) {
            return <span class="text-sm text-red-500"> {err_text}</span> 
        }
    }

    render() {
        return (
            <form onSubmit={this.handleLogin} class="w-1/3 mt-16 mb-5 mx-auto bg-white p-10 shadow-md">
                <h1 class="text-blue-500 font-bold text-xl pb-5"> EVOLVE Login</h1>
    
                <div >
                    <label> Username </label> <br/>
                    <input class="w-full mt-2 bg-gray-300 px-2 py-1 outline-none text-blue-500 rounded-md"
                        type="text" name="username" value={this.state.username} onChange={this.handleInputChange}/>
                </div>
                { this.handleErrorComponent('Username can not be empty!', this.state.username)}
    
                <div class="mt-5">
                    <label> Password </label> <br/>
                    <input type="password" name="password" value={this.state.password} onChange={this.handleInputChange}
                    class="w-full mt-2 bg-gray-300 px-2 py-1 outline-none text-blue-500 rounded-md"/>
                </div>
                { this.handleErrorComponent('Password can not be empty!', this.state.password)}
                
                <div class="flex justify-left pb-3">
                    <button class="bg-blue-500 mr-3 px-5 text-white py-1 rounded-2xl mt-5" type="submit"
                    > Login </button>
                </div>
    
                <a class="text-orange-400 text-sm border-b"> Sign up as new user </a>
                    
            </form>
            
        )
    }
}

export {Login}