import React, {useState} from 'react';
import { LabelDataInterface } from '../../interfaces/label-interfaces';
import { ScenarioDataInterface } from '../../interfaces/scenario-data-interfaces';

interface AddLabelViewProps {
    setIsAddLabelClicked:React.Dispatch<React.SetStateAction<boolean>>;
    activeScenario: ScenarioDataInterface;
    handleAddLabel: (scenarioId: number, labelname: string) => void;
    setReload: React.Dispatch<React.SetStateAction<number>>;
    labelData: LabelDataInterface[];
}

export const AddLabelView: React.FC<AddLabelViewProps> = ({
    setIsAddLabelClicked, activeScenario, handleAddLabel, setReload, labelData
}) => {
        
        const [activeLabel, setActiveLabel] = useState('')

        const handleFormSubmit = (e:any)=> {
            e.preventDefault()
            if (activeLabel) {
                handleAddLabel(activeScenario.id, activeLabel)
                setIsAddLabelClicked(false)
                setReload((value:number)=> value +1)
            }
        }
        return (
            <div className="w-1/3 p-5 bg-white relative">
                <div className="absolute right-3 top-2 bg-gray-300 rounded-full 
                    w-8 h-8 flex justify-center items-center hover:cursor-pointer hover:bg-gray-400"
                onClick={() => setIsAddLabelClicked(false)}> X </div>
                <form onSubmit={handleFormSubmit}>
                    <p className="border-b-2 mb-2 w-max"> Select a label for 
                        <span className="text-blue-500 font-bold"> {activeScenario.name}</span></p>
                    <div className="">
                        <select name="label" id="label" value={activeLabel} 
                            className="w-full px-2 border 
                            rounded-md text-blue-500 my-3 h-10"
                            onChange={(e:any)=> setActiveLabel(e.target.value)}
                        >
                            {
                                labelData.map((value: LabelDataInterface)=> {
                                    return <option value={value.labelname}> {value.labelname}</option>
                                })
                            }
                        </select>
                    </div>
                    <button type="submit"
                        className="bg-blue-500 mt-2 text-white 
                        rounded-md px-2 py-1"> Submit </button>
                </form>
            </div>
        );
}