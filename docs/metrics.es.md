# Explicación de las métricas

### Carga máxima


La carga máxima se define como la carga máxima durante un tiempo especificado. Matemáticamente se representa de la siguiente manera. 

$$
\operatorname{max}\{p_1, p_2, ...., p_t, ...., p_T\}
$$

### Consumo de energía

El consumo de energía es la suma del consumo de energía en todos los pasos de tiempo multiplicado por la resolución de tiempo. Tenga en cuenta que el consumo de energía que se muestra en el tablero de Evolution es en realidad un consumo de energía neto, por lo que un valor negativo significa que la energía se inyecta nuevamente a la red. La unidad predeterminada para el consumo de energía es MWh. Matemáticamente, el consumo de energía se representa de la siguiente manera. Aquí
$p_t$ es el consumo de energía en el momento $t$ y $\delta T$ 
es la resolución de tiempo en horas.

$$
\sum_{t=0}^{T} p_t \times \delta T
$$

### Tasa de rampa máxima

La tasa de rampa máxima en el panel de control de Evolution representa el cambio máximo absoluto en potencia por hora. Su unidad es MW/hr. Matemáticamente se representa de la siguiente manera.

$$
\operatorname{max} \{\frac{|p_{t}- p_{t-1}|}{\delta T}  \forall t \}
$$


### Relación promedio a pico

Se representa matemáticamente de la siguiente manera.

$$
\frac{\frac{1}{T}\sum_{t=0}^{T} p_t}{max\{p_1, p_2, ..., p_t, ..., p_T\}}
$$

### Reducción de picos


La reducción máxima es el porcentaje de reducción en la potencia máxima en el perfil de carga evolucionado (o nuevo) en comparación con el perfil base o de referencia.

### Reducción de energía


La reducción de energía es la reducción porcentual en el consumo de energía neta en el perfil de carga evolucionado (o nuevo) en comparación con el perfil base o de referencia.

### Reducción de rampa

La reducción de rampa es la reducción porcentual en la tasa de rampa máxima del perfil de carga evolucionado (o nuevo) en comparación con el perfil base o de referencia.

### Reducción promedio2P

La reducción Avg2P es la reducción porcentual en la potencia promedio a máxima del perfil de carga evolucionado (o nuevo) en comparación con el perfil base o de referencia.


## Métricas solares

---

###  Generacion de energia

La generación de energía solar es solo una suma de energía solar en todos los pasos de tiempo en una duración dada multiplicada por la resolución. La unidad de generación de energía solar expresada en EVOLVE es el kWh. 




