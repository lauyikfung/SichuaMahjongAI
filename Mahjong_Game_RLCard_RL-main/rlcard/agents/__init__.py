import subprocess
import sys
from distutils.version import LooseVersion

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

if 'torch' in installed_packages:
    from rlcard.agents.dqn_agent import DQNAgent as DQNAgent
    from rlcard.agents.nfsp_agent import NFSPAgent as NFSPAgent

from rlcard.agents.cfr_agent import CFRAgent
from rlcard.agents.random_agent import RandomAgent
