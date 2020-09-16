import React, {Component} from 'react'

class Table extends Component{

    constructor(props){
        super(props)
        this.state = {};
    }

    render () {
        return (
            <table class="table table-sm table-striped table-condensed">
                <tbody>
                    <tr>
                    <td>Peak load (kW)</td>
                    <td> {this.props.data.peakpower} </td>
                    </tr>
                    <tr>
                    <td>Energy Consumption (MWh)</td>
                    <td> {this.props.data.energy}</td>
                    </tr>
                    <tr>
                    <td>Maximum Ramp Rate (kw/(30-min))</td>
                    <td> {this.props.data.ramp}</td>
                    </tr>
                    <tr>
                    <td>Average to Peak Ratio</td>
                    <td> {this.props.data.avg2peak}</td>
                    </tr>
                </tbody>
            </table>
        )
    }

}

export default Table