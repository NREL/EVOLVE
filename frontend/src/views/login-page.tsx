import React, { Component, useState } from 'react';
import axios from 'axios';
import {save_user} from '../actions';


function Login(props: any) {

    const {navigation, location, dispatch } = props;
    const [username, setUsername] = useState(null)
    const [password, setPassword] = useState(null)
    

    const handleLogin = (event:any) => {
        event.preventDefault();
       
        // Submit password 
        if (username && password) {

            let formBody = new FormData()
            
            formBody.append('username',username)
            formBody.append('password', password)

            axios.post('/token',formBody).then((response)=> {
                console.log(response)
                let user = username
                let accessToken = response.data.access_token
                
               
                dispatch(save_user({user:user, accessToken:accessToken}))
                // Save the access token in the localstorage
                // localStorage.setItem('token', accessToken)
                
                const from = location.state?.from?.pathname || "/";
                navigation(from, { replace: true });
                
            }).catch((error)=> {
                console.log(error)
                window.alert("Login failed!")
            })
        }
    }

 

    const errorComponentView = (err_text:string) => {
            return <span className="text-sm text-red-500"> {err_text}</span> 
    }

    return (
        <div className='w-full h-[calc(100vh-70px)] flex items-center justify-center'>
            <form onSubmit={handleLogin} className="w-1/2 mx-auto bg-white p-10 shadow-md">
                <h1 className="text-blue-500 font-bold text-xl pb-5"> EVOLVE Login</h1>

                <div >
                    <label> Username </label> <br/>
                    <input className="w-full mt-2 bg-gray-300 px-2 py-1 outline-none text-blue-500 rounded-md"
                        type="text" name="username" value={username || ''} onChange={(e:any)=> {
                            setUsername(e.target.value)
                        }}/>
                </div>
                { !username && username !== null && errorComponentView('Username can not be empty!')}

                <div className="mt-5">
                    <label> Password </label> <br/>
                    <input type="password" name="password" value={password || ''} onChange={
                        (e:any) => {setPassword(e.target.value)}
                    }
                    className="w-full mt-2 bg-gray-300 px-2 py-1 outline-none text-blue-500 rounded-md"/>
                </div>
                { !password && password !== null && errorComponentView('Password can not be empty!') }
                
                <div className="flex justify-left pb-3">
                    <button className="bg-blue-500 mr-3 px-5 text-white py-1 rounded-2xl mt-5" type="submit"
                    > Login </button>
                </div>

                <a className="text-blue-500 text-sm border-b
                    hover:cursor-pointer hover:text-orange-400"
                    onClick={()=> navigation('/signup')}
                    > Sign up as new user </a>
                    
            </form>
        </div>
        
    )
}

export {Login}