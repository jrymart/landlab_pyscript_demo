from jinja2 import Environment, FileSystemLoader
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

def get_dynamic_params(parameters):
    fparams = flatten_dict(parameters)
    return [i[0] for i in fparams.items() if i[1]=="DYNAMIC"]

if __name__ == '__main__':
    param_file = open("demo_params.json", 'r')
    params = json.load(param_file)
    param_file.close()
    dynamic_params = get_dynamic_params(params)
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('index_template.html')
    new_file_str = template.render(dynamic_params=dynamic_params)
    indf = open('index.html', 'w')
    indf.write(new_file_str)
    indf.close()
