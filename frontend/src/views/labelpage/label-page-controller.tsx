import React, {useState} from 'react';
import {CreateLabelButton} from './create-label-button-view';
import {LabelTableView} from './label-table-view';
import {CreateLabelView} from './create-label-view';

interface LabelPageControllerProps {

}

export const LabelPageController: React.FC<LabelPageControllerProps> = ({}) => {
        
    const [labelCreateView, setLabelCreateView] = useState(false)
    
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
                <LabelTableView />
            </div>
        </React.Fragment>
        );
}