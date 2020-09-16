import React, {Component} from 'react'
// get our fontawesome imports
import { faArrowAltCircleDown, faArrowAltCircleUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import 'react-tippy/dist/tippy.css';
import {Tooltip,} from 'react-tippy';

class TextBlock extends Component {

    constructor(props){
        super(props)
        this.state = {}
    }

    render(){

        const my_icon = this.props.isnegative ? faArrowAltCircleDown: faArrowAltCircleUp; 
        return (
            <div className='col-3'>
                <div className="shadow pb-2 pt-2 mr-1 ml-1 mb-5 bg-white rounded row">
                    <div className="col-3 mt-3">
                        <FontAwesomeIcon icon={my_icon} color="red" size='2x'/>
                    </div>
                    <div className="col-9">
                        <Tooltip title="Shows percentage reduction. Negative value means increase." 
                                    size='small' position="right" arrow={true} >
                        <p className="mb-0 text-left">{this.props.heading}</p>
                        </Tooltip>
                        <h2 className="mt-0 text-left mb-0"> {this.props.value} </h2>
                    </div>
                </div>
            </div>
        )
    }
}

export default TextBlock