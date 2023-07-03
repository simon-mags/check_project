# my_modules/compare_files.py

from ansible.module_utils.basic import AnsibleModule
import json
import subprocess

# def install_dependencies():
#     try:
#         subprocess.check_call(["pip", "install", "deepdiff"])
#     except subprocess.CalledProcessError as e:
#         raise Exception(f"Failed to install dependencies: {e}")

def compare_files():
    # install_dependencies()

    from deepdiff import DeepDiff

    module_args = dict(
        before_file=dict(type='str', required=True),
        after_file=dict(type='str', required=True),
        ignore_list=dict(type='list', elements='str', default=[])  # Add default value and type validation
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    before_file = module.params['before_file']
    after_file = module.params['after_file']
    ignore_list = module.params['ignore_list']  # Retrieve the ignore_list value

    if not isinstance(ignore_list, list):
        module.fail_json(msg="ignore_list must be a list of strings.")

    try:
        with open(before_file, 'r') as f:
            before_data = json.load(f)
        with open(after_file, 'r') as f:
            after_data = json.load(f)

        # Use the ignore_list parameter in the DeepDiff call
        differences = DeepDiff(before_data, after_data, exclude_paths=ignore_list)

        result = {
            'before_file': before_file,
            'after_file': after_file,
            'ignore_list': ignore_list,  # Include ignore_list in the result
            'differences': differences.to_dict()
        }

        module.exit_json(changed=False, result=result)

    except Exception as e:
        module.fail_json(msg=str(e))

def main():
    compare_files()

if __name__ == '__main__':
    main()
