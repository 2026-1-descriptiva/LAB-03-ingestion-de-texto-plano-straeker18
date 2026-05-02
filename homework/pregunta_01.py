import re
from pathlib import Path
import pandas as pd


def _normalize_keywords(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s*,\s*", ", ", text)
    text = text.strip()
    if text.endswith("."):
        text = text[:-1]
    return text


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:
    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """
    base_path = Path(__file__).resolve().parents[1]
    file_path = base_path / "files" / "input" / "clusters_report.txt"
    lines = file_path.read_text(encoding="utf-8").splitlines()

    records = []
    current_block = []
    separator_found = False

    for line in lines:
        if not separator_found:
            if line.strip().startswith("---"):
                separator_found = True
            continue
        if not line.strip():
            if current_block:
                records.append(current_block)
                current_block = []
            continue
        current_block.append(line)

    if current_block:
        records.append(current_block)

    parsed = []
    for block in records:
        first_line = block[0]
        match = re.match(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s*(.*)$", first_line)
        if not match:
            continue

        cluster    = int(match.group(1))
        cantidad   = int(match.group(2))
        porcentaje = float(match.group(3).replace(",", "."))
        texto      = match.group(4)

        if len(block) > 1:
            continuation = " ".join(line.strip() for line in block[1:])
            texto = f"{texto} {continuation}"

        texto = _normalize_keywords(texto)

        parsed.append(
            {
                "cluster": cluster,
                "cantidad_de_palabras_clave": cantidad,
                "porcentaje_de_palabras_clave": porcentaje,
                "principales_palabras_clave": texto,
            }
        )

    df = pd.DataFrame(parsed)
    return df