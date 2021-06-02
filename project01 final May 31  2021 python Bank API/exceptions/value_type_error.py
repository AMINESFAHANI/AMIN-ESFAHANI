class TypeValueError(Exception):
    description: str = 'Occurs when type does not match'

    def __str__(self):
        return "The type of value is not match"
