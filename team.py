class Team:
    name = ''
    rank = 0
    score = 0
    win = False
    def __init__(self, name='', rank=0, score=0, win=False):
        self.name = name
        self.rank = rank
        self.score = score
        self.win = win