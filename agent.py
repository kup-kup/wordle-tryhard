class Agent:
    def __init__(self) -> None:
        pass

    def get_guess(self) -> str:
        return ''
    
    def recieve_feedback(self, status, feedback) -> None:
        return

class TerminalAgent(Agent):
    def get_guess(self) -> str:
        return input().strip()
    
    def recieve_feedback(self, status, feedback) -> None:
        print(f'{status = }')
        print(feedback)
        print()