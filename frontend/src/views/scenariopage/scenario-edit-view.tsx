import React, { useEffect, useState } from 'react';
import {
    scenarioJSONInterface
} from '../../interfaces/create-scenario-interfaces';
import { CreateScenario } from '../createscenariopage/create-scenario-controller';
import { TimeSeriesDataInfoModel } from '../../interfaces/data-manage-interfaces';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { StateModel } from '../../interfaces/redux-state';
import { profileInterface } from '../../interfaces/create-scenario-interfaces';
import { newSolarDataInterface } from '../../interfaces/create-scenario-interfaces';
import { AxiosResponse } from 'axios';
import { newESDataInterface } from '../../interfaces/create-scenario-interfaces';

interface ScenarioEditViewProps {
    scenJSON: scenarioJSONInterface;
    setIsEditClicked: React.Dispatch<React.SetStateAction<boolean>>;
}

export const ScenarioEditView: React.FC<ScenarioEditViewProps> = ({
    scenJSON, setIsEditClicked
}) => {

    const [loadProfile, setLoadProfile] = useState<TimeSeriesDataInfoModel | null>(null)

    let initialIrrProfile = scenJSON.solar ?
        scenJSON.solar.map((item: newSolarDataInterface) => {
            return {
                name: item.name,
                data: null
            }
        }) :
        [{
            name: 'Solar 1',
            data: null
        }]
    const [irrProfiles, setIrrProfiles] = useState<profileInterface[]>(initialIrrProfile)
    const [priceProfiles, setPriceProfiles] = useState<profileInterface[]>([{
        name: 'Energy Storage 1',
        data: null
    }])
    const accessToken = useSelector((state: StateModel) => state.auth.accessToken)

    useEffect(() => {
        axios.get(
            `/data/${scenJSON.basic.loadProfile}`,
            { headers: { 'Authorization': 'Bearer ' + accessToken } }
        ).then((response) => {
            setLoadProfile(response.data)
        }).catch((error) => {
            console.log(error)
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
        })

        scenJSON.solar && Promise.all(
            scenJSON.solar.map((item: newSolarDataInterface) => {
                return axios.get(`/data/${item.irradianceData}`,
                    { headers: { 'Authorization': 'Bearer ' + accessToken } }
                )
            })
        ).then((responses) => {
            setIrrProfiles(responses.map((response: AxiosResponse<any, any>, index: number) => {
                return {
                    'name': scenJSON.solar ? scenJSON.solar[index].name : '',
                    'data': response.data
                }
            }))
        }).catch((errors) => {
            console.log('Error fetching irr profiles ', errors)
        })


        if (scenJSON.energy_storage) {
            let profiles: profileInterface[] = []
            scenJSON.energy_storage.map((item: newESDataInterface) => {
                if (item.esStrategy === 'price') {
                    axios.get(
                        `/data/${item.priceProfile}`,
                        { headers: { 'Authorization': 'Bearer ' + accessToken } }
                    ).then((response) => {
                        profiles.push({
                            name: item.name,
                            data: response.data
                        })
                    }).catch((error) => {
                        console.log(error)
                        if (error.response.status === 401) {
                            localStorage.removeItem('state')
                        }
                    })
                } else {
                    profiles.push({
                        name: item.name,
                        data: null
                    })
                }
            })
            setPriceProfiles(profiles)
        }


    }, [])

    return (
        <div className="m-10 bg-gray-100 h-[calc(100vh-50px)] 
            overflow-y-scroll shadow-md relative">
            <div className="absolute right-3 top-2 bg-gray-300 rounded-full 
                    w-8 h-8 flex justify-center items-center hover:cursor-pointer hover:bg-gray-400"
                onClick={() => setIsEditClicked(false)}> X </div>
            <CreateScenario
                initialFormData={scenJSON}
                updateFlag={true}
                initialLoadProfile={loadProfile}
                irrProfiles={irrProfiles}
                priceProfiles={priceProfiles}
            />
        </div>
    );
}