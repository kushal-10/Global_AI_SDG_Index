#  Global‑AI‑SDG‑Index

This project investigates how leading companies in Germany, China, India, and the United States apply artificial intelligence (AI) to advance the United Nations’ [17 Sustainable Development Goals (SDGs)](https://sdgs.un.org/goals).  

Annual reports are converted to text, AI/SDG-related passages are extracted, and the passages are classified into SDG sub‑targets using OpenAI models.  

Aggregated results describe where corporate AI initiatives contribute toward sustainability.

---
## Features

- **Document preprocessing**
  - Convert PDFs or DOCX files into plain text (`pdf2text.py`, `doc2text.py`)
  - Detect and translate non‑English content (`check_non_ascii.py`, `translate_non_ascii.py`)
  - Helper scripts for file cleanup and progress tracking

- **Hybrid retrieval**
  - Regex filtering to discard non‑AI text (`retrieval/regex_filter.py`)
  - Semantic filtering with SBERT or GPT for false‑positive removal (`retrieval/semantic_filter.py`)
  - Maintains an audit log for each step

- **Classification**
  - GPT‑4.1 family models label passages by SDG sub‑targets (`classification/classification_gpt41.py`)
  - Optional majority voting across model sizes for robustness

- **Analysis & Results**
  - Frequency statistics per company, year, country, and sector (`analysis/frequency.py`)
  - CSV outputs and plotting scripts stored under `src/results` and `src/plots`
  - Example outputs: `frequency.csv`, `classified.csv`, `results.csv`

---

## Installation

```bash
git clone https://github.com/kushal-10/Global-AI-SDG-Index.git
cd Global-AI-SDG-Index
python3 -m venv .gasdg_venv
source .gasdg_venv/bin/activate
pip install -r requirements.txt
source prepare_path.sh
```

--- 

## Data

All annual reports are made publicly available on each firm's site. Place annual reports under:

```python
annual_reports/COUNTRY/FIRM/YEAR.pdf

# Example
annual_reports/USA/Microsoft/2023.pdf
```
--- 

## Pipeline

1. Convert Reports to text

```python
python3 src/preprocessing/pdf2text.py      # PDFs
python3 src/preprocessing/doc2text.py      # DOCX (Microsoft example)
```

2. Handle non-english reports
```python
python3 src/preprocessing/check_non_ascii.py
python3 src/preprocessing/translate_non_ascii.py
```

3. Filter AI passages
```python
python3 src/retrievalv2/regex_filter.py        # Regex filter
python3 src/retrievalv2/semantic_filter.py     # Optional GPT/SBERT refinement
```

4. Classify toward SDG sub‑targets
```python
python3 src/classification/classification_gpt41.py
```

---
## Results

- `src/results/frequency.csv` – SDG counts per company/year

- `src/results/results.csv` – Final combined classification outputs

- `src/plots/` – Example plot scripts built from result CSVs.

