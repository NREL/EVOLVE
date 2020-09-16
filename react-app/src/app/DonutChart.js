import React, {Component} from 'react';
import {Doughnut} from 'react-chartjs-2'; 

class DonutChart extends Component {

    constructor(props){
        super(props)
        this.state = {
        }
    }

    render() {
        
        const chartData = {
            labels: ['Domestic', 'Non Domestic', 'Industrial'],
            datasets:[
                {
                    data: this.props.data,
                    backgroundColor : ['rgba(255,0,0,1)','rgba(0,255,0,1)','rgba(0,0,255,1)']
                }
            ]
        }
        return (
            <div>
                <Doughnut
                    data =  {chartData}
                    width={100}
                    height={50}
                    options={{
                        title: {
                            display: true,
                            text: 'Number of Customers'
                        },
                        legend:{
                            display:true,
                            position:'right'
                        },
                    }}
                />
            </div>
        )
    }

}

export default DonutChart