"""
Módulo para geração de PSFs (Point Spread Functions) a partir de parâmetros.
"""

import numpy as np
from scipy import ndimage


def generate_gaussian_psf(size, sigma):
    """
    Gera uma PSF gaussiana.
    
    Args:
        size: Tamanho do kernel (int ou tupla (height, width))
        sigma: Desvio padrão do blur gaussiano (float ou tupla (sigma_y, sigma_x))
    
    Returns:
        numpy.ndarray: PSF normalizada
    """
    if isinstance(size, int):
        size = (size, size)
    
    if isinstance(sigma, (int, float)):
        sigma = (sigma, sigma)
    
    # Criar grid de coordenadas
    center = (size[0] // 2, size[1] // 2)
    y, x = np.ogrid[:size[0], :size[1]]
    
    # Calcular distâncias do centro
    y_centered = y - center[0]
    x_centered = x - center[1]
    
    # Calcular PSF gaussiana 2D
    psf = np.exp(-(x_centered**2 / (2 * sigma[1]**2) + y_centered**2 / (2 * sigma[0]**2)))
    
    # Normalizar
    psf = normalize_psf(psf)
    
    return psf


def generate_motion_psf(size, length, angle):
    """
    Gera uma PSF de movimento (motion blur).
    
    Args:
        size: Tamanho do kernel (int ou tupla (height, width))
        length: Comprimento do movimento em pixels (float)
        angle: Ângulo do movimento em graus (float, 0 = horizontal, 90 = vertical)
    
    Returns:
        numpy.ndarray: PSF normalizada
    """
    if isinstance(size, int):
        size = (size, size)
    
    # Converter ângulo para radianos
    angle_rad = np.deg2rad(angle)
    
    # Calcular deslocamento em x e y
    dx = length * np.cos(angle_rad)
    dy = length * np.sin(angle_rad)
    
    # Criar PSF vazia
    psf = np.zeros(size)
    center = (size[0] // 2, size[1] // 2)
    
    # Desenhar linha de movimento
    num_points = int(np.ceil(length))
    for i in range(num_points + 1):
        t = i / num_points - 0.5
        y = int(center[0] + t * dy)
        x = int(center[1] + t * dx)
        
        if 0 <= y < size[0] and 0 <= x < size[1]:
            psf[y, x] = 1.0
    
    # Aplicar suavização leve para evitar artefatos
    if length > 1:
        psf = ndimage.gaussian_filter(psf, sigma=0.5)
    
    # Normalizar
    psf = normalize_psf(psf)
    
    return psf


def normalize_psf(psf):
    """
    Normaliza uma PSF para que a soma seja 1.0.
    
    Args:
        psf: Array numpy com a PSF
    
    Returns:
        numpy.ndarray: PSF normalizada
    """
    psf_sum = np.sum(psf)
    if psf_sum > 0:
        psf = psf / psf_sum
    return psf

