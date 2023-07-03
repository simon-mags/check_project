def compare_files():
    from ansible.module_utils.basic import AnsibleModule
    import json
    import subprocess
    import re
    from deepdiff import DeepDiff

    module_args = dict(
        before_file=dict(type='str', required=True),
        after_file=dict(type='str', required=True),
        ignore_list=dict(type='list', elements='str', default=[])  # Update type to list of strings
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    before_file = module.params['before_file']
    after_file = module.params['after_file']
    ignore_list = module.params['ignore_list']

    if not isinstance(ignore_list, list):
        module.fail_json(msg="ignore_list must be a list of strings.")

    if ignore_list == []:
        module.fail_json(msg="ignore_list cannot be empty.")

    if not all(isinstance(item, str) for item in ignore_list):
        current_type = type(ignore_list).__name__
        expected_type = 'list of strings'
        module.fail_json(
            msg=f"Invalid ignore_list type. Current type: {current_type}, Expected type: {expected_type}"
        )

    try:
        with open(before_file, 'r') as f:
            before_data = json.load(f)
        with open(after_file, 'r') as f:
            after_data = json.load(f)

        differences = DeepDiff(
            before_data,
            after_data,
            exclude_paths=ignore_list  # Use ignore_list as exclude_paths
        )

        result = {
            'before_file': before_file,
            'after_file': after_file,
            'ignore_list': ignore_list,
            'differences': differences.to_dict()
        }

        module.exit_json(changed=False, result=result)

    except Exception as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    compare_files()
