import React from 'react';
import { TextField } from '../../components/text-field';
import { SelectField } from '../../components/select-field';

export function ESSettingsView (props:any) {
    const {formData, handleChange, errors} = props;

    return (
        <React.Fragment>
            <div className="bg-gray-300 w-full my-10 pb-5">
                <div className="bg-blue-500 h-8 flex items-center px-2">
                    <img src="./images/ev_icon.svg" width="25"/>
                    <p className="text-white pl-2"> Energy Storage </p>
                </div>

                <div className="mx-10 my-3">
                    <div className="flex items-center">
                            <p className="pr-2"> Optimal Capacity </p>
                            <SelectField 
                                    name="isESOptimal"
                                    checked={formData.isESOptimal}
                                    onChange={handleChange}
                                />
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-3 gap-y-2 mt-3">

                        {
                        !formData.isESOptimal && <React.Fragment>

                                <div>
                                    <p> Power Capacity (kW) </p>
                                    <TextField 
                                        error={errors.esPowerCapacity}
                                        name="esPowerCapacity"
                                        type="number"
                                        value={formData.esPowerCapacity}
                                        onChange={handleChange}
                                    />
                                </div>

                                <div>
                                    <p> Energy Capacity (kWh) </p>
                                    <TextField 
                                        error={errors.esEnergyCapacity}
                                        name="esEnergyCapacity"
                                        type="number"
                                        value={formData.esEnergyCapacity}
                                        onChange={handleChange}
                                    />
                                </div>
                        </React.Fragment>
                        }

                    </div>

                    <div className="flex items-center mt-5">
                            <p className="pr-2"> Charging/Discharging Strategy </p>
                            <select className="rounded-md h-8 w-32 px-2" name="esStrategy" value={formData.esStrategy} onChange={handleChange}>
                                <option value="time">Time Based</option>
                                <option value="price">Price Based</option>
                            </select>
                    </div>

                    {
                        formData.esStrategy === 'time' && <div className="grid grid-cols-2 md:grid-cols-3 gap-y-2 mt-3">

                                <div>
                                    <p> Charging hours </p>
                                    <TextField 
                                        error={errors.chargingHours}
                                        name="chargingHours"
                                        type="text"
                                        value={formData.chargingHours}
                                        onChange={handleChange}
                                    />
                                </div>

                                <div>
                                    <p> Discharging hours </p>
                                    <TextField 
                                        error={errors.disChargingHours}
                                        name="disChargingHours"
                                        type="text"
                                        value={formData.disChargingHours}
                                        onChange={handleChange}
                                    />
                                </div>
                        </div>
                    }

                    {
                        formData.esStrategy === 'price' && <div className="grid grid-cols-2 md:grid-cols-3 gap-y-2 mt-3">

                                <div>
                                    <p> Price profile </p>
                                    <TextField 
                                        error={errors.priceProfile}
                                        name="priceProfile"
                                        value={formData.priceProfile}
                                        onChange={handleChange}
                                    />
                                </div>
                                
                                <div>
                                    <p> Price threshold for charging ($) </p>
                                    <TextField 
                                        error={errors.chargingPrice}
                                        name="chargingPrice"
                                        type="number"
                                        value={formData.chargingPrice}
                                        onChange={handleChange}
                                    />
                                </div>

                                <div>
                                    <p>  Price threshold for discharging ($) </p>
                                    <TextField 
                                        error={errors.disChargingPrice}
                                        name="disChargingPrice"
                                        type="number"
                                        value={formData.disChargingPrice}
                                        onChange={handleChange}
                                    />
                                </div>
                        </div>
                    }

                        <div className="grid grid-cols-2 md:grid-cols-3 gap-y-2 mt-3">

                            <div>
                                <p> Charging rate </p>
                                <TextField 
                                    error={errors.esChargingThreshold}
                                    name="esChargingThreshold"
                                    type="number"
                                    value={formData.esChargingThreshold}
                                    onChange={handleChange}
                                />
                            </div>

                            <div>
                                <p> Discharging rate </p>
                                <TextField 
                                    error={errors.esDischargingThreshold}
                                    name="esDischargingThreshold"
                                    type="number"
                                    value={formData.esDischargingThreshold}
                                    onChange={handleChange}
                                />
                            </div>
                    
                        </div>


                </div>


            </div>
        </React.Fragment>
    )
}