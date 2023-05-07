
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

3. Update the `hosts` file with the IP address or hostname of the server you want to check.

4. Update the `vars/main.yml` file with any variables that are specific to your environment.

5. Run the playbook:

```
$ ansible-playbook main_playbook.yml -i hosts
```

## Roles

### `server_check_role`

This role checks the following:

- kernel version
- Disk usage
- major and minor operating system release
- Swap usage


the project will aim to write some further roles such as:

### `user_check_role`

This role checks the following:

- Password aging for all users

### `network_check_role`

This role checks the following:

- DNS resolution
- Network latency to a specified host
- Open ports on the server

## Custom Tests

You can add your own custom tests by creating YAML files in the `roles/server_check_role/tasks/custom_tests` directory. These files should contain a set of tasks that perform the tests you want to run. The output of these tests will be added to the server report.

## Server Report

After running the playbook, a report will be generated in the `server_report` directory. This report will contain the results of all checks performed, including any custom tests you've added. If any issues are found, they will be highlighted in red. If everything checks out, the report will be all green.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
