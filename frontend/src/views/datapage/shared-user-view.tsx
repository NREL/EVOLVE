import React from 'react';

export function SharedUser () {
    return (
        <div>
            <div className="flex bg-[#e9e9e9] w-full rounded-md mt-5">
                    <img src="./images/search.svg" className="pl-3 py-1" width="22"/>
                    <input 
                        placeholder="Search shared user" 
                        className="px-3 py-1 bg-[#e9e9e9] outline-0 border-0 w-full"
                        name="search"
                        />
                </div>
                <div className="px-3 py-2 mt-2 bg-gray-100 h-40 overflow-y-scroll">
                {
                    ["kapil", "suchana", 'erik'].map((u)=> {
                        return <div className="flex justify-between">
                            <div className="flex pt-1"> 
                                <div className="w-6 h-6 bg-blue-500 rounded-full text-white 
                                    flex justify-center items-center font-bold border-white border-2
                                    ">
                                    <p> {u[0].toUpperCase()} </p>
                                </div>
                                <p className="pl-2"> {u} </p>
                            </div>
                            <p> X </p>
                        </div>
                    })
                }
                </div>
        </div>
    )
}
