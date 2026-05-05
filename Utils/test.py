import os
import sys
import json
import time
from pathlib import Path
from typing import cast

# Ensure the repository root is importable when this file is run directly.
PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from generateData import generateData
from Algorithms.Build.RandomPlacement import randomPlacement
from Algorithms.Optimizing.RandomSwitch import randomSwitch
from Utils.UtilFunctions import makeEmptyArrangement
from Utils.printer import printArrangementWithValues
from Utils.ValueCalc import calcArrangement
from Utils.reader import readPeople, parsePeople



attribute_set_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../Inputs", "defaultAttributeSet.json")
with open(attribute_set_file, encoding="utf-8") as f:
    attribute_set_data = json.load(f)
attribute_set = attribute_set_data.get("attribute_set", []) if isinstance(attribute_set_data, dict) else []

testInput = generateData(300, cohesion=85)
testInput = parsePeople({"people": testInput}, attribute_set)
initial_arrangement = makeEmptyArrangement(len(testInput), 8)
a = randomPlacement(testInput, initial_arrangement)
start = time.perf_counter()
a = randomSwitch(a)
runtime = time.perf_counter() - start

print("Arrangement score:", calcArrangement(a)[0])
print(f"Runtime: {runtime:.2f}s")
# printArrangementWithValues(a)