import axios from 'axios';
import React, { useEffect, useState } from 'react';
import {useSelector} from 'react-redux';
import {StateModel} from '../../interfaces/redux-state';
import { ShardUsersEmptyView } from './shared-users-empty-view';


export function SharedUser (props:any) {

    const {data, handleAddSharedUser, handleDeleteSharedUser} = props;
    const [selectedUser, setSelectedUser] = useState('')
    const user = useSelector( (state: StateModel) => state.auth.user)
    const [searchUsers, setSearchUsers] = useState<string[]>([])
    const accessToken = useSelector((state:StateModel) => state.auth.accessToken)
    const [targetString, setTargetString] = useState('')

    useEffect(()=>
            {
                if(targetString) {
                    
                    axios.get(
                        `/users/${targetString}/limit/5`,
                        {headers: {'Authorization': 'Bearer ' + accessToken}}
                    ).then((response)=> {
                        setSearchUsers(response.data)
                    }).catch((error)=> {
                        console.log(error)
                        if (error.response.status === 401) {
                            localStorage.removeItem('state')
                        }
                    })
                }
            }
    
    , [targetString]) 


    return (
        <div>
                <p className="text-blue-500 border-b-2 w-max my-3 font-bold"> Shared Users </p>
                {
                    data.owner === user && <div>
                        <p className="text-sm text-gray-500 pb-2 "> Enter username below to share the data with other users. </p>
                        <div className="flex justify-between">
                            
                            <input 
                                className="border rounded-md mr-2 px-2 w-2/3"
                                value={selectedUser}
                                onChange={(e: any)=> 
                                    {
                                        setSelectedUser(e.target.value)
                                        setTargetString(e.target.value)
                                    }
                                }
                            />
                                
                            <div className="flex bg-gray-300 rounded-md py-1 w-1/3 
                                justify-center hover:bg-gray-200"
                                onClick={()=> handleAddSharedUser(selectedUser, data.id)}
                            >
                                <button className="pr-2">Share </button>
                                <img src="./images/share_users.svg" width="25"/>
                            </div>
                        </div>
                    </div>
                }

                {
                    searchUsers.length >0  && <div className="bg-gray-100 shadow-md p-2">
                    {
                        searchUsers.slice(0,5).map((u:string)=> {
                            return <p className="hover:bg-gray-200 px-2 hover:cursor-pointer 
                            hover:rounded-md" onClick={() => {
                                setSelectedUser(u)
                                setSearchUsers([])
                            }}> {u} </p>
                        })
                    }
                </div>
                }
                

                {/* <div className="flex bg-[#e9e9e9] w-full rounded-md mt-5">
                    <img src="./images/search.svg" className="pl-3 py-1" width="22"/>
                    <input 
                        placeholder="Search shared user" 
                        className="px-3 py-1 bg-[#e9e9e9] outline-0 border-0 w-full"
                        name="search"
                        />
                </div> */}
                {
                    data.shared_users.length > 1? 
                            <div className="px-3 py-2 mt-2 bg-gray-100 h-40 w-full overflow-scroll">
                                {
                                    data.shared_users.map((u:any)=> {
                                        return <div className="flex justify-between">
                                            <div className="flex pt-1"> 
                                                <div className="h-6 w-6 bg-blue-500 rounded-full text-white 
                                                    flex justify-center items-center font-bold border-white border-2
                                                    ">
                                                    <p> {u.username[0].toUpperCase()} </p>
                                                </div>
                                                {data.owner === u.username ? <p className="pl-2"> {u.username} 
                                                    <span className="ml-2 bg-blue-500 text-sm rounded-full px-1 text-white"> admin </span></p>:
                                                    <p className="pl-2"> {u.username} </p>
                                                }
                                            </div>
                                            {
                                                data.owner === user && data.owner !== u.username && 
                                                <div className="hover:bg-gray-300 hover:cursor-pointer hover:rounded-full h-6 w-6
                                                    flex align-center justify-center"
                                                    onClick={()=> handleDeleteSharedUser(u.username, data.id)}    
                                                >
                                                    X 
                                                </div>
                                            }
                                            {
                                                data.owner !== user && data.owner !== u.username && u.username === user &&
                                                <div className="hover:bg-gray-300 hover:cursor-pointer hover:rounded-full h-6 w-6
                                                    flex align-center justify-center"
                                                    onClick={()=> handleDeleteSharedUser(u.username, data.id)} 
                                                    >
                                                    X 
                                                </div>
                                                
                                            }
                                        </div>
                                    })
                                }
                                </div>: <ShardUsersEmptyView />
                }
        </div>
    )
}
