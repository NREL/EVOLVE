import React from 'react';
import { CreateScenarioButton } from './create-scenario-button-view';
import { ScenarioCardContainer } from './scenario-card-container-view';
import { ScenarioDataInterface } from '../../interfaces/scenario-data-interfaces';

type ScenarioPageProps = {
    setIsClicked: React.Dispatch<React.SetStateAction<ScenarioDataInterface | null>>;
    scenarios: ScenarioDataInterface[];
    clickedData: ScenarioDataInterface;
}

const ScenarioPage = (
    props: any
) => {
    const { setIsClicked, scenarios, clickedData } = props;
    return (
        <div className="relative">
            <CreateScenarioButton />
            <ScenarioCardContainer
                setIsClicked={setIsClicked}
                scenarioData={scenarios}
                clickedData={clickedData}
            />
        </div>
    );
}

export { ScenarioPage };