from __future__ import annotations

import json
import re
from pathlib import Path


NOTEBOOK_DIR = Path("notebooks")

TITLE_RE = re.compile(r"^##\s+Solu[cç][aã]o\s+(\d+)")
HEADER_RE = re.compile(r"^(#{1,6})\s+(.*)$")

SOLUTION_TITLES = {
    1: "## Solução 1 - Força bruta",
    2: "## Solução 2 - Melhorias da solução 1",
    3: "## Solução 3 - Melhor solução",
    4: "## Solução 4 - Solução enxuta para submissão no leetcode",
}

SUBSECTION_ORDER = [
    "descricao",
    "complexidade",
    "walkthrough",
    "ascii",
    "implementacao",
    "testes",
]

SUBSECTION_TITLES = {
    "descricao": "### Descrição da solução",
    "complexidade": "### Ordem de complexidade (memória e processamento)",
    "walkthrough": "### Mini walkthrough",
    "ascii": "### Exemplo de execuçaõ em ASCII sketch",
    "implementacao": {
        1: "### Implementação da força bruta",
        2: "### Implementação da melhoria",
        3: "### Implementação da melhoria",
        4: "### Implementação da melhoria",
    },
    "testes": "### Testes",
}


def markdown_cell(text: str) -> dict:
    if not text.endswith("\n"):
        text += "\n"
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": text,
    }


def code_cell(source: str, metadata: dict | None = None, outputs: list | None = None, execution_count=None) -> dict:
    return {
        "cell_type": "code",
        "metadata": metadata or {},
        "execution_count": execution_count,
        "outputs": outputs or [],
        "source": source,
    }


def split_markdown_sections(text: str) -> list[tuple[str | None, str]]:
    sections: list[tuple[str | None, str]] = []
    current_header: str | None = None
    buffer: list[str] = []

    for line in text.splitlines():
        match = HEADER_RE.match(line)
        if match:
            if current_header is not None or buffer:
                sections.append((current_header, "\n".join(buffer).strip()))
            current_header = match.group(2).strip()
            buffer = []
        else:
            buffer.append(line)

    if current_header is not None or buffer:
        sections.append((current_header, "\n".join(buffer).strip()))

    return sections


def classify_markdown_section(header: str | None, content: str) -> str:
    text = f"{header or ''}\n{content}".lower()

    if "complexidade" in text:
        return "complexidade"
    if "ascii" in text:
        return "ascii"
    if any(token in text for token in ["mini walkthrough", "passo a passo", "walkthrough", "exemplo com", "simulação", "como pensar", "intuição"]):
        return "walkthrough"
    if "teste" in text:
        return "testes"
    return "descricao"


def clean_markdown_content(header: str | None, content: str) -> str:
    parts = []
    if header and header.lower() not in {
        "descrição",
        "descricao",
        "complexidade",
        "testes",
        "ascii sketch",
        "mini walkthrough",
    }:
        parts.append(f"**{header}**")
    if content:
        parts.append(content.strip())
    return "\n\n".join(part for part in parts if part).strip()


def is_test_code(source: str) -> bool:
    lowered = source.lower()
    markers = [
        "teste",
        "casos_teste",
        "casos_de_teste",
        "validar_",
        "executar_bateria",
        "assert ",
        "print(",
    ]
    return any(marker in lowered for marker in markers) and "def " not in lowered and "class " not in lowered


def extract_title_and_description(first_cell: dict) -> tuple[str, str]:
    lines = "".join(first_cell.get("source", "")).splitlines()
    title = lines[0].strip() if lines else "# Desafio"
    body = "\n".join(lines[1:]).strip()
    if not body:
        body = "Breve descrição"
    return title, body


