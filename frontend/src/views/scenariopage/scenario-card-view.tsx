import React from 'react';
import { ScenarioDataInterface } from '../../interfaces/scenario-data-interfaces';


type scenarioCardViewProps = {
    cardData: ScenarioDataInterface;
    clickedData: ScenarioDataInterface;
}

const ScenarioCardView: React.FC<scenarioCardViewProps> = ({
    cardData, clickedData }) => {
    return (
        <div className={'w-full px-3 py-2 my-2 ' +
            'rounded-md grid grid-cols-5 shadow-md hover:cursor-pointer ' +
            `hover:bg-gray-100 ${cardData === clickedData ? 'bg-blue-100' : 'bg-white'}`}>

            <div className="flex">
                <img src="./images/scenario_card_icon.svg" width="20" />
                <p className="pl-2 text-blue-500 font-bold"> {cardData.name} </p>
            </div>

            <p> {cardData.description.length < 20 ? cardData.description : cardData.description.slice(0, 20) + '...'}</p>
            <p> {new Date(cardData.created_at).toLocaleDateString()}</p>
            <div className="flex">
                {cardData.solar && <img src="./images/solar_icon.svg" width="35" className="pr-2" />}
                {cardData.ev && <img src="./images/ev_icon.svg" width="35" className="pr-2" />}
                {cardData.storage && <img src="./images/storage_icon.svg" width="35" className="pr-2" />}
            </div>
        </div>
    )
}

export { ScenarioCardView };