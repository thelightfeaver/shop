from src.db.model import Ropa, Marca, Size, Categoria


def get_all_ropa():
    """
    Gets all the clothes from the database.
    Returns:
    - ropa: A list of clothes.
    """
    ropa =  Marca.select().where(Marca.eliminado == False)
    
    return ropa
