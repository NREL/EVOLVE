import React from 'react';

export function IsCardDataLoading(){
    return (
        
        <div className="grid grid-cols-3 gap-y-2 gap-x-3 animate-pulse">
            {
                [1,1,1,1,1,1].map((d)=> {
                    return <div className="bg-gray-200 h-64 p-5">
                    <div className="flex justify-between">
                        <div className="w-60 h-6 rounded-md bg-gray-300"></div>
                        <div className="w-10 h-6 rounded-md bg-gray-300"></div>
                    </div>
                    <div className="my-3 w-full h-6 rounded-md bg-gray-300"></div>
                    <div className="w-full h-20 rounded-md bg-gray-300"></div>
    
                    <div className="my-3 flex justify-between">
                        <div className="w-32 h-6 rounded-md bg-gray-300"></div>
                        <div className="w-32 h-6 rounded-md bg-gray-300"></div>
                    </div>
                    <div className="my-3 flex justify-between">
                        <div className="w-32 h-6 rounded-md bg-gray-300"></div>
                        <div className="w-12 h-6 rounded-md bg-gray-300"></div>
                    </div>
                </div>
                })
            }

        </div>

    )
}
