import torch
import pytest


# this test is marked xfail because I don't care if it is present or not, I just want to know
# in the pytest summary this appears as X for pass and lower-case x for fail
@pytest.mark.xfail
def test_cuda_present():
    assert torch.cuda.is_available()


@pytest.mark.xfail
def test_cuda_allocation():
    one = torch.randn(1, requires_grad=True, device="cuda")
    assert one.is_cuda

    million = torch.randn(1_000_000, requires_grad=True, device="cuda")
    assert million.is_cuda
