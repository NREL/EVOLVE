import {ScenarioHoverCard} from '../components/ScenarioHoverCard';
import React, { Component } from 'react';

class DataPage extends Component {

    constructor(props){
        super(props)
        this.state = {
            active_scenario : null
        }
    }

    handleScenarioHover (scenario_name) {
        this.setState({"active_scenario": scenario_name})
    }

    render(){
        let timeseries_data = [
            {
                "name": "Transformer-1",
                "description": "2019 time series old data",
                "created_at": "2022 Sept. 23",
                "date_range": "2019 Sep - 2022 Sep",
                "resolution_in_min": 15,
                "image": "./images/default_data.png"
                
            },
            {
                "name": "Transformer-1",
                "description": "2019 time series old data",
                "created_at": "2022 Sept. 23",
                "date_range": "2019 Sep - 2022 Sep",
                "resolution_in_min": 15,
                "image": "./images/default_data.png"
                
            },
            {
                "name": "Transformer-1",
                "description": "2019 time series old data",
                "created_at": "2022 Sept. 23",
                "date_range": "2019 Sep - 2022 Sep",
                "resolution_in_min": 15,
                "image": "./images/default_data.png"
                
            },
            {
                "name": "Transformer-1",
                "description": "2019 time series old data",
                "created_at": "2022 Sept. 23",
                "date_range": "2019 Sep - 2022 Sep",
                "resolution_in_min": 15,
                "image": "./images/default_data.png"
                
            },
        ]

        
    
        return (
            <div class="mb-5">
                <div class="flex justify-center bg-blue-500 w-60 h-12 rounded-md m-auto mt-12" onClick={()=> {this.props.navigation('/data/upload')}}>
                    <button type="button" class="text-xl text-white font-bold pr-3"> Upload data </button>
                    <img src="./images/upload_white_logo.svg" class="w-12"/> 
                </div>
    
                <div class="flex justify-between my-5">
                    <h1 class="text-xl text-blue-500 font-bold"> My Timeseries Data </h1>
                    <div class="flex">
                        <div class="flex bg-[#e9e9e9]">
                            <img src="./images/search.svg" class="pl-3 py-1" width="22" />
                            <input placeholder="Search by name" class="px-3 py-1 bg-[#e9e9e9] outline-0 border-0"/>
                        </div>
                        <button class="bg-blue-500 text-white py-1 px-3 rounded-md ml-3"> Filter </button>
                    </div>
                </div>
    
                <div class="grid grid-cols-3 gap-y-3 gap-x-3">
                {
                    timeseries_data.map((data)=> {
                        
                        return (
                            <div class="bg-white shadow-md py-3 px-5"> 
                                <div key={data.name} class="grid  grid-cols-2 items-center relative mb-3">
                                    
                                    <h1 class="text-xl"> {data.name }</h1>
                                    <div class="absolute right-0 top-2 hover:cursor-pointer">
                                        <img src="./images/three_dots_icon.svg" width="5" />
                                    </div>
                                
                                </div>
                                <p> { data.description }</p>
                                <img src={data.image} />
                                <div class="flex justify-between border-t pt-2">
                                    <h1> {data.date_range }</h1>
                                    <h1> {data.created_at }</h1>
                                </div>
                                <h1> Resolution (min): {data.resolution_in_min }</h1>
                            </div>
                        )
    
                    })
                }
                </div>
            </div>
        )
    }

    
}

export {DataPage}