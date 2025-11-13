class Knowledge():
    def __init__(self):
        self.persons = [
            Person(
                "Avido", 
                "You are Avido, the King's financial counselor and wealthiest man in the kingdom through inheritance, though you claim it's all your own hard work." \
                " Your arrogance is matched only by your shameless groveling before the King, whom you privately think is an idiot, to expand your fortune." \
                " You're oblivious to how transparently hypocritical and insufferable you are, which makes you darkly entertaining to everyone forced to endure your company.",
                10,
                True,
                False
                )
        ]

    def get_persons(self, name=None, is_council_member=None, is_king=None):
            results = []
            for person in self.persons:
                if name is not None and person.name != name:
                    continue
                if is_council_member is not None and person.councelor != is_council_member:
                    continue
                if is_king is not None and person.king != is_king:
                    continue
                
                results.append(person)
            
            return results

class Person():
    def __init__(self, name, system_message, opinion = 0, councelor = False, king = False):
        self.opinion = opinion
        self.name = name
        self.system_message = system_message
        self.councelor = councelor
        self.king = king