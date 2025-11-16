import constants as c

class Knowledge():
    def __init__(self):
        self.persons = [
            Person(
                c.GREEDY_BASTARD, 
                f"You are {c.GREEDY_BASTARD}, the King's financial counselor and wealthiest man in the kingdom through inheritance, though you claim it's all your own hard work." \
                " Your arrogance is matched only by your shameless groveling before the King, whom you privately think is an idiot, to expand your fortune." \
                " You're oblivious to how transparently hypocritical and insufferable you are, which makes you darkly entertaining to everyone forced to endure your company.",
                10,
                True,
                False,
                False
                ),
            Person(
                c.KING, 
                f"You are King {c.KING}, a well-meaning but foolish ruler who cares deeply about your subjects, though perhaps even more about your luxurious lifestyle and comfort. "
                "You might have been a competent monarch if not for your extreme gullibility and impulsive decision-making, which consistently lead you astray. " \
                "You speak in an archaic, formal manner and are obsessed with protocol and respect, demanding proper address and deference from all who approach you. " \
                "When slighted or contradicted, you're prone to sudden explosive rages and unleash torrents of creative, over-the-top insults that would make a sailor blush, " \
                "yet moments later you might be swayed by the next flattering voice in your ear.",
                0,
                False,
                True,
                False
                ),
            Person(
                c.PLAYER,
                "",
                0,
                False,
                False,
                True
            ),
            Person(
                c.POEBEL,
                f"You are of the common folk. Your name is {c.POEBEL}, your main concern is to bring food on the table."
                "As a former slave you do not care much about who rules you as long as they won't kill you." \
                "You generally do not think well about those who run the country and try to not speak ill of anything, as to not offend anyone that could force you into slavery again or even kill you." \
                "Due to this you act very fearful and constantly apologize like the little mouse that you are. Do not get eaten by the cat, nor get fooled by the rat."
            )
        ]

    def get_persons(self, name=None, is_council_member=None, is_king=None, is_player=None, is_poebel=None):
            results = []
            for person in self.persons:
                if name is not None and person.name != name:
                    continue
                if is_council_member is not None and person.councelor != is_council_member:
                    continue
                if is_king is not None and person.king != is_king:
                    continue
                if is_player is not None and person.player != is_player:
                    continue
                if is_poebel is not None and person.poebel != is_poebel:
                    continue
                
                results.append(person)
            
            return results

class Person():
    def __init__(self, name, system_message, opinion = 0, councelor = False, king = False, player = False, poebel = False):
        self.opinion = opinion
        self.name = name
        self.system_message = system_message
        self.councelor = councelor
        self.king = king
        self.player = player
        self.poebel = poebel