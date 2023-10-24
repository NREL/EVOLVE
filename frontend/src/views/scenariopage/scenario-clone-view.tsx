import React, { useState, useEffect } from 'react';
import { TextField } from '../../components/text-field';
import { handleChange, validateInput } from '../../helpers/form-related-utils';
import * as Yup from 'yup';
import { useSelector } from 'react-redux';
import { StateModel } from "../../interfaces/redux-state";
import axios from 'axios';
import { ScenarioDataInterface } from '../../interfaces/scenario-data-interfaces';

interface ScenarioCloneViewProps {
    setIsCloneClicked: React.Dispatch<React.SetStateAction<boolean>>;
    scenarioId: number;
    setIsClicked: React.Dispatch<React.SetStateAction<ScenarioDataInterface | null>>;
    setReload: React.Dispatch<React.SetStateAction<number>>;
    scenarioName: string;
}

interface ScenarioCloneInterface {
    name: string
}

export const ScenarioCloneView: React.FC<ScenarioCloneViewProps> = ({
    setIsCloneClicked, scenarioId, setIsClicked, setReload, scenarioName
}) => {

    const accessToken = useSelector((state: StateModel) => state.auth.accessToken)
    const [cloneFormData, setCloneFormData] = useState<ScenarioCloneInterface>({
        name: ''
    })
    const [errors, setErrors] = useState<Record<string, string>>({})
    const validationSchema = Yup.object({
        name: Yup.string().required().max(20)
    })

    useEffect(() => {
        validateInput(cloneFormData, validationSchema, setErrors)
    }, [cloneFormData])

    const handleScenarioClone = (e: any) => {
        e.preventDefault()
        axios.post(
            `/scenario/clone/${scenarioId}`,
            cloneFormData,
            { headers: { 'Authorization': 'Bearer ' + accessToken } },
        ).then((response) => {
            console.log(response)
            setIsCloneClicked(false)
            setIsClicked(null)
            setReload((value: number) => value + 1)
        }).catch((error) => {
            console.log(error)
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
        }
        )
    }

    return (
        <div className="w-1/2 h-[250px] bg-white 
            shadow-md px-10 py-8 relative">
            <div className="absolute right-3 top-2 bg-gray-300 rounded-full 
                    w-8 h-8 flex justify-center items-center hover:cursor-pointer hover:bg-gray-400"
                onClick={() => setIsCloneClicked(false)}> X </div>
            <p className="border-b mb-2"> Cloning scenario <span className="text-blue-500 font-bold"> {scenarioName} </span></p>
            <form onSubmit={handleScenarioClone}>
                <h1 className="mb-3"> Name for cloned scenario  </h1>
                <TextField
                    error={errors.name}
                    name="name"
                    type="text"
                    value={cloneFormData.name}
                    onChange={(e: any) => handleChange(e, cloneFormData, setCloneFormData)}
                />

                <button className="my-5 bg-blue-500 text-white px-2 py-1
                hover:cursor-pointer hover:bg-blue-600 rounded-md" type="submit"> Clone scenario </button>
            </form>

        </div>
    )
}