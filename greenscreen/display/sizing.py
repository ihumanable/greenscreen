class Sizing(object):
    def __init__(self, top: int=0, right: int=0, bottom: int=0, left: int=0):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    def vertical(self, size: int):
        self.top = size
        self.bottom = size

    def horizontal(self, size: int):
        self.left = size
        self.right = size
