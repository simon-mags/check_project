import re
from ansible.module_utils.basic import AnsibleModule
import json

def compare_files():
    # Define module arguments
    module_args = dict(
        before_file=dict(type='str', required=True),
        after_file=dict(type='str', required=True),
        ignore_list=dict(type='list', elements='str', default=[])  # Update type to list of strings
    )

    # Create Ansible module instance
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Extract module parameters
    before_file = module.params['before_file']
    after_file = module.params['after_file']
    ignore_list = module.params['ignore_list']

    if not isinstance(ignore_list, list):
        # Fail the module if ignore_list is not a list
        module.fail_json(msg="ignore_list must be a list of strings.")

    try:
        # Load data from before and after files
        with open(before_file, 'r') as f:
            before_data = json.load(f)
        with open(after_file, 'r') as f:
            after_data = json.load(f)

        # Compare JSON files and find differences
        differences = compare_json_files(before_data, after_data, ignore_list)

        # Prepare result dictionary
        result = {
            'before_file': before_file,
            'after_file': after_file,
            'ignore_list': ignore_list,
            'differences': differences
        }

        # Exit the module with the result
        module.exit_json(changed=False, result=result)

    except FileNotFoundError as e:
        # Handle file not found errors
        module.fail_json(msg=str(e))

    except json.JSONDecodeError as e:
        # Handle JSON decode errors
        module.fail_json(msg="Error decoding JSON: " + str(e))

    except Exception as e:
        # Handle other exceptions
        module.fail_json(msg="An error occurred: " + repr(e))

def compare_json_files(before_data, after_data, ignore_list):
    differences = {}

    for path in ignore_list:
        if path == 'root':
            continue

        before_value = get_value_by_path(before_data, path)
        after_value = get_value_by_path(after_data, path)

        if before_value != after_value:
            differences[path] = {
                'before_value': before_value,
                'after_value': after_value
            }

    return differences

def get_value_by_path(data, path):
    path = path.replace('[', '.').replace(']', '')
    path_parts = path.split('.')

    for part in path_parts:
        match = re.match(r'(\w+)(\[(\d+)\])?', part)
        key = match.group(1)
        index = match.group(3)

        if index is not None:
            data = data[key][int(index)]
        else:
            data = data[key]

    return data

if __name__ == '__main__':
    compare_files()
