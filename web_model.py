#import micropip
#await micropip.install("http://localhost:9000/landlab-2.7.1.dev0-cp311-cp311-emscripten_3_1_46_wasm32.whl")

#from hillslope_lem import HillslopeLem
from pyscript import window, document, display
import matplotlib.pyplot as plt
#from flask import render_template
#import jinja2
from collections.abc import MutableMapping
import json

def _flatten_dict_gen(d, parent_key, sep):
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            yield from flatten_dict(v, new_key, sep=sep).items()
        else:
            yield new_key, v


def flatten_dict(d: MutableMapping, parent_key: str = '', sep: str = '-'):
    return dict(_flatten_dict_gen(d, parent_key, sep))

# params = {
#         "grid": {
#             "source": "create",
#             "create_grid": {
#                 "RasterModelGrid": [
#                     (41, 5),
#                     {"xy_spacing": 5},
#                     ],
#                 },
#             },
#         "clock": {"start": 0.0, "stop": "DYNAMIC", "step": 1250},
#         "output": {
#             "plot_times": [10000001],
#             "save_times": [10000001],
#             "report_times": [10000001],
#             "save_path": "model_run",
#             "fields": None,
#             "plot_to_file":  True,
#             },
#         "baselevel": {
#             "uplift_rate": 0.0001,
#             },
#         "diffuser": {"D": "DYNAMIC"},
#         }
params = None
model = None

def get_dynamic_params(parameters):
    fparams = flatten_dict(parameters)
    return [i[0] for i in fparams.items() if i[1]=="DYNAMIC"]

def get_input(key):
    input_val = document.querySelector("#%s" % key)
    window.console.log("getting key: %s" % key)
    window.console.log("got value %s" % input_val)
    return float(input_val.value)

def create_model():
    global model
    global params
    dynamic_params = get_dynamic_params(params)
    for param in dynamic_params:
        input = get_input(param)
        working_params = params
        for key in param.split('-')[:-1]:
            working_params = working_params[key]
        working_params[param.split('-')[-1]] = input
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

def plot_model():
    global ax
    middle_swath = model.grid.at_node["topographic__elevation"].reshape(model.grid.shape)[:,2]
    ax.plot(middle_swath, label="TEST")
    ax.legend()
    display(fig, target="mpl", append=False)

#@when("click", "#go_button")
def go_button(event):
    #D_input = document.querySelector("#D_input")
    #D = float(D_input.value)
    window.console.log("Creating Model")
    create_model()
    window.console.log("running model")
    run_model()
    window.console.log("Generating output")
    plot_model()
    output_val = get_model_output()
    output_div = document.querySelector("#output")
    output_div.innerText = str(output_val)

fig, ax = plt.subplots()
#param_file = open("demo_params.json", 'r')
#params = json.load(param_file)
#param_file.close()

#if __name__ == '__main__':
#    #global params
#    dynamic_params = get_dynamic_params(params)
#    env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
#    template = env.get_template('index_template.html')
#    new_file_str = template.render(dynamic_params=dynamic_params)
#    indf = open('index.html', 'w')
#    indf.write(new_file_str)
