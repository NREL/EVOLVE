import React from 'react';
import { useState, useEffect } from "react";
import axios from 'axios';
import {useSelector} from 'react-redux';
import fileDownload from 'js-file-download'


function CardHover(props){

    const {data, setIsClicked, setcardData, handleDeleteData,
        handleDataDownload} = props

    const [deleteLabel, setDeleteLabel] = useState(false)
    const [downloadLabel, setDownloadLabel] =  useState(false)
    const [comment, setComment] = useState('Enter your comment!')

    const comments = [
        {
            "date": "2022-01-02 12:32:00",
            "message": "Nice dataset!",
            "user": "kduwadi"
        },
        {
            "date": "2022-01-02 12:32:00",
            "message": "The dataset has issues around mid year.",
            "user": "kduwadi"
        }
    ]

    const handleClose = () => {
        setIsClicked(false)
        setcardData({})
    }
   
    return (
        <div class="relative">
            <div class="absolute w-8 h-8 top-0 flex items-center justify-center 
                rounded-full right-0 hover:cursor-pointer hover:bg-gray-300"
                onClick={()=> handleClose()}
                >X 
            </div>
            <div class="px-3 py-3">
                <h1 class="font-bold text-blue-500
                border-b-2 w-max"> 
                { data.name } </h1>
                <p class="pt-2 text-sm text-gray-500"> {data.description} </p>

                <div class="py-3 text-sm text-gray-500">
                <p> Data resolution </p>

                <p class="bg-blue-500 px-2 rounded-md text-white w-fit">
                    { data.resolution_in_min } min </p>
                
                <p class="pt-2"> Data start time </p>
                
                <p class="px-2 rounded-md bg-blue-500 text-white w-fit">
                        {data.start_date.toDateString() } </p> 

                <p class="pt-2"> Data end time </p>
                
                <p class="px-2 rounded-md bg-blue-500 text-white w-fit">
                        {data.end_date.toDateString() }  </p> 

                <p class="pt-2"> Created at </p>
                
                <p class="px-2 rounded-md bg-blue-500 text-white w-fit">
                        {data.created_at.toDateString() }  </p> 

                <p class="pt-2"> Data category </p>
                
                <p class="px-2 rounded-md bg-blue-500 text-white w-fit">
                        {data.category} </p> 

                <div class="grid grid-cols-2 my-5 gap-y-5 place-items-center">
                    <div class="relative bg-gray-100 w-16 h-16 rounded-full flex justify-center items-center hover:border-2 
                    hover:border-blue-500 hover:cursor-pointer"
                    onMouseOver={()=> setDeleteLabel(true)}
                    onMouseLeave={()=> setDeleteLabel(false)}
                    onClick={()=> handleDeleteData(data)}
                    >
                        <img src="./images/delete_light.svg" />
                        {
                            deleteLabel ?
                            <p class="absolute text-sm top-14 w-20 left--2 bg-orange-300 
                            rounded-md text-slate-600 px-1 opacity-90"> Delete data</p>: null
                        }


                    </div>
                    <div class="relative bg-gray-100 w-16 h-16 rounded-full flex justify-center items-center hover:border-2 
                    hover:border-blue-500 hover:cursor-pointer"
                    onMouseOver={()=> setDownloadLabel(true)}
                    onMouseLeave={()=> setDownloadLabel(false)}
                    onClick={()=> handleDataDownload(data)}
                    >
                        <img src="./images/download_light.svg" />
                        {
                            downloadLabel ?
                            <p class="absolute text-sm top-14 w-20 left--2 bg-orange-300 
                            rounded-md text-slate-600 px-1 opacity-90"> Download </p>: null
                        }
                    </div>
                    
                </div>

                <div>
                     <h1 class="text-blue-500 font-bold pb-2"> Comments </h1>
                     <input type="textarea" name="comment" 
                     class="border w-full px-2 h-10 outline-none" placeholder="Enter your comment"
                     onChange={(e)=> setComment(e.target.value())}
                     />
                </div>

                {
                    comments.map((c)=> {
                        return <div class="py-2 border-b">
                            
                            <p class="text-sm"> 
                                <span class="bg-blue-500 text-white rounded-md px-1">  {c.user} </span> <span class="pl-1"> commented at {c.date}</span> 
                            </p>
                    
                            <p class="pt-2">{c.message}</p>
                        </div>
                    })
                }

                </div>
            </div>
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

    const {data, isClicked, setcardData, setIsClicked} = props
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
        'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    const handleOnClick = (d) => {
        setIsClicked(d.id)
        setcardData(d)
    }

    return (
            data.map((d, id)=> {
                return (
                    <div className={isClicked === d.id ? 'bg-gray-200': 'bg-white'}>
                        <div class="shadow-md py-3 px-5 hover:cursor-pointer 
                        hover:bg-gray-100 hover:border-blue-500 " onClick={
                        () => handleOnClick(d)  
                        }> 
                        
                        
                            {/* <img src={d.image} class="shadow"/> */}
                            <div key={d.name} class="grid  grid-cols-1 items-center relative mb-1">
                                <h1 class="text-xl"> {d.name.length>15 ? d.name.slice(0,15) + ' ...': d.name  }</h1>
                            </div>
                            <p class="text-sm text-gray-500"> {d.description.length>25 ? d.description.slice(0,25) + ' ...': d.description  }</p>
                            
                            <div class="flex justify-between pt-2 text-sm text-gray-500 mt-2">
                                <h1> {d.start_date.getFullYear()} {months[d.start_date.getMonth()]} - { d.end_date.getFullYear()} {months[d.end_date.getMonth()]}</h1>
                                <h1> {d.created_at.getFullYear()}-{d.created_at.getMonth()}
                                -{d.created_at.getDay()}</h1>
                            </div>
                            <div class="flex justify-between text-sm pt-1 text-gray-500">
                                <h1> Resolution (min): {d.resolution_in_min }</h1>
                                <p class="bg-gray-500 text-white rounded-md px-2 max-h-fit"> { d.category }</p>
                            </div>
                        </div>
                    </div>
                )

            })
    )
}

