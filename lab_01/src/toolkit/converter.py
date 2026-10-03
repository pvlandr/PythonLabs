import decimal
import json
import pathlib
from decimal import Decimal

from toolkit.errors import *

# decimal.getcontext().prec = 10

class UnitCategory:
    """Категория единиц измерения"""
    def __init__(self, name: str, base_unit_name: str, base_unit_min: Decimal | None, base_unit_max: Decimal | None):
        self.name = name
        self.base_unit_name = base_unit_name
        self.base_unit_min = base_unit_min
        self.base_unit_max = base_unit_max

    def verify_base_unit_value(self, value: Decimal):
        """Создает ошибку, если число в основной велечине категории выходит за предел допустимых значений"""
        if(self.base_unit_min != None) and (value < self.base_unit_min):
            raise ConversionError(f"{self.name} ({value} {self.base_unit_name}) is less than the minimum of {self.base_unit_min} {self.base_unit_name}")
        if(self.base_unit_max != None) and (value > self.base_unit_max):
            raise ConversionError(f"{self.name} ({value} {self.base_unit_name}) is greater than the maximum of {self.base_unit_max} {self.base_unit_name}")

class Unit:
    def __init__(self, name: str, category_name: str, mult: Decimal, add: Decimal):
        self.name = name
        self.category_name = category_name
        self.mult = mult
        self.add = add

    def convert_to_base_unit(self, value: Decimal):
        """Переводит число из этой величины в основнуюЫ"""
        return (value - self.add) / self.mult

    def convert_from_base_unit(self, value: Decimal):
        """Переводит число из основной величины в эту"""
        return (self.mult * value) + self.add

def deserialize_conversions():
    """Загружает единицы измерения из таблицы конвертаций"""
    path_to_lab_folder = pathlib.Path(__file__).parent
    path_to_conv_table = pathlib.Path(path_to_lab_folder, "conversion_table.json")
    parsed_json: any
    with open(path_to_conv_table) as conv_table_file:
        parsed_json = json.load(conv_table_file)

    unit_categories: dict[str, UnitCategory] = {}
    units: dict[str, Unit] = {}

    j_unit_categories = parsed_json["unit_categories"]
    for j_unit_cat in j_unit_categories:
        cat_name: str = ""
        try:
            cat_name = j_unit_cat["name"]
        except KeyError:
            raise ConversionTableError("A unit category is missing a name")

        try:
            base_unit_name = j_unit_cat["base_unit_name"]
            base_unit_min = None
            if("base_unit_min" in j_unit_cat):
                base_unit_min = Decimal(j_unit_cat["base_unit_min"])
            base_unit_max = None
            if("base_unit_max" in j_unit_cat):
                base_unit_max = Decimal(j_unit_cat["base_unit_max"])
            unit_cat = UnitCategory(cat_name, base_unit_name, base_unit_min, base_unit_max)
            unit_categories[cat_name] = unit_cat

            j_units = j_unit_cat["units"]
            for j_unit in j_units:
                unit_name: str = ""
                try:
                    unit_name = j_unit["name"]
                except KeyError:
                    raise ConversionTableError(f"A unit in category \"{cat_name}\" is missing a name")

                try:
                    unit_mult = Decimal(1)
                    if("mult" in j_unit):
                        unit_mult = Decimal(j_unit["mult"])
                    unit_add = Decimal(0)
                    if("add" in j_unit):
                        unit_add = Decimal(j_unit["add"])
                    unit = Unit(unit_name, cat_name, unit_mult, unit_add)
                    units[unit_name] = unit
                except KeyError:
                    raise ConversionTableError(f"Unit \"{unit_name}\" in category \"{cat_name}\" is missing required properties")
        except KeyError:
            raise ConversionTableError(f"Category \"{cat_name}\" is missing required properties")

    return unit_categories, units

unit_categories, units = deserialize_conversions()

def convert(value: Decimal, from_unit_name: str, to_unit_name: str) -> Decimal:
    """Переводит число в другую единицу измерения"""
    from_unit_name = from_unit_name.lower()
    to_unit_name = to_unit_name.lower()

    if(from_unit_name not in units):
        raise UnitError(f"Invalid unit: {from_unit_name}")

    if(to_unit_name not in units):
        raise UnitError(f"Invalid unit: {to_unit_name}")

    from_unit = units[from_unit_name]
    to_unit = units[to_unit_name]

    if(from_unit.category_name != to_unit.category_name):
        raise UnitError(f"Units {from_unit} and {to_unit} are incompatible")

    if(to_unit.category_name not in unit_categories):
        raise UnitError(f"Invalid unit category {to_unit.category_name}")

    category = unit_categories[to_unit.category_name]
    base_unit_value = from_unit.convert_to_base_unit(value)
    category.verify_base_unit_value(base_unit_value)
    converted_value = to_unit.convert_from_base_unit(base_unit_value)

    return converted_value