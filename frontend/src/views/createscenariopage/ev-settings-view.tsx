import React from 'react';
import { TextField } from '../../components/text-field';

export function EVSettingsView (props:any) {
    const {formData, handleChange, errors} = props;

    return (
        <React.Fragment>
            <div className="bg-gray-300 w-full my-10 pb-5">
                <div className="bg-blue-500 h-8 flex items-center px-2">
                    <img src="./images/ev_icon.svg" width="25"/>
                    <p className="text-white pl-2"> Electric Vehicles </p>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-3 mx-10 my-3 gap-y-2 gap-x-5">

                    <div>
                        <p> Number of vehicles </p>
                        <p className='text-sm text-gray-500 pb-2'> Estimated number of electric vehicles.</p>
                        <TextField 
                                error={errors.numberOfEV}
                                name="numberOfEV"
                                type="number"
                                value={formData.numberOfEV}
                                onChange={handleChange}
                            />
                    </div>
                    
                    <div>
                        <p> Percentage of residential vehicles </p>
                        <p className='text-sm text-gray-500 pb-2'> Percentage of residential vehicles in the mix.</p>
                        <TextField 
                            error={errors.pctResEV}
                            name="pctResEV"
                            type="text"
                            value={formData.pctResEV}
                            onChange={handleChange}
                        />
                    </div>


                    
                </div>
            </div>
        </React.Fragment>
    )
}