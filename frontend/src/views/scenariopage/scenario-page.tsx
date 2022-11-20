import React from 'react';
import {CreateScenarioButton} from './create-scenario-button-view';
import {ScenarioCardContainer} from './scenario-card-container-view';

const ScenarioPage = () => {
    return (
        <div>
            <CreateScenarioButton />
            <ScenarioCardContainer />
        </div>
    )
}

export {ScenarioPage};