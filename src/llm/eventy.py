import random
import llm.knowledge as knw
import llm.llm as llm
import elements.text_box_bundler as tbb
import core.chat_log as cl
import constants as c
import re

class Eventy:
    def __init__(self, initiator, conditions, initial_message, porposal_system_message, effects_success, effects_failure, parent):
        self.initiator = initiator
        self.conditions = conditions
        self.porposal_system_message = porposal_system_message
        self.initial_message = initial_message
        self.effects_success = effects_success
        self.effects_failure = effects_failure
        self.parent = parent

    def conditions_met(self):
        return self.conditions()
    
    def success(self):
        self.effects_success()
        self._remove()

    def failure(self):
        self.effects_failure()
        self._remove()

    def _remove(self):
        self.parent.all_events.remove(self)
        self.parent.message_cd = c.MESSAGE_CD * 4
        self.parent.message_pending = False

class World:
    def __init__(self, tb_bundler : tbb.TextBoxBundler):
        self.all_events = [
            Eventy(
                c.KING,
                self._always_true,
                "Hark, mine subjects! Should We not erect a statue of Our royal self for all the kingdom to behold?",
                "Should a grand statue of the King be built?",
                self._on_success_statue,
                self._on_failure_statue,
                self
            ),
            Eventy(
                c.KING,
                self._always_true,
                f"Heed the, I am bored. How about we behead {c.PLAYER} for our our personal enjoyment?",
                f"Should the advisor {c.PLAYER} be killed?",
                self._on_success_player_beheading,
                self._on_failure_player_beheading,
                self
            ),
            Eventy(
                c.REVOLT,
                self._always_true,
                "Your Majesty, the neighboring kingdom has rallied its armies. All signs point toward war. How shall we respond?",
                f"Should the King prepare for the war?",
                self._on_success_war,
                self._on_failure_war,
                self
            )
        ]
        self.knowledge = knw.Knowledge()
        self.llm = llm.LLM()
        self.current_event = None
        self.cl = cl.ChatLog()
        self.message_cd = 0
        self.message_pending = False
        self.limit = 5
        self.tbb = tb_bundler
        self.failed = False

    ### Event functions

    def _always_true(self):
        return True
    
    def _on_success_statue(self):
        for person in self.knowledge.get_persons(is_poebel=True):
            person.opinion *= 1.25

        for person in self.knowledge.get_persons(is_king=True):
            person.opinion += 5

    def _on_failure_statue(self):
        for person in self.knowledge.get_persons(is_king=True):
            person.opinion -= 15

    def _on_success_player_beheading(self):
        for person in self.knowledge.get_persons(is_king=True):
            person.opinion += 5

    def _on_failure_player_beheading(self):
        self.game_over()

    def _on_success_war(self):
        for person in self.knowledge.get_persons(is_king=True):
            person.opinion += 50

        for person in self.knowledge.get_persons(is_council_member=True):
            person.opinion += 50

    def _on_failure_war(self):
        self.game_over()    

    ### Actual class

    def pick_random_event(self):
        events = []
        for event in self.all_events:
            if event.conditions_met():
                events.append(event)

        if len(events) > 0:
            index = random.randint(0, len(events)-1)
            return events[index]
        
        return None
    
    def game_over(self):
        self.failed = True
    
    def update(self, delta_time):
        if self.current_event == None:
            self.current_event = self.pick_random_event()

            if self.current_event == None:
                self.game_over()
                return
            
            self.cl.clear_chat_log()
            self.cl.add_message(self.current_event.initiator, self.current_event.initial_message)
            self.tbb.add_message(self.current_event.initiator, self.current_event.initial_message)

            self.continue_dialogue()

        if self.message_cd < 0 and not self.message_pending:
            unique_senders = self.cl.get_speaker_count()
            message_amount = self.cl.get_message_count()
            index = random.randint(0,unique_senders*2+message_amount)
            if index > self.limit:
                self.limit += 2
                self.prompt_decision()
            else:
                self.continue_dialogue()

        self.message_cd -= delta_time

    def prompt_decision(self):
        king = self.knowledge.get_persons(is_king=True)
        prompt = self.cl.get_king_verdict(king[0], self.current_event.porposal_system_message) # type: ignore
        self.message_pending = True
        self.llm.get_response(prompt, self.decision_finished)

    def continue_dialogue(self):
        persons = self.knowledge.get_persons(is_player=False)
        index = random.randint(0,len(persons)-1)
        prompt = self.cl.get_message(persons[index])
        self.message_pending = True
        self.message_cd = c.MESSAGE_CD
        self.llm.get_response(prompt, self.prompt_finished)
            
    def prompt_finished(self, text):
        sender, message = parse_response(text)
        if self.check_legal_response(sender, message):
            self.cl.add_message(sender, message)
            self.tbb.add_message(sender, message)

        self.message_pending = False

    def decision_finished(self, text):
        sender, accepted, reasoning = parse_king_verdict(text)
        if accepted == None:
            self.prompt_decision()
            return
        if accepted:
            self.current_event.effects_success() # type: ignore
        else:
            self.current_event.effects_failure() # type: ignore
        self.tbb.add_message(sender, reasoning)
        self.all_events.remove(self.current_event)
        self.current_event = None
        self.message_pending = False

    def check_legal_response(self, sender, message) -> bool:
        if len(self.knowledge.get_persons(name=sender)) == 1 and message is not None and message != "":
            return True
        return False

def parse_response(response):
    pattern = r'([A-Z][a-zA-Z]+)\s*:\s*"([^"]+)"'
    match = re.search(pattern, response)
    
    if match:
        sender = match.group(1)
        message = match.group(2)
        return sender, message
    
    pattern_no_quotes = r'([A-Z][a-zA-Z]+)\s*:\s*(.+?)(?:\n|$)'
    match = re.search(pattern_no_quotes, response)
    
    if match:
        sender = match.group(1)
        message = match.group(2).strip()
        return sender, message
    
    return None, None

def parse_king_verdict(response):
    pattern = r'([A-Z][a-zA-Z]+)\s*:\s*"?(ACCEPT|REJECT)\s*-\s*([^"]+)"?'
    match = re.search(pattern, response, re.IGNORECASE)
    
    if match:
        sender = match.group(1)
        decision = match.group(2).upper()
        reasoning = match.group(3).strip()
        accepted = (decision == 'ACCEPT')
        return sender, accepted, reasoning
    
    colon_index = response.rfind(':')
    if colon_index == -1:
        if 'ACCEPT' in response.upper():
            return None, True, response.strip()
        elif 'REJECT' in response.upper():
            return None, False, response.strip()
        return None, None, response.strip()
    
    sender = response[:colon_index].strip()
    rest = response[colon_index + 1:].strip()
    
    if rest.startswith('"') and rest.endswith('"'):
        message = rest[1:-1]
    elif rest.startswith('"'):
        message = rest[1:]
    else:
        message = rest
    
    message_upper = message.upper()
    
    if message_upper.startswith('ACCEPT'):
        accepted = True
        reasoning = message[6:].strip()
    elif message_upper.startswith('REJECT'):
        accepted = False
        reasoning = message[6:].strip()
    elif 'ACCEPT' in message_upper:
        accepted = True
        reasoning = message
    elif 'REJECT' in message_upper:
        accepted = False
        reasoning = message
    else:
        accepted = None
        reasoning = message
    
    if reasoning.startswith('-'):
        reasoning = reasoning[1:].strip()
    
    return sender, accepted, reasoning