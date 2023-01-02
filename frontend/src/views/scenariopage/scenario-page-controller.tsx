import React, { useState } from "react";
import { ScenarioPage } from "./scenario-page";
import ScenarioDetailController from "./scenario-card-detail-controller";
import { useScenarioData } from '../../hooks/scenariomanagepage/use-scen-data';
import { useScenarioJSON } from '../../hooks/scenariomanagepage/use-scen-json';
import { ScenarioDataInterface } from "../../interfaces/scenario-data-interfaces";
import { ScenarioTableView } from "./scenario-table-view";
import { ScenarioEditView } from "./scenario-edit-view";

type ScenarioPageCtrlProps = {};

const ScenarioPageController: React.FC<ScenarioPageCtrlProps> = ({ }) => {

    const [isClicked, setIsClicked] = useState<ScenarioDataInterface | null>(null);
    const [isViewClicked, setIsViewClicked] = useState(false)
    const [isEditClicked, setIsEditClicked] = useState(false)
    const [scenarios, isLoading, setReload] = useScenarioData()
    const [scenJSON, handleFetchJSON] = useScenarioJSON(isClicked)


    let scenarioContainer = <ScenarioPage
        setIsClicked={setIsClicked}
        scenarios={scenarios}
        clickedData={isClicked}
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
                    />
                </div>
            </div>
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
