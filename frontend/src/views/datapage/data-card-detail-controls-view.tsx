import { TimeSeriesDataInfoModel } from "../../interfaces/data-manage-interfaces";
import React from 'react';

export function DataCardDetailControlView(props: {
    data: TimeSeriesDataInfoModel;
    deleteLabel: boolean;
    setDeleteLabel: any;
    handleDeleteData: any;
    downloadLabel: boolean;
    setDownloadLabel: any;
    handleDataDownload: any;
}) {
    const {data, deleteLabel, setDeleteLabel, handleDeleteData, downloadLabel,
        setDownloadLabel, handleDataDownload
    } =  props;
    
    
    return (
        <div className="grid grid-cols-3 my-5 gap-y-5 place-items-center">
            <div className="relative bg-gray-100 w-12 h-12 rounded-full flex justify-center items-center hover:border-2 
            hover:border-blue-500 hover:cursor-pointer"
            onMouseOver={()=> setDeleteLabel(true)}
            onMouseLeave={()=> setDeleteLabel(false)}
            onClick={()=> handleDeleteData(data)}
            >
                <img src="./images/delete_light.svg" className="w-4 h-4" />
                {
                    deleteLabel ?
                    <p className="absolute text-sm top-14 w-20 left--2 bg-orange-300 
                    rounded-md text-slate-600 px-1 opacity-90"> Delete data</p>: null
                }


            </div>
            <div className="relative bg-gray-100 w-12 h-12 rounded-full flex justify-center items-center hover:border-2 
            hover:border-blue-500 hover:cursor-pointer"
            onMouseOver={()=> setDownloadLabel(true)}
            onMouseLeave={()=> setDownloadLabel(false)}
            onClick={()=> handleDataDownload()}
            >
                <img src="./images/download_light.svg" className="w-4 h-4" />
                {
                    downloadLabel ?
                    <p className="absolute text-sm top-14 w-20 left--2 bg-orange-300 
                    rounded-md text-slate-600 px-1 opacity-90"> Download </p>: null
                }
            </div>

            
        </div>
    )
}