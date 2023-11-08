import React from 'react';
import { ScenarioDataInterface } from '../../interfaces/scenario-data-interfaces';


type scenarioCardViewProps = {
    cardData: ScenarioDataInterface;
    clickedData: ScenarioDataInterface;
}

const shortenText = (text:string, length: number) => {
    return text.length < length ? text : text.slice(0, length) + ' ...'
}

const ScenarioCardView: React.FC<scenarioCardViewProps> = ({
    cardData, clickedData }) => {
    return (
        <div className={'w-full px-3 py-2 my-2 ' +
            'rounded-md grid grid-cols-5 shadow-md hover:cursor-pointer' +
            `hover:bg-gray-100 ${cardData === clickedData ? 'bg-blue-100' : 'bg-white'}`}>

            <div className="flex items-center">
                <img src="./images/scenario_card_icon.svg" width="20" />
                <p className="pl-2 text-blue-500 font-bold"> {shortenText(cardData.name, 20)} </p>
            </div>

            <p className="flex items-center"> {shortenText(cardData.description, 20)}</p>
            <p className="flex items-center"> {new Date(cardData.created_at).toLocaleDateString()}</p>
            <div className="flex">
                {cardData.solar && <img src="./images/solar_icon.svg" width="35" className="pr-2" />}
                {cardData.ev && <img src="./images/ev_icon.svg" width="35" className="pr-2" />}
                {cardData.storage && <img src="./images/storage_icon.svg" width="35" className="pr-2" />}
            </div>
            <div className="flex flex-wrap">
                {
                    cardData.labels.slice(0,2).map((label: {labelname: string})=> {
                        return <p className="bg-orange-500 mb-1 text-white rounded-md px-2 text-sm font-bold mr-2"> 
                        {label.labelname.length > 8 ? label.labelname.slice(0,8) + '.': label.labelname } </p>
                    })
                }
            </div>
        </div>
    )
}

export { ScenarioCardView };