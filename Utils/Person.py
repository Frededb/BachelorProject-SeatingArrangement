class Person:
    def __init__(self, initials, studyprogram, year, preferences = [], avoidances = []):
        self.initials = initials
        self.studyprogram = studyprogram
        self.year = year
        self.preferences = preferences
        self.avoidances = avoidances
        self.coords = []