def split_main_blocks(cells: list[dict]) -> tuple[list[dict], dict[int, list[dict]], list[dict]]:
    preamble: list[dict] = []
    solutions: dict[int, list[dict]] = {1: [], 2: [], 3: [], 4: []}
    benchmark: list[dict] = []

    current_solution: int | None = None
    in_benchmark = False

    for cell in cells[1:]:
        if cell["cell_type"] == "markdown":
            text = "".join(cell.get("source", ""))
            stripped = text.strip()
            if stripped.startswith("## Benchmark"):
                in_benchmark = True
                current_solution = None
                benchmark.append(cell)
                continue

            match = TITLE_RE.match(stripped.splitlines()[0]) if stripped else None
            if match:
                current_solution = int(match.group(1))
                in_benchmark = False
                solutions[current_solution].append(cell)
                continue

        if in_benchmark:
            benchmark.append(cell)
        elif current_solution is None:
            preamble.append(cell)
        else:
            solutions[current_solution].append(cell)

    return preamble, solutions, benchmark


def build_enunciado_cell(preamble: list[dict]) -> dict:
    original_parts: list[str] = []
    simple_parts: list[str] = []

    for cell in preamble:
        if cell["cell_type"] != "markdown":
            continue
        text = "".join(cell.get("source", ""))
        if not text.strip().startswith("## Enunciado"):
            continue
        for header, content in split_markdown_sections(text):
            if header is None:
                continue
            lowered = header.lower()
            if "linguagem simples" in lowered or "palavras simples" in lowered:
                if content:
                    simple_parts.append(content)
            elif "enunciado" in lowered:
                continue
            else:
                block = clean_markdown_content(header, content)
                if block:
                    original_parts.append(block)

    original_text = "\n\n".join(original_parts).strip() or "Enunciado original"
    simple_text = "\n\n".join(simple_parts).strip() or "Enunciado traduzido em linguagem simples"

    return markdown_cell(
        "## Enunciado\n\n"
        "### Enunciado original\n\n"
        f"{original_text}\n\n"
        "### Enunciado traduzido em linguagem simples\n\n"
        f"{simple_text}"
    )


def build_imports_cells(preamble: list[dict]) -> list[dict]:
    first_code = next((cell for cell in preamble if cell["cell_type"] == "code"), None)
    cells = [markdown_cell("## Imports\n\nColocar aqui todos os imports necessários")]
    if first_code is not None:
        cells.append(
            code_cell(
                "".join(first_code.get("source", "")),
                first_code.get("metadata"),
                first_code.get("outputs"),
                first_code.get("execution_count"),
            )
        )
    return cells


def build_funcoes_uteis_cells(preamble: list[dict]) -> list[dict]:
    markdown_parts: list[str] = []
    code_cells: list[dict] = []
    first_code_consumed = False

    for cell in preamble:
        if cell["cell_type"] == "code":
            if not first_code_consumed:
                first_code_consumed = True
                continue
            source = "".join(cell.get("source", ""))
            code_cells.append(code_cell(source, cell.get("metadata"), cell.get("outputs"), cell.get("execution_count")))
            continue

        text = "".join(cell.get("source", "")).strip()
        if not text or text.startswith("## Enunciado"):
            continue
        for header, content in split_markdown_sections(text):
            cleaned = clean_markdown_content(header, content)
            if cleaned:
                markdown_parts.append(cleaned)

    description = "\n\n".join(markdown_parts).strip() or "Funções que podem ser utilizadas durante o emprego das soluções"
    cells = [markdown_cell(f"## Funções uteis\n\n{description}")]
    cells.extend(code_cells)
    return cells


