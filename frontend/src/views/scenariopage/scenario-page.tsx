import React, {useState} from 'react';
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
    const [searchWord, setSearchWord] = useState('');

    return (
        <div className="relative">
            <div className="mx-10 mt-5 flex bg-[#f9f9f9] w-1/3 rounded-md">
                    <img src="./images/search.svg" className="pl-3 py-1" width="22"/>
                    <input 
                        placeholder="Search by name" 
                        className="px-3 py-1 bg-[#f9f9f9] outline-0 border-0"
                        name="search"
                        onChange={(e: any)=> setSearchWord(e.target.value)}
                        />
            </div>
            <CreateScenarioButton />
            <ScenarioCardContainer
                setIsClicked={setIsClicked}
                scenarioData={scenarios.filter(
                    (el:ScenarioDataInterface)=> el.name.search(searchWord) !== -1
                )}
                clickedData={clickedData}
            />
        </div>
    );
}

export { ScenarioPage };