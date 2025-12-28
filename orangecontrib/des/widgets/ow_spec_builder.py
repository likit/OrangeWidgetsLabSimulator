# orangecontrib/des/widgets/ow_spec_builder.py
from Orange.widgets.widget import OWWidget, Output
from Orange.widgets import gui
from orangewidget.settings import Setting

from orangecontrib.des.sim.engine import SimulationSpec

class OWSpecBuilder(OWWidget):
    name = "DES Spec Builder"
    description = "Create a simulation specification"
    icon = "icons/spec.svg"
    priority = 10

    class Outputs:
        spec = Output("Simulation Spec", object)

    seed = Setting(1)
    sim_time = Setting(480.0)
    interarrival_mean = Setting(5.0)
    service_mean = Setting(4.0)

    def __init__(self):
        super().__init__()
        box = gui.widgetBox(self.controlArea, "Parameters")

        gui.spin(box, self, "seed", 1, 10_000, label="Seed")
        gui.doubleSpin(box, self, "sim_time", 1.0, 1e7, label="Sim time (min)")
        gui.doubleSpin(box, self, "interarrival_mean", 0.001, 1e6, label="Interarrival mean")
        gui.doubleSpin(box, self, "service_mean", 0.001, 1e6, label="Service mean")

        gui.button(self.controlArea, self, "Send Spec", callback=self.commit)
        self.commit()

    def commit(self):
        spec = SimulationSpec(
            seed=int(self.seed),
            sim_time=float(self.sim_time),
            interarrival_mean=float(self.interarrival_mean),
            service_mean=float(self.service_mean),
        )
        self.Outputs.spec.send(spec)
