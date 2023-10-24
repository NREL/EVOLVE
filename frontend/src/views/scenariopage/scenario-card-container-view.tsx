
import React, {useState} from 'react';
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

    const [pageIndex, setPageIndex] = useState(1)
    const [cardsPerPage, setCardsPerPage] = useState(10)

    return (
        <div className="px-10 py-5">
            <div className="flex justify-between">
                <p className="text-xl text-blue-500 font-bold pb-3"> My Scenarios </p>
                <div className="flex justify-center items-center">
                    <p className="pr-2"> Cards per page </p>
                    <input 
                        type="number"
                        value={cardsPerPage}
                        onChange={
                            ((e:any)=> {
                                setCardsPerPage(e.target.value)
                            })
                        }
                        className="mr-2 border-none border outline-none px-2 w-16"
                    />
                    <p className="w-8 h-8 bg-gray-300 rounded-md mr-2 flex 
                        justify-center text-xl text-white font-bold hover:cursor-pointer hover:bg-blue-600"
                        onClick={()=> {
                            if(pageIndex > 1) {
                                setPageIndex((value:number)=> value - 1)
                            } 
                        }}
                    > {'<'}</p>
                    <p className="text-gray-400 text-sm"> {pageIndex} of {Math.ceil(scenarioData.length/cardsPerPage)}</p>
                    <p className="w-8 h-8 bg-gray-300 rounded-md ml-2 flex 
                        justify-center text-xl text-white font-bold hover:cursor-pointer hover:bg-blue-600"
                        onClick={()=> {
                            if(pageIndex < Math.ceil(scenarioData.length/cardsPerPage)) {
                                setPageIndex((value:number)=> value + 1)
                            } 
                        }}
                    > {'>'}</p>
                </div>
            </div>
            
            {
                scenarioData.slice(
                    (pageIndex-1)*cardsPerPage, 
                    Math.min(pageIndex*cardsPerPage, scenarioData.length))
                .map((data: ScenarioDataInterface) => {
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