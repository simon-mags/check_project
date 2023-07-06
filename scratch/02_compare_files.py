from ansible.module_utils.basic import AnsibleModule
import json
import subprocess
import re
from deepdiff import DeepDiff
import traceback

def convert_to_string(item):
    if isinstance(item, bytes):
        return item.decode('utf-8')
    return str(item)

def compare_files(module, before_file, after_file, ignore_whole_lines, ignore_regex_patterns):
    ignore_whole_lines = [str(line) for line in ignore_whole_lines]
    ignore_regex_patterns = [str(pattern) for pattern in ignore_regex_patterns]

    print(f"ignore_whole_lines - type: {type(ignore_whole_lines)}, value: {ignore_whole_lines}")
    print(f"ignore_regex_patterns - type: {type(ignore_regex_patterns)}, value: {ignore_regex_patterns}")

    try:
        with open(before_file, 'r') as f:
            before_data = json.load(f)
        with open(after_file, 'r') as f:
            after_data = json.load(f)

        ignored_paths = []

        if ignore_whole_lines:
            ignored_paths.extend(ignore_whole_lines)

        if ignore_regex_patterns:
            regex_patterns = [re.escape(pattern) for pattern in ignore_regex_patterns]
            paths_to_ignore = [
                path
                for path in DeepDiff(before_data, after_data, view='tree')
                for pattern in regex_patterns
                if re.search(pattern, path)
            ]
            ignored_paths.extend(paths_to_ignore)

        differences = DeepDiff(before_data, after_data, exclude_paths=ignored_paths)

        result = {
            'before_file': before_file,
            'after_file': after_file,
            'ignore_whole_lines': ignore_whole_lines,
            'ignore_regex_patterns': ignore_regex_patterns,
            'differences': differences.to_dict()
        }

        module.exit_json(changed=False, result=result)

    except Exception as e:
        traceback.print_exc()
        module.fail_json(msg=str(e))

def main():
    module_args = dict(
        before_file=dict(type='str', required=True),
        after_file=dict(type='str', required=True),
        ignore_whole_lines=dict(type='list', elements='str'),
        ignore_regex_patterns=dict(type='list', elements='str')
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    compare_files(module,
                  module.params['before_file'],
                  module.params['after_file'],
                  module.params['ignore_whole_lines'],
                  module.params['ignore_regex_patterns'])

if __name__ == '__main__':
    main()
