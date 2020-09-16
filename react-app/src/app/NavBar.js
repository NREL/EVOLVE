import React, {Component} from 'react';
import logo1 from '../assets/nrel.png';
import logo2 from '../assets/usaid.png';
import logo3 from '../assets/indiamop.png';

class NavBar extends Component{

    constructor(props){
        super(props)
        this.state = {}
    }

    render () {
        return (
            <nav className='navbar navbar-expand-lg navbar-dark bg-primary d-flex justify-content-between'>

                <div style={{color:'white'}}>
                    {/* <img src={logo1} width='100px' className='mr-3 img-thumbnail'/> */}
                    {/* <img src={logo2} width='100px' className='mr-3 img-thumbnail'/>
                    <img src={logo3} width='100px' className='mr-3 img-thumbnail'/> */}
                    {/* <span>EVOLVE Dashboard - 2020</span> */}
                    {/* <span style={{marginLeft:'50px'}}><button className='btn btn-info'>Storage Sizing</button></span> */}
                
                    <p>Greening the Grid Program</p>
                        <p className='mt-n3'>A Joint Initiative of USAID/India and Ministry of Power </p>
                </div>

 
                <div class="dropdown">
                        
                        <button class="btn btn-outline-light dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Switch Screen
                        </button>
                    
                        
                        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            <a class="dropdown-item" href="/dashboard">Load profile analysis</a>
                            <a class="dropdown-item" href="/profile">Profile Disaagregation</a>
                        </div>
                </div>
                
            </nav>
        )
    }

}

export default NavBar

