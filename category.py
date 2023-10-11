class Category:
    # Perfect 10
    # Almost Perfect 9
    # Very Good 7 
    # Good 6
    
    # Mid 3 
    # Havent heard Surprisingly Good 2
    # Havent heard Good 1
    # Bad 0
    # Havent heard Not add worthy -1
    # Havent Heard Bad -2


    def __init__(self, description: str, rank: int):
        self.description = description
        self.rank = rank
    
    def __str__(self):
        return self.description

