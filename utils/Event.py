# https://emptypage.jp/notes/pyevent.en.html
import asyncio

class Event(object):

    def __init__(self):
        self.handlers = []
    
    def add(self, handler):
        """Add new event handler function.
        
        Event handler function must be defined like func(sender, earg).
        You can add handler also by using '+=' operator.
        """
        self.handlers.append(handler)
        return self
    
    def remove(self, handler):
        """Remove existing event handler function.
        
        You can remove handler also by using '-=' operator.
        """
        self.handlers.remove(handler)
        return self
    
    def fire(self, *args, **keywargs): # ex: onMessage()
    """Fire event and call all handler functions
        
        You can call EventHandler object itself like e(earg) instead of 
        e.fire(earg).
        """
        for handler in self.handlers:
            asyncio.get_event_loop().create_task(handler(*args, **keywargs))
    
    __iadd__ = add
    __isub__ = remove
    __call__ = fire
