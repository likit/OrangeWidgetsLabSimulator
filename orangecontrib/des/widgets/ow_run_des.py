# orangecontrib/des/widgets/ow_run_des.py
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui
from orangewidget.settings import Setting

import Orange
from Orange.data import Domain, ContinuousVariable, DiscreteVariable, StringVariable

from orangecontrib.des.sim.engine import SimulationSpec, run_mm1

class OWRunDES(OWWidget):
    name = "Run DES"
    description = "Run discrete-event simulation and output results"
    icon = "icons/run.svg"
    priority = 20

    class Inputs:
        spec = Input("Simulation Spec", object)

    class Outputs:
        results = Output("Simulation Result", object)
        events = Output("Events (Table)", Orange.data.Table)

    autorun = Setting(True)

    def __init__(self):
        super().__init__()
        self.spec = None

        box = gui.widgetBox(self.controlArea, "Run")
        gui.checkBox(box, self, "autorun", "Auto-run on input change")
        gui.button(box, self, "Run", callback=self.run)

        self.info_box = gui.widgetBox(self.controlArea, "KPIs")
        self.kpi_label = gui.label(self.info_box, self, "")

    @Inputs.spec
    def set_spec(self, spec):
        self.spec = spec
        if self.autorun and self.spec is not None:
            self.run()

    def run(self):
        if self.spec is None:
            self.Outputs.results.send(None)
            self.Outputs.events.send(None)
            self.kpi_label.setText("No spec.")
            return

        res = run_mm1(self.spec)
        self.kpi_label.setText(
            f"served={res.kpis['served']}  avg_wait={res.kpis['avg_wait']:.3f}  util={res.kpis['utilization']:.3f}"
        )

        table = self._events_to_table(res.events)
        self.Outputs.results.send(res)
        self.Outputs.events.send(table)

    def _events_to_table(self, rows):
        # Define schema: time numeric, entity numeric, event categorical, plus optional fields
        t_var = ContinuousVariable("t")
        entity_var = ContinuousVariable("entity")
        event_var = DiscreteVariable("event", values=["arrive", "start_service", "end_service"])
        wait_var = ContinuousVariable("wait")
        service_var = ContinuousVariable("service")

        domain = Domain([t_var, entity_var, wait_var, service_var], metas=[event_var])

        X = []
        metas = []
        for r in rows:
            X.append([
                float(r.get("t", 0.0)),
                float(r.get("entity", 0.0)),
                float(r.get("wait", 0.0)) if "wait" in r else float("nan"),
                float(r.get("service", 0.0)) if "service" in r else float("nan"),
            ])
            metas.append([r.get("event", "")])

        return Orange.data.Table.from_list(domain, [x + m for x, m in zip(X, metas)])
