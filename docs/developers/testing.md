Running Armory Tests
=========================

# Core Testing
Tests have to download a bunch of code (external repos,etc.) and model weights the first
time around so that one can take a while.  

You will need to have the `ARMORY_GITHUB_TOKEN` env variable set (which may be done by 
armory configure...but will need to make sure)

Can use pytest -s to run all tests:
```bash
pytest -s ./tests/`
```

To only run a single file:
```bash
pytest -s ./tests/test_file.py
```
or to run only a single tests
```bash
pytest -s ./tests/test_file.py::test_name
```

If a test is parameterized to see how to only run one of the 
parameters sets use:
```bash
pytest --collect-only -q 
```
Then run the one you want (for example):
```bash
 pytest -s tests/test_models.py::test_model_creation[armory.baseline_models.pytorch.cifar-get_art_model-None-cifar10-500-1-1-100-1-numpy-0.25]
```

# Experimental Testing (Old Dependencies)
Many Armory users have outside constraints that require the use of older dependencies
(e.g. Docker version, CUDA versions, etc.) which are not directly supported by Armory
developers.  The following is intended to provide some support for how to go about 
testing these environments, however mileage may vary.

## Running Armory with older Docker versions
Armory currently depends on Docker >= 19.03.1 however many users require using an older
version.  The trouble comes with the interactions between `nvidia-container-runtime` and
`nvidia-container-toolkit`.  For more detailed discussion see [Armory Issue #157](https://github.com/twosixlabs/armory/issues/157).

To test whether you setup will work properly, the following steps may be useful.

First, make sure you have an appropriate docker environment setup, for details see 
[https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)
Next you will need to have armory installed.  For details on this see: [Armory README](../../README.md).

Next, try to run the [cifar_10_baseline.json](../../scenario_configs/cifar10_baseline.json) with:
```bash
armory run cifar10_baseline.json --use-gpu --gpu all --check
```
Note, you will want to monitor the gpu utilization using `nvidia-smi` to make sure the 
evaluation is actually utilizing the GPU(s).  If that is successful and the gpus were
utilized then you are off to the races.  
