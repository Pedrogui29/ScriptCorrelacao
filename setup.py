from setuptools import setup, find_packages

setup(
    name='ScriptCorrelacao',  # Nome do seu pacote
    version='1.0.5',  # Versão do seu pacote
    packages=find_packages(),  # Para descobrir automaticamente os pacotes na estrutura de diretórios
    install_requires=[  # Dependências externas que seu pacote pode precisar
        'numpy',  # Exemplo de dependência
        'scipy',  # Exemplo de dependência
        'requests',  # Exemplo de dependência
    ],
    python_requires='>=3.6',  # Especificando a versão mínima do Python
    description='Pacote para análise de correlação entre séries temporais',  # Uma breve descrição do pacote
    long_description=open('README.md').read(),  # Um arquivo README.md para detalhes adicionais
    long_description_content_type='text/markdown',  # Tipo de conteúdo do README
    author='Pedro Guilherme Fernandes Oliveira',  # Seu nome
    author_email='pedropgfo@gmail.com',  # Seu e-mail
    url='https://github.com/Pedrogui29/ScriptCorrelacao',  # URL do repositório do projeto
    classifiers=[  # Classificações que ajudam a categorizar seu pacote
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Ou a licença que você usa
        'Operating System :: OS Independent',
    ],
)