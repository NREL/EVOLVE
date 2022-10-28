import React from "react";
import { TimeSeriesDataInfoModel } from "../../interfaces/data-manage-interfaces"

export function DataCards(props: {
    data: TimeSeriesDataInfoModel[];
    isClicked: number;
    setcardData: any;
    setIsClicked: any;
}) {

    const {data, isClicked, setcardData, setIsClicked} = props
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
        'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    const handleOnClick = (d:TimeSeriesDataInfoModel) => {
        setIsClicked(d.id)
        setcardData(d)
    }

    const users = ["kapil", "erik", "suchana", "damn", "h"]

    return (
            <div className="grid grid-cols-3 gap-y-3 gap-x-3 lg:grid-cols-3 sm:grid-cols-2">
                {
                    data.map((d:TimeSeriesDataInfoModel, id:number)=> {

                        let d_mod = {...d, 
                            start_date: new Date(d.start_date),
                            end_date: new Date(d.end_date),
                            created_at: new Date(d.created_at)
                        }
                        
                        return (
                            <div className={isClicked === d_mod.id ? 'bg-gray-200': 'bg-white'}>
                                <div className="shadow-md py-3 px-5 hover:cursor-pointer 
                                hover:bg-gray-100 hover:border-blue-500 " onClick={
                                () => handleOnClick(d)  
                                }> 
                                
                                
                                    {/* <img src={d.image} class="shadow"/> */}
                                    <div key={d.name} className="flex justify-between items-center relative mb-1">
                                        <h1 className="text-xl"> {d_mod.name.length>8 ? d_mod.name.slice(0,8) + ' ...': d_mod.name  }</h1>
                                        <div className="flex">
                                            {
                                                users.slice(0,3).map((u, id)=> {
                                                    return (
                                                        id <= 1 ? <div className="bg-blue-500 w-6 h-6 rounded-full flex justify-center 
                                                            items-center text-white font-bold ring-2 ring-white">
                                                            {u[0].toUpperCase()}
                                                        </div> :
                                                        <div className="bg-blue-500 w-6 h-6 rounded-full flex justify-center 
                                                            items-center text-white font-bold ring-2 ring-white text-sm">
                                                            <p>{users.length - 2}+</p>
                                                        </div>
                                                    )
                                                })
                                            }
                                        </div>
                                    </div>
                                    <p className="text-sm text-gray-500"> {d_mod.description.length>25 ? d_mod.description.slice(0,25) + ' ...': d_mod.description  }</p>
                                    
                                    <div className="flex justify-between pt-2 text-sm text-gray-500 mt-2">
                                        <h1> {d_mod.start_date.getFullYear()} {months[d_mod.start_date.getMonth()]} - { d_mod.end_date.getFullYear()} {months[d_mod.end_date.getMonth()]}</h1>
                                        <h1> {d_mod.created_at.getFullYear()}-{d_mod.created_at.getMonth()}
                                        -{d_mod.created_at.getDay()}</h1>
                                    </div>
                                    <div className="flex justify-between text-sm pt-1 text-gray-500">
                                        <h1> Resolution (min): {d_mod.resolution_min }</h1>
                                        <p className="bg-gray-500 text-white rounded-md px-2 max-h-fit"> { d_mod.category }</p>
                                    </div>
                                </div>
                            </div>
                        )
        
                    })
                }
            </div>
    )
}
