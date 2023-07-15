# filter_plugins/convert_to_string.py

def convert_to_string(input_list):
    print("Converting to string...")
    converted_list = [str(item.encode('utf-8')) for item in input_list]
    print("Converted list:", converted_list)
    return converted_list

class FilterModule(object):
    def filters(self):
        return {
            'convert_to_string': convert_to_string,
        }
