import logging
from typing import List, Optional

from fast_downward.driver.main import main

import os

_KEY = "FD_MAX_SEARCH_TIME_SECONDS"
if _KEY not in os.environ:
    raise ValueError(f"Environment variable {_KEY} not specified! ")

_FD_MAX_SEARCH_TIME = int(os.environ[_KEY])

# Use LMCut as it is quicker
_DEFAULT_OPTS = ["--search", f"astar(lmcut(), max_time={_FD_MAX_SEARCH_TIME})"]

_log = logging.getLogger(__name__)


def get_optimal_actions(domain_pddl, problem_pddl) -> Optional[List[str]]:
    """
    Runs Fast Downward to get the optimal plan
    :param domain_pddl:
    :param problem_pddl:
    :return: List[str] with action names
    """
    exit_code = main(argv=[domain_pddl, problem_pddl] + _DEFAULT_OPTS)

    if exit_code == 12:
        _log.error(
            f"Search incomplete for {domain_pddl}, {problem_pddl} within {_FD_MAX_SEARCH_TIME}s"
        )
        return None
    elif exit_code != 0:
        raise RuntimeError(
            f"Something went wrong, exit code {exit_code} from Fast Downward (http://www.fast-downward.org/ExitCodes)"
        )

    # Read the plan to get actions, remove \n and ignore final cost line
    plan = open("sas_plan", "r").readlines()
    plan = [line[:-1] for line in plan if line.startswith("(") and line.endswith(")\n")]

    # Remove the plan
    os.remove("sas_plan")
    return plan
