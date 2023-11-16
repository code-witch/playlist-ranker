class Category:

    def __init__(self, description: str, rank: int):
        self.description = description
        self.rank = rank
    
    def __str__(self):
        return self.description

