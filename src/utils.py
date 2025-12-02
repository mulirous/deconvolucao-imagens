"""
Funções utilitárias para carregamento e salvamento de imagens.
"""

import sys
import numpy as np
from PIL import Image


def load_image(image_path):
    """
    Carrega uma imagem do disco.
    
    Args:
        image_path: Caminho para o arquivo de imagem
    
    Returns:
        numpy.ndarray: Imagem como array numpy (valores normalizados entre 0 e 1)
    """
    try:
        img = Image.open(image_path)
        # Converter para RGB se necessário
        if img.mode != 'RGB' and img.mode != 'L':
            img = img.convert('RGB')
        
        # Converter para array numpy e normalizar para [0, 1]
        img_array = np.array(img, dtype=np.float64) / 255.0
        
        return img_array
    except Exception as e:
        print(f"Erro ao carregar imagem: {e}", file=sys.stderr)
        sys.exit(1)


def save_image(image_array, output_path):
    """
    Salva uma imagem no disco.
    
    Args:
        image_array: Array numpy com a imagem (valores entre 0 e 1)
        output_path: Caminho para salvar a imagem
    """
    try:
        # Garantir que os valores estão no range [0, 1]
        image_array = np.clip(image_array, 0, 1)
        
        # Converter para uint8 [0, 255]
        image_array = (image_array * 255).astype(np.uint8)
        
        # Converter para PIL Image e salvar
        if len(image_array.shape) == 3:
            img = Image.fromarray(image_array, 'RGB')
        else:
            img = Image.fromarray(image_array, 'L')
        
        img.save(output_path)
        print(f"Imagem salva em: {output_path}")
    except Exception as e:
        print(f"Erro ao salvar imagem: {e}", file=sys.stderr)
        sys.exit(1)

