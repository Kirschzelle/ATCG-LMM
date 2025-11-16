import constants as c
import llm.knowledge as knw

class ChatLog():
    def __init__(self):
        self.cl = []

    def add_message(self, sender, message):
        self.cl.append((sender, message))

    def clear_chat_log(self):
        self.cl.clear()

    def get_message(self, person : knw.Person):
        prompt = f"{person.system_message}\n\n"
    
        if self.cl:
            prompt += "Conversation so far:\n"
            for (sender, message) in self.cl:
                prompt += f'{sender}: "{message}"\n'
            prompt += "\n"
        
        prompt += f'CRITICAL INSTRUCTION: Reply with EXACTLY ONE SHORT SENTENCE of dialogue only.\n\n'\
              f'What to include: ONLY the words {person.name} speaks out loud\n'\
              f'What to EXCLUDE: descriptions, actions, thoughts, narration, context\n'\
              f'Length: 10-15 words maximum\n\n'\
              f'Repetition: Do not repeat anything already said!\n\n'\
              f'WRONG: {person.name}: *smirks* "I disagree" *crosses arms*\n'\
              f'WRONG: {person.name}: "I disagree with this proposal for many reasons..."\n'\
              f'CORRECT: {person.name}: "I disagree."\n'\
              f'CORRECT: {person.name}: "This is foolish."\n\n'
                
        return prompt
    
    def get_king_verdict(self, king : knw.Person, proposal):
        prompt = f"{king.system_message}\n\n"
        
        prompt += f"Proposal being discussed: {proposal}\n\n"
        
        if self.cl:
            prompt += "Council discussion:\n"
            for (sender, message) in self.cl:
                prompt += f'{sender}: "{message}"\n'
            prompt += "\n"
        
        prompt += f'CRITICAL: As {king.name}, you must now make your FINAL DECISION.\n\n'\
            f'You MUST respond in this EXACT format:\n'\
            f'{king.name}: "ACCEPT - [one short sentence]"\n'\
            f'OR\n'\
            f'{king.name}: "REJECT - [one short sentence]"\n\n'\
            f'RULES:\n'\
            f'- Start with ONLY "ACCEPT" or "REJECT"\n'\
            f'- Follow with a dash and ONE brief reason (10-15 words)\n'\
            f'- NO descriptions, NO actions, NO additional commentary\n'\
            f'- Just the decision and reasoning\n\n'\
            f'WRONG: {king.name}: "After careful consideration, I have decided to ACCEPT this proposal because..."\n'\
            f'CORRECT: {king.name}: "ACCEPT - The treasury requires replenishment."\n'\
            f'CORRECT: {king.name}: "REJECT - This burdens the people too greatly."\n\n'\
        
        return prompt
    
    def get_message_count(self):
        return len(self.cl)

    def get_speaker_count(self):
        return len(set(sender for sender, message in self.cl))