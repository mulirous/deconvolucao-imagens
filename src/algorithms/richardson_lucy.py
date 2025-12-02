"""
Implementação do algoritmo Richardson-Lucy para deconvolução.
"""

import numpy as np
from scipy.signal import convolve2d
from .base import DeconvolutionAlgorithm


class RichardsonLucy(DeconvolutionAlgorithm):
    """
    Algoritmo Richardson-Lucy para deconvolução de imagens.
    
    Um método iterativo de máxima verossimilhança para deconvolução.
    Implementado do zero sem dependências externas de deconvolução.
    """
    
    @property
    def name(self):
        return "richardson_lucy"
    
    @property
    def description(self):
        return "Algoritmo Richardson-Lucy - Método iterativo de máxima verossimilhança"
    
    def deconvolve(self, image, psf, num_iterations=30, clip=True, logger=None, **kwargs):
        """
        Aplica o algoritmo Richardson-Lucy para deconvolução de imagem.
        
        O algoritmo Richardson-Lucy é um método iterativo que resolve:
        g = h * u + n
        
        Onde:
        - g é a imagem observada (borrada)
        - h é a PSF (Point Spread Function)
        - u é a imagem original (a ser estimada)
        - n é ruído
        
        A atualização iterativa é:
        u^(n+1) = u^n * (h^T * (g / (h * u^n)))
        
        Args:
            image: Imagem de entrada (numpy.ndarray, pode ser RGB ou grayscale)
            psf: Point Spread Function (numpy.ndarray)
            num_iterations: Número de iterações do algoritmo (int, padrão: 30)
            clip: Se True, limita os valores entre 0 e 1 após deconvolução (bool, padrão: True)
            logger: Logger opcional para mensagens de progresso (DeconvolutionLogger)
            **kwargs: Parâmetros adicionais (ignorados)
        
        Returns:
            numpy.ndarray: Imagem deconvoluída
        """
        # Verificar se a imagem é RGB ou grayscale
        is_rgb = len(image.shape) == 3 and image.shape[2] == 3
        
        if logger:
            image_type = "RGB" if is_rgb else "Grayscale"
            logger.info(f"Iniciando deconvolução Richardson-Lucy ({image_type}, {num_iterations} iterações)")
        
        if is_rgb:
            # Processar cada canal separadamente
            deconvolved_channels = []
            for channel in range(3):
                if logger:
                    logger.info(f"Processando canal {channel + 1}/3")
                channel_data = image[:, :, channel]
                deconvolved_channel = self._richardson_lucy_single_channel(
                    channel_data,
                    psf,
                    num_iterations,
                    clip,
                    logger
                )
                deconvolved_channels.append(deconvolved_channel)
            
            deconvolved = np.stack(deconvolved_channels, axis=2)
        else:
            # Processar imagem em escala de cinza
            deconvolved = self._richardson_lucy_single_channel(
                image,
                psf,
                num_iterations,
                clip,
                logger
            )
        
        if logger:
            logger.info("Deconvolução concluída com sucesso")
        
        return deconvolved
    
    def _richardson_lucy_single_channel(self, image, psf, num_iterations, clip, logger=None):
        """
        Aplica o algoritmo Richardson-Lucy em um único canal (grayscale).
        
        Args:
            image: Imagem de entrada (numpy.ndarray 2D)
            psf: Point Spread Function (numpy.ndarray 2D)
            num_iterations: Número de iterações
            clip: Se True, limita valores entre 0 e 1
            logger: Logger opcional para mensagens de progresso
        
        Returns:
            numpy.ndarray: Imagem deconvoluída
        """
        # Garantir que a imagem e PSF são arrays numpy
        image = np.asarray(image, dtype=np.float64)
        psf = np.asarray(psf, dtype=np.float64)
        
        if logger:
            logger.info(f"Normalizando PSF (tamanho: {psf.shape})")
        
        # Normalizar PSF se necessário
        psf_sum = np.sum(psf)
        if psf_sum > 0:
            psf = psf / psf_sum
        
        # PSF rotacionada 180 graus (transposta para convolução reversa)
        psf_flipped = np.flip(np.flip(psf, 0), 1)
        
        # Inicializar estimativa com a imagem observada
        # Adicionar um pequeno valor para evitar divisão por zero
        estimate = np.maximum(image, 1e-10)
        
        if logger:
            logger.info(f"Iniciando {num_iterations} iterações do algoritmo Richardson-Lucy")
        
        # Iterações do algoritmo Richardson-Lucy
        for iteration in range(num_iterations):
            # Convolução da estimativa atual com a PSF
            # mode='same' mantém o tamanho da imagem original
            convolved = convolve2d(estimate, psf, mode='same', boundary='symm')
            
            # Evitar divisão por zero
            convolved = np.maximum(convolved, 1e-10)
            
            # Calcular razão entre imagem observada e convolução
            ratio = image / convolved
            
            # Convolução reversa da razão com a PSF rotacionada
            correction = convolve2d(ratio, psf_flipped, mode='same', boundary='symm')
            
            # Atualizar estimativa
            estimate = estimate * correction
            
            # Garantir valores não-negativos
            estimate = np.maximum(estimate, 0)
            
            # Log de progresso a cada 10% ou a cada iteração se menos de 10 iterações
            if logger:
                if num_iterations <= 10 or (iteration + 1) % max(1, num_iterations // 10) == 0:
                    progress = ((iteration + 1) / num_iterations) * 100
                    logger.info(f"Iteração {iteration + 1}/{num_iterations} ({progress:.1f}%)")
        
        # Aplicar clipping se solicitado
        if clip:
            if logger:
                logger.info("Aplicando clipping de valores")
            estimate = np.clip(estimate, 0, 1)
        
        return estimate

