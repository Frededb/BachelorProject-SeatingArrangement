class Person:
    def __init__(self, name, studyprogram, year, preferences = [], avoidances = []):
        self.name = name
        self.studyprogram = studyprogram
        self.year = year
        self.preferences = preferences
        self.avoidances = avoidances
    def __str__(self) -> str:
        return f"{self.name}"
    def __repr__(self) -> str:
        return self.__str__()
    def __lt__(self, other):
        return self.name < other.name