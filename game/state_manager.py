class StateManager:
    def __init__(self):
        self.states = {}
        self.current = None

        self.play_state = None  # ← store active game

    def add(self, name, factory):
        self.states[name] = factory

    def set_state(self, name):
        self.current = self.states[name]()

        # rebuild menu buttons when entering menu
        if name == "menu":
            self.current.build_buttons()

    def set_play_state(self, play_state):
        self.play_state = play_state
        self.current = play_state

    def continue_game(self):
        if self.play_state:
            self.current = self.play_state

    def has_active_game(self):
        return self.play_state is not None

    def clear_game(self):
        self.play_state = None

    def handle_events(self, events):
        self.current.handle_events(events)

    def update(self):
        self.current.update()

    def draw(self, screen, clock):
        self.current.draw(screen, clock)