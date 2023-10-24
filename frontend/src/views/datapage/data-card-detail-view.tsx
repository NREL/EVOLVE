import { TimeSeriesDataInfoModel } from "../../interfaces/data-manage-interfaces";
import React from 'react';

export function DataCardDetailView(props: {
    data:TimeSeriesDataInfoModel;
}) {
    const data = props.data;
    
    return (
        <div>
                <h1 className="font-bold text-blue-500 border-b-2 w-max"> 
                { data.name } 
                
                </h1>

                <p className="pt-2 text-sm text-gray-500"> {data.description} </p>

                <div className="py-3 text-sm text-gray-500">
                <p> Data resolution </p>

                <p className="bg-blue-500 px-2 rounded-md text-white w-fit">
                    { data.resolution_min } min </p>
                
                <p className="pt-2"> Data start time </p>
                
                <p className="px-2 rounded-md bg-blue-500 text-white w-fit">
                        {new Date(data.start_date).toDateString() } </p> 

                <p className="pt-2"> Data end time </p>
                
                <p className="px-2 rounded-md bg-blue-500 text-white w-fit">
                        {new Date(data.end_date).toDateString() }  </p> 

                <p className="pt-2"> Created at </p>
                
                <p className="px-2 rounded-md bg-blue-500 text-white w-fit">
                        {new Date(data.created_at).toDateString() }  </p> 

                <p className="pt-2"> Data category </p>
                
                <p className="px-2 rounded-md bg-blue-500 text-white w-fit">
                        {data.category} </p> 
            </div>

        </div>
    )
}