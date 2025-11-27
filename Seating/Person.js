export class  Person{
    constructor(initials, studyprogram, year, preferences = [], avoidances = []) {
        this.initials = initials;
        this.studyprogram = studyprogram;
        this.year = year;
        this.preferences = preferences;
        this.avoidances = avoidances;
        this.coords = [];
    }
}