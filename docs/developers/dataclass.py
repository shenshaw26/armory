#%%

from enum import Enum
from dataclasses import dataclass
from pprint import pprint
import yaml


class Mode(Enum):
    native = "native"
    host = "host"


@dataclass
class DataSplit:
    train: int
    test: int


@dataclass
class Dataset:
    name: str
    split: DataSplit
    batch: int


@dataclass
class Experiment:
    description: str
    dataset: Dataset
    attack_module: str
    batches: int = 1


@dataclass
class Environment:
    mode: Mode = Mode.native
    gpus: str = "all"


def loadit():
    ds = Dataset(name="cifar10", split=DataSplit(train=45000, test=5000), batch=128)
    env = Environment()
    exp = Experiment(
        description="cifar experiment",
        dataset=ds,
        attack_module="art.attack.evasion",
        batches=5,
    )
    return (env, exp)


env, exp = loadit()
pprint(exp.asdict())
