import React, {useState, useEffect} from 'react';
import { TextField } from '../../components/text-field';
import { handleChange } from '../../helpers/form-related-utils';
import * as Yup from 'yup';
import { validateInput } from '../../helpers/form-related-utils';
import { useSelector } from 'react-redux';
import { StateModel } from "../../interfaces/redux-state";
import axios from 'axios';

interface CreateLabelViewProps {
    setLabelCreateView: React.Dispatch<React.SetStateAction<boolean>>
}

interface LabelFormInterface {
    name: string;
    description: string;
}


export const CreateLabelView: React.FC<CreateLabelViewProps> = ({
    setLabelCreateView
}) => {
        const [formData, setFormData] = useState<LabelFormInterface>({
            name: '', description: ''
        })
        const [errors, setErrors] = useState<Record<string, any>>({})
        const accessToken = useSelector((state: StateModel) => state.auth.accessToken)
        const validationSchema = Yup.object({
            name: Yup.string().required().max(20),
            description: Yup.string().required().max(100)
        })

        useEffect(() => {
            validateInput(formData, validationSchema, setErrors)
        }, [formData])

        const handleLabelCreate = (e:any) => {
            e.preventDefault()
            axios.post(
                `/label`,
                formData,
                { headers: { 'Authorization': 'Bearer ' + accessToken } },
            ).then((response) => {
                console.log(response.data)
                setLabelCreateView(false)
            }).catch((error) => {
                console.log(error)
                if (error.response.status === 401) {
                    localStorage.removeItem('state')
                }
            })
        }


        return (
            <div className="w-1/3 bg-gray-300 p-10 shadow-md relative">
                <div className="absolute right-3 top-2 bg-gray-400 rounded-full 
                    w-8 h-8 flex justify-center items-center hover:cursor-pointer hover:bg-gray-500"
                onClick={() => setLabelCreateView(false)}> X </div>
                <h1 className="font-bold w-max border-b border-white"> 
                Create tag or label </h1>

                <form onSubmit={handleLabelCreate}>
                    <div className="my-3">
                        <p className="mb-2"> Name </p> 
                        <TextField
                            error={errors.name}
                            name="name"
                            type="text"
                            value={formData.name}
                            onChange={(e:any)=> handleChange(e, formData, setFormData)}
                        />
                    </div>

                    <div className="mb-3">
                        <p className="mb-2"> Description </p> 
                        <TextField
                            error={errors.description}
                            name="description"
                            type="text"
                            value={formData.description}
                            onChange={(e:any)=> handleChange(e, formData, setFormData)}
                        />
                    </div>

                    <button className="bg-blue-500 mt-2 px-2 py-1 rounded-md 
                        hover:cursor-pointer hover:bg-blue-600 text-white" type="submit"> Create </button>
                </form>

            </div>
        )
}