def normalize_solution_block(solution_number: int, cells: list[dict]) -> list[dict]:
    buckets: dict[str, list] = {key: [] for key in SUBSECTION_ORDER}
    current_bucket = "descricao"

    for cell in cells:
        if cell["cell_type"] == "markdown":
            text = "".join(cell.get("source", "")).strip()
            if not text:
                continue

            first_line = text.splitlines()[0]
            if TITLE_RE.match(first_line):
                sections = split_markdown_sections(text)
                for header, content in sections[1:]:
                    bucket = classify_markdown_section(header, content)
                    cleaned = clean_markdown_content(header, content)
                    if cleaned:
                        buckets[bucket].append(cleaned)
                        current_bucket = bucket
                continue

            for header, content in split_markdown_sections(text):
                bucket = classify_markdown_section(header, content)
                cleaned = clean_markdown_content(header, content)
                if cleaned:
                    buckets[bucket].append(cleaned)
                    current_bucket = bucket
            continue

        source = "".join(cell.get("source", ""))
        cloned = code_cell(source, cell.get("metadata"), cell.get("outputs"), cell.get("execution_count"))
        if current_bucket == "testes" or is_test_code(source):
            buckets["testes"].append(cloned)
            current_bucket = "testes"
        else:
            buckets["implementacao"].append(cloned)
            current_bucket = "implementacao"

    normalized: list[dict] = [markdown_cell(SOLUTION_TITLES[solution_number])]

    for key in SUBSECTION_ORDER:
        title = SUBSECTION_TITLES[key]
        if isinstance(title, dict):
            title = title[solution_number]

        content = buckets[key]
        if content:
            if key in {"implementacao", "testes"}:
                normalized.append(markdown_cell(title))
                for item in content:
                    if isinstance(item, dict):
                        normalized.append(item)
                    else:
                        normalized.append(markdown_cell(str(item)))
            else:
                normalized.append(markdown_cell(f"{title}\n\n" + "\n\n".join(content)))
        else:
            placeholder = {
                "descricao": "Descrição intuitiva da solução.",
                "complexidade": "Explicação detalhada da complexidade de memória e processamento.",
                "walkthrough": "Exibição de alguns exemplos de como o algoritmo funciona.",
                "ascii": "Exibição de algum exemplo do passo a passo do algoritmo.",
                "implementacao": "Função que implementa a solução.",
                "testes": "Exibição de alguns resultados da execução da solução.",
            }[key]
            normalized.append(markdown_cell(f"{title}\n\n{placeholder}"))

    return normalized


def build_benchmark_cells(benchmark_cells: list[dict]) -> list[dict]:
    if not benchmark_cells:
        return [
            markdown_cell(
                "## Benchmark\n\n"
                "Construção de casos de testes para progressivos para mostrar\n"
                "que as soluções se tornam cada vez mais otimizadas.\n"
                "Exibir gráficos e tabelas de comparação entre as soluções pertinentes."
            )
        ]

    texts: list[str] = []
    others: list[dict] = []

    for cell in benchmark_cells:
        if cell["cell_type"] == "markdown":
            text = "".join(cell.get("source", "")).strip()
            if text.startswith("## Benchmark"):
                remaining = "\n".join(text.splitlines()[1:]).strip()
                if remaining:
                    for header, content in split_markdown_sections(remaining):
                        cleaned = clean_markdown_content(header, content)
                        if cleaned:
                            texts.append(cleaned)
            else:
                for header, content in split_markdown_sections(text):
                    cleaned = clean_markdown_content(header, content)
                    if cleaned:
                        texts.append(cleaned)
        else:
            others.append(code_cell("".join(cell.get("source", "")), cell.get("metadata"), cell.get("outputs"), cell.get("execution_count")))

    intro = (
        "Construção de casos de testes para progressivos para mostrar\n"
        "que as soluções se tornam cada vez mais otimizadas.\n"
        "Exibir gráficos e tabelas de comparação entre as soluções pertinentes."
    )
    if texts:
        intro = f"{intro}\n\n" + "\n\n".join(texts)

    return [markdown_cell(f"## Benchmark\n\n{intro}"), *others]


def transform_notebook(path: Path) -> None:
    data = json.loads(path.read_text())
    cells = []
    for cell in data["cells"]:
        if isinstance(cell, dict):
            cells.append(cell)
        else:
            cells.append(markdown_cell(str(cell)))
    if not cells:
        return

    title, description = extract_title_and_description(cells[0])
    preamble, solutions, benchmark = split_main_blocks(cells)

    new_cells: list[dict] = [markdown_cell(f"{title}\n\n{description}")]
    new_cells.append(build_enunciado_cell(preamble))
    new_cells.extend(build_imports_cells(preamble))
    new_cells.extend(build_funcoes_uteis_cells(preamble))

    for solution_number in range(1, 5):
        new_cells.extend(normalize_solution_block(solution_number, solutions[solution_number]))

    new_cells.extend(build_benchmark_cells(benchmark))

    data["cells"] = new_cells
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")


def main() -> None:
    for path in sorted(NOTEBOOK_DIR.glob("*.ipynb")):
        transform_notebook(path)
        print(f"Padronizado: {path}")


if __name__ == "__main__":
    main()
