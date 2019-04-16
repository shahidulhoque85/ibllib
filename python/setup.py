from setuptools import setup, find_packages
import sys
from pathlib import Path

CURRENT_DIRECTORY = Path(__file__).parent.absolute()

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of idtrackerai requires Python {}.{}, but you're trying to
install it on Python {}.{}.
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)

with open(CURRENT_DIRECTORY.parent / "README.md", 'r') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    require = [x.strip() for x in f.readlines()]

setup(
    name='ibllib',
    version='0.4.35rc0',
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    description='IBL libraries',
    license="MIT",
    long_description=long_description,
    author='IBL Staff',
    url="https://www.internationalbrainlab.com/",
    packages=find_packages(exclude=['scratch']),  # same as name
    # external packages as dependencies
    install_requires=require,
    scripts={
        'alf/transfer_rig_data.py',
        'alf/one_iblrig.py',
        'alf/purge_rig_data.py',
    }
)
