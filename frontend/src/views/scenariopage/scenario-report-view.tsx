import React, {useState, useEffect} from 'react';
import { ScenarioDataInterface } from '../../interfaces/scenario-data-interfaces';
import * as Yup from 'yup';
import { useSelector } from 'react-redux';
import { StateModel } from "../../interfaces/redux-state";
import axios from 'axios';
import { handleChange, validateInput } from '../../helpers/form-related-utils';
import { TextField } from '../../components/text-field';

interface ScenarioReportViewProps {
    setIsRunClicked: React.Dispatch<React.SetStateAction<boolean>>;
    scenarioId: number;
    setIsClicked: React.Dispatch<React.SetStateAction<ScenarioDataInterface | null>>;
    setReload: React.Dispatch<React.SetStateAction<number>>;
    scenarioName: string;
}

export const ScenarioReportView: React.FC<ScenarioReportViewProps> = ({
    setIsRunClicked, scenarioId, setIsClicked, setReload, scenarioName
}) => {
        const accessToken = useSelector((state: StateModel) => state.auth.accessToken)
        const [runFormData, setRunFormData] = useState<{name: string; description: string}>({
            name: '',
            description: ''
        })
        const [errors, setErrors] = useState<Record<string, string>>({})
        const validationSchema = Yup.object({
            name: Yup.string().required().max(20),
            description: Yup.string().required().max(1000)
        })

        useEffect(() => {
            validateInput(runFormData, validationSchema, setErrors)
        }, [runFormData])

        const handleRunScenario = (e: any) => {
            e.preventDefault()
            axios.post(
                `/scenario/${scenarioId}/report`,
                runFormData,
                { headers: { 'Authorization': 'Bearer ' + accessToken } },
            ).then((response) => {
                console.log(response)
                setIsRunClicked(false)
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
            <div className="w-1/2 bg-white 
            shadow-md px-10 py-8 relative">
            <div className="absolute right-3 top-2 bg-gray-300 rounded-full 
                    w-8 h-8 flex justify-center items-center hover:cursor-pointer hover:bg-gray-400"
                onClick={() => setIsRunClicked(false)}> X </div>
            <p className="border-b mb-2"> Running scenario <span className="text-blue-500 font-bold"> {scenarioName} </span></p>
            <form onSubmit={handleRunScenario}>
                <h1 className="mb-3"> Report name  </h1>
                <TextField
                    error={errors.name}
                    name="name"
                    type="text"
                    value={runFormData.name}
                    onChange={(e: any) => handleChange(e, runFormData, setRunFormData)}
                />

                <h1 className="my-3"> Report description  </h1>
                <TextField
                    error={errors.description}
                    name="description"
                    type="text"
                    value={runFormData.description}
                    onChange={(e: any) => handleChange(e, runFormData, setRunFormData)}
                />

                <button className="my-5 bg-blue-500 text-white px-2 py-1
                hover:cursor-pointer hover:bg-blue-600 rounded-md" type="submit"> Run scenario </button>
            </form>

        </div>
        );
}