import React from 'react'
import { LabelDataInterface } from '../../interfaces/label-interfaces'
import { CreateLabelView } from './create-label-view';

interface LabelTableViewProps {
    labelData:LabelDataInterface[];
    handleDeleteLabel: (id: number) => void;
    setLabelEdit: React.Dispatch<React.SetStateAction<LabelDataInterface | null>>;
    isLoading: boolean;
}


const EmptyLabelsView: React.FC<{}>  = ({}) => {
    return (
        <React.Fragment>
            <div className="flex justify-center items-center h-[calc(100vh-300px)]">
                <div className='w-60 h-60 bg-gray-200 rounded-full flex justify-center items-center'>
                    <img src="./images/label_icon_light.svg" width="150"/>
                </div>
            </div>
            <p className="text-center text-gray-500"> Oops looks like you have not yet created labels. <br/> Consider creating label first.</p>
        </React.Fragment>
    )
}

const LoadingLabelsView: React.FC<{}> = ({}) => {
    return (
        <div className="animate-pulse">
            <table className="w-full text-left table-fixed px-5">
                <tr className="bg-gray-300"> 
                    <th className="py-5 pl-3"> </th>  <th> </th>  <th> </th>  <th> </th>  <th> </th>
                </tr>
                <tr className="bg-gray-200 border-b border-white"> 
                    <td className="py-5 pl-3"> </td>  <td> </td>  <td> </td>  <td> </td>  <td> </td>
                </tr>
                <tr className="bg-gray-200 border-b border-white"> 
                    <td className="py-5 pl-3"> </td>  <td> </td>  <td> </td>  <td> </td>  <td> </td>
                </tr>
                <tr className="bg-gray-200 border-b border-white"> 
                    <td className="py-5 pl-3"> </td>  <td> </td>  <td> </td>  <td> </td>  <td> </td>
                </tr>
                <tr className="bg-gray-200 border-b border-white"> 
                    <td className="py-5 pl-3"> </td>  <td> </td>  <td> </td>  <td> </td>  <td> </td>
                </tr>
                <tr className="bg-gray-200 border-b border-white"> 
                    <td className="py-5 pl-3"> </td>  <td> </td>  <td> </td>  <td> </td>  <td> </td>
                </tr>
                <tr className="bg-gray-200 border-b border-white"> 
                    <td className="py-5 pl-3"> </td>  <td> </td>  <td> </td>  <td> </td>  <td> </td>
                </tr>
                <tr className="bg-gray-200 border-b border-white"> 
                    <td className="py-5 pl-3"> </td>  <td> </td>  <td> </td>  <td> </td>  <td> </td>
                </tr>
            </table>
        </div>
    )
}

export const LabelTableView: React.FC<LabelTableViewProps> = ({
    labelData, handleDeleteLabel, setLabelEdit, isLoading
}) => {
        return (
            <div className="pt-5">
                <h1 className="text-xl text-blue-500 font-bold pb-3"> My labels</h1>
                {
                    isLoading ? <LoadingLabelsView/> : 
                    labelData.length ===0 ? 
                    <EmptyLabelsView />: 
                    <table className="w-full text-left table-fixed px-5">
                        <tr className="bg-gray-300">
                            {/* <th className="py-2 pl-3"> Id </th> */}
                            <th className="py-2 pl-3"> Name </th>
                            <th> Description </th>
                            <th> Created at</th>
                            <th> </th>
                        </tr>
                        {
                            labelData.map((value: LabelDataInterface)=> {
                                return <tr className="bg-gray-200 border-b border-white">
                                    {/* <td className="pl-3 py-2"> {value.id} </td> */}
                                    <td className="py-2 pl-3"> <p className="bg-teal-600 w-max text-white px-2 rounded-md"> {value.labelname} </p> </td>
                                    <td> {value.description} </td>
                                    <td> {new Date(value.created_at).toLocaleDateString()} </td>
                                    <td> 
                                        <div className="flex">
                                            <div className="bg-gray-100 w-8 h-8 rounded-full flex justify-center
                                                hover:cursor-pointer hover:bg-red-300"
                                                onClick={()=> handleDeleteLabel(value.id)}
                                            >
                                                <img src="./images/delete_light.svg" width="16"/>
                                            </div>
                                            <div className="bg-gray-100 w-8 h-8 rounded-full flex justify-center ml-3
                                            hover:cursor-pointer hover:bg-blue-300"
                                            onClick={()=> setLabelEdit(value)} 
                                            >
                                                <img src="./images/edit_light.svg" width="16"/>
                                            </div>
                                        </div>    
                                    </td>
                                </tr>
                            })
                        }
                    </table>
                }
            </div>
            
        );
}