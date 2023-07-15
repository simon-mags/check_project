
# Ansible Project to perform server checks

This Ansible project is designed to check various aspects of a server and compile the results of those commands into a report on any issues found. The project consists of several roles, each of which performs a specific check or set of checks.

## Requirements

- Ansible 2.9 or higher
- Python 3.x

## Usage

1. Clone this repository:

```
$ git clone https://github.com/simon-mags/check_project.git
```

2. Navigate to the project directory:

```
$ cd check_project
```

3. Update the `inventory` file with the IP address or hostname of the server you want to check or run against your own Inventory

4. Update the `vars/main.yml` file with any variables that are specific to your environment.

5. Run the playbook with "before":

```
$ ansible-playbook main_playbook.yml -i inventory -l localhost --extra-vars "report_state=before"
```

6. Run the playbook with "before":
Make a change on your server, i.e. patch and update it

7. Run the playbook with "after":
```
$ ansible-playbook main_playbook.yml -i inventory -l localhost --extra-vars "report_state=after"
```

## Roles

### `server_check_role`

This role checks the following:

- kernel version
- Disk usage
- major and minor operating system release
- Swap usage

The project will aim to write some further functions such as:

The ability to check on the status of the following items:

- Password aging for all users
- DNS resolution
- Network latency to a specified host
- Open ports on the server

## Custom Tests

You can add your own custom tests by creating YAML files in the `roles/server_check_role/tasks/custom_tests` directory. These files should contain a set of tasks that perform the tests you want to run. The output of these tests will be added to the server report.

## Server Report

After running the playbook, a report will be generated in the `server_report` directory. This report will contain the results of all checks performed, including any custom tests you've added. If any issues are found, they will be highlighted in red. If everything checks out, the report will be all green.

## Role Variables

Many vars are defined within the role `vars/` folder, these may need to be updated with any variables that are specific to your environment.

### `diff_report_files`

This role runs a diff command across the 'before' and 'after' files via a custom python library which uses the Deepdiff module.

It has been configured with ability to add ignore_whole_lines as a variable so that when you are looking through Ansible Facts you don't need to compare the memory used or memory free as an example from the before and after files, you can exclude it so that the diff only shows you important information which you care about.

Work is in progress on adding functionality to also ignore lines based on a regular expression.

## Diff report output

After running the playbook, a report will be generated in the `report_sample_output` directory. This report will contain the results of the diff of the before and after files, excluding any lines passed through in the ignore_whole_lines variable.

## Role Variables

A few vars are defined within the role `defaults/` folder, these may need to be updated with any variables that are specific to your environment.


## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
