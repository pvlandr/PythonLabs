import json
import pathlib

class UnitCategory:
    def __init__(self, name: str, base_unit_name: str, base_unit_min: float | None, base_unit_max: float | None):
        self.name = name
        self.base_unit_name = base_unit_name
        self.base_unit_min = base_unit_min
        self.base_unit_max = base_unit_max

    def verify_base_unit_value(self, value: float):
        if(self.base_unit_min != None) and (value < self.base_unit_min):
            raise ValueError(f"{self.name} ({value} {self.base_unit_name}) is less than the minimum of {self.base_unit_min} {self.base_unit_name}")
        if(self.base_unit_max != None) and (value > self.base_unit_max):
            raise ValueError(f"{self.name} ({value} {self.base_unit_name}) is greater than the maximum of {self.base_unit_max} {self.base_unit_name}")

class Unit:
    def __init__(self, name: str, category_name: str, mult: float, add: float):
        self.name = name
        self.category_name = category_name
        self.mult = mult
        self.add = add

    def convert_to_base_unit(self, value: float):
        return (value - self.add) / self.mult

    def convert_from_base_unit(self, value: float):
        return (self.mult * value) + self.add

def deserialize_conversions():
    path_to_lab_folder = pathlib.Path(__file__).parent.parent
    path_to_conv_table = pathlib.Path(path_to_lab_folder, "conversion_table.json")
    parsed_json = json.load(open(path_to_conv_table))

    unit_categories: dict[str, UnitCategory] = {}
    units: dict[str, Unit] = {}

    j_unit_categories = parsed_json["unit_categories"]
    for j_unit_cat in j_unit_categories:
        cat_name: str = j_unit_cat["name"]
        base_unit_name = j_unit_cat["base_unit_name"]
        base_unit_min = None
        if("base_unit_min" in j_unit_cat):
            base_unit_min = float(j_unit_cat["base_unit_min"])
        base_unit_max = None
        if("base_unit_max" in j_unit_cat):
            base_unit_max = float(j_unit_cat["base_unit_max"])
        unit_cat = UnitCategory(cat_name, base_unit_name, base_unit_min, base_unit_max)
        unit_categories[cat_name] = unit_cat

        j_units = j_unit_cat["units"]
        for j_unit in j_units:
            unit_name: str = j_unit["name"]
            unit_mult = 1.0
            if("mult" in j_unit):
                unit_mult = float(j_unit["mult"])
            unit_add = 0.0
            if("add" in j_unit):
                unit_add = float(j_unit["add"])
            unit = Unit(unit_name, cat_name, unit_mult, unit_add)
            units[unit_name] = unit

    return unit_categories, units

unit_categories, units = deserialize_conversions()

def convert(value: float, from_unit_name: str, to_unit_name: str) -> int:
    if(from_unit_name not in units):
        raise ValueError(f"Invalid unit: {from_unit_name}")

    if(to_unit_name not in units):
        raise ValueError(f"Invalid unit: {to_unit_name}")

    from_unit = units[from_unit_name]
    to_unit = units[to_unit_name]

    if(from_unit.category_name != to_unit.category_name):
        raise ValueError(f"{from_unit} and {to_unit} are different categories")

    if(to_unit.category_name not in unit_categories):
        raise ValueError(f"Invalid unit category {to_unit.category_name}")

    category = unit_categories[to_unit.category_name]
    base_unit_value = from_unit.convert_to_base_unit(value)
    category.verify_base_unit_value(base_unit_value)
    converted_value = to_unit.convert_from_base_unit(base_unit_value)

    return converted_value