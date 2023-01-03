import React, { useEffect, useState } from 'react';
import { TextField } from '../../components/text-field';
import { TechnologiesView } from './technologies-view';
import { BaseSettingsView } from './base-settings-view';
import { SolarSettingsView } from './solar-settings-view';
import { EVSettingsView } from './ev-settings-view';
import { ESSettingsView } from './es-settings-view';
import {
    handleChangeArray, handleChange, validateInput,
    validateSolarInputArray, validateInputArray,
    validateESInputArray
} from '../../helpers/form-related-utils';
import {
    newESDataInterface, newSolarDataInterface,
    newEVDataInterface
} from '../../interfaces/create-scenario-interfaces';
import {
    UseSolarForm, UseESForm, UseEVForm, UseBasicForm,
    UseTimeseriesData, UseSelectedProfile
} from '../../hooks/createscenariopage';
import { useFormValidation } from '../../hooks/createscenariopage/use-form-validation';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { StateModel } from "../../interfaces/redux-state";


export function CreateScenario(props: any) {

    // Form error 
    const { navigation } = props;
    const [formError, setFormError] = useState(false)
    const accessToken = useSelector((state: StateModel) => state.auth.accessToken)

    // Get time series data
    const [allTSdata, setallTSdata] = UseTimeseriesData()

    // Get basic form data 
    const [formData, setFormData, errors, setErrors,
        selectedProfile, setSelectedProfile,
        fillData, setFillData, dateRange, setDateRange] = props.updateFlag &&
            props.initialFormData.basic ? UseBasicForm(
                props.initialFormData.basic, props.initialLoadProfile
            ) : UseBasicForm(null, null)

    // Get solar form data
    const [solarFormDataArray, setSolarFormDataArray,
        solarErrorsArray, setSolarErrorsArray, handleAddSolar,
        handleSolarDelete, selectedIrrProfile, setSelectedIrrProfile] = props.updateFlag &&
            props.initialFormData.solar ?
            UseSolarForm(props.initialFormData.solar, props.irrProfiles) :
            UseSolarForm(null, null)

    // Get energy storage form data
    const [esFormDataArray, setESFormDataArray,
        esErrorsArray, setESErrorsArray, handleAddEnergyStorage,
        handleEnergyStorageDelete, selectedPriceProfile, setSelectedPriceProfile] = props.updateFlag &&
            props.initialFormData.energy_storage ?
            UseESForm(props.initialFormData.energy_storage, props.priceProfiles) :
            UseESForm(null, null)

    // Get electric vehicle form data
    const [evFormDataArray, setEVFormDataArray,
        evErrorsArray, setEVErrorsArray, handleAddEV,
        handleEVDelete] = props.updateFlag &&
            props.initialFormData.ev ? UseEVForm(props.initialFormData.ev) : UseEVForm(null)

    // Get selected profiles states
    UseSelectedProfile(formData.resolution, selectedProfile,
        selectedIrrProfile, selectedPriceProfile, setDateRange, setFillData)


    // Get validation schema for all form types
    const [solarValidationSchema,
        esValidationSchema,
        basicValidationSchema,
        evValidationSchema
    ] = useFormValidation(dateRange)

    useEffect(() => {
        validateSolarInputArray(solarFormDataArray, solarValidationSchema,
            setSolarErrorsArray, selectedIrrProfile)
    }, [solarFormDataArray, selectedIrrProfile])

    useEffect(() => {
        validateInput(formData, basicValidationSchema, setErrors)
    }, [formData, dateRange])

    useEffect(() => {
        validateInputArray(evFormDataArray, evValidationSchema,
            setEVErrorsArray)
    }, [evFormDataArray])

    useEffect(() => {
        validateESInputArray(esFormDataArray, esValidationSchema,
            setESErrorsArray, selectedPriceProfile)
    }, [esFormDataArray, selectedPriceProfile])


    const handleFormSubmit = (e: any) => {
        e.preventDefault()

        // needs to do validation before we submit
        if (Object.keys(errors).length > 0) {
            setFormError(true)
            return
        }

        // Check for errors in solar array form
        if (formData.technologies.includes('solar')) {
            solarFormDataArray.forEach((item) => {
                if (Object.keys(item).length > 0) {
                    setFormError(true)
                    return
                }
            })
        }

        // Check for errors in ev form
        if (formData.technologies.includes('ev')) {
            evFormDataArray.forEach((item) => {
                if (Object.keys(item).length > 0) {
                    setFormError(true)
                    return
                }
            })
        }

        // Check for errors in es form
        if (formData.technologies.includes('energy_storage')) {
            esFormDataArray.forEach((item) => {
                if (Object.keys(item).length > 0) {
                    setFormError(true)
                    return
                }
            })
        }

        setFormError(false)
        let fullFormData = {
            'basic': {
                ...formData,
                'loadProfile': selectedProfile ? selectedProfile.id : ''
            },
            'solar': formData.technologies.includes('solar') ? solarFormDataArray.map(
                (d: Record<string, any>) => {
                    return {
                        ...d,
                        'irradianceData': selectedIrrProfile.filter((irr) => irr.name === d.name)[0].data?.id
                    }
                }
            ) : [],
            'ev': formData.technologies.includes('ev') ? evFormDataArray : [],
            'energy_storage': formData.technologies.includes('energy_storage') ? esFormDataArray.map(
                (d: Record<string, any>) => {
                    return {
                        ...d,
                        'priceProfile': selectedPriceProfile.filter((irr) => irr.name === d.name)[0].data.id
                    }
                }
            ) : [],
        }

        console.log(fullFormData)
        if (props.updateFlag) {
            props.onUpdate(fullFormData)
        } else {
            axios.post(
                '/scenario',
                fullFormData,
                { headers: { 'Authorization': 'Bearer ' + accessToken } },
            ).then((response) => {
                console.log(response)
                navigation('/scenarios')
            }).catch((error) => {
                console.log(error)
                if (error.response.status === 401) {
                    localStorage.removeItem('state')
                }
            }
            )
        }


    }

    return (

        <div className="my-10 mx-20">

            <form onSubmit={handleFormSubmit}>

                {

                    props.updateFlag ? <p className="text-blue-500 font-bold text-xl border-b-2 
                    w-max mb-3"> Update Scenario </p> :
                        <p className="text-blue-500 font-bold text-xl border-b-2 
                    w-max mb-3"> Create Scenario </p>
                }

                <div className="flex">
                    <p className="pr-3"> Name </p>

                    <TextField
                        error={errors.scenarioName}
                        name="scenarioName"
                        type="text"
                        placeholder="Enter scenario name"
                        value={formData.scenarioName}
                        onChange={(e: any) => handleChange(e, formData, setFormData)}
                    />


                </div>

                <TechnologiesView
                    handleChange={(e: any) => handleChange(e, formData, setFormData)}
                    technologies={formData.technologies}
                />


                <BaseSettingsView
                    handleChange={(e: any) => handleChange(e, formData, setFormData)}
                    formData={formData}
                    errors={errors}
                    allTSdata={allTSdata}
                    selectedProfile={selectedProfile}
                    setSelectedProfile={setSelectedProfile}
                    dateRange={dateRange}
                    fillData={fillData}
                    updateFlag={props.updateFlag}
                />
                {
                    formData.technologies.includes('solar') && <div>
                        {
                            solarFormDataArray.length <= 5 && <div>
                                <p className='bg-blue-500 bg-blue-500 text-white rounded-md px-2 w-max py-1'
                                    onClick={handleAddSolar}> Add solar </p>
                                <p className='text-sm text-gray-500 pb-2'> Add upto 5 PV systems. </p>
                            </div>
                        }
                        {
                            solarFormDataArray.map((solarItem: newSolarDataInterface, index: number) => {
                                return <div key={solarItem.id} className="flex">
                                    <SolarSettingsView
                                        formData={solarItem}
                                        handleChange={(e: any) => handleChangeArray(
                                            e, solarItem.id, solarFormDataArray, setSolarFormDataArray)}
                                        errors={solarErrorsArray[index]}
                                        allTSdata={allTSdata}
                                        selectedIrrProfile={selectedIrrProfile[index]}
                                        setSelectedIrrProfile={setSelectedIrrProfile}
                                        handleSolarDelete={handleSolarDelete}
                                        updateFlag={props.updateFlag}
                                    />
                                </div>
                            })
                        }
                    </div>
                }
                {
                    formData.technologies.includes('ev') && <div>
                        {evFormDataArray.length <= 5 &&
                            <div>
                                <p className='bg-blue-500 bg-blue-500 text-white rounded-md px-2 py-1 w-max'
                                    onClick={handleAddEV}> Add electric vehicle </p>
                                <p className='text-sm text-gray-500 pb-2'> Add upto 5 Electric Vehicles </p>
                            </div>
                        }
                        {
                            evFormDataArray.map(
                                (
                                    evItem: newEVDataInterface,
                                    index: number
                                ) => {
                                    return <div key={evItem.id} className="flex">

                                        <EVSettingsView
                                            handleChange={(e: any) => handleChangeArray(
                                                e, evItem.id, evFormDataArray, setEVFormDataArray)}
                                            formData={evItem}
                                            errors={evErrorsArray[index]}
                                            handleEVDelete={handleEVDelete}
                                        />

                                    </div>
                                }
                            )
                        }

                    </div>


                }
                {
                    formData.technologies.includes('energy_storage') && <div>
                        {
                            esFormDataArray.length <= 5 && <div>
                                <p className='bg-blue-500 bg-blue-500 text-white rounded-md px-2 py-1 w-max'
                                    onClick={handleAddEnergyStorage}> Add energy storage </p>
                                <p className='text-sm text-gray-500 pb-2'> Add upto 5 Energy Storage Systems </p>
                            </div>
                        }
                        {
                            esFormDataArray.map(
                                (
                                    esItem: newESDataInterface,
                                    index: number
                                ) => {
                                    return <div key={esItem.id} className="flex">
                                        <ESSettingsView
                                            handleChange={(e: any) => handleChangeArray(
                                                e, esItem.id, esFormDataArray, setESFormDataArray)}
                                            formData={esItem}
                                            errors={esErrorsArray[index]}
                                            allTSdata={allTSdata}
                                            selectedPriceProfile={selectedPriceProfile}
                                            setSelectedPriceProfile={setSelectedPriceProfile}
                                            handleEnergyStorageDelete={handleEnergyStorageDelete}
                                            updateFlag={props.updateFlag}
                                        />
                                    </div>
                                }
                            )

                        }
                    </div>
                }

                <button className="bg-blue-500 px-3 text-white font-bold rounded-md py-1" type="submit">
                    {props.updateFlag ? 'Update' : 'Submit'} </button>
                {
                    formError && <p className="text-red-500"> Fix errors first before submitting ! &#x1F613;</p>
                }

                {/* {
                    JSON.stringify(evFormDataArray, null, 2)
                } */}


            </form>

        </div>
    )
}