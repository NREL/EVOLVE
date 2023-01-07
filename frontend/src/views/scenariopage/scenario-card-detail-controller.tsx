import React, { useState } from 'react';
import { ScenarioDataInterface } from '../../interfaces/scenario-data-interfaces';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { StateModel } from "../../interfaces/redux-state";


interface ControlDataInterface {
    id: string;
    image: string;
    label: string;
    handlerFunc: () => void;
}

type ControllerProps = {
    data: ScenarioDataInterface | null;
    setIsClicked: React.Dispatch<React.SetStateAction<ScenarioDataInterface | null>>;
    setReload: React.Dispatch<React.SetStateAction<number>>;
    setIsViewClicked: React.Dispatch<React.SetStateAction<boolean>>;
    setIsEditClicked: React.Dispatch<React.SetStateAction<boolean>>;
    setCloneClicked: React.Dispatch<React.SetStateAction<boolean>>;
    setIsAddLabelClicked: React.Dispatch<React.SetStateAction<boolean>>;
}

type BasicDetailProps = {
    data: ScenarioDataInterface;
    handleScenariolabelDelete: (labelid: string) => void;
}

type ScenarioControlsProps = {
    controls: ControlDataInterface[]
}

type SingleControlProps = {
    labelInfo: string,
    imagePath: string
}

const ScenarioBasicDetailView: React.FC<BasicDetailProps> = ({ 
    data, handleScenariolabelDelete
 }) => {
    return (
        <div>

            <h1 className="font-bold text-blue-500 border-b-2 w-max">
                {data.name}
            </h1>
            <p className="pt-2 text-sm text-gray-500"> {data.description} </p>

            <h1 className="font-bold text-blue-500 border-b-2 w-max my-3">
                Labels
            </h1>

            <div className="flex flex-wrap">
                {
                    data.labels.map((label: {labelname: string})=> {
                        return <div className="w-max mr-2 mb-2 bg-orange-500 text-white 
                            rounded-md px-2 py-1 text-sm font-bold flex justify-center items-center">
                            <p className="pr-2"> 
                            { label.labelname }  </p>
                            {/* <img src="./images/delete_light.svg" width="15"/> */}
                            <p className='w-4 h-4 border-2 border-gray-200 rounded-full 
                            flex justify-center items-center pb-1 hover:cursor-pointer 
                            hover:border-gray-800 hover:text-gray-800'
                            onClick={()=> handleScenariolabelDelete(label.labelname)}
                            > - </p>
                        </div>
                    })
                }
            </div>

            <p className="pt-2 mt-2"> Created at </p>

            <p className="px-2 rounded-md bg-blue-500 text-white w-fit">
                {new Date(data.created_at).toDateString()}  </p>

        </div>
    )
}

const SingleControlView: React.FC<SingleControlProps> = ({
    labelInfo, imagePath
}) => {

    const [label, setLabel] = useState<boolean>(false)
    return (
        <div className="relative bg-gray-100 w-12 h-12 rounded-full flex justify-center items-center hover:border-2 
                    hover:border-blue-500 hover:cursor-pointer"
            onMouseOver={() => setLabel(true)}
            onMouseLeave={() => setLabel(false)}
        >
            <img src={imagePath} className="w-6 h-6" />
            {
                label ?
                    <p className="absolute text-sm top-10 w-20 left--2 bg-orange-300 
                            rounded-md text-slate-600 px-1 opacity-90"> {labelInfo} </p> : null
            }


        </div>
    )
}

const ScenarioControlsView: React.FC<ScenarioControlsProps> = ({ controls }) => {


    return (
        <div>
            <p className="text-blue-500 border-b-2 w-max my-3 font-bold"> Scenario controls </p>
            <p className="text-sm text-gray-500 pb-2 "> Hover to see what each of these controls are for. </p>


            <div className="grid grid-cols-3 my-5 gap-y-5 place-items-center">

                {
                    controls.map((control: ControlDataInterface) => {
                        return (
                            <div onClick={() => control.handlerFunc()} key={control.id}>
                                <SingleControlView
                                    imagePath={control.image}
                                    labelInfo={control.label}
                                />
                            </div>
                        )
                    })
                }


            </div>
        </div>
    )
}

const ScenarioDetailController: React.FC<ControllerProps> = ({
    data, setIsClicked, setReload, setIsViewClicked,
    setIsEditClicked, setCloneClicked, setIsAddLabelClicked

}) => {

    const accessToken = useSelector(
        (state: StateModel) => state.auth.accessToken
    )

    const handleControl = () => {

    }

    // Handle deleteing the scenario
    const handleScenarioDelete = () => {

        data && axios.delete(`/scenario/${data.id}`,
            { headers: { 'Authorization': 'Bearer ' + accessToken } }).then((response) => {
                console.log(response.data)
                setReload((value: number) => value + 1)
                setIsClicked(null)
            }).catch((error) => {
                if (error.response.status === 401) {
                    localStorage.removeItem('state')
                }
            })

    }

    // Handle deleteing the scenario label
    const handleScenariolabelDelete = (labelid: string) => {

        data && axios.delete(`/scenario/${data.id}/label/${labelid}`,
            { headers: { 'Authorization': 'Bearer ' + accessToken } }).then((response) => {
                console.log(response.data)
                setReload((value: number) => value + 1)
                setIsClicked(null)
            }).catch((error) => {
                if (error.response.status === 401) {
                    localStorage.removeItem('state')
                }
            })

    }

    const handleScenarioView = () => {
        setIsViewClicked(true)
    }

    const handleScenarioEdit = () => {
        setIsEditClicked(true)
    }

    const handleScenarioClone = () => {
        setCloneClicked(true)
    }

    const handleAddLabel = () => {
        setIsAddLabelClicked(true)
    }

    let controls = [
        { id: 'delete_ctrl', image: './images/delete_light.svg', label: 'Delete scen', handlerFunc: handleScenarioDelete },
        { id: 'view_ctrl', image: './images/view_light.svg', label: 'View Scen.', handlerFunc: handleScenarioView },
        { id: 'edit_ctrl', image: './images/edit_light.svg', label: 'Edit Scen.', handlerFunc: handleScenarioEdit },
        { id: 'clone_ctrl', image: './images/clone_light.svg', label: 'Clone Scen.', handlerFunc: handleScenarioClone },
        { id: 'run_ctrl', image: './images/run_icon.svg', label: 'Run Scen.', handlerFunc: handleControl },
        { id: 'add_label', image: './images/add_light.svg', label: 'Add Tag', handlerFunc: handleAddLabel}
    ]

    return data && (
        <div className="relative">
            <div className="absolute w-8 h-8 top-0 flex items-center justify-center 
                rounded-full right-0 hover:cursor-pointer hover:bg-gray-300"
                onClick={() => setIsClicked(null)}
            >X
            </div>

            <ScenarioBasicDetailView 
                data={data}
                handleScenariolabelDelete={handleScenariolabelDelete}
            />
            <ScenarioControlsView controls={controls} />
        </div>
    )
}

export default ScenarioDetailController;