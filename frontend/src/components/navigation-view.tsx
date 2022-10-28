import {useSelector} from 'react-redux';
import {Link} from 'react-router-dom';
import React from 'react';
import { StateModel } from '../interfaces/redux-state';

export function Nav() {

    // Get current user 
    const user = useSelector((state:StateModel) => state.auth.user)

    return (
        <div className="px-20 h-12 bg-blue-800 text-white flex justify-between items-center">
            <h1 className="w-1/4 text-xl font-bold"> EVOLVE </h1>
            <div className="flex w-1/4 justify-between">
                <Link to="/">Home</Link>
                <a target="_blank" href="https://nrel.github.io/EVOLVE/">Docs</a>
                <a target="_blank" href="https://github.com/NREL/EVOLVE">Repo</a>
            </div>
            <div className="w-1/4 flex justify-end hover:cursor-pointer">
                {
                    user ?
                        <div className="w-8 h-8 rounded-full bg-blue-600 border-2 flex items-center justify-center">
                            <h1 className="text-xl"> {user[0].toUpperCase()} </h1>
                        </div> :
                        <img src="./images/default_user.svg" width="35"/>
                }

                
            </div>
        </div>
    )
}
