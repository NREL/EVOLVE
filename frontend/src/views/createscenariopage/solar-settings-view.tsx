import React from 'react';
import { TextField } from '../../components/text-field';

export function SolarSettingsView (props:any) {
    const {formData, handleChange, errors} = props;

    return (
        <React.Fragment>
            <div className="bg-gray-300 w-full my-10 pb-5">
                <div className="bg-blue-500 h-8 flex items-center px-2">
                    <img src="./images/solar_icon.svg" width="25"/>
                    <p className="text-white pl-2"> Solar </p>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-3 mx-10 my-3 gap-y-2">

                    <div>
                        <p> Capacity (kW) </p>
                        <TextField 
                                error={errors.solarCapacity}
                                name="solarCapacity"
                                type="number"
                                value={formData.solarCapacity}
                                onChange={handleChange}
                            />
                    </div>
                    
                    <div>
                        <p> Irradiance data </p>
                        <TextField 
                            error={errors.irradianceData}
                            name="irradianceData"
                            type="text"
                            value={formData.irradianceData}
                            onChange={handleChange}
                        />
                    </div>

                    <div>
                        <p> Azimuth (degrees) </p>
                        <TextField 
                            error={errors.panelAzimuth}
                            name="panelAzimuth"
                            type="number"
                            value={formData.panelAzimuth}
                            onChange={handleChange}
                        />
                    </div>

                    <div>
                        <p> Tilt (degrees) </p>
                        <TextField 
                            error={errors.panelTilt}
                            name="panelTilt"
                            type="number"
                            value={formData.panelTilt}
                            onChange={handleChange}
                        />
                    </div>

                    
                </div>
            </div>
        </React.Fragment>
    )
}