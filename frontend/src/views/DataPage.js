import React from 'react';
import { useState, useEffect } from "react";
import axios from 'axios';
import {useSelector} from 'react-redux';


function CardHover(){
    return (
        <div>
            add
        </div>
    )
}


function FilterPage(props){

    
    let { kWFilterValue, irrFilterValue, sortDateValue, setkWFilterValue, 
        setirrFilterValue, setSortDateValue} = props


    return (
        <div>
            <div class="mb-2"> <h1 class="border-b max-w-max"> Filter by data category </h1> </div>
            <label>
                <input
                    type="checkbox" 
                    checked={kWFilterValue}
                    onChange={
                        ()=> {
                            setkWFilterValue(!kWFilterValue)
                        }
                    }
                />
                <span class="pl-1"> kW </span>
            </label>
            <label>
                <input
                    type="checkbox" 
                    checked={irrFilterValue}
                    onChange={
                        ()=> {
                            setirrFilterValue(!irrFilterValue)
                        }
                    }
                />
                <span class="pl-1"> irradiance </span>
            </label>

            <h1 class="my-2 border-b max-w-max"> Sort by date </h1>
            
            <label>
                <input
                    type="radio" 
                    checked={sortDateValue === 'ascending'}
                    onChange={() => setSortDateValue('ascending')}
                />
                <span class="pl-1"> ascending </span>
            </label>
            <label>
                <input
                    type="radio" 
                    checked={sortDateValue === 'descending'}
                    onChange={() => setSortDateValue('descending')}
                />
                <span class="pl-1"> descending </span>
            </label>
        </div>
    )
}

function DataCards(props) {

    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
        'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    return (
            props.data.map((data)=> {
                return (
                    <div class="bg-white shadow-md py-3 px-5"> 
                        <div key={data.name} class="grid  grid-cols-2 items-center relative mb-1">
                            
                            <h1 class="text-xl"> {data.name.length>10 ? data.name.slice(0,10) + ' ...': data.name  }</h1>
                            <div class="absolute right-0 top-2 hover:cursor-pointer">
                                <img src="./images/three_dots_icon.svg" width="4" />
                            </div>

                            <div class="absolute top-3 right-0 bg-gray-100 w-48 shadow-md opacity-98 p-2">
                                <CardHover />
                            </div>
                        
                        </div>
                        <p class="text-sm text-gray-500"> { data.description }</p>
                        <img src={data.image} />
                        <div class="flex justify-between border-t pt-2 text-sm text-gray-500">
                            <h1> {data.start_date.getFullYear()} {months[data.start_date.getMonth()]} - { data.end_date.getFullYear()} {months[data.end_date.getMonth()]}</h1>
                            <h1> {data.created_at.getFullYear()}-{data.created_at.getMonth()}
                            -{data.created_at.getDay()}</h1>
                        </div>
                        <div class="flex justify-between text-sm pt-1 text-gray-500">
                            <h1> Resolution (min): {data.resolution_in_min }</h1>
                            <p class="bg-gray-500 text-white rounded-md px-2"> { data.category }</p>
                        </div>
                    </div>
                )

            })
    )
}

function DataPage(props) {

    const [timeseriesData, setTimeseriesData] = useState([])
    const [timeseriesDataBackup, setTimeseriesDataBackup] = useState([])
    const [filterHover, setFilterHover] = useState(false)
    const [isLoading, setIsLoading] = useState(true)
    
    const [kWCheck, setkWCheck] = useState(true)
    const [irrCheck, setIrrCheck] = useState(true)
    const [sortDate, setSortDate] = useState('descending')

    const accessToken = useSelector(state => state.auth.accessToken)

    
    const handleSearch = (event) => {
        setTimeseriesData(
            timeseriesDataBackup.filter( 
                el=> el.name.search(event.target.value) !== -1
            )
        )
    }

    useEffect(()=> {
        
        let sortedTimeseriesData = []
        if (sortDate === 'descending'){
            sortedTimeseriesData = timeseriesDataBackup.sort(
                (a,b) => {
                    return new Date(b.created_at) - new Date(a.created_at)
                }
            )
        } else {
            sortedTimeseriesData = timeseriesDataBackup.sort(
                (a,b) => {
                    return new Date(a.created_at) - new Date(b.created_at)
                }
            )
        }
        setTimeseriesData(
            sortedTimeseriesData.filter( el => {
                return (el.category === 'kW' && kWCheck) ||
                (el.category === 'irradiance' && irrCheck)
            })
        )

    }, [kWCheck, irrCheck, sortDate])


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
            setTimeseriesData(transformed_data.sort((a,b)=> {
                return new Date(b.created_at) - new Date(a.created_at)
            }))
            setIsLoading(false)
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
                    <FilterPage 
                        kWFilterValue={kWCheck}
                        irrFilterValue={irrCheck}
                        sortDateValue={sortDate}
                        setkWFilterValue={setkWCheck}
                        setirrFilterValue={setIrrCheck}
                        setSortDateValue={setSortDate}
                    />
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

            {
                isLoading ? 
                    <div class="absolute top-48 right-1/2 bottom-1/2  transform translate-x-1/2 translate-y-1/2 ">
                        <div class="border-t-transparent border-solid animate-spin  rounded-full border-blue-400 border-8 h-40 w-40">
                        </div>
                    </div> :
            
                    <div class="grid grid-cols-1 gap-y-3 gap-x-3 lg:grid-cols-3 sm:grid-cols-2">
                        <DataCards data={timeseriesData} />
                    </div>
            }

        </div>
    )
}


export {DataPage}