import json
import re
import subprocess
from deepdiff import DeepDiff

def install_dependencies():
    # Install required dependencies using pip
    try:
        subprocess.check_call(["pip", "install", "deepdiff"])
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to install dependencies: {e}")

def convert_to_string(item):
    # Convert byte strings to string
    if isinstance(item, bytes):
        return item.decode('utf-8')
    return str(item)

def compare_files(module):
    # Retrieve the values of the module arguments
    before_file = module.params['before_file']
    after_file = module.params['after_file']
    ignore_whole_lines = module.params['ignore_whole_lines'] or []
    ignore_regex_patterns = module.params['ignore_regex_patterns'] or []

    # Print the ignore_whole_lines and ignore_regex_patterns
    print(f"Ignore whole lines: {', '.join(map(convert_to_string, ignore_whole_lines))}")
    print(f"Ignore regex patterns: {', '.join(map(convert_to_string, ignore_regex_patterns))}")

    try:
        # Load the JSON data from the before and after files
        with open(before_file, 'r') as f:
            before_data = json.load(f)
        with open(after_file, 'r') as f:
            after_data = json.load(f)

        # Create a list to store ignored paths
        ignored_paths = []

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

        # Use the ignored_paths in the DeepDiff call to exclude them from the comparison
        differences = DeepDiff(before_data, after_data, exclude_paths=ignored_paths)

        # Prepare the result to be returned
        result = {
            'before_file': before_file,
            'after_file': after_file,
            'ignore_whole_lines': ignore_whole_lines,
            'ignore_regex_patterns': ignore_regex_patterns,
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
        ignore_whole_lines=dict(type='list', elements='str'),
        ignore_regex_patterns=dict(type='list', elements='str')
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
