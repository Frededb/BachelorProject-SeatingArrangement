export class Formation {
    constructor(tables) {
        this.tables = tables;
        this.value = this.calculateFormationValue();
    }

    calculateFormationValue() {
        let totalValue = 0;
        for (let table of this.tables) {
            totalValue += table.value;
        }
        return totalValue;
    }

    printFormation() {
        console.log("Formation total value:", Number(this.value).toFixed(2));
        for (let table of this.tables) {
            table.printTable();
        }
        console.log();
    }
}