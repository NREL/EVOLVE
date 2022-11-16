import React, { useEffect, useState } from 'react';
import * as Yup from 'yup';
import { TextField } from '../../components/text-field';
import { TechnologiesView } from './technologies-view';
import { BaseSettingsView } from './base-settings-view';
import { SolarSettingsView} from './solar-settings-view';
import { EVSettingsView } from './ev-settings-view';
import { ESSettingsView } from './es-settings-view';
import axios from 'axios';
import {StateModel} from '../../interfaces/redux-state';
import {useSelector} from 'react-redux';
import {handleChangeArray, handleChange, validateInput, 
    validateInputArray} from '../../helpers/form-related-utils';
import {newESDataInterface, newSolarDataInterface} from '../../interfaces/create-scenario-interfaces';
import {UseSolarForm, UseESForm} from '../../hooks/createscenariopage';
import { useFormValidation } from '../../hooks/createscenariopage/use-form-validation';

export function CreateScenario(props: any)  {

    const [dateRange, setDateRange] = useState({
        min: "1990-01-01",
        max: "2050-01-01"
    })
    const [allTSdata, setallTSdata] = useState<Record<string, any>>([])
    const [selectedProfile, setSelectedProfile] = useState<Record<string, any>>({})
    const [selectedIrrProfile, setSelectedIrrProfile] = useState<Record<string, any>>({})
    const [selectedPriceProfile, setSelectedPriceProfile] = useState<Record<string, any>>({})
    const [fillData, setFillData] = useState(false)
    const [errors, setErrors] = useState<Record<string, string>>({})
    

    const [formData, setFormData] = useState<Record<string, any>>({
        scenarioName: '',
        technologies: [],
        loadProfile: '',
        startDate: null,
        endDate: null,
        resolution: 1,
        dataFillingStrategy: 'interpolate',
        numberOfEV: 1,
        pctResEV: 100
    })

    const [solarFormDataArray, setSolarFormDataArray,
        solarErrorsArray, setSolarErrorsArray, handleAddSolar, 
        handleSolarDelete] = UseSolarForm()

    const [solarValidationSchema] = useFormValidation(formData, selectedIrrProfile)
    
    const [esFormDataArray, setESFormDataArray,
        esErrorsArray, setESErrorsArray, handleAddEnergyStorage, 
        handleEnergyStorageDelete] = UseESForm()

    const validationSchema:any = Yup.object({
        scenarioName: Yup.string().required().max(20),
        loadProfile: Yup.string().required().test(
            {
                message: "Load profile is not selected",
                test: function(this:any) {
                    return selectedProfile.name ? true : false
                }
            }
        ),
        startDate: Yup.date().min(dateRange.min).max(dateRange.max),
        endDate: Yup.date().min(Yup.ref('startDate')?Yup.ref('startDate'):dateRange.min).max(dateRange.max),
        resolution: Yup.number().positive().integer().test({
            message: "Resolution should be factor of all data resolution.",
            test: function(this:any, val:any) {
                return (
                    selectedProfile.name ? selectedProfile.resolution_min % val === 0: true &&
                    selectedIrrProfile.name ? selectedIrrProfile.resolution_min % val === 0: true &&
                    selectedPriceProfile.name ? selectedPriceProfile.resolution_min % val === 0: true
                )
            }
        }),
        numberOfEV: Yup.number().positive(),
        pctResEV: Yup.number().min(0).max(100),
        esPowerCapacity: Yup.number().positive(),
        esEnergyCapacity: Yup.number().positive(),
        priceProfile: Yup.string().test(    
            {   
                message: "Price profile is not selected",   
                test: function(this:any) {  
                    if (this.parent.technologies.includes('energy_storage') && 
                    this.parent.esStrategy === 'price'
                    ){  
                        return selectedPriceProfile.name ? true : false
                    }
                    return true
                }
            }
        ),
    })
    
    
    

    const accessToken = useSelector((state:StateModel) => state.auth.accessToken)
    
    useEffect(()=> {  
        axios.get(
            `/data`,
            {headers: {'Authorization': 'Bearer ' + accessToken}}
        ).then((response)=> {
            setallTSdata(response.data)
        }).catch((error)=> {
            console.log(error)
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
        })
    }, [])

    useEffect(()=> {

        const maxDataResolution = Math.max(...[
            selectedProfile.name ? selectedProfile.resolution_min: 0,
            selectedIrrProfile.name ? selectedIrrProfile.resolution_min: 0,
            selectedPriceProfile.name ? selectedPriceProfile.resolution_min: 0
        ])

        if (maxDataResolution !==0 && formData.resolution < maxDataResolution){
            setFillData(true)
        } else {
            setFillData(false)
        }

    }, [formData.resolution, selectedProfile, selectedIrrProfile, selectedPriceProfile ])

    useEffect(()=> {
        if (selectedProfile.start_date || selectedIrrProfile.start_date){
            setDateRange({
                min: new Date(Math.max(...[ 
                    new Date(selectedProfile.start_date ? selectedProfile.start_date : '1990-01-01' ).getTime(),
                    new Date(selectedIrrProfile.start_date ? selectedIrrProfile.start_date : '1990-01-01').getTime(),
                ])).toISOString().split('T')[0],
                max: new Date(Math.min(...[ 
                    new Date(selectedProfile.end_date ? selectedProfile.end_date: "2050-01-01" ).getTime(),
                    new Date(selectedIrrProfile.end_date ? selectedIrrProfile.end_date: "2050-01-01" ).getTime(),
                ])).toISOString().split('T')[0]
            })
        } else {
            setDateRange({
                min: "1990-01-01",
                max: "2050-01-01"
            })
        }
        
    }, [selectedProfile, selectedIrrProfile])

    
    useEffect(()=> {
        validateInput(formData, validationSchema, setErrors)
        validateInputArray(solarFormDataArray, solarValidationSchema, setSolarErrorsArray)

    }, [formData, dateRange, solarFormDataArray])

    const handleFormSubmit = (e:any) => {
        e.preventDefault()
        validateInput(formData, validationSchema, setErrors)
        // validateInput(solarFormData, solarValidationSchema, setSolarErrors)
        validationSchema.isValid(formData).then(
            (val:any)=> {
                if (val){
                    console.log('Validated! +++++ ', val)
                } else {
                    console.log('Invalid ---', val)
                }
            }
        ).catch((err:any)=> {
            console.log('Error running a validation')
        })
    }

    return (
        
        <div className="my-10 mx-20">
            
            <form onSubmit={handleFormSubmit}>

                <p className="text-blue-500 font-bold text-xl border-b-2 
                    w-max mb-3"> Create Scenario </p>

                <div className="flex">
                    <p className="pr-3"> Name </p>

                    <TextField 
                        error={errors.scenarioName}
                        name="scenarioName"
                        type="text"
                        placeholder="Enter scenario name"
                        value={formData.scenarioName}
                        onChange={(e:any)=> handleChange(e, formData, setFormData)}
                    />
                    

                </div>

                <TechnologiesView handleChange={(e:any)=> handleChange(e, formData, setFormData)}/>
                <BaseSettingsView 
                    handleChange={(e:any)=> handleChange(e, formData, setFormData)} 
                    formData={formData} 
                    errors={errors}
                    allTSdata={allTSdata}
                    selectedProfile={selectedProfile}
                    setSelectedProfile={setSelectedProfile} 
                    dateRange= {dateRange} 
                    fillData={fillData} 
                />
                {
                    formData.technologies.includes('solar') && <div>
                        <button className='bg-blue-500 bg-blue-500 text-white rounded-md px-2 py-1 disabled:bg-red-500'
                            onClick={handleAddSolar} disabled={solarFormDataArray.length >= 5}> Add solar </button>
                        <p className='text-sm text-gray-500 pb-2'> Add upto 5 PV systems. </p>
                        {
                            solarFormDataArray.map((solarItem: newSolarDataInterface, index:number)=> {
                                return <div key={solarItem.id} className="flex">
                                    <SolarSettingsView 
                                        formData={solarItem}
                                        handleChange={(e:any)=> handleChangeArray(
                                            e, solarItem.id, solarFormDataArray , setSolarFormDataArray)} 
                                        errors={solarErrorsArray[index]} 
                                        allTSdata={allTSdata}
                                        selectedIrrProfile={selectedIrrProfile} 
                                        setSelectedIrrProfile={setSelectedIrrProfile}
                                        handleSolarDelete={handleSolarDelete} 
                                    />
                                </div>
                            })
                        }
                    </div>
                }
                {
                    formData.technologies.includes('ev') && 
                    <EVSettingsView 
                        handleChange={(e:any)=> handleChange(e, formData, setFormData)} 
                        formData={formData} 
                        errors={errors}
                    />
                }
                {
                    formData.technologies.includes('energy_storage') && <div>
                        <button className='bg-blue-500 bg-blue-500 text-white rounded-md px-2 py-1 disabled:bg-red-500'
                            onClick={handleAddEnergyStorage} disabled={esFormDataArray.length >= 5}> Add energy storage </button>
                        <p className='text-sm text-gray-500 pb-2'> Add upto 5 Energy Storage Systems </p>
                        {
                            esFormDataArray.map(
                                (
                                    esItem: newESDataInterface,
                                    index: number
                                ) => {
                                    return <div key={esItem.id} className="flex">
                                        <ESSettingsView 
                                            handleChange={(e:any)=> handleChangeArray(
                                                e, esItem.id, esFormDataArray, setESFormDataArray)} 
                                            formData={esItem} 
                                            errors={esErrorsArray[index]}
                                            allTSdata={allTSdata}
                                            selectedPriceProfile={selectedPriceProfile} 
                                            setSelectedPriceProfile={setSelectedPriceProfile}
                                            handleEnergyStorageDelete={handleEnergyStorageDelete}
                                        />
                                    </div>
                                }
                            )
                            
                        }
                    </div>
                }

                <button className="bg-blue-500 px-3 text-white font-bold rounded-md py-1" type="submit"> Submit </button>
                {/* <pre>
                    {JSON.stringify(solarFormDataArray, null, 2)}
                </pre>
                <pre>
                    {JSON.stringify(solarErrorsArray, null, 2)}
                </pre> */}

            </form>

        </div>
    )
}