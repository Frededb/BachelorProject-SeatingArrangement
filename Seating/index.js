import {Person} from './Person.js';
import {Table} from './Table.js';
import {Formation} from "./Formation.js";

let time = Date.now();

let worstFormation = null;
let worstValue = Infinity;
let bestFormation = null;
let bestValue = -Infinity;
let avgValue = 0;
let countPermutations = 0;

let emptyPerson = new Person("Empty", "None", 0);

let persons = [];
persons.push(new Person("Lisa", "SWU", 2023, ["fbuu"], ["D2"]));
persons.push(new Person("D1", "DS", 2023, ["D2"]));
persons.push(new Person("D2", "DS", 2023, ["D1"]));
persons.push(new Person("aubu", "SWU", 2023, ["fbuu", "Lisa", "M"]));
persons.push(new Person("M", "SWU", 2024));
persons.push(new Person("fbuu", "SWU", 2023, ["Lisa", "aubu"]));


persons.push(new Person("Alex", "SWU", 2021, ["Ben", "Cara"]));
persons.push(new Person("Ben", "DS", 2022));
persons.push(new Person("Cara", "GBI", 2023, ["Diana"]));
persons.push(new Person("Diana", "SWU", 2024, ["Eli"], ["Fay"]));

let tableSizes = [6, 4];
let totalTableSeats = tableSizes.reduce((a, b) => a + b, 0);
let emptySeats = totalTableSeats - persons.length;
for (let i = 0; i < emptySeats; i++) {
    persons.push(emptyPerson);
}
calculateAllPermutations(persons);

function calculateAllPermutations(persons) {
    const used = new Array(persons.length).fill(false);

    function backtrack(path) {
        if (path.length === persons.length) {
            calculatePermutation(path.slice());
            countPermutations++;
            return;
        }
        for (let i = 0; i < persons.length; i++) {
            if (used[i]) continue;
            used[i] = true;
            path.push(persons[i]);
            backtrack(path);
            path.pop();
            used[i] = false;
        }
    }

    backtrack([]);
}



function calculatePermutation ( permutedPersons ) {

    if(countPermutations % 1000000 === 0) {
        console.log("Calculating permutation number:", countPermutations);
    }

    let tables = [];
    let personIndex = 0;
    for (let size of tableSizes) {
        let tablePersons = permutedPersons.slice(personIndex, personIndex + size);
        let table = new Table(tablePersons);
        tables.push(table);
        personIndex += size;
    }
    let formation = new Formation(tables);
    let value = formation.value;

    avgValue += value;
    if (value < worstValue) {
        worstFormation = formation;
        worstValue = value;
    }
    if (value > bestValue) {
        bestFormation = formation;
        bestValue = value;
    }
}

avgValue /= countPermutations;
console.log("Calculated formations: ", countPermutations);
console.log("Average formation value:", avgValue);
console.log();
console.log("Worst formation arrangement: ");
worstFormation.printFormation()
console.log("Best formation arrangement: ");
bestFormation.printFormation()

console.log("Total calculation time (ms): ", Date.now() - time);