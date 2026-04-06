# Leet Code Studies

Repositório com soluções de problemas de algoritmos em notebooks Jupyter, escrito com foco didático e organizado para futura geração de um livro com **Jupyter Book**. A ideia é transformar os estudos em material público, claro e fácil de navegar, com possibilidade de publicação no **GitHub Pages**.

## Pré-requisitos

Antes de começar, recomendamos ter:

- **Python** recente instalado
- **uv** para gerenciamento de dependências
- **Jupyter Book** para gerar o livro a partir dos notebooks
- um ambiente virtual, se você preferir isolar as dependências do projeto

## Instalação

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd leet_code_studies
```

### 2. Instalar as dependências do projeto

O projeto já usa `uv` como gerenciador de pacotes. Para instalar as dependências declaradas em `pyproject.toml`, execute:

```bash
uv sync
```

### 3. Garantir suporte para o livro

O `jupyter-book` já faz parte das dependências do projeto. Depois de `uv sync`, o ambiente fica pronto para gerar o livro localmente.

Se você estiver reaproveitando um ambiente já existente e quiser adicionar a ferramenta manualmente, o comando equivalente é:

```bash
uv add jupyter-book
```

As dependências de análise e visualização também já estão contempladas no projeto, incluindo `jupyterlab`, `numpy`, `pandas`, `matplotlib` e `seaborn`.

## Organização do projeto

A estrutura principal é simples: os notebooks ficam em `notebooks/` e servem como base para o conteúdo didático. Abaixo está a estrutura atual do projeto com os arquivos do livro.

```text
leet_code_studies/
├── notebooks/
│   └── 0001 - Two Sum.ipynb
├── index.md
├── myst.yml
├── README.md
├── pyproject.toml
├── notebooks/index.md
└── _build/
    └── site/          # saída gerada pelo build do livro
```

### Arquivos e pastas principais

- `notebooks/`: contém os notebooks com as soluções comentadas e explicadas.
- `index.md`: página inicial do livro.
- `notebooks/index.md`: página de seção para agrupar os problemas resolvidos.
- `myst.yml`: configuração moderna do livro com a navegação.
- `README.md`: documentação principal do repositório.
- `pyproject.toml`: define o projeto Python e suas dependências.
- `_build/site/`: diretório normalmente criado após gerar o livro HTML.

Se você já tiver um fluxo antigo baseado em `_config.yml` e `_toc.yml`, ele pode existir em outros projetos, mas aqui o fluxo principal é o moderno, via `myst.yml`.

## Como gerar o livro com Jupyter Book

O fluxo típico para transformar os notebooks em um livro é este:

1. preparar os notebooks dentro de `notebooks/`
2. criar os arquivos de configuração do MyST / Jupyter Book
3. executar o build
4. revisar o resultado gerado
5. publicar no GitHub Pages, se desejado

### Estrutura atual do livro

Este projeto já usa a configuração moderna baseada em `myst.yml`, com a navegação definida no próprio arquivo e uma página inicial em `index.md`.

Arquivos principais:

- `myst.yml`: configuração do projeto e da navegação
- `index.md`: página inicial do livro
- `notebooks/index.md`: seção com os notebooks disponíveis

### 1. Configurar o livro

No fluxo atual do MyST, a navegação principal fica no `myst.yml`. Isso mantém a estrutura mais simples de manter e mais fácil de crescer conforme novos notebooks forem adicionados.

### 2. Gerar o build

Depois de configurar o livro, rode o comando de build a partir da raiz do projeto:

```bash
jupyter-book build --html
```

Na CLI atual do Jupyter Book baseada em MyST, esse comando constrói o livro e inicia uma prévia local em `http://localhost:3000`.

O projeto lê `myst.yml`, monta as páginas e deixa o conteúdo pronto para navegação local.

### 3. Iniciar um projeto local

Se você quiser abrir o projeto em modo local, o comando de entrada do Jupyter Book pode ser usado a partir da raiz do projeto:

```bash
jupyter-book start
```

### 4. Visualizar localmente

Depois de iniciar a prévia, abra `http://localhost:3000` no navegador. Os arquivos intermediários do projeto ficam em `_build/site/`.

### 5. Publicar no GitHub Pages

Depois de validado localmente, o conteúdo do livro pode ser publicado no **GitHub Pages**. Esse é um passo natural para transformar o material didático em documentação navegável e pública.

> Se o site mostrar a mensagem `Site not loading correctly? This may be due to an incorrect BASE_URL configuration`, isso normalmente significa que o livro está sendo servido em uma subpasta.
> Nesse caso, ajuste a variável `BASE_URL` antes do build.
>
> Exemplos:
>
> ```bash
> BASE_URL='' uv run jupyter-book build --html
> ```
>
> Para GitHub Pages em um repositório como `https://<usuario>.github.io/<repositorio>/`, use:
>
> ```bash
> BASE_URL=/<repositorio> uv run jupyter-book build --html
> ```

## Próximos passos

Alguns passos naturais para evoluir este repositório são:

- adicionar novos notebooks com outros problemas
- criar `_config.yml` e `_toc.yml`
- organizar uma estrutura de livro mais completa
- automatizar o build e a publicação no GitHub Pages
