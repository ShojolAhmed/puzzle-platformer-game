from level.level_loader import load_level


class LevelManager:
    LEVELS = [
        "maps/testMap.tmx",
        "maps/level2.tmx",
        "maps/level3.tmx"
    ]

    def __init__(self):
        self.current_level = 0
        self.data = load_level(self.LEVELS[self.current_level])

    def reload(self):
        self.data = load_level(self.LEVELS[self.current_level])

    def next_level(self):
        self.current_level += 1

        if self.current_level >= len(self.LEVELS):
            return False

        self.data = load_level(self.LEVELS[self.current_level])
        return True