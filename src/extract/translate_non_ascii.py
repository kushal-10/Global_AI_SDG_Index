import os
import logging
from tqdm import tqdm
from langdetect import detect, DetectorFactory
from unidecode import unidecode
from openai import OpenAI

# For consistent language-detection
DetectorFactory.seed = 0

# Configure logging
target_log = os.path.join("src", "extract", "non_ascii.log")
logging.basicConfig(
    filename=target_log,
    level=logging.INFO,
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    filemode='a'
)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
oai_api_key = os.getenv("OPENAI_API_KEY")
if not oai_api_key:
    raise EnvironmentError(
        "OPENAI_API_KEY environment variable not set. Please set it before running script."
    )
client = OpenAI(api_key=oai_api_key)


def detect_language(text):
    try:
        return detect(text)
    except Exception:
        return "unknown"


def is_non_ascii(text, threshold=0.05):
    non_ascii = sum(1 for c in text if ord(c) > 127)
    return non_ascii / max(len(text), 1) > threshold


def chunk_text(text, max_chars=3000):
    """Split text into chunks of up to max_chars characters."""
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]


def translate_chunks(chunks, lang, model="gpt-4o-mini"):
    """Translate each chunk via OpenAI and concatenate results."""
    translated = []
    for chunk in tqdm(chunks, desc="Translating chunks", leave=False):
        prompt = (
            f"Translate the following {lang} text to ASCII-only English.\n"
            f"{chunk}\n"
        )
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        translated.append(resp.choices[0].message.content)
    return "".join(translated)


def process_txt_files(base_dir, threshold=0.05):
    txt_paths = []
    for root, _, files in os.walk(base_dir):
        for fname in files:
            if fname.lower().endswith('.txt'):
                txt_paths.append(os.path.join(root, fname))

    non_ascii_count = 0
    for path in tqdm(txt_paths, desc="Scanning .txt files"):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {path}: {e}")
            continue

        if not is_non_ascii(content, threshold):
            continue

        lang = detect_language(content)
        preview = content[:100].replace("\n", " ")
        logger.info(f"{path} — Detected language: {lang} — Preview: {preview}")

        # Fast path for Latin-script languages: transliterate whole file
        if lang in ('en', 'de', 'fr', 'es', 'pt', 'it', 'nl'):
            out_text = unidecode(content)
        else:
            # Chunk non-Latin content into larger blocks to reduce API calls
            chunks = chunk_text(content)
            out_text = translate_chunks(chunks, lang)

        out_path = path.replace('.txt', '.ascii.txt')
        try:
            with open(out_path, 'w', encoding='ascii', errors='ignore') as f:
                f.write(out_text)
            logger.info(f"Translated and wrote ASCII file: {out_path}")
            non_ascii_count += 1
        except Exception as e:
            print(f"Error writing {out_path}: {e}")

    logger.info(f"Processed {non_ascii_count} non-ASCII files for translation.")
    return non_ascii_count


if __name__ == '__main__':
    base_directory = "annual_txts_fitz"
    count = process_txt_files(base_directory)
    print(f"Finished translating {count} file(s) to ASCII.")
