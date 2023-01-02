
import React from 'react';
import { ScenarioCardView } from './scenario-card-view';
import { ScenarioDataInterface } from '../../interfaces/scenario-data-interfaces';

type ScenarioCardProps = {
    setIsClicked: React.Dispatch<React.SetStateAction<ScenarioDataInterface | null>>,
    clickedData: ScenarioDataInterface;
    scenarioData: ScenarioDataInterface[]
}

const ScenarioCardContainer: React.FC<ScenarioCardProps> = (
    { setIsClicked, scenarioData, clickedData }
) => {
    return (
        <div className="px-10 py-5">
            <p className="text-xl text-blue-500 font-bold pb-3"> My Scenarios </p>
            {
                scenarioData.map((data: ScenarioDataInterface) => {
                    return <div onClick={() => setIsClicked(data)} key={'scenario_' + data.id}>
                        <ScenarioCardView
                            cardData={data}
                            clickedData={clickedData}
                        />
                    </div>

                })
            }
        </div>
    )
}

export { ScenarioCardContainer };