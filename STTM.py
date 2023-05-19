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
        """Fetch the data by given feild name """

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
        pass

    # built-in function that creates and returns a property object
    # get data by: get_data_source_target_mapping.get(dict_key)
    @property
    def get_data_source_target_mapping(self):
        return {
            "source": [
                {
                    "id": 1,
                    "source_field_name": "Gender",
                    "source_field_mapping": "$.Gender",
                    "source_field_type": "str", # use python types
                    "is_required": True,
                },
                {
                    "id": 2,
                    "source_field_name": "Married",
                    "source_field_mapping": "$.Married",
                    "source_field_type": "str",
                    "is_required": True,
                },
                {
                    "id": 3,
                    "source_field_name": "Age",
                    "source_field_mapping": "$.Age",
                    "source_field_type": "str",  # use python types
                    "is_required": True,
                },
                {
                    "id": 4,
                    "source_field_name": "Dependents",
                    "source_field_mapping": "$.Dependents",
                    "source_field_type": "str",
                    "is_required": True,
                },
                {
                    "id": 5,
                    "source_field_name": "Education",
                    "source_field_mapping": "$.Education",
                    "source_field_type": "str",  # use python types
                    "is_required": True,
                },
                {
                    "id": 6,
                    "source_field_name": "Self_Employed",
                    "source_field_mapping": "$.Self_Employed",
                    "source_field_type": "str",
                    "is_required": True,
                },
                {
                    "id": 7,
                    "source_field_name": "Applicant_Income",
                    "source_field_mapping": "$.Applicant_Income",
                    "source_field_type": "str",  # use python types
                    "is_required": True,
                },
                {
                    "id": 8,
                    "source_field_name": "Coapplicant_Income",
                    "source_field_mapping": "$.Coapplicant_Income",
                    "source_field_type": "str",
                    "is_required": True,
                },
                {
                    "id": 9,
                    "source_field_name": "Load_Date",
                    "source_field_mapping": "$.Load_Date",
                    "source_field_type": "str",  # use python types
                    "is_required": True,
                },
                {
                    "id": 10,
                    "source_field_name": "Loan_Amount",
                    "source_field_mapping": "$.Loan_Amount",
                    "source_field_type": "str",
                    "is_required": True,
                },
                {
                    "id": 11,
                    "source_field_name": "Term",
                    "source_field_mapping": "$.Term",
                    "source_field_type": "str",
                    "is_required": True,
                },
                {
                    "id": 12,
                    "source_field_name": "Credit_History",
                    "source_field_mapping": "$.Credit_History",
                    "source_field_type": "str",  # use python types
                    "is_required": True,
                },
                {
                    "id": 13,
                    "source_field_name": "Area",
                    "source_field_mapping": "$.Area",
                    "source_field_type": "str",
                    "is_required": True,
                }
            ],
            "destination": [
                {
                    "id": 1,
                    "destination_field_name": "Gender",
                    "destination_field_mapping": "$.Gender",
                    "destination_field_type": "str",  # use python types
                    "default_value": "n/a",
                },
                {
                    "id": 2,
                    "destination_field_name": "Married",
                    "destination_field_mapping": "$.Married",
                    "destination_field_type": "str",
                    "default_value": "n/a",
                },
                {
                    "id": 3,
                    "destination_field_name": "Age",
                    "destination_field_mapping": "$.Age",
                    "destination_field_type": "float",  # use python types
                    "default_value": "n/a",
                },
                {
                    "id": 4,
                    "destination_field_name": "Dependents",
                    "destination_field_mapping": "$.Dependents",
                    "destination_field_type": "float",
                    "default_value": 0,
                },
                {
                    "id": 5,
                    "destination_field_name": "Education",
                    "destination_field_mapping": "$.Education",
                    "destination_field_type": "str",  # use python types
                    "default_value": "n/a",
                },
                {
                    "id": 6,
                    "destination_field_name": "Self_Employed",
                    "destination_field_mapping": "$.Self_Employed",
                    "destination_field_type": "str",
                    "default_value": "n/a",
                },
                {
                    "id": 7,
                    "destination_field_name": "Applicant_Income",
                    "destination_field_mapping": "$.Applicant_Income",
                    "destination_field_type": "float",  # use python types
                    "default_value": 0,
                },
                {
                    "id": 8,
                    "destination_field_name": "Coapplicant_Income",
                    "destination_field_mapping": "$.Coapplicant_Income",
                    "destination_field_type": "float",
                    "default_value": 0,
                },
                {
                    "id": 9,
                    "destination_field_name": "Load_Date",
                    "destination_field_mapping": "$.Load_Date",
                    "destination_field_type": "str",  # use python types
                    "default_value": "n/a",
                },
                {
                    "id": 10,
                    "destination_field_name": "Loan_Amount",
                    "destination_field_mapping": "$.Loan_Amount",
                    "destination_field_type": "float",
                    "default_value": 0,
                },
                {
                    "id": 11,
                    "destination_field_name": "Term",
                    "destination_field_mapping": "$.Term",
                    "destination_field_type": "float",
                    "default_value": "n/a",
                },
                {
                    "id": 12,
                    "destination_field_name": "Credit_History",
                    "destination_field_mapping": "$.Credit_History",
                    "destination_field_type": "int",  # use python types
                    "default_value": 0,
                },
                {
                    "id": 13,
                    "destination_field_name": "Area",
                    "destination_field_mapping": "$.Area",
                    "destination_field_type": "str",
                    "default_value": "n/a",
                }
            ],
            "transform": [# using the Enums
                {
                    "id": 1,
                    "transform_mask": 'CAPITAL_LETTER'
                },
                {
                    "id": 2,
                    "transform_mask": 'CAPITAL_LETTER'
                },
                {
                    "id": 5,
                    "transform_mask": 'CAPITAL_LETTER'
                },
                {
                    "id": 6,
                    "transform_mask": 'CAPITAL_LETTER'
                },
                {
                    "id": 13,
                    "transform_mask": 'CAPITAL_LETTER'
                }
            ],
            "mapping": [
                {
                    "id": 1,
                    "mapping_source": 1,
                    "mapping_destination": 1,
                    "mapping_transform": 1
                },
                {
                    "id": 2,
                    "mapping_source": 2,
                    "mapping_destination": 2,
                    "mapping_transform": 2
                },
                {
                    "id": 3,
                    "mapping_source": 3,
                    "mapping_destination": 3,
                },
                {
                    "id": 4,
                    "mapping_source": 4,
                    "mapping_destination": 4,
                },
                {
                    "id": 5,
                    "mapping_source": 5,
                    "mapping_destination": 5,
                    "mapping_transform": 5
                },
                {
                    "id": 6,
                    "mapping_source": 6,
                    "mapping_destination": 6,
                    "mapping_transform": 6
                },
                {
                    "id": 7,
                    "mapping_source": 7,
                    "mapping_destination": 7,
                },
                {
                    "id": 8,
                    "mapping_source": 8,
                    "mapping_destination": 8,
                },
                {
                    "id": 9,
                    "mapping_source": 9,
                    "mapping_destination": 9,
                },
                {
                    "id": 10,
                    "mapping_source": 10,
                    "mapping_destination": 10,
                },
                {
                    "id": 11,
                    "mapping_source": 11,
                    "mapping_destination": 11,
                },
                {
                    "id": 12,
                    "mapping_source": 12,
                    "mapping_destination": 12,
                },
                {
                    "id": 13,
                    "mapping_source": 13,
                    "mapping_destination": 13,
                    "mapping_transform": 13
                }
            ]
        }
