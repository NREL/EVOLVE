# Modeling Solar Panel Installation

### Modeling Fixed Axis Solar Installation

Here is an example script to get started on modeling fixed axis solar installation.

```py title="Fixed Axis Solar Model"

import random
from datetime import datetime, timedelta
import pandas as pd
from evolve.solar.solar import (
    FixedAxisSolarModel,
    SolarBasicModel,
    FixedAxisModel,
    InverterModel
)
 
timestamps = [datetime(2023,1,1,0,0,0)+ timedelta(minutes=60*i) for i in range(24)]
irradiance_df = pd.DataFrame({
    "timestamp": timestamps,
    "ghi": [0 if i< 6 or i>17 else random.random()*1000 for i in range(24)],
    "dhi": [0 if i< 6 or i>17 else random.random()*1000 for i in range(24)],
    "dni": [0 if i< 6 or i>17 else random.random()*1000 for i in range(24)]
})

solar_instance = FixedAxisSolarModel(
    solar_basic_model=SolarBasicModel(
        longitude=9.0, latitude=36.0, kw=5.0, irradiance=irradiance_df
    ),
    axis_model=FixedAxisModel(surface_azimuth=130, surface_tilt=20),
    inv_model=InverterModel(acdcratio=1.0),
)

print(solar_instance.get_inverter_ac_output())

```