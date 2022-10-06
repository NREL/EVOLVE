import React, { Component } from 'react';
import { useState, useEffect } from "react";
import axios from 'axios';
import {useSelector} from 'react-redux';


function FilterPage(){
    return (
        <div> Filter by data category </div>
    )
}

function DataPage(props) {


    const [activeScenario, setActiveScenario] = useState(null)
    const [timeseriesData, setTimeseriesData] = useState([])
    const [timeseriesDataBackup, setTimeseriesDataBackup] = useState([])
    const [filterHover, setFilterHover] = useState(false)

    const accessToken = useSelector(state => state.auth.accessToken)
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
        'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    const handleSearch = (event) => {
        setTimeseriesData(timeseriesDataBackup.filter( el=> el.name.search(event.target.value) !== -1))
    }
    useEffect(()=> {

        axios.get(
            '/data',
            {headers: {'Authorization': 'Bearer ' + accessToken}}
        ).then((response)=> {
            let transformed_data = response.data.map((d)=> {
                    return {
                        name: d.name,
                        description: d.description,
                        created_at: new Date(d.created_at),
                        start_date: new Date(d.start_date),
                        end_date: new Date(d.end_date),
                        resolution_in_min: d.resolution_min,
                        image: "./images/default_data.png",
                        category: d.category
                    }
                })
            setTimeseriesDataBackup(transformed_data)
            setTimeseriesData(transformed_data)
        }).catch((error)=> {
            console.log(error)
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
        })

    }, [])
    
    
    return (
        <div class="mb-5 relative">
            
            <div class="flex mt-5">
                <div class="flex bg-[#e9e9e9] w-full rounded-md">
                    <img src="./images/search.svg" class="pl-3 py-1" width="22"/>
                    <input 
                        placeholder="Search by name" 
                        class="px-3 py-1 bg-[#e9e9e9] outline-0 border-0 w-full"
                        name="search"
                        onChange={handleSearch}
                        />
                </div>
                <button 
                    class="bg-blue-500 text-white py-1 px-3 rounded-md ml-3"
                    onMouseOver={()=> setFilterHover(true)}
                    onMouseLeave={()=> setFilterHover(false)}
                    > 
                    Filter 
                </button>
            </div>

            { filterHover ? 
                    <div 
                        class="absolute right-0 top-5 right-5 px-3 py-3 bg-gray-100 w-1/4 shadow-md z-25 hover:cursor-pointer"
                        onMouseOver={()=> setFilterHover(true)}
                        onMouseLeave={()=> setFilterHover(false)}
                    >
                    <FilterPage />
                    </div> : null
            }

            <div class="flex justify-center bg-blue-500 w-full sm:w-60 h-10 rounded-md m-auto mt-5" 
                onClick={()=> {props.navigation('/data/upload')}}>
                <button type="button" class="text-xl text-white font-bold pr-3"> Upload data </button>
                <img src="./images/upload_white_logo.svg" class="w-12"/> 
            </div>

            <div class="flex justify-between my-5">
                <h1 class="text-xl text-blue-500 font-bold"> My Timeseries Data </h1>
            </div>

            <div class="grid grid-cols-1 gap-y-3 gap-x-3 lg:grid-cols-3 sm:grid-cols-2">
            {
                timeseriesData.map((data)=> {
                    
                    return (
                        <div class="bg-white shadow-md py-3 px-5"> 
                            <div key={data.name} class="grid  grid-cols-2 items-center relative mb-3">
                                
                                <h1 class="text-xl"> {data.name.length>10 ? data.name.slice(0,10) + ' ...': data.name  }</h1>
                                <div class="absolute right-0 top-2 hover:cursor-pointer">
                                    <img src="./images/three_dots_icon.svg" width="5" />
                                </div>
                            
                            </div>
                            <p class="text-sm"> { data.description }</p>
                            <img src={data.image} />
                            <div class="flex justify-between border-t pt-2 text-sm">
                                <h1> {data.start_date.getFullYear()} {months[data.start_date.getMonth()]} - { data.end_date.getFullYear()} {months[data.end_date.getMonth()]}</h1>
                                <h1> {data.created_at.getFullYear()}-{data.created_at.getMonth()}
                                -{data.created_at.getDay()}</h1>
                            </div>
                            <div class="flex justify-between text-sm pt-2">
                                <h1> Resolution (min): {data.resolution_in_min }</h1>
                                <p class="bg-blue-500 text-white rounded-md px-2"> { data.category }</p>
                            </div>
                        </div>
                    )

                })
            }
            </div>
        </div>
    )
}


export {DataPage}