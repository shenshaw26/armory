# from pydantic import BaseModel
from armory.logs import log
import os
import yaml
import json
from armory.utils import parse_overrides
from importlib import import_module
from dataclasses import dataclass


# TODO: Figure out appropriate defaults
# TODO: Change Attribute names
#  - `name` -> function_name
#  - kwargs??
#  -
@dataclass
class AttackParameters:
    """Armory Data Class for `Attack` Parameters"""

    name: str
    module: str
    knowledge: str
    kwargs: dict
    targeted: bool = False
    targeted_labels: dict = None
    use_adversarial_trainer: bool = False
    sweep_params: dict = None
    generate_kwargs: dict = None
    use_label: bool = False
    type: str = None


@dataclass
class DatasetParameters:
    """Armory Dataclass For `Dataset` Parameters"""

    name: str
    module: str
    framework: str
    batch_size: int
    kwargs: dict = None
    eval_split: str = None
    train_split: str = None


@dataclass
class DefenseParameters:
    """Armory Dataclass for `Defense` Parameters"""

    name: str
    module: str
    kwargs: dict
    type: str = None
    data_augmentation: dict = None


@dataclass
class MetricParameters:
    """Armory Dataclass for Evaluation `Metric` Parameters"""

    means: bool
    perturbation: str
    record_metric_per_sample: bool
    task: list


@dataclass
class ModelParameters:
    """Armory Dataclass for `Model` Parameters"""

    name: str
    module: str
    wrapper_kwargs: dict
    model_kwargs: dict
    fit_kwargs: dict
    fit: bool
    weights_file: str = None
    predict_kwargs: dict = None


@dataclass
class ScenarioParameters:
    """Armory Dataclass for `Scenario` Parameters"""

    name: str
    module: str
    kwargs: dict
    export_samples: int = None


# TODO: restructure experiments to use metadata key that
#  contains information like name and description

@dataclass
class ExperimentParameters:
    _description: str
    dataset: DatasetParameters
    model: ModelParameters
    scenario: ScenarioParameters
    adhoc: dict = None
    attack: AttackParameters = None
    defense: DefenseParameters = None
    metric: MetricParameters = None
    # sysconfig: SystemConfigurationParameters = None

    @classmethod
    def load(cls, filename, overrides=[]):
        overrides = parse_overrides(overrides)
        valid_ext = (".aexp", ".json")
        fname, fext = os.path.splitext(filename)
        log.info(f"Attempting to Load Experiment from file: {filename}")
        if fext == ".json":
            with open(filename, "r") as f:
                data = json.loads(f.read())
        elif fext in (".aexp", ".yml", ".yaml"):
            with open(filename, "r") as f:
                data = yaml.safe_load(f.read())
        else:
            raise ValueError(
                f"Experiment File: {filename} has invalid extension....must be in {valid_ext}"
            )

        if "sysconfig" in data:
            env_pars = data["sysconfig"]
            data.pop("sysconfig")
        else:
            env_pars = None

        log.debug(f"Parsing Class Object from: {data}")
        exp = cls(**data)
        return exp, env_pars


class Experiment(object):
    def __init__(self, experiment_parameters, environment_parameters):
        log.info(f"Constructing Experiment using parameters: \n{experiment_parameters}")
        self.exp_pars = experiment_parameters
        self.env_pars = environment_parameters
        log.info(f"Importing Scenario Module: {self.exp_pars.scenario.module_name}")
        self.scenario_module = import_module(self.exp_pars.scenario.module_name)
        log.info(f"Loading Scenario Function: {self.exp_pars.scenario.function_name}")
        self.scenario_fn = getattr(
            self.scenario_module, self.exp_pars.scenario.function_name
        )



# class MetaData(BaseModel):
#     name: str
#     author: str
#     description: str
#
#
# class PoisonParameters(BaseModel):
#     pass

# @dataclass
# class ExperimentParameters:
#     """Armory Dataclass for Experiment Parameters"""
#
#     _meta: MetaData
#     poison: PoisonParameters = None
#     attack: AttackParameters = None
#     dataset: DatasetParameters
#     defense: DefenseParameters = None
#     metric: MetricParameters = None
#     model: ModelParameters
#     scenario: ScenarioParameters
#     # sysconfig: SystemConfigurationParameters = None
#
#     # def save(self, filename):
#     #     with open(filename, "w") as f:
#     #         f.write(self.json())
#
#     @classmethod
#     def load(cls, filename, overrides=[]):
#         overrides = parse_overrides(overrides)
#         valid_ext = (".aexp", ".json")
#         fname, fext = os.path.splitext(filename)
#         log.info(f"Attempting to Load Experiment from file: {filename}")
#         if fext == ".json":
#             with open(filename, "r") as f:
#                 data = json.loads(f.read())
#         elif fext in (".aexp", ".yml", ".yaml"):
#             with open(filename, "r") as f:
#                 data = yaml.safe_load(f.read())
#         else:
#             raise ValueError(
#                 f"Experiment File: {filename} has invalid extension....must be in {valid_ext}"
#             )
#
#         log.debug(f"Parsing Class Object from: {data}")
#         exp = cls.parse_obj(data)
#         # Getting Environment Overrides from File (if available)
#         if "environment" in data:
#             file_overrides = parse_overrides(data["environment"])
#         else:
#             file_overrides = []
#
#         return exp, file_overrides
#
#
# class Experiment(object):
#     """Execution Class to `run` armory experiments
#
#     """
#
#     def __init__(self, experiment_parameters, environment_parameters):
#         log.info(f"Constructing Experiment using parameters: \n{experiment_parameters}")
#         self.exp_pars = experiment_parameters
#         self.env_pars = environment_parameters
#         log.info(f"Importing Scenario Module: {self.exp_pars.scenario.module_name}")
#         self.scenario_module = import_module(self.exp_pars.scenario.module_name)
#         log.info(f"Loading Scenario Function: {self.exp_pars.scenario.function_name}")
#         self.scenario_fn = getattr(
#             self.scenario_module, self.exp_pars.scenario.function_name
#         )
