# orangecontrib/des/sim/engine.py
from dataclasses import dataclass
import random
import simpy

@dataclass
class SimulationSpec:
    name: str = "mm1"
    seed: int = 1
    sim_time: float = 480.0          # minutes
    interarrival_mean: float = 5.0   # minutes
    service_mean: float = 4.0        # minutes

@dataclass
class SimulationResult:
    kpis: dict
    events: list  # list of dict rows

def expovariate(mean, rng):
    return rng.expovariate(1.0 / mean)

def run_mm1(spec: SimulationSpec) -> SimulationResult:
    rng = random.Random(spec.seed)
    env = simpy.Environment()
    server = simpy.Resource(env, capacity=1)

    events = []
    n_served = 0
    total_wait = 0.0
    busy_time = 0.0
    last_start = None

    def customer(i):
        nonlocal n_served, total_wait, busy_time, last_start
        arrival_t = env.now
        events.append({"t": arrival_t, "entity": i, "event": "arrive"})
        with server.request() as req:
            yield req
            start_t = env.now
            wait = start_t - arrival_t
            total_wait += wait
            events.append({"t": start_t, "entity": i, "event": "start_service", "wait": wait})

            service_t = expovariate(spec.service_mean, rng)
            last_start = start_t
            yield env.timeout(service_t)
            end_t = env.now
            busy_time += (end_t - last_start)
            events.append({"t": end_t, "entity": i, "event": "end_service", "service": service_t})
            n_served += 1

    def arrivals():
        i = 0
        while True:
            ia = expovariate(spec.interarrival_mean, rng)
            yield env.timeout(ia)
            i += 1
            env.process(customer(i))

    env.process(arrivals())
    env.run(until=spec.sim_time)

    avg_wait = (total_wait / n_served) if n_served else 0.0
    util = busy_time / spec.sim_time if spec.sim_time > 0 else 0.0

    kpis = {
        "served": n_served,
        "avg_wait": avg_wait,
        "utilization": util,
        "sim_time": spec.sim_time,
        "seed": spec.seed,
    }
    return SimulationResult(kpis=kpis, events=events)
