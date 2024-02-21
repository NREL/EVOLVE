import React, {useState, useEffect} from 'react';
import { CreateScenarioButton } from './create-scenario-button-view';
import { ScenarioCardContainer } from './scenario-card-container-view';
import { ScenarioDataInterface } from '../../interfaces/scenario-data-interfaces';
import { LabelDataInterface } from '../../interfaces/label-interfaces';

type ScenarioPageProps = {
    setIsClicked: React.Dispatch<React.SetStateAction<ScenarioDataInterface | null>>;
    scenarios: ScenarioDataInterface[];
    clickedData: ScenarioDataInterface;
}

const ScenarioPage = (
    props: any
) => {
    const { setIsClicked, scenarios, clickedData, labelData,
        filterTags, handleFilterTags } = props;
    
    const [searchWord, setSearchWord] = useState('');

    return (
        <div className="relative">
            <div className="flex mx-10 mt-5 flex-wrap space-y-2.5">
                <div className="flex bg-[#f9f9f9] w-1/3 rounded-md mr-10">
                        <img src="./images/search.svg" className="pl-3 py-1" width="22"/>
                        <input 
                            placeholder="Search by name" 
                            className="px-3 py-1 bg-[#f9f9f9] outline-0 border-0"
                            name="search"
                            onChange={(e: any)=> setSearchWord(e.target.value)}
                            />
                </div>
                {
                    labelData.slice(0,20).map((item:LabelDataInterface) => {
                        return <p className={"py-1 px-3 mr-5 " + 
                        "text-sm rounded-md hover:cursor-pointer hover:bg-blue-200 " + 
                        `${filterTags.includes(item.labelname)? 'bg-blue-500 text-white': 'bg-gray-200'}`
                        }
                        onClick={()=> handleFilterTags(item.labelname)}
                        > 
                        { item.labelname }</p>
                    })
                }
            </div>
            <CreateScenarioButton />
            <ScenarioCardContainer
                setIsClicked={setIsClicked}
                scenarioData={scenarios.filter(
                    (el:ScenarioDataInterface)=> {
                    const  commonLabels = el.labels.filter(function(n) {
                            return filterTags.indexOf(n.labelname) !== -1;
                        })
                    return  filterTags.length > 0? 
                    el.name.search(searchWord) !== -1 && commonLabels.length >0
                    : el.name.search(searchWord) !== -1
                    }
                )}
                clickedData={clickedData}
            />
        </div>
    );
}

export { ScenarioPage };