import React from 'react';
import { SelectField } from '../../components/select-field';

export function TechnologiesView(props:any) {

    const {handleChange} = props;
    return (
        <React.Fragment>
            <p className="text-blue-500 font-bold text-xl border-b-2 
                    w-max my-5"> Select technologies </p>

            <div className="flex">
                <div className="flex items-center pr-5">
                    <SelectField name="technologies" value="solar" onChange={handleChange}/>
                    <img src="./images/solar_icon.svg" width="30" className="mx-3"/>
                    <p> Solar </p>
                    
                </div>
            
                <div className="flex items-center pr-5">
                    <SelectField name="technologies" value="ev" onChange={handleChange}/>
                    <img src="./images/ev_icon.svg" width="35" className="mx-3"/>
                    <p> Electric vehicle </p>
                </div>

                <div className="flex items-center">
                    
                    <SelectField name="technologies" value="energy_storage" onChange={handleChange}/>
                    <img src="./images/storage_icon.svg" width="35" className="mx-3"/>
                    <p> Energy Storage </p>
                    
                </div>
            </div>
        </React.Fragment>
    )
}