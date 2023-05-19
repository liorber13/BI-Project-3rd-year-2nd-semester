import os
import json
import numpy as np
import pandas as pd
import sqlite3
import functools as ft
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from jsonpath_ng import parse
from enum import Enum
# %matplotlib inline

# abstract class
class Interface(ABC):

    @abstractmethod
    def get_data_by_field(self, field_name):
        """Fetch the data by given field name """

    @abstractmethod
    def get_data_by_id(self, id):
        """Fetch the data by given ID  """

    @abstractmethod
    def get(self):
        """Fetch all data """


class TransformMask(Enum):
    # add here any masks you want
    CLEAN_STRING = ".strip().lower()"
    CAPITAL_LETTER = ".strip().lower().title()"


class Database:
    def __init__(self):
        self.db = {
            "source": [],
            "destination": [],
            "transform": [],
            "mapping": []
        }

    def get_data_by_field(self, field_name):
        data = self.get
        for item in data:
            for key, value in item.items():
                if key == field_name:
                    return item
        return None

    def get_data_by_id(self, id):
        self.id = id
        data = self.get
        for x in data:
            if x.get("id") == self.id:
                return x
        return None

    # def add_source(id, source_field_name, source_field_mapping, source_field_type, is_required):
    #     pass
    #
    # def add_destination(id, source_field_name, source_field_mapping, source_field_type, is_required):
    #     pass
    #
    # def add_transform(id, source_field_name, source_field_mapping, source_field_type, is_required):
    #     pass
    #
    # def add_mapping(id, source_field_name, source_field_mapping, source_field_type, is_required):
    #     pass

    @property
    def get_data_source_target_mapping(self):
        return self.db

class Source(Interface, Database):
    def __init__(self):
        Database.__init__(self)
        Database.get_data_by_field(self)
        Database.get_data_by_id(self)

    @property
    def get(self):
        return self.get_data_source_target_mapping.get("source")

class Target(Interface, Database):
    def __init__(self):
        Database.__init__(self)
        Database.get_data_by_field(self)
        Database.get_data_by_id(self)

    @property
    def get(self):
        return self.get_data_source_target_mapping.get("destination")

class Transform(Interface, Database):

    def __init__(self):
        Database.__init__(self)
        Database.get_data_by_field(self)
        Database.get_data_by_id(self)

    @property
    def get(self):
        return self.get_data_source_target_mapping.get("transform", [])

class Mappings(Interface, Database):

    def __init__(self):
        Database.__init__(self)
        Database.get_data_by_field(self)
        Database.get_data_by_id(self)

    @property
    def get(self):
        return self.get_data_source_target_mapping.get("mapping")

class STTM:
    def __init__(self, input_json):
        self.input_json = input_json
        self.mapping_instance = Mappings()
        self.source_instance = Source()
        self.destination_instance = Target()
        self.transform_instance = Transform()
        self.look_up_mask = {i.name: i.value for i in TransformMask}
        self.json_data_transformed = {}

    def _get_mapping_data(self):
        return self.mapping_instance.get

    def _get_mapping_source_data(self):
        return self.source_instance.get

    def get_transformed_data(self):

        for mappings in self._get_mapping_data():

            """fetch the source mapping """
            mapping_source_id = mappings.get("mapping_source")
            mapping_destination_id = mappings.get("mapping_destination")
            mapping_transform_id = mappings.get("mapping_transform")

            mapping_source_data = self.source_instance.get_data_by_id(id=mapping_source_id)
            transform_data = self.transform_instance.get_data_by_id(id=mapping_transform_id)

            """Fetch Source  field Name"""
            source_field_name = mapping_source_data.get("source_field_name")

            """if field given is not present incoming json """
            if source_field_name not in self.input_json.keys():
                if mapping_source_data.get("is_required"):
                    raise Exception(
                        "Alert ! Field {} is not present in JSON please FIX mappings ".format(source_field_name))
                else:
                    pass

            else:
                source_data_value = JsonQuery(
                    json_path=mapping_source_data.get("source_field_mapping"),
                    json_data=self.input_json
                ).get()

                """check the data type for source if matches with what we have """
                if mapping_source_data.get("source_field_type") != type(source_data_value).__name__:
                    if source_data_value is not None:
                        _message = (
                            "Alert ! Source Field :{} Datatype has changed from {} to {} ".format(source_field_name,
                                                                                                  mapping_source_data.get(
                                                                                                      "source_field_type"),
                                                                                                  type(
                                                                                                      source_data_value).__name__))
                        print(_message)
                        raise Exception(_message)

                """Query and fetch the Destination | target """
                destination_mappings_json_object = self.destination_instance.get_data_by_id(
                    id=mappings.get("mapping_destination"))

                destination_field_name = destination_mappings_json_object.get("destination_field_name")
                destination_field_type = destination_mappings_json_object.get("destination_field_type")

                dtypes = [str, float, list, int, set, dict]

                for dtype in dtypes:

                    """Datatype Conversion """
                    if destination_field_type == str(dtype.__name__):

                        """is source is none insert default value"""
                        if source_data_value is None:
                            self.json_data_transformed[destination_field_name] = dtype.__call__(
                                destination_mappings_json_object.get("default_value")
                            )

                        else:
                            """check if you have items to transform"""
                            if transform_data is not None:
                                """ check for invalid mask name """
                                if transform_data.get("transform_mask") not in list(self.look_up_mask.keys()):
                                    raise Exception(
                                        f"Specified Transform {transform_data.get('transform_mask')} is not available please select from following Options :{list(self.look_up_mask.keys())}")
                                else:
                                    mask_apply = self.look_up_mask.get(transform_data.get("transform_mask"))
                                    converted_dtype = dtype.__call__(source_data_value)
                                    mask = f'converted_dtype{mask_apply}'
                                    curated_value = eval(mask)
                                    self.json_data_transformed[destination_field_name] = curated_value

                            else:
                                self.json_data_transformed[destination_field_name] = dtype.__call__(source_data_value)

        return self.json_data_transformed

transformed_data = []
for item in data:
    helper = STTM(input_json=item)
    response = helper.get_transformed_data()
    transformed_data.append(response)
    print(response)

pd.DataFrame(transformed_data)

pd.DataFrame(transformed_data).groupby("job_title").mean()
