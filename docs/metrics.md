# Explanation for Metrics

### Peak load

Peak load is defined as maximum load for specified time duration. Mathematically it is represented as below. 

$$
\operatorname{max}\{p_1, p_2, ...., p_t, ...., p_T\}
$$

### Energy consumption

Energy consumption is sum of power consumption at all time steps multiplied by time resolution. Note energy consumption shown in evolve dashboard is actually net energy consumption so negative value means energy is injected back to the grid. Default unit for energy consumption is MWh. Mathematically energy consumption is rereseneted as below. Here 
$p_t$ is power consumtion at time $t$ and $\delta T$ is time resolution in hour.

$$
\sum_{t=0}^{T} p_t \times \delta T
$$

### Maximum Ramp Rate

Maximum ramp rate in evolve dashboard represents absolute maximum change in power per hour. It's unit is MW/hr. Mathematically it is represented as below.

$$
\operatorname{max} \{\frac{|p_{t}- p_{t-1}|}{\delta T}  \forall t \}
$$


### Average to Peak Ratio

It is mathematically represented as below.

$$
\frac{\frac{1}{T}\sum_{t=0}^{T} p_t}{max\{p_1, p_2, ..., p_t, ..., p_T\}}
$$

### Peak Reduction

Peak reduction is percentage reduction in peak power in evolved (or new) load profile compared to base or reference profile.

### Energy Reduction

Energy reduction is percentage reduction in net energy consumption in evolved (or new) load profile compared to base or reference profile.

### Ramp Reduction

Ramp reduction is percentage reduction in maximum ramp rate of evolved (or new) load profile compared to base or reference profile.

### Avg2P Reduction

Avg2P reduction is percentage reduction in average to peak power of evolved (or new) load profile compared to base or reference profile.