function IsLoading(){
    return (
        
        <div class="grid grid-cols-3 gap-y-2 gap-x-3 animate-pulse">
            {
                [1,1,1,1,1,1].map((d)=> {
                    return <div class="bg-gray-200 h-64 p-5">
                    <div class="flex justify-between">
                        <div class="w-60 h-6 rounded-md bg-gray-300"></div>
                        <div class="w-10 h-6 rounded-md bg-gray-300"></div>
                    </div>
                    <div class="my-3 w-full h-6 rounded-md bg-gray-300"></div>
                    <div class="w-full h-20 rounded-md bg-gray-300"></div>
    
                    <div class="my-3 flex justify-between">
                        <div class="w-32 h-6 rounded-md bg-gray-300"></div>
                        <div class="w-32 h-6 rounded-md bg-gray-300"></div>
                    </div>
                    <div class="my-3 flex justify-between">
                        <div class="w-32 h-6 rounded-md bg-gray-300"></div>
                        <div class="w-12 h-6 rounded-md bg-gray-300"></div>
                    </div>
                </div>
                })
            }

        </div>

    )
}

function DataPageWrapper(props) {

    
    const {setcardData, isClicked, setIsClicked, timeseriesData,
        setTimeseriesData, timeseriesDataBackup,
        filterHover, setFilterHover, isLoading, kWCheck,
        setkWCheck, irrCheck, setIrrCheck, sortDate, setSortDate} = props


    
    const handleSearch = (event) => {
        setTimeseriesData(
            timeseriesDataBackup.filter( 
                el=> el.name.search(event.target.value) !== -1
            )
        )
    }

    
    return (
        <div class="mb-5 relative px-10">
            
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
                    <IsLoading/> :
            
                    <div class="grid grid-cols-1 gap-y-3 gap-x-3 lg:grid-cols-3 sm:grid-cols-2">
                        <DataCards 
                            data={timeseriesData}
                            isClicked={isClicked} 
                            setcardData={setcardData}
                            setIsClicked={setIsClicked}
                            />
                    </div>
            }

        </div>
    )
}

