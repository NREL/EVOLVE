import {useSelector} from 'react-redux';
import {Link} from 'react-router-dom';

function Nav() {

    // Get current user 
    const user = useSelector(state => state.auth.user)

    return (
        <div class="px-20 h-12 bg-blue-800 text-white flex justify-between items-center">
            <h1 class="w-1/4 text-xl font-bold"> EVOLVE </h1>
            <div class="flex w-1/4 justify-between">
                <Link to="/">Home</Link>
                <a target="_blank" href="https://nrel.github.io/EVOLVE/">Docs</a>
                <a target="_blank" href="https://github.com/NREL/EVOLVE">Repo</a>
            </div>
            <div class="w-1/4 flex justify-end hover:cursor-pointer">
                {
                    user ?
                        <div class="w-8 h-8 rounded-full bg-blue-600 border-2 flex items-center justify-center">
                            <h1 class="text-xl"> {user[0].toUpperCase()} </h1>
                        </div> :
                        <img src="./images/default_user.svg" width="35"/>
                }

                
            </div>
        </div>
    )
}

export {Nav}