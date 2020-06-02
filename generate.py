import sys
import json
import jinja2
import os

def apply_transform(env, transform, json_repr, output_name):
    template = env.get_template(transform)
    file_output = open(output_name, 'w')
    file_output.write(template.render(json=json_repr))
    file_output.close()
    os.system('astyle {0}'.format(output_name))

input_file = open(sys.argv[1], 'r')
json_repr = json.load(input_file)
 
component_name = json_repr['registerMap']['name']
 
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'))
env.trim_blocks = True


apply_transform(env, 'airhdl_to_header.jinja', json_repr, '{0}.h'.format(component_name))
apply_transform(env, 'airhdl_to_body.jinja', json_repr, '{0}.c'.format(component_name))
