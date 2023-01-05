import React, {useState} from 'react';
import {CreateLabelButton} from './create-label-button-view';
import {LabelTableView} from './label-table-view';
import {CreateLabelView} from './create-label-view';
import { useLabelData } from '../../hooks/labelpage/use-label-data';

interface LabelPageControllerProps {

}

export const LabelPageController: React.FC<LabelPageControllerProps> = ({}) => {
        
    const [labelCreateView, setLabelCreateView] = useState(false)
    const [labelData, isLoading, setReload] = useLabelData()
    
    return (
        <React.Fragment>
            {labelCreateView && <div className="min-h-screen 
                absolute opacity-95 top-0 bg-white w-full
                flex justify-center items-center">
                        <CreateLabelView 
                            setLabelCreateView={setLabelCreateView}
                        />
                    </div>
                    }
            <div className="mx-10">
                
                <div onClick={()=> setLabelCreateView(true)}>
                    <CreateLabelButton />
                </div>
                <LabelTableView 
                    labelData={labelData}
                />
            </div>
        </React.Fragment>
        );
}