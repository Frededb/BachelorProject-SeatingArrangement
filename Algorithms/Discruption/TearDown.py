from queue import PriorityQueue
import math
import random

from Utils.UtilFunctions import getAllPeople
from Utils.ValueCalc import calcPerson
from Utils.printer import printArrangementWithValues
from Utils.reader import emptyPerson


def _calc_person_theoretical_max(person_a, people, table_size):
    padded_people = people[:]
    while len(padded_people) < table_size:
        padded_people.append(emptyPerson)

    pq = PriorityQueue()
    for i, person_b in enumerate(padded_people):
        person_value = calcPerson([person_a, person_b], 0)
        pq.put((-person_value, i, person_b))

    top = [pq.get()[2] for _ in range(table_size - 1)]

    if table_size == 8:
        perfect_table = [top[0], person_a, top[2], top[5], top[3], top[1], top[4], top[6]]
        return calcPerson(perfect_table, 1)

    perfect_table = [person_a] + top
    return calcPerson(perfect_table, 0)


def TearDown(arrangement):
    print("before:")
    printArrangementWithValues(arrangement)

    table_size = max((len(table) for table in arrangement), default=0)

    all_coords = getAllPeople(arrangement)
    non_empty_coords = [
        (table_i, seat_i)
        for table_i, seat_i in all_coords
        if arrangement[table_i][seat_i].name != "Empty"
    ]

    all_people = [arrangement[table_i][seat_i] for table_i, seat_i in non_empty_coords]

    if not all_people:
        return arrangement

    ranked_people = []
    for table_i, seat_i in non_empty_coords:
        person = arrangement[table_i][seat_i]
        theoretical_max = _calc_person_theoretical_max(person, all_people, table_size)
        actual_score = calcPerson(arrangement[table_i], seat_i)
        ranked_people.append((theoretical_max - actual_score, table_i, seat_i))

    ranked_people.sort(reverse=True, key=lambda item: item[0])

    people_to_remove_count = max(1, math.ceil(len(non_empty_coords) / 3))
    removed_people = []

    for _, table_i, seat_i in ranked_people[:people_to_remove_count]:
        person = arrangement[table_i][seat_i]
        if person.name == "Empty":
            continue
        removed_people.append(person)
        arrangement[table_i][seat_i] = emptyPerson

    tables_to_remove_count = max(1, math.ceil(len(arrangement) / 3))
    selected_tables = random.sample(range(len(arrangement)), tables_to_remove_count)

    for table_i in selected_tables:
        for seat_i in range(len(arrangement[table_i])):
            person = arrangement[table_i][seat_i]
            if person.name == "Empty":
                continue
            removed_people.append(person)
            arrangement[table_i][seat_i] = emptyPerson

    empty_coords = [
        (table_i, seat_i)
        for table_i, seat_i in getAllPeople(arrangement)
        if arrangement[table_i][seat_i].name == "Empty"
    ]

    print("After TearDown:")
    printArrangementWithValues(arrangement)

    random.shuffle(removed_people)
    random.shuffle(empty_coords)

    for person, (table_i, seat_i) in zip(removed_people, empty_coords):
        arrangement[table_i][seat_i] = person

    print("After rebuild:")
    printArrangementWithValues(arrangement)
    return arrangement
