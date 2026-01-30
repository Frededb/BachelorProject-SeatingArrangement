class Person:
    def __init__(self, initials, studyprogram, year, preferences = [], avoidances = []):
        self.name = initials
        self.studyprogram = studyprogram
        self.year = year
        self.preferences = preferences
        self.avoidances = avoidances