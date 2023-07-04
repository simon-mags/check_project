from ansible.module_utils.basic import AnsibleModule
import json
import subprocess
import re
from deepdiff import DeepDiff

def install_dependencies():
    # Install required dependencies using pip
    try:
        subprocess.check_call(["pip", "install", "deepdiff"])
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to install dependencies: {e}")

def convert_to_string(item):
    # Convert AnsibleUnicode to string
    if isinstance(item, str):
        return (item)
    return str(item)
def compare_files(module):

    # Retrieve the values of the module arguments
    before_file = module.params['before_file']
    after_file = module.params['after_file']
    ignore_whole_lines = module.params['ignore_whole_lines'] or []
    ignore_regex_patterns = module.params['ignore_regex_patterns'] or []

    # Print the ignore_whole_lines and its type
    print(f"Ignore whole lines: {ignore_whole_lines}")
    print(f"Ignore whole lines type: {type(ignore_whole_lines)}")

  # Check if ignore_whole_lines is empty or contains only one data type
    if ignore_whole_lines:
        # Add whole lines to ignored_paths
        ignored_paths.extend(ignore_whole_lines)

    # Check if ignore_regex_patterns is empty or contains only one data type
    if ignore_regex_patterns:
        # Add regex patterns to ignored_paths
        regex_patterns = [re.escape(pattern) for pattern in ignore_regex_patterns]
        paths_to_ignore = [
            path
            for path in DeepDiff(before_data, after_data, view='tree')
            for pattern in regex_patterns
            if re.search(pattern, path)
        ]
        ignored_paths.extend(paths_to_ignore)
    # Convert ignore_list items to the appropriate data type
    converted_ignore_list = []
    for ignore_item in ignore_list:
        converted_ignore_list.append(eval(ignore_item))

    try:
        # Load the JSON data from the before and after files
        with open(before_file, 'r') as f:
            before_data = json.load(f)
        with open(after_file, 'r') as f:
            after_data = json.load(f)

        # Create a list to store ignored paths
        ignored_paths = []

        # Check if ignore_list is empty or contains only one data type
        if ignore_list:
            regex_patterns = []
            string_paths = []
            for ignore_item in ignore_list:
                if ignore_item.startswith('/'):
                    # If the item starts with '/', consider it a whole line to ignore
                    string_paths.append(ignore_item)
                else:
                    # If it doesn't start with '/', treat it as a regex pattern
                    regex_patterns.append(re.escape(ignore_item))

            # Add regex patterns to ignored_paths
            if regex_patterns:
                regex_pattern = '|'.join(regex_patterns)
                paths_to_ignore = [
                    path
                    for path in DeepDiff(before_data, after_data, view='tree')
                    if re.search(regex_pattern, path)
                ]
                ignored_paths.extend(paths_to_ignore)

            # Add string paths to ignored_paths
            ignored_paths.extend(string_paths)

        # Use the ignored_paths in the DeepDiff call to exclude them from the comparison
        differences = DeepDiff(before_data, after_data, exclude_paths=ignored_paths)

        # Prepare the result to be returned
        result = {
            'before_file': before_file,
            'after_file': after_file,
            'ignore_list': ignore_list,
            'ignored_paths': ignored_paths,
            'differences': differences.to_dict()
        }

        # Exit the module execution and return the result
        module.exit_json(changed=False, result=result)

    except Exception as e:
        # If any exception occurs, fail the module and return the error message
        module.fail_json(msg=str(e))

def main():
    # Define the expected module arguments
    module_args = dict(
        before_file=dict(type='str', required=True),
        after_file=dict(type='str', required=True),
        ignore_list=dict(type='list', elements='str')
    )

    # Create an AnsibleModule instance with the provided arguments
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Call the compare_files function to execute the module logic
    compare_files(module)  # Pass the 'module' argument here

if __name__ == '__main__':
    # Invoke the main function when the script is run directly
    main()
