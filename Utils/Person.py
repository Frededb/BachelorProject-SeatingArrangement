class Person:
    def __init__(self, person_id, atributes = None, atribute_set = None):
        self.id = person_id
        # Keep `name` as alias so existing utility code can still identify people.
        self.name = person_id
        self.atributes = [] if atributes is None else atributes
        self.atribute_set = [] if atribute_set is None else atribute_set

        # Temporary compatibility fields for modules not yet migrated.
        self.preferences = set()
        self.avoidances = set()
    def __str__(self) -> str:
        return f"{self.id}"
    def __repr__(self) -> str:
        return self.__str__()
    def __lt__(self, other):
        return self.id < other.id
