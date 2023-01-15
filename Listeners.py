from Events import *
import pygame


class EventListener:

    """
    This class is to handle all new listeners and events, it allows to add new event which is handle in every listener, it means in every class 
    which have a refresh function and in init function add itself to listeners.
    """

    def __init__(self):
        self.listeners = {}
        self.events = []
        self.newListeners = []
        self.oldListeners = []

    def addListener(self, listener):
        self.newListeners.append(listener)

    def refreshListeners(self):
        for listener in self.newListeners:
            self.listeners[listener] = 1
        for listener in self.oldListeners:
            if listener in self.listeners:
                del self.listeners[listener]

    def removeListener(self, listener):
        self.oldListeners.append(listener)
    
    def voidEvents(self):
        for event in self.events:
            for listener in self.listeners:
                listener.refresh(event)
            if self.newListeners:
                self.refreshListeners()
        self.events = []
    
    def addEventToQueue(self, event):
        """
        This function allows to add new event to queue, refresh listeners and void refresh function in every listener
        """

        self.events.append(event)
        if isinstance(event, ClockEvent):
            self.refreshListeners()
            self.voidEvents()

class KeyboardController:

    """
    This class is to handle all events on user keyboard, if user click any button on the keyboard, with next clock event this key event is 
    handle and right event is called
    """

    def __init__(self, eventManager):
        self.eventManager = eventManager
        self.eventManager.addListener(self)
        self.moneyText = ""

    def refresh(self, event):
        if isinstance(event, ClockEvent):
            for event in pygame.event.get():
                ev = None
                if event.type == pygame.QUIT:
                    ev = QuitEvent()
                elif event.type == pygame.KEYDOWN \
                        and event.key == pygame.K_ESCAPE:
                    ev = QuitEvent()

                elif event.type == pygame.KEYDOWN \
                        and event.key == pygame.K_RETURN:
                    ev = NextMoveEvent()

                elif event.type == pygame.KEYDOWN \
                        and event.key == pygame.K_RIGHT:
                    ev = GameStartEvent(-1)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.moneyText = self.moneyText[:-1]
                    else:
                        self.moneyText += event.unicode
                    ev = MoneyTextEvent(self.moneyText)
                if ev:
                    self.eventManager.addEventToQueue(ev)
        if isinstance(event, ClearMoneyEvent):
            self.moneyText = ""
