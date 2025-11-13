import random
import llm.knowledge as knw
import llm.llm as llm
import elements.text_box_bundler as tbb

class Eventy:
    def __init__(self, initiator, conditions, initial_message, effects_success, effects_failure, parent):
        self.initiator = initiator
        self.conditions = conditions
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

class World:
    def __init__(self):
        self.all_events = [
            Eventy(

            )
        ]
        self.knowledge = knw.Knowledge()
        self.llm = llm.LLM()
        self.current_event = None

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
        pass # TODO: Implement game over.
    
    def update(self, delta_time, tb_bundler : tbb.TextBoxBundler):
        if self.current_event == None:
            self.current_event = self.pick_random_event()

            if self.current_event == None:
                self.game_over()