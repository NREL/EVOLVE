import {useSelector} from 'react-redux';
import {Link} from 'react-router-dom';
import React, {useState, useEffect} from 'react';
import { StateModel } from '../interfaces/redux-state';
import { NotificationData } from '../interfaces/notification-interfaces';
import axios from 'axios'


interface NotificationViewprops {

}

export const NotificationView: React.FC<NotificationViewprops> = ({}) => {
        return (
            <div>
                I am viewing notifications.
            </div>
        );
}

export function Nav() {

    // Get current user 
    const user = useSelector((state:StateModel) => state.auth.user)
    const [notifications, setNotification] = useState<NotificationData[]>([])
    const accessToken = useSelector( (state: StateModel) => state.auth.accessToken)
    const [isNotificationView, setIsNotificationView] = useState(false)
    

    const fetchNotifications = () => {
        axios.get(`/notification/?visited=false&since_last=2022-01-01T00:00:00`,
            {headers: {'Authorization': 'Bearer ' + accessToken}}
        ).then((response)=> {
            setNotification(response.data)
        })
    }

    useEffect(() => {
        // let now_date = new Date.now();
        fetchNotifications()
      
    }, [])

    const handleNotificationDelete = (id: string) => {
        axios.delete(`/notification/${id}`,
            {headers: {'Authorization': 'Bearer ' + accessToken}}
        ).then((response)=> {
            console.log(response.data)
            fetchNotifications()
        })
    }

    const handleClearNotifications = () => {
        axios.delete(`/notification`,
            {headers: {'Authorization': 'Bearer ' + accessToken}}
        ).then((response)=> {
            console.log(response.data)
            fetchNotifications()
        })
    }
    
    return (
        <div className="px-20 h-12 bg-blue-800 text-white flex justify-between items-center">
            <h1 className="w-1/4 text-xl font-bold"> EVOLVE </h1>
            <div className="flex w-1/4 justify-between">
                <Link to="/">Home</Link>
                <a target="_blank" href="https://nrel.github.io/EVOLVE/">Docs</a>
                <a target="_blank" href="https://github.com/NREL/EVOLVE">Repo</a>
            </div>
            <div className="w-1/4 flex justify-end hover:cursor-pointer relative">
                {
                    user ?
                        <div className="w-8 h-8 rounded-full bg-blue-600 border-2 flex items-center justify-center">
                            <h1 className="text-xl"> {user[0].toUpperCase()} </h1>
                        </div> :
                        <img src="./images/default_user.svg" width="35"/>
                } 
                {
                    notifications.length > 0 && <div className="w-5 h-5 rounded-full bg-red-500 absolute 
                        top-[-5px] right-[-10px] shadow-md text-sm font-bold flex justify-center items-center
                        hover:bg-orange-500 hover:cursor-pointer"
                        onClick={()=> setIsNotificationView(true)}
                        >
                            <p> { notifications.length > 5 ? '5+': notifications.length} </p>
                    </div>
                }
                
            </div>

            {
                notifications.length > 0 && isNotificationView && <div className="w-72 fixed h-60 overflow-y-scroll bg-white right-5 
                    z-20 bottom-5 shadow-md rounded-md opacity-95 text-black p-5 border-2 border-blue-500">
                        <p className="w-8 h-8 rounded-full flex justify-center 
                            items-center text-gray-500
                            absolute right-0 top-0 hover:bg-gray-500
                            hover:text-white hover:cursor-pointer text-xl"
                            onClick={()=> setIsNotificationView(false)}
                                        > <span> x </span> </p>

                        <p className="text-sm text-white bg-blue-500 px-1 rounded-md 
                        w-max my-2 hover:bg-blue-600 hover:cursor-pointer"
                        onClick={()=> handleClearNotifications()}
                        > Clear all </p>
                        {
                            notifications.map((item: NotificationData) => {
                                return (
                                    <div className="bg-gray-100 p-3 text-sm my-2 relative hover:bg-gray-200">
                                        <p className="w-5 h-5 bg-white 
                                            rounded-full flex justify-center text-gray-500
                                            shadow-md absolute right-0 top-[-5px] hover:bg-gray-500
                                            hover:text-white hover:cursor-pointer"
                                        onClick={()=> handleNotificationDelete(item.id)}
                                        > x </p>
                                        <p> <span className="bg-blue-200 rounded-md mr-2 px-1"> {new Date(item.created_at).toDateString()} </span>{item.message} </p>
                                    </div>
                                )
                            })
                        }
                </div>
            }
            
        </div>
    )
}
