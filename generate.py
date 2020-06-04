#!/usr/bin/env python

# author: Piotr P. Nikiel <piotr@nikiel.info>
# date: May 2020

import sys
import json
import jinja2
import os
import argparse

def cap_first(word):
    """Capitalizes first letter of the string.
    Often used to generate setCapitalCase and other verb methods"""
    return word[0].upper() + word[1:]
    
def to_camel(id):
    """Converts under_score separation to underScore camel case"""
    return ''.join(cap_first(x) for x in id.split('_'))

Jobs = { 
    'c_lib_header'  :   {'xform': 'airhdl_to_header.jinja',     'output': '{component_name}.h'},
    'c_lib_body'    :   {'xform': 'airhdl_to_body.jinja',       'output': '{component_name}.c'},
    'cpp_lib_header':   {'xform': 'airhdl_to_cppheader.jinja',  'output': '{cpp_class_name}.hpp'},
    'cpp_lib_body'  :   {'xform': 'airhdl_to_cppbody.jinja',    'output': '{cpp_class_name}.cpp'},
    'cpp_python'    :   {'xform': 'airhdl_to_cpppython.jinja',  'output': '{cpp_class_name}Python.cpp'},
    }

def apply_transform(env, transform, json_repr, output_name, output_dir):
    if not os.path.isdir(output_dir):
        print('Creating {0} as it doesnt exist...'.format(output_dir))
        os.makedirs(output_dir)
    
    render_args = {}
    render_args['json'] = json_repr
    
    # ClassName, for C++ library
    component_name = json_repr['registerMap']['name']
    render_args['CppClassName'] = to_camel(component_name)
    
    output_fn = os.path.sep.join([output_dir, output_name])
    print('Generating {0}...'.format(output_fn))
    template = env.get_template(transform)
    file_output = open(output_fn, 'w')
    file_output.write(template.render(render_args))
    file_output.close()
    os.system('astyle {0}'.format(output_fn))

def main():
    parser = argparse.ArgumentParser(
        description='Creates software components from AirHdl AXI4 regmaps')
    parser.add_argument('regmap', help="path to AirHdl regmap in JSON format")
    parser.add_argument('--output_dir', default='output', help='output directory')
    
    args = parser.parse_args()

    input_file = open(args.regmap, 'r')
    json_repr = json.load(input_file)
     
    component_name = json_repr['registerMap']['name']
    print('Component name is {0}'.format(component_name))
    
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates'))
    env.trim_blocks = True
    env.filters['cap_first'] = cap_first
    env.filters['to_camel'] = to_camel

    for job_name in Jobs:
        print("Will generate {0}".format(job_name))
        job = Jobs[job_name]
        apply_transform(env, job['xform'], json_repr, job['output'].format(
            component_name=component_name,
            cpp_class_name=to_camel(component_name)),
            args.output_dir)

if __name__ == "__main__":
    main()
