

function DataUpload(props) {

    return (
        <div class="w-1/2 mt-16 mb-5 mx-auto bg-white p-10">
            <h1 class="text-center text-blue-500 font-bold text-xl pb-5"> Upload data</h1>

            <div class="grid grid-cols-2 gap-y-3 gap-x-3">

                <div >
                    <label> Time stamp column name </label> <br/>
                    <input class="w-full mt-2 bg-gray-300 px-2 py-1 outline-none text-blue-500 rounded-md"/>
                </div>

                <div>
                    <label> Data resolution (min.) </label> <br/>
                    <input class="w-full mt-2 bg-gray-300 px-2 py-1 outline-none text-blue-500 rounded-md"/>
                </div>

                <div>
                    <label> Data category </label> <br/>
                    <input class="w-full mt-2 bg-gray-300 px-2 py-1 outline-none text-blue-500 rounded-md"/>
                </div>

                <div>
                    <label> Description </label> <br/>
                    <input type="textarea" class="w-full mt-2 bg-gray-300 px-2 py-1 outline-none text-blue-500 rounded-md"/>
                </div>

            </div>

            <input class="mt-4" type="file"/>

            <div class="flex justify-center mt-5 text-white">
                <button class="bg-blue-500 mr-3 px-2 py-1 rounded-md"> Submit</button>
                <button class="bg-blue-500 px-2 py-1 rounded-md" onClick={()=> {props.navigation('/data')}}> Cancel </button>
            </div>
        </div>
        
    )
}

export {DataUpload}