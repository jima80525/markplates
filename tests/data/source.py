class Square:
    def __init__(self, side):
        self.side = side

    def area(self):
        """Area of this square"""
        return self.side * self.side


def area(length, width):
    """Badly named function returning the area of a rectangle"""
    return length * width


my_squares = [
    Square(1, 1),
    Square(2, 2),  # twice as much square
]
