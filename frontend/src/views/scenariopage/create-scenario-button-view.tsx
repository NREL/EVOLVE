import React from 'react';
import { useNavigate } from 'react-router-dom';

const CreateScenarioButton = (props: any) => {
    const navigation = useNavigate();
    return (
        <div className="flex justify-center bg-blue-500 w-60 rounded-md m-auto mt-12"
            onClick={()=> navigation('/create-scenario')}
        >
            <button type="button" className="text-xl text-white font-bold"> Create scenario </button>
            <img src="./images/create_scenario_button.svg" className="w-12"/> 
        </div>
    )
}

export {CreateScenarioButton};