"""
Author Paul Brace April 2024
SpriteList class for game objects
"""

class SpriteList():
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)


    def draw(self,screen):
        for item in self.items:
            item.draw(screen)

    def number(self):
        return len(self.items)

    def clear_done(self):
        for item in self.items:
            if item.done:
                self.items.remove(item)

    def clear_all(self):
        self.items.clear()
