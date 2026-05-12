import sys
import os
# Ensure project root is on sys.path for imports when running test directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Algorithms.Optimizing.Anealing import annealing
from Utils.reader import parsePeople
from Utils.UtilFunctions import makeEmptyArrangement

# Minimal synthetic input: 8-seat table with 8 people so calcArrangement works
people_input = {
    "people": [
        {"id": "A", "attributes": [["x"], ["y"]]},
        {"id": "B", "attributes": [["x"], ["z"]]},
        {"id": "C", "attributes": [["a"], ["y"]]},
        {"id": "D", "attributes": [["b"], ["z"]]},
        {"id": "E", "attributes": [["x"], ["y"]]},
        {"id": "F", "attributes": [["a"], ["z"]]},
        {"id": "G", "attributes": [["b"], ["y"]]},
        {"id": "H", "attributes": [["x"], ["z"]]}
    ]
}
attribute_set = [
    {"index": 0, "header": "studyprogram", "kind": "traits", "weight": 3},
    {"index": 1, "header": "year", "kind": "prefence", "weight": 1}
]

people = parsePeople(people_input, attribute_set)
arr = makeEmptyArrangement(len(people), 8)
# Fill arrangement sequentially
for i, person in enumerate(people):
    arr[0][i] = person

score_tracker = [0.0]
# Run annealing with small iteration budget but deterministic seed
result = annealing(arr, k=200, seed=42, max_seconds=2, score_tracker=score_tracker)
# Instead compute via function import
from Utils.ValueCalc import calcArrangement
final_value = calcArrangement(result)[0]
print("score_tracker (best observed):", score_tracker[0])
print("final returned score:", final_value)
print("best difference:", round(score_tracker[0] - final_value, 4))