function DataPage(props) {
    

    const [cardData, setcardData] = useState({})
    const [isClicked, setIsClicked] = useState(false)
    const [timeseriesData, setTimeseriesData] = useState([])
    const [timeseriesDataBackup, setTimeseriesDataBackup] = useState([])
    const [filterHover, setFilterHover] = useState(false)
    const [isLoading, setIsLoading] = useState(true)
    const [kWCheck, setkWCheck] = useState(true)
    const [irrCheck, setIrrCheck] = useState(true)
    const [sortDate, setSortDate] = useState('descending')
    const accessToken = useSelector(state => state.auth.accessToken)

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

    const handleDataDownload = (data) => {
        axios.get(`/data/${data.id}/file`,
            {headers: {'Authorization': 'Bearer ' + accessToken}}
        ).then((response)=> {
            
            fileDownload(response.data, `${data.name}.csv`)
        })
    }

    const handleDeleteData = (data) => {
        // First let's delete the data

        axios.delete(`/data/${data.id}`,
            {headers: {'Authorization': 'Bearer ' + accessToken}}
        ).then((response)=> {
            console.log("Sucessfully deleted data ", response)
            
            // Disable card clicked view
            setIsClicked(false)
            setcardData({})

            // Refetch the data from API
            handleFetchData()

        }).catch((error)=> {
            console.log('Not successful', error)
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
        })
        
        
    }

    const handleFetchData = () => {
        axios.get(
            '/data',
            {headers: {'Authorization': 'Bearer ' + accessToken}}
        ).then((response)=> {
            let transformed_data = response.data.map((d)=> {
                    return {
                        id: d.id,
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
    }


    useEffect(()=> {
        handleFetchData()
    }, [])
    
    return (
        
            isClicked ? 
                <div class="flex justify-between">
                    <div class="h-[calc(100vh-0rem)] overflow-y-scroll w-full">
                    <DataPageWrapper
                        setcardData={setcardData}
                        isClicked={isClicked}
                        setIsClicked={setIsClicked} 
                        timeseriesData={timeseriesData}
                        setTimeseriesData={setTimeseriesData}
                        timeseriesDataBackup={timeseriesDataBackup}
                        filterHover={filterHover}
                        setFilterHover={setFilterHover}
                        isLoading={isLoading}
                        kWCheck={kWCheck}
                        setkWCheck={setkWCheck}
                        irrCheck={irrCheck}
                        setIrrCheck={setIrrCheck}
                        sortDate={sortDate}
                        setSortDate={setSortDate}
                    />
                    </div>
                    
                    <div class="h-screen overflow-y-scroll bg-white w-80 shadow-md 
                    opacity-98 p-2 z-10 transition duration-150 ease-linear">
                        <CardHover 
                            data={cardData} 
                            setIsClicked={setIsClicked}
                            setcardData={setcardData}
                            handleDeleteData={handleDeleteData}
                            handleDataDownload={handleDataDownload}
                        />
                    </div> 
                </div> :
                <div class="">
                    <DataPageWrapper
                        setcardData={setcardData}
                        isClicked={isClicked}
                        setIsClicked={setIsClicked} 
                        timeseriesData={timeseriesData}
                        setTimeseriesData={setTimeseriesData}
                        timeseriesDataBackup={timeseriesDataBackup}
                        filterHover={filterHover}
                        setFilterHover={setFilterHover}
                        isLoading={isLoading}
                        kWCheck={kWCheck}
                        setkWCheck={setkWCheck}
                        irrCheck={irrCheck}
                        setIrrCheck={setIrrCheck}
                        sortDate={sortDate}
                        setSortDate={setSortDate}
                    />
                </div>
        
        
    )
}

export {DataPage}