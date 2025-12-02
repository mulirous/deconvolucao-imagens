# Deconvolução de Imagens

Aplicação em Python para deconvolução de imagens com suporte a múltiplos algoritmos. Disponível em duas versões: interface gráfica e linha de comando.

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

### Interface Gráfica (Recomendado)

Para usar a interface gráfica, execute:

```bash
python gui.py
```

A interface permite:
- Selecionar uma imagem através de um diálogo de arquivo
- Escolher o algoritmo de deconvolução através de um menu dropdown
- Escolher o tipo de blur (Gaussiano ou Movimento) através de um menu dropdown
- Configurar os parâmetros do algoritmo
- Visualizar a imagem original e a versão deconvoluída lado a lado
- Executar a deconvolução com um único clique

### Linha de Comando

### Deconvolução com Blur Gaussiano

```bash
python main.py --image input.jpg --blur-type gaussian --size 15 --sigma 5.0 --algorithm richardson_lucy --iterations 30 --output output.jpg
```

### Deconvolução com Blur de Movimento

```bash
python main.py --image input.jpg --blur-type motion --size 20 --length 10 --angle 45 --algorithm richardson_lucy --iterations 30 --output output.jpg
```

## Parâmetros

### Obrigatórios:
- `--image` ou `-i`: Caminho para a imagem de entrada
- `--blur-type` ou `-t`: Tipo de blur (`gaussian` ou `motion`)
- `--size` ou `-s`: Tamanho do kernel PSF em pixels
- `--output` ou `-o`: Caminho para salvar a imagem deconvoluída

### Opcionais:
- `--algorithm` ou `-a`: Algoritmo de deconvolução a ser usado (padrão: `richardson_lucy`)
- `--sigma`: Desvio padrão para blur gaussiano (obrigatório se `--blur-type=gaussian`)
- `--length`: Comprimento do movimento em pixels (obrigatório se `--blur-type=motion`)
- `--angle`: Ângulo do movimento em graus (padrão: 0, apenas para `--blur-type=motion`)
- `--iterations` ou `-n`: Número de iterações do algoritmo (padrão: 30)
- `--no-clip`: Não limita os valores entre 0 e 1 após deconvolução

## Exemplos

### Exemplo 1: Blur Gaussiano Leve
```bash
python main.py -i foto.jpg -t gaussian -s 10 --sigma 3.0 -a richardson_lucy -n 20 -o resultado.jpg
```

### Exemplo 2: Blur de Movimento Horizontal
```bash
python main.py -i foto.jpg -t motion -s 25 --length 15 --angle 0 -a richardson_lucy -n 40 -o resultado.jpg
```

### Exemplo 3: Blur de Movimento Diagonal
```bash
python main.py -i foto.jpg -t motion -s 30 --length 20 --angle 45 -a richardson_lucy -n 50 -o resultado.jpg
```

## Algoritmos

O projeto suporta múltiplos algoritmos de deconvolução através de uma arquitetura modular:

- **Richardson-Lucy**: Método iterativo de máxima verossimilhança (implementado usando `scikit-image`)

Novos algoritmos podem ser facilmente adicionados seguindo a interface base em `src/algorithms/base.py`.

## Estrutura do Projeto

```
.
├── src/
│   ├── __init__.py
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── base.py              # Classe base para algoritmos
│   │   └── richardson_lucy.py   # Implementação do algoritmo Richardson-Lucy
│   ├── deconvolution.py         # Módulo principal de deconvolução
│   ├── psf_generator.py         # Geração de PSFs
│   ├── utils.py                 # Funções utilitárias (carregar/salvar imagens)
│   ├── main.py                  # Interface de linha de comando
│   └── gui.py                   # Interface gráfica
├── main.py                      # Script de entrada CLI
├── gui.py                       # Script de entrada GUI
├── requirements.txt             # Dependências do projeto
└── README.md                    # Este arquivo
```

