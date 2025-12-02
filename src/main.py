"""
Aplicação de linha de comando para deconvolução de imagens.
"""

import argparse
import sys
from .psf_generator import generate_gaussian_psf, generate_motion_psf
from .deconvolution import deconvolve, get_available_algorithms
from .utils import load_image, save_image


def main():
    algorithms = get_available_algorithms()
    
    parser = argparse.ArgumentParser(
        description='Aplicação de deconvolução de imagens',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Exemplos de uso:
  # Deconvolução com blur gaussiano:
  python -m src.main --image input.jpg --blur-type gaussian --size 15 --sigma 5.0 --algorithm richardson_lucy --iterations 30 --output output.jpg
  
  # Deconvolução com blur de movimento:
  python -m src.main --image input.jpg --blur-type motion --size 20 --length 10 --angle 45 --algorithm richardson_lucy --iterations 30 --output output.jpg

Algoritmos disponíveis: {', '.join(algorithms)}
        """
    )
    
    # Argumentos obrigatórios
    parser.add_argument('--image', '-i', required=True,
                        help='Caminho para a imagem de entrada')
    
    parser.add_argument('--blur-type', '-t', required=True,
                        choices=['gaussian', 'motion'],
                        help='Tipo de blur: gaussian ou motion')
    
    parser.add_argument('--size', '-s', type=int, required=True,
                        help='Tamanho do kernel PSF (em pixels)')
    
    parser.add_argument('--output', '-o', required=True,
                        help='Caminho para salvar a imagem deconvoluída')
    
    # Argumentos opcionais
    parser.add_argument('--algorithm', '-a', type=str, default='richardson_lucy',
                        choices=algorithms,
                        help=f'Algoritmo de deconvolução a ser usado (padrão: richardson_lucy). Opções: {", ".join(algorithms)}')
    
    parser.add_argument('--sigma', type=float,
                        help='Desvio padrão para blur gaussiano (obrigatório se blur-type=gaussian)')
    
    parser.add_argument('--length', type=float,
                        help='Comprimento do movimento para blur de movimento (obrigatório se blur-type=motion)')
    
    parser.add_argument('--angle', type=float, default=0.0,
                        help='Ângulo do movimento em graus (padrão: 0, apenas para blur-type=motion)')
    
    parser.add_argument('--iterations', '-n', type=int, default=30,
                        help='Número de iterações do algoritmo (padrão: 30)')
    
    parser.add_argument('--no-clip', action='store_true',
                        help='Não limita os valores entre 0 e 1 após deconvolução')
    
    args = parser.parse_args()
    
    # Validação de argumentos
    if args.blur_type == 'gaussian' and args.sigma is None:
        print("Erro: --sigma é obrigatório quando --blur-type=gaussian", file=sys.stderr)
        sys.exit(1)
    
    if args.blur_type == 'motion' and args.length is None:
        print("Erro: --length é obrigatório quando --blur-type=motion", file=sys.stderr)
        sys.exit(1)
    
    # Carregar imagem
    print(f"Carregando imagem: {args.image}")
    image = load_image(args.image)
    print(f"Imagem carregada: {image.shape}")
    
    # Gerar PSF
    print(f"Gerando PSF do tipo '{args.blur_type}'...")
    if args.blur_type == 'gaussian':
        psf = generate_gaussian_psf(args.size, args.sigma)
        print(f"PSF gaussiana gerada: size={args.size}, sigma={args.sigma}")
    else:  # motion
        psf = generate_motion_psf(args.size, args.length, args.angle)
        print(f"PSF de movimento gerada: size={args.size}, length={args.length}, angle={args.angle}°")
    
    # Aplicar deconvolução
    print(f"Aplicando deconvolução usando algoritmo '{args.algorithm}' ({args.iterations} iterações)...")
    deconvolved = deconvolve(
        image,
        psf,
        algorithm_name=args.algorithm,
        num_iterations=args.iterations,
        clip=not args.no_clip
    )
    
    # Salvar resultado
    save_image(deconvolved, args.output)
    print("Deconvolução concluída!")


if __name__ == '__main__':
    main()

