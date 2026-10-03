import subprocess
import sys


def run_module(*args):
    return subprocess.run(
        [sys.executable, "-m", "toolkit", *args],
        text=True,
        timeout=10,
        check=False
    )

def test_help_return_code():
    assert run_module("--help").returncode == 0
    assert run_module("calc", "--help").returncode == 0
    assert run_module("convert", "--help").returncode == 0

def test_success_return_code():
    assert run_module("calc", "2 + 2").returncode == 0
    assert run_module("convert", "10", "--from", "m", "--to", "km").returncode == 0

def test_error_return_code():
    assert run_module("calc").returncode == 2
    assert run_module("convert", "2").returncode == 2
    assert run_module("convert", "--from", "C", "--to", "K").returncode == 2