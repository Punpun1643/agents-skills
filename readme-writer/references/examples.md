# Worked README examples

Two complete, filled-in READMEs to use as models. Each is wrapped in a fenced block so the inner code blocks display as-is. Adapt structure and tone; never copy fabricated commands or results into a real project — re-derive every command from the actual repo.

---

## Example 1 — Library / package (Python)

Notice: identity in one line, a real install, the smallest meaningful usage with real output, an honest "why this over alternatives", and no decorative noise.

````markdown
# chunkwise

Token-aware text chunking for LLM pipelines. Splits long documents into overlapping chunks that respect a model's token budget — without cutting words or sentences mid-stride.

[![PyPI](https://img.shields.io/pypi/v/chunkwise)](https://pypi.org/project/chunkwise/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Why chunkwise

Naive character-count splitting breaks tokens and sentences, which hurts retrieval quality. `chunkwise` counts real tokens (via `tiktoken`) and prefers natural boundaries — paragraphs, then sentences, then words — falling back only when a single unit exceeds the budget.

## Install

```bash
pip install chunkwise
```

## Usage

```python
from chunkwise import chunk

text = open("article.txt").read()
chunks = chunk(text, max_tokens=512, overlap=64)

print(f"{len(chunks)} chunks")
print(chunks[0].text[:80])
print(chunks[0].token_count)
```

```
7 chunks
The history of cartography is, in part, a history of the instruments used to
311
```

Each chunk carries its `token_count` and the character `span` it came from, so you can map results back to the source.

## Options

| Argument     | Default | Description                                  |
| ------------ | ------- | -------------------------------------------- |
| `max_tokens` | `512`   | Hard ceiling per chunk.                      |
| `overlap`    | `0`     | Tokens of overlap carried between chunks.    |
| `model`      | `cl100k_base` | Tokenizer encoding to count against.   |

## License

MIT — see [LICENSE](LICENSE).
````

---

## Example 2 — Research / ML repo

Notice: reproducibility is foreground — exact environment, data access with licensing, seeds, where the weights live, and an expected-results table the reader can check against. A citation block closes it. Status of what's released is explicit.

````markdown
# qwen-text2sql-moe

Fine-tuned Qwen2.5-3B for natural-language-to-SQL over school administrative data, with a Value-RAG retrieval layer. Reproduces the results in our course report (68.6% execution accuracy on the held-out split).

[![Model on HF](https://img.shields.io/badge/%F0%9F%A4%97-checkpoints-yellow)](https://huggingface.co/your-handle/qwen-text2sql-moe)

> **Status:** Research artifact. Training code and adapters are released; the raw school dataset is access-controlled (see Data).

## Method in brief

A base Qwen2.5-3B-Instruct is adapted with SFT then GRPO. At inference, a ChromaDB-backed Value-RAG layer injects schema- and value-grounded hints into the prompt before generation. See [`docs/method.md`](docs/method.md) for the full pipeline.

## Setup

```bash
git clone https://github.com/your-handle/qwen-text2sql-moe.git
cd qwen-text2sql-moe
conda env create -f environment.yml   # pins CUDA, torch, transformers, trl, chromadb
conda activate text2sql
```

Requires one GPU with ≥24 GB VRAM for training; inference runs on ≥12 GB.

## Data

The school dataset is not redistributable. Request access via [the form](https://example.org/data-access), place the files under `data/raw/`, then build the value index:

```bash
python -m scripts.build_value_index --data data/raw --out artifacts/chroma
```

## Reproduce

```bash
# Train (SFT → GRPO). Seeds are fixed in configs/train.yaml.
python -m scripts.train --config configs/train.yaml

# Evaluate on the held-out split.
python -m scripts.evaluate --checkpoint artifacts/grpo/best --split test
```

Results are deterministic given the pinned seeds and library versions; minor drift (±0.4%) can occur across GPU architectures.

### Expected results

| Configuration        | Execution accuracy | Δ vs. base |
| -------------------- | ------------------ | ---------- |
| Base (zero-shot)     | 41.2%              | —          |
| + SFT                | 60.3%              | +19.1      |
| + GRPO               | 64.8%              | +4.5       |
| + Value-RAG (full)   | **68.6%**          | +3.8       |

## Using the released adapters

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-3B-Instruct")
model = PeftModel.from_pretrained(base, "your-handle/qwen-text2sql-moe")
tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-3B-Instruct")
```

## Citation

```bibtex
@misc{qwen_text2sql_moe_2026,
  title  = {Value-Grounded Text-to-SQL with Qwen2.5-3B},
  author = {Your Name},
  year   = {2026},
  note   = {https://github.com/your-handle/qwen-text2sql-moe}
}
```

## License

Code under Apache-2.0. Model weights inherit the base model's license; review before redistribution.
````
