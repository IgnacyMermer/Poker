from PyGameView import PygameView
from listeners.Events import ClockEvent, QuitEvent
from Game import Game
from listeners.Listeners import EventListener, KeyboardController


class Clock:
    """
    Class to generate clock events until application is running, it allows to
    check other events like keyboard events and it helps with
    refreshing the screen.
    """

    def __init__(self, eventManager):
        self.eventManager = eventManager
        self.eventManager.addListener(self)
        self.keepGoing = True

    def run(self):
        while self.keepGoing:
            event = ClockEvent()
            self.eventManager.addEventToQueue(event)

    def refresh(self, event):
        if isinstance(event, QuitEvent):
            self.keepGoing = False


def main():
    eventListener = EventListener()
    KeyboardController(eventListener)
    clock = Clock(eventListener)
    PygameView(eventListener)
    Game(eventListener)
    clock.run()


if __name__ == "__main__":
    main()
