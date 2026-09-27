import json
import pathlib

path_to_lab_folder = pathlib.Path(__file__).parent.parent
path_to_conv_table = pathlib.Path(path_to_lab_folder, "conversion_table.json")
convs = json.load(open(path_to_conv_table))

units = {}
for u_list in convs:
    units_here = convs[u_list]

    for unit in units_here:
        

def convert(value: int, from_unit: str, to_unit: str) -> int:
    return 0