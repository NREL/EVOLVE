import React, { useEffect, useState } from 'react';
import * as Yup from 'yup';
import { TextField } from '../../components/text-field';
import { TechnologiesView } from './technologies-view';
import { BaseSettingsView } from './base-settings-view';
import { SolarSettingsView} from './solar-settings-view';
import { EVSettingsView } from './ev-settings-view';
import { ESSettingsView } from './es-settings-view';


export function CreateScenario(props: any)  {

    const [formData, setFormData] = useState<Record<string, any>>({
        scenarioName: '',
        technologies: [],
        loadProfile: '',
        startDate: new Date(),
        endDate: new Date(),
        solarCapacity: 10,
        irradianceData: '',
        panelAzimuth: 0,
        panelTilt: 0,
        numberOfEV: 1,
        pctResEV: 100,
        isESOptimal: false,
        esPowerCapacity: 10,
        esEnergyCapacity: 10,
        esStrategy: 'time',
        chargingHours: '',
        disChargingHours: '',
        chargingPrice: 0,
        disChargingPrice: 0,
        priceProfile: '',
        esChargingThreshold: 0.6,
        esDischargingThreshold: 0.5
    })
    const [errors, setErrors] = useState<Record<string, string>>({})

    const validationSchema = Yup.object({
        scenarioName: Yup.string().required().max(10),
        loadProfile: Yup.string().required(),
        startDate: Yup.date(),
        endDate: Yup.date(),
        solarCapacity: Yup.number().positive(),
        panelAzimuth: Yup.number().min(0).max(360),
        panelTilt: Yup.number().min(0).max(90),
        numberOfEV: Yup.number().positive(),
        pctResEV: Yup.number().min(0).max(100),
        esPowerCapacity: Yup.number().positive(),
        esEnergyCapacity: Yup.number().positive()
    })

    const handleChange = (e: any) => {

     
        if (e.target.type == 'checkbox') {

            if (formData[e.target.name] instanceof Array) {
                let items = formData[e.target.name];
                if (e.target.checked && !items.includes(e.target.value)) {
                    items.push(e.target.value)
                } else if (!e.target.checked && items.includes(e.target.value)){
                    items.splice(items.indexOf(e.target.value))
                }
                setFormData({...formData, 
                    [e.target.name]: items})

            } else {
                setFormData({...formData, 
                    [e.target.name]: e.target.checked})
            }

        } else {

            setFormData({...formData, 
                [e.target.name]: e.target.value})
        }
        
    }

    useEffect(()=> {
        validationSchema.validate(formData, { abortEarly: false }).catch((err)=> {
            setErrors(err.inner.reduce((result:any, item:any)=> {
                result[item.path] = item.message
                return result
            }, {}))
        })
        
    }, [formData])

    

    return (
        
        <div className="my-10 mx-20">
            
            <form>

                <p className="text-blue-500 font-bold text-xl border-b-2 
                    w-max mb-3"> Create Scenario </p>

                <div className="flex">
                    <p className="pr-3"> Name </p>

                    <TextField 
                        error={errors.scenarioName}
                        name="scenarioName"
                        placeholder="Enter scenario name"
                        value={formData.scenarioName}
                        onChange={handleChange}
                    />
                    

                </div>

                <TechnologiesView handleChange={handleChange}/>
                <BaseSettingsView handleChange={handleChange} formData={formData} errors={errors}/>
                {
                    formData.technologies.includes('solar') && 
                    <SolarSettingsView handleChange={handleChange} formData={formData} errors={errors} />
                }
                {
                    formData.technologies.includes('ev') && 
                    <EVSettingsView handleChange={handleChange} formData={formData} errors={errors}/>
                }
                {
                    formData.technologies.includes('energy_storage') && 
                    <ESSettingsView handleChange={handleChange} formData={formData} errors={errors}/>
                }

                <button className="bg-blue-500 px-3 text-white font-bold rounded-md py-1"> Submit </button>
                

                
                {/* <pre>
                    {JSON.stringify(formData, null, 2)}
                </pre>
                <pre>
                    {JSON.stringify(errors, null, 2)}
                </pre> */}
                

            </form>

        </div>
    )
}