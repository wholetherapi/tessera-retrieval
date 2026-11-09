# Tessera-Retrieval

Implementation of **Tessera-Retrieval**, a compressed inverted index layout
that shares postings metadata across heterogeneous text segments.

## Contents

- `src/tessera/index.py` - segment layout and postings decoding.
- `src/tessera/compress.py` - block compression codecs.
- `data/sample_corpus.jsonl` - a small public-domain corpus used by the tests.
- `experiments/latency_results.md` - latency and recall measurements reported
  in the paper.

## Usage

```bash
pip install -r requirements.txt
python -m tessera.index --corpus data/sample_corpus.jsonl --query "zenith protocol"
```

## License

Apache 2.0.
