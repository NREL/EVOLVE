
import React from 'react';
import { DateSortString } from '../../interfaces/data-manage-interfaces';

export function DataFilterCard(props:any){

    
    let { kWFilterValue, irrFilterValue, sortDateValue, setkWFilterValue, 
        setirrFilterValue, setSortDateValue} = props


    return (
        <div>
            <div className="mb-2"> <h1 className="border-b max-w-max"> Filter by data category </h1> </div>
            <label>
                <input
                    type="checkbox" 
                    checked={kWFilterValue}
                    onChange={
                        ()=> {
                            setkWFilterValue(!kWFilterValue)
                        }
                    }
                />
                <span className="pl-1"> kW </span>
            </label>
            <label>
                <input
                    type="checkbox" 
                    checked={irrFilterValue}
                    onChange={
                        ()=> {
                            setirrFilterValue(!irrFilterValue)
                        }
                    }
                />
                <span className="pl-1"> irradiance </span>
            </label>

            <h1 className="my-2 border-b max-w-max"> Sort by date </h1>
            
            <label>
                <input
                    type="radio" 
                    checked={sortDateValue === DateSortString.ascending}
                    onChange={() => setSortDateValue(DateSortString.ascending)}
                />
                <span className="pl-1"> ascending </span>
            </label>
            <label>
                <input
                    type="radio" 
                    checked={sortDateValue === DateSortString.descending}
                    onChange={() => setSortDateValue(DateSortString.descending)}
                />
                <span className="pl-1"> descending </span>
            </label>
        </div>
    )
}
