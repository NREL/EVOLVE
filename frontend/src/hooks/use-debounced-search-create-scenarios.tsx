import React, {useEffect } from 'react';
import { debounce } from "lodash";
import { TimeSeriesDataInfoModel } from '../interfaces/data-manage-interfaces';

const useDebouncedSearch = (
    allTSdata: TimeSeriesDataInfoModel[],
    formVariable: any,
    filterText: string,
    setSearchProfiles: any
) => {


    const debouncedSearch = debounce((searchText: string) => {
        if (searchText){
            let profiles = allTSdata.filter((d:any)=> {
                return d.category === filterText && d.name.includes(searchText)
            })
            setSearchProfiles(profiles.slice(0,4))
        } else {
            setSearchProfiles([])
        }
        
    }, 100)
    
    useEffect(()=> {
            debouncedSearch(formVariable)
        }, [formVariable])
}

export {useDebouncedSearch}