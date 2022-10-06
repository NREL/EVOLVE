import React, { Component } from 'react';
import axios from 'axios';
import {save_user} from '../actions';



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
       
        // Submit password 
        if (this.state.username && this.state.password) {

            let formBody = new FormData()
            
            formBody.append('username', this.state.username)
            formBody.append('password', this.state.password)

            axios.post('/token',formBody).then((response)=> {
                console.log(response)
                let user = this.state.username
                let accessToken = response.data.access_token
                
               
                this.props.dispatch(save_user({user:user, accessToken:accessToken}))
                // Save the access token in the localstorage
                localStorage.setItem('token', accessToken)
                
                const from = this.props.location.state?.from?.pathname || "/";
                this.props.navigation(from, { replace: true });
                
            }).catch((error)=> {
                console.log(error)
                window.alert("Login failed!")
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