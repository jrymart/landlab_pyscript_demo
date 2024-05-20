from landlab.core import load_params
from landlab.components import LinearDiffuser

from model_base import LandlabModel

class HillslopeLem(LandlabModel):

    DEFAULT_PARAMS = {
        "grid": {
            "source": "create",
            "create_grid": {
                "RasterModelGrid": [
                    (41, 5),
                    {"xy_spacing": 5},
                    ],
                },
            },
        "clock": {"start": 0.0, "stop": 1000000, "step": 1250},
        "output": {
            "plot_times": [100, 100000, 1000000],
            "save_times": [1000001],
            "report_times": [1000001],
            "save_path": "model_run",
            "fields": None,
            "plot_to_file":  True,
            },
        "baselevel": {
            "uplift_rate": 0.0001,
            },
        "diffuser": {"D": 0.01},
        }

    def __init__(self, params={}):
        """Initialize the Model"""
        super().__init__(params)

        if not ("topographic__elevation" in self.grid.at_node.keys()):
            self.grid.add_zeros("topographic__elevation", at="node")
        self.topo = self.grid.at_node["topographic__elevation"]

        self.uplift_rate = params["baselevel"]["uplift_rate"]
        self.diffuser = LinearDiffuser(
            self.grid,
            linear_diffusivity = params["diffuser"]["D"]
            )

    def update(self, dt):
        """Advance the model by one time step of duration dt."""
        self.topo[self.grid.core_nodes] += self.uplift_rate * dt
        self.diffuser.run_one_step(dt)
        self.current_time += dt
        

        
