import { useState } from "react";
import axios from 'axios';
import {useSelector} from 'react-redux';
import { useNavigate} from "react-router-dom";
import React from 'react';
import { TimeSeriesDataCategory } from "../interfaces/data-manage-interfaces";
import { StateModel } from "../interfaces/redux-state";

function DataUpload(props:any) {

    const [dataForm, setData] = useState({
        timestamp:null, resolution:null, category: TimeSeriesDataCategory.kW , description: null
    })
    const [dataFile, setFile] = useState({
        file: null
    })
    const navigation = useNavigate();
    
    const handleChange = (event:any) => {
        setData({ ...dataForm, [event.target.name]: event.target.value });
      };
    const accessToken = useSelector((state:StateModel) => state.auth.accessToken)
    const handleSubmit = (event:any) => {
        event.preventDefault();
        
        const formData = new FormData()
        formData.append('metadata', JSON.stringify(dataForm))

        if (dataFile['file']){
            formData.append('file', dataFile['file'])
        }
        
        axios.post(
            '/data/upload',
            formData,
            {headers: {'Authorization': 'Bearer ' + accessToken}},
        ).then((response)=> {
            console.log(response)
            navigation('/data')
        }).catch((error)=> {
            console.log(error)
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
        }
        )
    }

    return (
        <form onSubmit={handleSubmit}>
            <div className="w-1/2 mt-16 mb-5 mx-auto bg-white p-10">
                <h1 className="text-center text-blue-500 font-bold text-xl pb-5"> Upload data</h1>

                <div className="grid grid-cols-2 gap-y-3 gap-x-3">

                    <div >
                        <label> Time stamp column name </label> <br/>
                        <input 
                            className="w-full mt-2 bg-gray-300 px-2 py-1 outline-none text-blue-500 rounded-md"
                            type="text"
                            name="timestamp"
                            placeholder="Enter column name for timestamp ..."
                            value={dataForm.timestamp || ''}
                            onChange={handleChange}
                            />
                    </div>

                    <div>
                        <label> Data resolution (min.) </label> <br/>
                        <input 
                            className="w-full mt-2 bg-gray-300 px-2 py-1 outline-none text-blue-500 rounded-md"
                            type="number"
                            name="resolution"
                            placeholder="Resolution in minute"
                            value={dataForm.resolution || ''}
                            onChange={handleChange}
                            />
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
                            className="w-full mt-2 bg-gray-300 px-2 py-1 outline-none text-blue-500 rounded-md"
                            name="description"
                            placeholder="Description"
                            value={dataForm.description || ''}
                            onChange={handleChange}/>
                    </div>

                </div>

                <input 
                    className="mt-4" 
                    type="file"
                    name="file"
                    onChange={(event:any) => {
                        setFile({ ...dataFile, [event.target.name]: event.target.files[0] });
                      }}
                />

                <div className="flex justify-center mt-5 text-white">
                    <button className="bg-blue-500 mr-3 px-2 py-1 rounded-md" type="submit"> Submit</button>
                    <button className="bg-blue-500 px-2 py-1 rounded-md" onClick={()=> {props.navigation('/data')}}> Cancel </button>
                </div>
            </div>
        </form>
        
    )
}

export {DataUpload}