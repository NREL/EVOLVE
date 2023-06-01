import { useState, useEffect } from "react";
import axios from 'axios';
import {useSelector} from 'react-redux';
import { useNavigate} from "react-router-dom";
import React from 'react';
import * as Yup from 'yup';
import { validateInput } from '../helpers/form-related-utils';
import { TimeSeriesDataCategory } from "../interfaces/data-manage-interfaces";
import { StateModel } from "../interfaces/redux-state";
import {HiOutlineInformationCircle} from 'react-icons/hi';
import { TransparentBackGroundLayout } from './utility/description-layout';

interface DescViewProps {
    setCloseView: React.Dispatch<React.SetStateAction<boolean>>
}

export const DataDescriptionView: React.FC<DescViewProps> = ({
    setCloseView
}) => {

    const kw_data = [
        ['2019-01-01 00:00:00', 400.2, 50.3],
        ['2019-01-01 00:10:00', 330.4, 78.3],
        ['2019-01-01 00:20:00', 420.0, 99.3],
        ['2019-01-01 00:30:00', 350.2, 10.3],
        ['2019-01-01 00:40:00', 451.2, 60.3],
        ['2019-01-01 00:50:00', 379.2, 30.3]
    ]

    const irr_data = [
        ['2019-01-01 00:00:00', 400.2, 600.3, 800.3],
        ['2019-01-01 00:10:00', 400.2, 600.3, 800.3],
        ['2019-01-01 00:20:00', 400.2, 600.3, 800.3],
        ['2019-01-01 00:30:00', 400.2, 600.3, 800.3],
        ['2019-01-01 00:40:00', 440.2, 600.3, 800.3],
        ['2019-01-01 00:50:00', 400.2, 600.3, 800.3]
    ]
    
    return <TransparentBackGroundLayout setCloseView={setCloseView}>
        <>
            <h1 className='font-bold pb-1 mb-3 text-xl border-b'> Data Requirements! </h1>
            <p> <span className="text-blue-500 font-bold"> Timestamp column </span> <br/>
             Before uploading csv file make sure you have column with datetime values in it. The data resolution 
             must be consistent otherwise upload would not be successful.

            </p>

            <p> <span className="text-blue-500 font-bold"> Irradiance data </span> <br/>
                If you are uploadling irradiance data make sure columns <span className="text-blue-500"> ghi </span>, 
                <span className="text-blue-500"> dhi </span>, 
                <span className="text-blue-500"> dni </span> exist along with column consisting of datetime values. 
                <span className="text-blue-500"> ghi </span> is an acronym for Global Horizontal Irradiance which represents
                the total amount of shortwave radiation received from above by a surface which is parallel to the ground.
                <span className="text-blue-500"> dhi </span>  is acronym for Diffused Horizontal Irradiance which represents 
                solar radiation that does not arrive on a direct path from the sun, 
                but has been scattered by clouds and particles in the atmosphere and comes equally from all directions. 
                <span className="text-blue-500"> dni </span> is acronym for Diffused Normal Irradiance which represents the 
                amount of light that is coming perpendicular to surface. The surface here represents ground or 
                something parallel to ground. 
            </p>

            <p className="pt-2"> e.g. kW csv file  </p>
            <table className='table-fixed w-full text-left mt-3'>
                <thead>
                    <tr className='border-b'>
                        <th> datetime</th>
                        <th> feeder 1</th>
                        <th> sample transformer </th>
                    </tr>
                </thead>
                <tbody>
                    {kw_data.map((item:any)=> {
                        return <tr className='border-b'>
                            {item.map((val:any)=> <td> {val} </td>)}
                        </tr>
                    })}
                </tbody>
            </table>

            <p className="pt-2"> e.g. Irradiance csv file  </p>
            <table className='table-fixed w-full text-left mt-3'>
                <thead>
                    <tr className='border-b'>
                        <th> datetime</th>
                        <th> ghi</th>
                        <th> dhi </th>
                        <th> dni </th>
                    </tr>
                </thead>
                <tbody>
                    {irr_data.map((item:any)=> {
                        return <tr className='border-b'>
                            {item.map((val:any)=> <td> {val} </td>)}
                        </tr>
                    })}
                </tbody>
            </table>


            
        </>
    </TransparentBackGroundLayout>
}

