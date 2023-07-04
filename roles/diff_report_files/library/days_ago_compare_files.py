from ansible.module_utils.basic import AnsibleModule
import json
import subprocess
import re

def install_dependencies():
    # Install required dependencies using pip
    try:
        subprocess.check_call(["pip", "install", "deepdiff"])
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to install dependencies: {e}")

def compare_files():
    # Install dependencies before importing them
    install_dependencies()

    # Import necessary modules
    from deepdiff import DeepDiff

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

    # Retrieve the values of the module arguments
    before_file = module.params['before_file']
    after_file = module.params['after_file']
    ignore_list = module.params['ignore_list']

    try:
        # Load the JSON data from the before and after files
        with open(before_file, 'r') as f:
            before_data = json.load(f)
        with open(after_file, 'r') as f:
            after_data = json.load(f)

        # Create a list to store ignored paths
        ignored_paths = []

        # Iterate over each item in the ignore_list
        for ignore_item in ignore_list:
            if ignore_item.startswith('/'):
                # If the item starts with '/', consider it a whole line to ignore
                ignored_paths.append(ignore_item)
            else:
                # If it doesn't start with '/', treat it as a regex pattern
                regex = re.compile(ignore_item)
                # Find paths matching the regex pattern and add them to ignored_paths
                paths_to_ignore = [
                    path
                    for path in DeepDiff(before_data, after_data, view='tree')
                    if regex.search(path)
                ]
                ignored_paths.extend(paths_to_ignore)

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
    # Call the compare_files function to execute the module logic
    compare_files()

if __name__ == '__main__':
    # Invoke the main function when the script is run directly
    main()