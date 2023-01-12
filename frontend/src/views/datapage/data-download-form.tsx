import React from 'react'

interface DataDownloadFormProps {

}

export const DataDownloadForm: React.FC<DataDownloadFormProps> = ({}) => {
        return (
            <div>
                <p className="text-blue-500 border-b-2 w-max my-3 font-bold"> Manage Data Download </p>

                <form>

                    <p className="text-gray-500 pb-2"> Start Date </p>
                    <input
                        className="border rounded-md mr-2 px-2 w-full"
                        type="date"
                        />

                    <p className="text-gray-500 py-2"> End Date </p>
                    <input
                        className="border rounded-md mr-2 px-2 w-full"
                        type="date"
                        />

                    <button className="px-2 my-3 text-sm py-1 bg-blue-500 
                        rounded-md text-white" type="submit"> 
                        Download data </button>

                </form>
            </div>
        );
}