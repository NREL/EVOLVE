import React, { useState } from 'react';
import { TextField } from '../../components/text-field';

export function EVSettingsView(props: any) {
    const { formData, handleChange, errors, handleEVDelete } = props;
    const [collpased, setCollapsed] = useState(false)

    return (
        <React.Fragment>
            <div className="bg-gray-300 w-full my-10 pb-5">
                <div className="bg-blue-500 h-8 flex items-center justify-between px-2">
                    <div className="flex">
                        <img src="./images/ev_icon.svg" width="25" />
                        <p className="text-white pl-2"> {formData.name} </p>
                        <p className="w-6 h-6 bg-blue-800 text-white flex items-center 
                                justify-center pb-1 ml-5 rounded-full hover:bg-blue-600 hover:cursor-pointer"
                            onClick={() => handleEVDelete(formData.id)}
                        > x </p>
                    </div>
                    <div
                        className="hover:cursor-pointer"
                        onClick={() => setCollapsed(value => !value)}
                    >
                        {collpased ? <img src="./images/collapse.svg" /> : <img src="./images/uncollapse.svg" />}
                    </div>
                </div>

                {
                    !collpased && <React.Fragment>
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
                    </React.Fragment>
                }


            </div>
        </React.Fragment>
    )
}