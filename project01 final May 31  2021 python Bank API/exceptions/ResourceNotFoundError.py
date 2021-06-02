class ResourceNotFoundError(Exception):
    description: str = 'Occurs when a resource is not found'

    def __str__(self):
        return "The Resource was not found"
