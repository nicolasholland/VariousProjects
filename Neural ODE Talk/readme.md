Neural Ordinary Differential Equation Julia Talk
================================================

Here are some notes in preperation of our (hopefully) upcoming talk on Neural ODEs.


Possible topics / slides
------------------------

* NNs, ODEs and Neural ODEs
* Conventional weather forecasting (Navier-Stokes, NWP)
* Delhi dataset, train/test split and evalation
* Julia code/implementation, e.g. live demo?
* DiffEqFlux, OrdinaryDiffEq and Flux
* Mention that it was popular topic at JuliaCon? (eg. could link to talks)

Topics that could be extra slides or things to talk about afterwards

* Go into why this can't work for things like day-ahead forecasts?
  (missing spatial info, ode vs. pde, ...)
* Mention possible applications within my field of application


Used versions
-------------

* Julia v"1.5"

```
  "DiffEqFlux"     => v"1.18.0"
  "OrdinaryDiffEq" => v"5.42.1"
  "Flux"           => v"0.11.0"
```



References
----------

* [Neural Ordinary Differential Equations paper](https://arxiv.org/abs/1806.07366)

* DiffEqFlux [package](https://julialang.org/blog/2019/01/fluxdiffeq/) ([中文](https://julialang.org/blog/2019/04/fluxdiffeq-zh_tw/)), [paper](https://arxiv.org/abs/1902.02376)
  (I love that they turned the blogpost into a paper :D )

* Neural ODE for weather forecast [blogpost](https://sebastiancallh.github.io/post/neural-ode-weather-forecast/)


Fixes
-----

The post had some missing imports/definitions and a typo


```
    using Dates
    features = ["meantemp", "humidity", "wind_speed", "meanpressure"]

    function train(θ = nothing, maxiters = 150, lr = 1e-2)
        log_results(θs, losses) =
	    (θ, loss) -> begin
                push!(θs, copy(θ))
                push!(losses, loss)
                false
            end

        θs, losses = [], []
        num_obs = 4:4:length(train_t)
        for k in num_obs
            node = neural_ode(train_t[1:k], size(y, 1))
            θ = train_one_round(
                node, θ, train_y[:, 1:k],
                ADAMW(lr), maxiters;
                cb = log_results(θs, losses)
            )
        end
        θs, losses
    end
```

The call to train_one_node had a typo.

