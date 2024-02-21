### Evolution of Net Load Variation from Emerging Technologies (EVOLVE)

<p align="center">
<img src="evolve-docs/docs/images/evolve_logo.svg" width="350" style="display:flex;justify-content:center;">
</p>

---

[Click here for full documentation](https://nrel.github.io/EVOLVE/)


EVOLVE is an opensource [python](https://www.python.org/) package to assess net load profile in the presence of combination of `distributed energy resource (DER)` technologies. 

Features of `evolve-core` package:

**Modeling Solar :** `EVOLVE` uses [pvlib](https://pvlib-python.readthedocs.io/en/stable/) to produce generation profile for different types of solar installations. 

**Modeling Battery :** `EVOLVE` uses it's own battery model to simulate timeseries charging discharging for different strategies. For example, time based, peak load shaving, and self consumption.

**Modeling Electric Vehicle:** `EVOLVE` is also able to model electric vehicles and charging stations based on user driven inputs. 

`EVOLVE` also has [React](https://react.dev/) based user interface which user can use to create, manage and simulate scenarios in a human friendly way. UI is backed by REST API developed using [FastAPI](https://fastapi.tiangolo.com/) framework in python. The simulation run if created using UI is queued using [RabbitMQ](https://rabbitmq.com/) and simulated in first come first serve basis. 

If you just want to use evolve-core, we have also published python package named `evolve-core` which you can install in any python environment. If you do want to use UI then you can use `compose.yml` available at the root of this [repo](https://github.com/nrel/evolve).
