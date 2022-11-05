import React from 'react';
import { TextField } from '../../components/text-field';

export function BaseSettingsView (props:any) {
    const {formData, handleChange, errors} = props;
    return (
        <React.Fragment>
            <div className="bg-gray-300 w-full my-10 pb-5">
                <div className="bg-blue-500 h-8 flex items-center px-2">
                    <img src="./images/solar_icon.svg" width="25"/>
                    <p className="text-white pl-2"> Basic settings </p>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-3 mx-10 my-3 gap-y-2">

                    <div>
                        <p> Load profile </p>
                        <TextField 
                                error={errors.loadProfile}
                                name="loadProfile"
                                value={formData.loadProfile}
                                onChange={handleChange}
                            />
                    </div>
                    
                    <div>
                        <p> Start Date </p>
                        <TextField 
                            error={errors.startDate}
                            name="startDate"
                            type="date"
                            value={formData.startDate}
                            onChange={handleChange}
                        />
                    </div>

                    <div>
                        <p> End Date </p>
                        <TextField 
                            error={errors.endDate}
                            name="endDate"
                            type="date"
                            value={formData.endDate}
                            onChange={handleChange}
                        />
                    </div>

                    
                </div>
            </div>
        </React.Fragment>
    )
}