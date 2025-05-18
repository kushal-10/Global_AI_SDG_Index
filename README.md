# Sustainability Index

The goal of this project is to analyse the implementation of AI by top firms across Germany, China, India and USA towards achieving the [17 Sustainable Development Goals](https://sdgs.un.org/goals) defined by the United Nations. 


### Setup

```python
git clone https://github.com/kushal-10/sustainability_index.git
cd sustainability_index
```

Install required libraries

```python
python3 -m venv .si_venv
source .si_venv/bin/activate
pip install -r requirements.txt
```

Have the data of annual reports under `annual_reports` in the following format `annual_reports/COUNTRY/FIRM/YEAR.pdf`.

Most of the annual reports can be found on - [https://www.annualreports.com/](https://www.annualreports.com/). Remaining ones were collected directly from the firms website.

### Data Preprocessing


Generating plain text from PDFs

```python
python3 src/preprocessing/pdf2text.py
```

Generating plain text from Docx
```python
python3 src/preprocessing/doc2text.py
```

Check and Translate non-EN text

```python
python3 src/preprocessing/check_non_ascii.py
python3 src/preprocessing/translate_non_ascii.py
```

Some helper/cleanup scripts
```python
python3 src/preprocessing/clean_pdfs.py # Use according to your dataset structure, before converting PDF/DOC to Text
python3 src/preprocessing/del_ascii.py # Use after translation, to remove extra files
```

### Retrieval

Use Regex to filter out non AI related chunks from the text files

```python
python3 src/retrievalv2/regex_filter.py 
```
