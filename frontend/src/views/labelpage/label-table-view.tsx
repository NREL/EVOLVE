import React from 'react'
import { LabelDataInterface } from '../../interfaces/label-interfaces'

interface LabelTableViewProps {
    labelData:LabelDataInterface[]
}

export const LabelTableView: React.FC<LabelTableViewProps> = ({
    labelData
}) => {
        return (
            <div className="pt-5">
                <h1 className="text-xl text-blue-500 font-bold pb-3"> My labels</h1>
            
                <table className="w-full text-left table-fixed">
                    <tr className="bg-gray-300">
                        <th className="py-2"> Id </th>
                        <th> Name </th>
                        <th> Description </th>
                        <th> Created at</th>
                        <th> </th>
                    </tr>
                    {
                        labelData.map((value: LabelDataInterface)=> {
                            return <tr>
                                <td> {value.id} </td>
                                <td> {value.labelname} </td>
                                <td> {value.description} </td>
                                <td> {value.created_at} </td>
                                <td>  </td>
                            </tr>
                        })
                    }
                </table>
            </div>
            
        );
}