function DataUpload(props:any) {

    const [dataForm, setData] = useState({
        timestamp:undefined, resolution:undefined, category: TimeSeriesDataCategory.kW , 
        description: undefined
    })
    const [dataFile, setFile] = useState({
        file: null
    })
    const [closeDesView, setCloseDesView] = useState(true)
    const [descriptionComp, setDescriptionComp] = useState<any>(null)
    const [errors, setErrors] = useState<Record<string, string>>({})
    const validationSchema = Yup.object({
        timestamp: Yup.string().required(),
        resolution: Yup.number().required().min(0),
        description: Yup.string().required()
    })
    const [submitError, setSubmitError] = useState<any>(null)

    const navigation = useNavigate();

    useEffect(() => {
        validateInput(dataForm, validationSchema, setErrors)
    }, [dataForm])

    
    const handleChange = (event:any) => {
        setData({ ...dataForm, [event.target.name]: event.target.value });
      };

    const accessToken = useSelector((state:StateModel) => state.auth.accessToken)
    const handleSubmit = (event:any) => {
        event.preventDefault();
        
        if (Object.keys(errors).length > 0) {
            setSubmitError('Not so fast! Please fix the error first!')
            return
        }
        const formData = new FormData()
        formData.append('metadata', JSON.stringify(dataForm))

        if (dataFile['file']){
            formData.append('file', dataFile['file'])
            axios.post(
                '/data/upload',
                formData,
                {headers: {'Authorization': 'Bearer ' + accessToken}},
            ).then((response)=> {
                navigation('/data')
            }).catch((error)=> {
                console.log(error)
                if (error.response.status === 401) {
                    localStorage.removeItem('state')
                }
            }
            )
        } else {
            setSubmitError('Not so fast! Please upload the file first!')
            return 
        }
    }

    return (
        <>
            {!closeDesView && descriptionComp}
            <div className="h-[calc(100vh-70px)] w-full flex items-center justify-center">
                <form onSubmit={handleSubmit} className="w-1/2">
            
                <div className="bg-white p-10 shadow-md">
                    <div className="text-blue-500 
                        border-b text-xl pb-1 mb-3 flex 
                        items-center justify-between"> 
                        <p className="font-bold"> Upload data </p>
                        <div className="flex gap-x-1 text-blue-500 hover:cursor-pointer 
                            hover:text-blue-900"
                            onClick={()=> {
                                setCloseDesView(false)
                                setDescriptionComp(
                                    <DataDescriptionView setCloseView={setCloseDesView} />
                                )}}
                            >
                            <HiOutlineInformationCircle size={20} />
                            <p className="text-sm"> Learn about data requirements! </p>

                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-y-3 gap-x-5">

                        <div >
                            <label> Time stamp column name </label> <br/>
                            <input 
                                className={`w-full mt-2 bg-gray-300 px-2 py-1 outline-none 
                                    text-blue-500 rounded-md ` + 
                                    (errors.timestamp ? 'border-2 border-red-500': '')}
                                type="text"
                                name="timestamp"
                                placeholder="Enter column name for timestamp ..."
                                value={dataForm.timestamp || ''}
                                onChange={handleChange}
                                />
                            {errors.timestamp && <p className="text-sm text-red-500">{errors.timestamp}</p>}
                        </div>

                        <div>
                            <label> Data resolution (min.) </label> <br/>
                            <input 
                                className={`w-full mt-2 bg-gray-300 px-2 py-1 outline-none 
                                    text-blue-500 rounded-md ` + (errors.timestamp ? 'border-2 border-red-500': '')}
                                type="number"
                                name="resolution"
                                placeholder="Resolution in minute"
                                value={dataForm.resolution || ''}
                                onChange={handleChange}
                                />
                            {errors.resolution && <p className="text-sm text-red-500">{errors.resolution}</p>}
                        </div>

                        <div>
                            <label> Data category </label> <br/>
                            <select 
                                className="w-full mt-2 bg-gray-300 px-2 py-1 outline-none text-blue-500 rounded-md"
                                id="category" 
                                name="category"
                                value={dataForm.category}
                                onChange={handleChange}>
                                <option value="kW">kW</option>
                                <option value="irradiance">irradiance</option>
                            </select>
                        </div>

                        <div>
                            <label> Description </label> <br/>
                            <input 
                                type="textarea" 
                                className={`w-full mt-2 bg-gray-300 px-2 py-1 outline-none 
                                    text-blue-500 rounded-md ` + (errors.description ? 'border-2 border-red-500': '')}
                                name="description"
                                placeholder="Description"
                                value={dataForm.description || ''}
                                onChange={handleChange}/>
                            {errors.description && <p className="text-sm text-red-500">{errors.description}</p>}
                        </div>

                    </div>

                    <div>
                    <input 
                        className="mt-4" 
                        type="file"
                        name="file"
                        accept=".csv"
                        onChange={(event:any) => {
                            setFile({ ...dataFile, [event.target.name]: event.target.files[0] });
                            }}
                    />
                    <p className="text-sm"> Only csv file is accepted! </p>
                    </div>

                    <div className="flex mt-5 text-white">
                        <button className="bg-blue-500 mr-3 px-2 py-1 rounded-md
                            hover:bg-blue-700" type="submit"> Submit</button>
                        <button className="bg-blue-500 px-2 py-1 rounded-md
                            hover:bg-blue-700" onClick={()=> {props.navigation('/data')}}> Cancel </button>
                    </div>
                    {submitError && <p className="pt-2 font-bold text-red-500 
                        text-sm"> {submitError} </p>}
                </div>
            </form>
            </div>
        
        </>
    )
}

export {DataUpload}