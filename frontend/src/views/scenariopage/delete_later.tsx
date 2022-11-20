// import {ScenarioHoverCard} from '../components/ScenarioHoverCard';
import React, { Component, useState } from 'react';

function ScenarioPage () {

    const [activeScenario, setActiveScenario] = useState(null)
   
    let scenarios = [
            {
                "name": "Scenario-1",
                "created_at": "2022 Sept. 23",
                "techonologies": ["./images/solar_icon.svg", "./images/storage_icon.svg", "./images/ev_icon.svg"],
                "labels": ['important']
            },
            {
                "name": "Scenario-2",
                "created_at": "2022 Sept. 23",
                "techonologies": ["./images/solar_icon.svg", "./images/ev_icon.svg"],
                "labels": ['important']
            },
            {
                "name": "Scenario-3",
                "created_at": "2022 Sept. 23",
                "techonologies": [ "./images/storage_icon.svg"],
                "labels": ['important']
            }
        ]

        
    
    return (
        <div>
            <div className="flex justify-center bg-blue-500 w-60 rounded-md m-auto mt-12">
                <button type="button" className="text-xl text-white font-bold"> Create scenario </button>
                <img src="./images/create_scenario_button.svg" className="w-12"/> 
            </div>

            <div className="flex justify-between my-5">
                <h1 className="text-xl text-blue-500 font-bold"> My Scenarios </h1>
                <div className="flex">
                    <div className="flex bg-[#e9e9e9]">
                        <img src="./images/search.svg" className="pl-3 py-1" width="22" />
                        <input placeholder="Search by name" className="px-3 py-1 bg-[#e9e9e9] outline-0 border-0"/>
                    </div>
                    <button className="bg-blue-500 text-white py-1 px-3 rounded-md ml-3"> Filter </button>
                </div>
            </div>

            {
                scenarios.map((scenario:any)=> {
                    
                    return (
                        <div key={scenario.name} className="grid grid-cols-4 bg-white shadow-md 
                            pr-2 pl-5 py-2 items-center relative mb-3">
                            <div className="flex items-center">
                                <img src="./images/scenario_card_icon.svg" width="35"/>
                                <h1 className="text-xl pl-5"> {scenario.name }</h1>
                            </div>
                            <h1 className="text-xl pl-5"> {scenario.created_at }</h1>
                            
                            <div className="flex">
                                {
                                    scenario.techonologies.map((tech:string, i:number)=> {
                                        return (
                                            <img src={tech} key={i} width="40" className="pr-2"/>
                                        )
                                    })
                                }
                            </div>

                            <div className="grid grid-cols-3 pr-5 gap-y-1">
                                {
                                    scenario.labels.map((label:string, i: number)=> {
                                        return (
                                            <p key={i} className="bg-blue-500 px-1 text-white rounded-md mr-2 text-center"> {label} </p>
                                        )
                                    })
                                }
                                
                            </div>

                            <div className="pr-3 absolute right-0 hover:cursor-pointer" 
                                onMouseOver={()=> setActiveScenario(scenario.name)}
                                onMouseLeave={()=> setActiveScenario(null)}>
                                <img src="./images/three_dots_icon.svg" width="5" />
                            </div>

                        
                            <div className={activeScenario === scenario.name ? 'inline-block': 'hidden'}
                                >
                                <div className="absolute right-3 top-3 opacity-95 z-10" 
                                onMouseOver={()=> setActiveScenario(scenario.name)}
                                onMouseLeave={()=> setActiveScenario(null)}>
                                    {/* <ScenarioHoverCard /> */}
                                </div>

                            </div>
                            
                            
                        </div>
                    )

                })
            }
        </div>
    )
    

    
}

export {ScenarioPage}