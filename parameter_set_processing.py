import json
import ast
import re
import os


def prepare_data(root_path, parameter_name):
    with open(f"{root_path}/vertex_3k.txt", "r", encoding='utf-8') as f:
        data = f.read()
        data_list = data.replace("[\n", "").split("\n]\n")

    with open(f"{root_path}/Data.txt", "r", encoding='utf-8') as f:
        pattern = r'\{([-+]?\d*\.?\d+([eE][-+]?\d+)?)\}'
        data = f.read().replace("'", '"'
                                ).replace('0,0,0,', '[0,0,0],')
        data = re.sub(pattern, r'\1', data)
        parameter_data = data.split("\n}\n")

    ready_parameters = []
    for row_parameters in parameter_data:
        if row_parameters:
            parameter_dict = ast.literal_eval(row_parameters + '\n}')
            ready_parameters.append(parameter_dict)

    ready_data_front = []
    ready_data_angle = []
    ready_data_side = []
    for row_data in data_list:
        data_dict = json.loads('{'+row_data+'}')
        if data_dict:
            data_parameters = ready_parameters[int(data_dict['batch'][2].strip('image='))]['parameters']
            data_dict['parameters'] = data_parameters
            data_dict['batch_number'] = data_dict['batch'][0].strip('batch=')
            data_dict['camera_angle'] = data_dict['batch'][1].strip('camera=')
            data_dict['image_id'] = data_dict['batch'][2].strip('image=')
            data_dict.pop('batch', None)

            match data_dict['camera_angle']:
                case 'Camera_Front':
                    ready_data_front.append(data_dict)
                case 'Camera_45':
                    ready_data_angle.append(data_dict)
                case 'Camera_Sid':
                    ready_data_side.append(data_dict)

    ready_data_front = sorted(ready_data_front, key=lambda x: x['parameters'][parameter_name])
    ready_data_angle = sorted(ready_data_angle, key=lambda x: x['parameters'][parameter_name])
    ready_data_side = sorted(ready_data_side, key=lambda x: x['parameters'][parameter_name])

    print('Saving cleaned data into json format')
    if not os.path.exists('data/clean_parameter_set/'):
        os.makedirs('data/clean_parameter_set/')

    with open(f"data/clean_parameter_set/front_data_{parameter_name}", "w") as f:
        json.dump(ready_data_front, f)

    with open(f"data/clean_parameter_set/angle_data_{parameter_name}", "w") as f:
        json.dump(ready_data_angle, f)

    with open(f"data/clean_parameter_set/side_data_{parameter_name}", "w") as f:
        json.dump(ready_data_side, f)
