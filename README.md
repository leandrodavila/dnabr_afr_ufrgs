# DNABR_AFR

Python application for mitochondrial haplogroup classification using Haplogrep3.

This project provides a Python wrapper for the Haplogrep3 CLI tool, enabling automated processing of VCF files to determine mitochondrial haplogroups.

## Features

- 🔧 **Clean Python Wrapper**: Easy-to-use interface for Haplogrep3 CLI
- 📦 **Batch Processing**: Process multiple VCF files efficiently
- 📊 **Multiple Metrics**: Support for Kulczynski, Hamming, and Jaccard classification methods
- 📝 **Comprehensive Documentation**: Detailed API reference and usage examples
- 🎯 **Type Safe**: Full type hints for better IDE support
- ⚡ **Error Handling**: Robust error handling and result validation

## Project Structure

```text
dnabr_afr/
├── haplogrep_wrapper/          # Main wrapper package
│   ├── __init__.py
│   └── wrapper.py
├── examples/                   # Usage examples
│   └── haplogrep_example.py
├── docs/                       # Documentation
│   ├── HAPLOGREP_WRAPPER_GUIDE.md
│   └── PROJECT_STRUCTURE.md
├── VCFs/                       # Input VCF files
├── results/                    # Output results
└── haplogrep/                  # Haplogrep3 executable
```

## Setup

1. Create and activate virtual environment:

   ```bash
   # Windows
   .\venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

2. Install the haplogrep_wrapper package in development mode:

   ```bash
   pip install -e .
   ```

3. Install additional dependencies (if any):

   ```bash
   pip install -r requirements.txt
   ```

4. Verify Haplogrep3 installation:

   ```bash
   # Check if haplogrep3 is accessible
   C:\repos\dnabr_afr\haplogrep\haplogrep3.exe trees
   ```

## Quick Start

```python
from haplogrep_wrapper import Haplogrep3Wrapper

# Initialize the wrapper
wrapper = Haplogrep3Wrapper(
    haplogrep_path="C:/repos/dnabr_afr/haplogrep/haplogrep3.exe",
    default_tree="phylotree-fu-rcrs@1.2"
)

# Classify a VCF file
result = wrapper.classify(
    input_file="C:/repos/dnabr_afr/VCFs/sample.vcf",
    output_file="C:/repos/dnabr_afr/results/output.txt"
)

if result.success:
    print("Classification successful!")
    print(wrapper.read_results(result.output_file))
else:
    print(f"Error: {result.stderr}")
```

## Usage Examples

### Single File Classification

```python
from haplogrep_wrapper import Haplogrep3Wrapper, ClassificationMetric

wrapper = Haplogrep3Wrapper(
    haplogrep_path="C:/repos/dnabr_afr/haplogrep/haplogrep3.exe"
)

result = wrapper.classify(
    input_file="sample.vcf",
    output_file="results.txt",
    metric=ClassificationMetric.HAMMING,
    extend_report=True
)
```

### Batch Processing

```python
from pathlib import Path
from haplogrep_wrapper import Haplogrep3Wrapper

wrapper = Haplogrep3Wrapper(
    haplogrep_path="C:/repos/dnabr_afr/haplogrep/haplogrep3.exe"
)

vcf_files = list(Path("C:/repos/dnabr_afr/VCFs").glob("*.vcf"))

results = wrapper.classify_batch(
    input_files=vcf_files,
    output_dir="C:/repos/dnabr_afr/results",
    extend_report=True
)

successful = sum(1 for r in results if r.success)
print(f"Processed {len(results)} files: {successful} successful")
```

### Run Example Script

```bash
python examples/haplogrep_example.py
```

## Documentation

- **[Haplogrep Wrapper Guide](docs/HAPLOGREP_WRAPPER_GUIDE.md)** - Complete API reference and usage examples
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Detailed project organization
- **[Haplogrep3 Official Docs](https://haplogrep.readthedocs.io/)** - Official Haplogrep3 documentation

## API Overview

### Main Classes

- **`Haplogrep3Wrapper`**: Main wrapper class
  - `classify()`: Classify a single VCF file
  - `classify_batch()`: Process multiple VCF files
  - `get_available_trees()`: List available phylogenetic trees
  - `read_results()`: Read classification results

- **`ClassificationMetric`**: Enum for classification methods
  - `KULCZYNSKI`: Default measure
  - `HAMMING`: Hamming distance
  - `JACCARD`: Jaccard index

- **`Haplogrep3Result`**: Result dataclass with execution details

## Requirements

- Python 3.7+
- Haplogrep3 executable
- Standard Python library (no external dependencies)

## Contributing

See [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) for guidelines on extending the project.

## License

This project is provided as-is. Haplogrep3 has its own licensing terms.

## Resources

- [Haplogrep3 Quickstart](https://haplogrep.readthedocs.io/en/latest/quickstart/)
- [Haplogrep3 Parameters](https://haplogrep.readthedocs.io/en/latest/parameters/)
