import React, {useState} from 'react';
import {CreateLabelButton} from './create-label-button-view';
import {LabelTableView} from './label-table-view';
import {CreateLabelView} from './create-label-view';
import { useLabelData } from '../../hooks/labelpage/use-label-data';
import { LabelDataInterface } from '../../interfaces/label-interfaces'

interface LabelPageControllerProps {

}

export const LabelPageController: React.FC<LabelPageControllerProps> = ({}) => {
        
    const [labelCreateView, setLabelCreateView] = useState(false)
    const [labelEdit, setLabelEdit] = useState<LabelDataInterface| null>(null)
    const [labelData, isLoading, setReload, handleDeleteLabel] = useLabelData()

    
    return (
        <React.Fragment>
            {labelCreateView && !labelEdit && <div className="min-h-screen 
                absolute opacity-95 top-0 bg-white w-full
                flex justify-center items-center">
                        <CreateLabelView 
                            setLabelCreateView={setLabelCreateView}
                            setReload={setReload}
                        />
                    </div>
            }
            {labelEdit && !labelCreateView && <div className="min-h-screen 
                absolute opacity-95 top-0 bg-white w-full
                flex justify-center items-center">
                        <CreateLabelView 
                            setLabelEditView={setLabelEdit}
                            initialState={{'name': labelEdit.labelname, 'description': labelEdit.description}}
                            updateFlag={labelEdit.id}
                            setReload={setReload}
                        />
                    </div>
            }
            <div className="px-10 overflow-y-scroll max-h-[calc(100vh-100px)]">
                
                <div onClick={()=> setLabelCreateView(true)}>
                    <CreateLabelButton />
                </div>
                <LabelTableView 
                    labelData={labelData}
                    handleDeleteLabel={handleDeleteLabel}
                    setLabelEdit={setLabelEdit}
                    isLoading={isLoading}
                />
            </div>
        </React.Fragment>
        );
}