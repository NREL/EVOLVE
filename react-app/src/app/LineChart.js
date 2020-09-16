/* App.js */
import React, {Component} from 'react'
import {Bar, Line, Pie} from 'react-chartjs-2';
import * as Zoom from 'chartjs-plugin-zoom';

 
class LineChart extends Component {	

    constructor(props){
        super(props);
        
        this.state = { }

    }

    render () {
        const original_array = this.props.data
        const data_set = original_array.map((d)=> {
                return {
                        label: d.key,
                        fill: false,
                        lineTension: 0.5,
                        backgroundColor: d.color,
                        borderColor: d.color,
                        borderWidth: 2,
                        data: d.data,
                        pointRadius: 1
                } }
            )

        const line_data = {
            labels: this.props.date.data.map((d)=> new Date(d)),
            datasets : data_set
        }
        return (
            <div>
                <Line
                    data =  {line_data}
                    width={this.props.width}
                    height={this.props.height}
                    options={{
                        title:{
                            display:false,
                            text:'Effect of DERs on load profile',
                            fontSize:20
                        },
                        legend:{
                            display:true,
                            position:'right'
                        },
                        scales: {
                            xAxes: [{
                                type: 'time',
                                time: {
                                    unit: this.props.date.format
                                }
                            }],
                            yAxes: [{
                              scaleLabel: {
                                display: true,
                                labelString: this.props.ylabel
                              }
                            }]
                        },
                        pan: {
                            enabled: false,
                            mode: 'x',
                            speed: 1000
                        },
                        zoom: {
                            enabled: true,
                            mode: 'x',
                            drag: true
                        }
                    }}
                />
            </div>
        )
    }

}

export default LineChart