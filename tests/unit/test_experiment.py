import pytest

# from armory.experiment import Experiment
import armory.experiment as ae
import glob
import os
import json


@pytest.mark.parametrize(
    "config", glob.glob(os.path.join("./scenario_configs", "*.json"), recursive=True)
)
@pytest.mark.parametrize(
    "key, cls",
    [
        ("attack", ae.AttackParameters),
        ("defense", ae.DefenseParameters),
        ("metric", ae.MetricParameters),
        ("model", ae.ModelParameters),
        ("scenario", ae.ScenarioParameters),
        # ("sysconfig", ae.SystemConfigurationParameters),
    ],
)
def test_all_experiment_parameters(config, key, cls):
    with open(config, "r") as f:
        data = json.loads(f.read())

    if data[key] is not None:
        obj = cls(**data[key])


@pytest.mark.parametrize(
    "config", glob.glob(os.path.join("./scenario_configs", "*.json"), recursive=True)
)
def test_experiment_parameters_load(config):
    exp = ae.ExperimentParameters.load(config)

@pytest.mark.parametrize(
    "config", ["./scenario_configs/no_docker/cifar_short.json"]
)
def test_experiment(config):

