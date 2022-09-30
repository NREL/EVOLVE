
function Nav() {
    return (
        <div class="px-20 h-12 bg-blue-800 text-white flex justify-between items-center">
            <h1 class="w-1/4 text-xl font-bold"> EVOLVE </h1>
            <div class="flex w-1/4 justify-between">
                <h1>Home</h1>
                <h1>Docs</h1>
                <h1>Repo</h1>
            </div>
            <div class="w-1/4 flex justify-end">
                <div class="w-8 h-8 rounded-full bg-blue-600 border-2 flex items-center justify-center">
                    <h1 class="text-xl"> K </h1>
                </div>
                
            </div>
        </div>
    )
}

export {Nav}