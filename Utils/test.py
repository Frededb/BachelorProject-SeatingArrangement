import os
import sys
import json
from pathlib import Path
from typing import cast

# Ensure the repository root is importable when this file is run directly.
PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from Algorithms.Build.RandomPlacement import RandomPlacement
from Utils.UtilFunctions import makeEmptyArrangement
from Utils.printer import printArrangementWithValues
from Utils.reader import readPeople



testInput = readPeople("./Inputs/input100People.json", "./Inputs/defaultAttributeSet.json")
initial_arrangement = makeEmptyArrangement(len(testInput), 8)
a = RandomPlacement(testInput, initial_arrangement)


printArrangementWithValues(a)