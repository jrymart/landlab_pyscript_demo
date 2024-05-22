#import micropip
#await micropip.install("http://localhost:9000/landlab-2.7.1.dev0-cp311-cp311-emscripten_3_1_46_wasm32.whl")

#from hillslope_lem import HillslopeLem
from pyscript import window, document, display
import matplotlib.pyplot as plt

model = None

def create_model(D):
    global model
    params = HillslopeLem.DEFAULT_PARAMS
    params["diffuser"]["D"] = D
    params["output"]["plot_to_file"] = False
    params["output"]["plot_times"] = [10000001]
    params["output"]["save_times"] = [10000001]
    model = HillslopeLem(params)

def run_model():
    global model
    if model is not None:
        model.run()
    else:
        window.console.log("No Model Initialized")

def get_model_output():
    middle_swath = model.grid.at_node["topographic__elevation"].reshape(model.grid.shape)[:,2]
    return middle_swath.mean()

def plot_model(val):
    global ax
    middle_swath = model.grid.at_node["topographic__elevation"].reshape(model.grid.shape)[:,2]
    ax.plot(middle_swath, label="D=%f" % val)
    ax.legend()
    display(fig, target="mpl", append=False)

#@when("click", "#go_button")
def go_button(event):
    D_input = document.querySelector("#D_input")
    D = float(D_input.value)
    window.console.log("Creating Model with D=%f" % D)
    create_model(D)
    window.console.log("running model")
    run_model()
    window.console.log("Generating output")
    plot_model(D)
    output_val = get_model_output()
    output_div = document.querySelector("#output")
    output_div.innerText = str(output_val)

fig, ax = plt.subplots()
