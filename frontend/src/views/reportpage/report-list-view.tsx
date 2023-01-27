import React from 'react';
import {ReportDataInterface} from '../../interfaces/report-interfaces';
import { useNavigate } from "react-router-dom";

interface ReportListViewProps {
    reports: ReportDataInterface[],
    handleReportDelete: (reportid: number) => void
}

export const ReportListView: React.FC<ReportListViewProps> = ({
    reports, handleReportDelete
}) => {
        const navigation = useNavigate();
        return (
            <div>
                <p className="text-blue-500 border-b-2 w-max my-3 font-bold"> 
                Reports </p>

                {
                    reports.map((item: ReportDataInterface)=> {
                        return <div className="bg-gray-100 px-2 py-3 rounded-md shadow-md relative mb-3
                                    hover:cursor-pointer hover:bg-gray-200"
                                >
                            <div className="flex flex-row-reverse absolute right-0 top-2">
                                <div className="flex justify-center mx-2 items-center bg-gray-300 
                                    w-6 h-6 rounded-full hover:cursor-pointer hover:bg-red-500"
                                    onClick={()=> navigation(`/report/${item.id}`, { replace: true })}
                                >
                                    <img src="./images/view_light.svg" width="13"/>
                                </div>
                                <div className="flex justify-center mx-2 items-center bg-gray-300 
                                    w-6 h-6 rounded-full hover:cursor-pointer hover:bg-red-500"
                                    onClick={()=> handleReportDelete(item.id)}
                                >
                                    <img src="./images/delete_light.svg" width="13"/>
                                </div>
                                <div className="flex justify-center items-center bg-gray-300 
                                    w-6 h-6 rounded-full hover:cursor-pointer hover:bg-red-500">
                                    <img src="./images/edit_light.svg" width="13"/>
                                </div>
                            </div>
                            <p className="border-b text-indigo-500 font-bold"> {item.name} </p>
                            <p className="text-sm text-gray-500"> {item.description} </p>
                            <div className="flex justify-between mt-2">
                                <p className="text-sm px-1 bg-blue-300 rounded-md"> {new Date(item.created_at).toDateString()}</p>
                                <p className="text-sm px-1 bg-orange-300 rounded-md"> {item.status}</p>
                            </div>
                        </div>
                    })
                }
            </div>
        );
}