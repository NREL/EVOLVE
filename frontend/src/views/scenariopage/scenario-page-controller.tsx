import React, { useState, useEffect } from "react";
import { ScenarioPage } from "./scenario-page";
import ScenarioDetailController from "./scenario-card-detail-controller";
import { useScenarioData } from '../../hooks/scenariomanagepage/use-scen-data';
import { useScenarioJSON } from '../../hooks/scenariomanagepage/use-scen-json';
import { ScenarioDataInterface } from "../../interfaces/scenario-data-interfaces";
import { ScenarioTableView } from "./scenario-table-view";
import { ScenarioEditView } from "./scenario-edit-view";
import { ScenarioCloneView } from "./scenario-clone-view";
import { AddLabelView } from "./add-label-view";
import axios from 'axios';
import { useSelector } from 'react-redux';
import { StateModel } from "../../interfaces/redux-state";
import { useLabelData } from '../../hooks/labelpage/use-label-data';

type ScenarioPageCtrlProps = {};

const ScenarioPageController: React.FC<ScenarioPageCtrlProps> = ({ }) => {

    const [isClicked, setIsClicked] = useState<ScenarioDataInterface | null>(null);
    const [isViewClicked, setIsViewClicked] = useState(false)
    const [isEditClicked, setIsEditClicked] = useState(false)
    const [isCloneClicked, setIsCloneClicked] = useState(false)
    const [isAddLabelClicked, setIsAddLabelClicked] = useState(false)
    const [scenarios, isLoading, setReload] = useScenarioData()
    const [scenJSON, handleFetchJSON] = useScenarioJSON(isClicked)

    const initialFilterStates = localStorage.getItem('filterTags')
    const [filterTags, setFilterTags] = useState<string[]>(
        initialFilterStates ? JSON.parse(initialFilterStates): []
    )
    const [labelData ] = useLabelData()

    const accessToken = useSelector(
        (state: StateModel) => state.auth.accessToken
    )

    const handleFilterTags = (label: string) => {
        if (filterTags.includes(label)){
            setFilterTags((tags: string[])=> {
                const tags_fil = tags.filter((item: string)=> item !== label)
                return tags_fil
            })
        } else {
            setFilterTags((tags: string[])=> {
                return tags.concat(label)
            })
        }
    }

    useEffect(()=> {
        localStorage.setItem('filterTags', JSON.stringify(filterTags))
    }, [filterTags])

    const handleAddLabel = (scenarioId: number, labelname:string)=> {
        axios.post(
            '/scenario/label/',
            {scenarioid: scenarioId, labelname: labelname},
            { headers: { 'Authorization': 'Bearer ' + accessToken } }
        ).then((response) => {
            console.log(response.data)
            setReload((value:number)=> value + 1)
            setIsClicked(null)
        }).catch((error) => {
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
        })
    }

    let scenarioContainer = <ScenarioPage
        setIsClicked={setIsClicked}
        scenarios={scenarios}
        clickedData={isClicked}
        labelData={labelData}
        filterTags={filterTags}
        handleFilterTags={handleFilterTags}
    />


    return isClicked ? (
        <React.Fragment>
            <div className="flex justify-between relative">
                <div className="h-[calc(100vh-0rem)] overflow-y-scroll w-full">
                    {scenarioContainer}
                </div>
                <div className="h-screen overflow-y-scroll bg-white w-1/3 shadow-md p-5">
                    <ScenarioDetailController
                        data={isClicked}
                        setIsClicked={setIsClicked}
                        setReload={setReload}
                        setIsViewClicked={setIsViewClicked}
                        setIsEditClicked={setIsEditClicked}
                        setCloneClicked={setIsCloneClicked}
                        setIsAddLabelClicked={setIsAddLabelClicked}
                    />
                </div>
            </div>
            {isAddLabelClicked && <div className="absolute w-full bg-gray-900 
                top-0 opacity-95 h-[calc(100vh+100px)] flex justify-center items-center
                shadow-md">
                <AddLabelView
                    setIsAddLabelClicked={setIsAddLabelClicked}
                    activeScenario={isClicked}
                    handleAddLabel={handleAddLabel}
                    setReload={setReload}
                    labelData={labelData}
                />
            </div>
            }
            {isViewClicked && <div className="absolute w-full bg-gray-900 
                top-0 opacity-95 min-h-screen">
                <ScenarioTableView
                    scenJSON={scenJSON}
                    setIsViewClicked={setIsViewClicked}
                />
            </div>
            }
            {isEditClicked && <div className="absolute w-full bg-gray-900 
                top-0 opacity-95">
                <ScenarioEditView
                    scenJSON={scenJSON}
                    setIsEditClicked={setIsEditClicked}
                    scenarioId={isClicked.id}
                    setIsClicked={setIsClicked}
                    setReload={setReload}
                />
            </div>
            }
            {isCloneClicked && <div className="absolute w-full bg-gray-900 
                top-0 opacity-95 h-[calc(100vh+100px)] flex items-center justify-center">
                <ScenarioCloneView
                    setIsCloneClicked={setIsCloneClicked}
                    scenarioId={isClicked.id}
                    setIsClicked={setIsClicked}
                    setReload={setReload}
                    scenarioName={isClicked.name}
                />
            </div>
            }
        </React.Fragment>
    ) : (
        <div>
            {scenarioContainer}
        </div>
    );
};

export default ScenarioPageController;
