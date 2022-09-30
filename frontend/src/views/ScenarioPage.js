import {ScenarioHoverCard} from '../components/ScenarioHoverCard';
import React, { Component } from 'react';

class ScenarioPage extends Component {

    constructor(){
        super()
        this.state = {
            active_scenario : null
        }
    }

    handleScenarioHover (scenario_name) {
        this.setState({active_scenario: scenario_name})
    }

    handleScenarioUnhover () {
        
        this.setState({active_scenario: ''})
        console.log(this.state)
    }


    render(){
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
                <div class="flex justify-center bg-blue-500 w-60 rounded-md m-auto mt-12">
                    <button type="button" class="text-xl text-white font-bold"> Create scenario </button>
                    <img src="./images/create_scenario_button.svg" class="w-12"/> 
                </div>
    
                <div class="flex justify-between my-5">
                    <h1 class="text-xl text-blue-500 font-bold"> My Scenarios </h1>
                    <div class="flex">
                        <div class="flex bg-[#e9e9e9]">
                            <img src="./images/search.svg" class="pl-3 py-1" width="22" />
                            <input placeholder="Search by name" class="px-3 py-1 bg-[#e9e9e9] outline-0 border-0"/>
                        </div>
                        <button class="bg-blue-500 text-white py-1 px-3 rounded-md ml-3"> Filter </button>
                    </div>
                </div>
    
                {
                    scenarios.map((scenario)=> {
                        
                        return (
                            <div key={scenario.name} class="grid grid-cols-4 bg-white shadow-md pr-2 pl-5 py-2 items-center relative mb-3">
                                <div class="flex items-center">
                                    <img src="./images/scenario_card_icon.svg" width="35"/>
                                    <h1 class="text-xl pl-5"> {scenario.name }</h1>
                                </div>
                                <h1 class="text-xl pl-5"> {scenario.created_at }</h1>
                                
                                <div class="flex">
                                    {
                                        scenario.techonologies.map((tech, i)=> {
                                            return (
                                                <img src={tech} key={i} width="40" class="pr-2"/>
                                            )
                                        })
                                    }
                                </div>
    
                                <div class="grid grid-cols-3 pr-5 gap-y-1">
                                    {
                                        scenario.labels.map((label, i)=> {
                                            return (
                                                <p key={i} class="bg-blue-500 px-1 text-white rounded-md mr-2 text-center"> {label} </p>
                                            )
                                        })
                                    }
                                    
                                </div>
    
                                <div class="pr-3 absolute right-0 hover:cursor-pointer" 
                                    onMouseOver={()=> this.handleScenarioHover(scenario.name)}
                                    onMouseLeave={()=> this.handleScenarioUnhover()}>
                                    <img src="./images/three_dots_icon.svg" width="5" />
                                </div>
    
                           
                                <div className={this.state.active_scenario === scenario.name ? 'inline-block': 'hidden'}
                                    >
                                    <div class="absolute right-3 top-3 opacity-95 z-10" 
                                    onMouseOver={()=> this.handleScenarioHover(scenario.name)}
                                    onMouseLeave={()=> this.handleScenarioUnhover()}>
                                        <ScenarioHoverCard />
                                    </div>

                                </div>
                                
                                
                            </div>
                        )
    
                    })
                }
            </div>
        )
    }

    
}

export {ScenarioPage}