from src.db.model import Ropa, Marca, Size, Categoria


def get_all_ropa():
    """
    Gets all the clothes from the database.
    Returns:
    - ropa: A list of clothes.
    """
    ropa = (
        Ropa.select()
        .join(Marca, on=(Marca.id == Ropa.marca))
        .join(Size, on=(Size.id == Ropa.size))
        .join(Categoria, on=(Categoria.id == Ropa.categoria))
        .where(Ropa.eliminado == False)
    )

    return ropa
