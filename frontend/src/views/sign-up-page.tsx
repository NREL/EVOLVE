import React, {useState, useEffect} from 'react';
import * as Yup from 'yup';
import { handleChange, validateInput } from '../helpers/form-related-utils';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


interface SignUpPageProps {

}

export const SignUpPage: React.FC<SignUpPageProps> = ({}) => {

        const [signUpFormData, setSignUpFormData] = useState({
            'username': '', 'hashed_password': '', 'email': ''
        });
        const navigate = useNavigate()
        const [errors, setErrors] = useState<Record<string, string>>({})
        const validationSchema = Yup.object({
            username: Yup.string().required().max(20),
            hashed_password: Yup.string().required().min(8),
            email: Yup.string().required()
        })

        useEffect(() => {
            validateInput(signUpFormData, validationSchema, setErrors)
        }, [signUpFormData])

        const handleSignUp = (e: any) => {
            e.preventDefault()
            axios.post(
                `/users`,
                signUpFormData
            ).then((response) => {
                console.log(response)
                navigate('/login')
            }).catch((error) => {
                console.log(error)
            }
            )
        }

        return (
            <div>
                <form className="w-1/3 mt-5 mb-5 mx-auto 
                    bg-white p-10 shadow-md"
                    onSubmit={handleSignUp}>

                    <h1 className="text-blue-500 font-bold text-xl pb-5"> EVOLVE Sign Up</h1>

                    <div >
                        <label> Username </label> 
                        
                        <div className="mb-2">
                            <input 
                                className={
                                    `w-full mt-2 bg-gray-300 px-2 py-1 outline-none text-blue-500 rounded-md ${errors.username ? 'border-2 border-red-500': ''}`
                                }
                            type="text" 
                            name="username" 
                            value={signUpFormData.username} 
                            onChange={(e: any) => handleChange(e, signUpFormData, setSignUpFormData)}/>
                            {errors.username && <p className="text-sm text-red-500">{errors.username}</p>}
                        </div>
              
                        <label> Password </label> 
                        <div className="mb-2">
                            <input 
                                className={
                                    `w-full mt-2 bg-gray-300 px-2 py-1 outline-none text-blue-500 rounded-md ${errors.hashed_password ? 'border-2 border-red-500': ''}`
                                }
                            type="password" 
                            name="hashed_password" 
                            value={signUpFormData.hashed_password} 
                            onChange={(e: any) => handleChange(e, signUpFormData, setSignUpFormData)}/>
                            {errors.hashed_password && <p className="text-sm text-red-500">{errors.hashed_password.replace('hashed_', '')}</p>}
                        </div>

                        <label> Email </label> 
                        
                        <div>
                            <input 
                                className={
                                    `w-full mt-2 bg-gray-300 px-2 py-1 outline-none text-blue-500 rounded-md ${errors.email ? 'border-2 border-red-500': ''}`
                                }
                            type="text" 
                            name="email" 
                            value={signUpFormData.email} 
                            onChange={(e: any) => handleChange(e, signUpFormData, setSignUpFormData)}/>
                            {errors.email && <p className="text-sm text-red-500">{errors.email}</p>}
                        </div>
                   
                    </div>
                   
                    <div className="flex justify-left pb-3">
                        <button className="bg-blue-500 mr-3 px-5 text-white py-1 rounded-2xl mt-5" 
                        type="submit"
                        > Sign Up </button>
                    </div>

                    <a className="text-blue-500 text-sm border-b
                        hover:cursor-pointer hover:text-orange-400"
                        onClick={()=> navigate('/login')}
                    > Login </a>
                </form>
            </div>
        )}