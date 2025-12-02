"""
Módulo principal de deconvolução com suporte a múltiplos algoritmos.
"""

from .algorithms import get_algorithm, list_algorithms


def deconvolve(image, psf, algorithm_name='richardson_lucy', logger=None, **kwargs):
    """
    Aplica deconvolução na imagem usando o algoritmo especificado.
    
    Args:
        image: Imagem de entrada (numpy.ndarray, pode ser RGB ou grayscale)
        psf: Point Spread Function (numpy.ndarray)
        algorithm_name: Nome do algoritmo a ser usado (str, padrão: 'richardson_lucy')
        logger: Logger opcional para mensagens de progresso (DeconvolutionLogger)
        **kwargs: Parâmetros específicos do algoritmo
    
    Returns:
        numpy.ndarray: Imagem deconvoluída
    
    Raises:
        ValueError: Se o algoritmo não for encontrado
    """
    algorithm = get_algorithm(algorithm_name)
    return algorithm.deconvolve(image, psf, logger=logger, **kwargs)


def get_available_algorithms():
    """
    Retorna lista de algoritmos disponíveis.
    
    Returns:
        Lista de strings com nomes dos algoritmos
    """
    return list_algorithms()

