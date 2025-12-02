"""
Classe base para algoritmos de deconvolução.
"""

from abc import ABC, abstractmethod
import numpy as np


class DeconvolutionAlgorithm(ABC):
    """
    Classe abstrata base para algoritmos de deconvolução.
    """
    
    @property
    @abstractmethod
    def name(self):
        """Nome do algoritmo."""
        pass
    
    @property
    @abstractmethod
    def description(self):
        """Descrição do algoritmo."""
        pass
    
    @abstractmethod
    def deconvolve(self, image, psf, logger=None, **kwargs):
        """
        Aplica o algoritmo de deconvolução na imagem.
        
        Args:
            image: Imagem de entrada (numpy.ndarray, pode ser RGB ou grayscale)
            psf: Point Spread Function (numpy.ndarray)
            logger: Logger opcional para mensagens de progresso (DeconvolutionLogger)
            **kwargs: Parâmetros específicos do algoritmo
        
        Returns:
            numpy.ndarray: Imagem deconvoluída
        """
        pass
    
    def _process_rgb_image(self, image, process_channel_func):
        """
        Processa uma imagem RGB canal por canal.
        
        Args:
            image: Imagem RGB (numpy.ndarray com shape (H, W, 3))
            process_channel_func: Função que processa um único canal
        
        Returns:
            numpy.ndarray: Imagem processada
        """
        deconvolved_channels = []
        for channel in range(3):
            channel_data = image[:, :, channel]
            deconvolved_channel = process_channel_func(channel_data)
            deconvolved_channels.append(deconvolved_channel)
        
        return np.stack(deconvolved_channels, axis=2)

