import React from 'react'

interface LabelTableViewProps {

}

export const LabelTableView: React.FC<LabelTableViewProps> = ({}) => {
        return (
            <div className="pt-5">
                <h1 className="text-xl text-blue-500 font-bold pb-3"> My labels</h1>
            </div>
        );
}