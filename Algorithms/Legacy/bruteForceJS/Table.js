import {SY, S, P, A} from "./constants.js";

export class Table {
    constructor(persons) {
        this.persons = persons;
        this.length = persons.length / 2;
        // Assign coordinates based on index
        for (let i = 0; i < persons.length; i++) {
            persons[i].coords = [i % this.length, Math.floor(i / this.length)];
        }
        this.value = this.calculateTableValue();
    }

    getDistanceTo(personA, personB) {
        return Math.sqrt(Math.pow(personA.coords[0] - personB.coords[0], 2) + Math.pow(personA.coords[1] - personB.coords[1], 2));
    }

    calculatePersonValue(person) {
        let totalValue = 0;
        for (let otherPerson of this.persons) {
            if (person === otherPerson || person.name === "Empty" || otherPerson.name === "Empty") {
                continue; // Skip self and empty persons
            }
            const d = this.getDistanceTo(person, otherPerson);
            if (person.studyprogram === otherPerson.studyprogram && person.year === otherPerson.year) {
                totalValue += SY/d; // Same study program and year
            }
            if (person.studyprogram === otherPerson.studyprogram) {
                totalValue += S/d; // Same study program
            }
            if (person.preferences.includes(otherPerson.initials)) {
                totalValue += P/d; // Preferences
            }
            if (person.avoidances.includes(otherPerson.initials)) {
                totalValue += A/d; // Avoidances
            }
        }
        return totalValue;
    }

    calculateTableValue() {
        let totalValue = 0;
        for (let person of this.persons) {
            totalValue += this.calculatePersonValue(person);
        }
        return totalValue;
    }

    printTable() {
        console.log("Table with value:", Number(this.value).toFixed(2));
        const initials = this.persons.map(p => p.initials);
        console.log(initials.slice(0, this.length).join(' '));
        console.log(initials.slice(this.length).join(' '));
        console.log();
    }
}