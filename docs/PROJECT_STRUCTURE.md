# Python Project Structure

This document describes the organization of the dnabr_afr project.

## Directory Structure

```
dnabr_afr/
├── haplogrep_wrapper/          # Main wrapper package
│   ├── __init__.py             # Package initialization
│   └── wrapper.py              # Haplogrep3 wrapper implementation
├── examples/                   # Usage examples
│   └── haplogrep_example.py    # Demonstration script
├── docs/                       # Documentation
│   ├── HAPLOGREP_WRAPPER_GUIDE.md  # Complete wrapper documentation
│   └── PROJECT_STRUCTURE.md    # This file
├── VCFs/                       # Input VCF files
├── results/                    # Output directory for results
├── haplogrep/                  # Haplogrep3 executable location
│   └── haplogrep3.exe
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # Project overview
```

## Package: haplogrep_wrapper

The main Python package containing the Haplogrep3 wrapper.

### `__init__.py`

- Exports main classes and enums
- Defines package version
- Provides clean import interface

### `wrapper.py`

Core implementation containing:

- **`Haplogrep3Wrapper`**: Main wrapper class
  - `get_available_trees()`: Retrieve available phylogenetic trees
  - `classify()`: Classify a single VCF file
  - `classify_batch()`: Batch process multiple VCF files
  - `read_results()`: Read classification results

- **`ClassificationMetric`**: Enum for classification methods
  - `KULCZYNSKI`: Default Kulczynski measure
  - `HAMMING`: Hamming distance
  - `JACCARD`: Jaccard index

- **`Haplogrep3Result`**: Dataclass for classification results
  - Contains output file path, success status, stdout, stderr, return code

## Examples Directory

Contains demonstration scripts showing wrapper usage:

- **`haplogrep_example.py`**: Comprehensive examples including:
  - Single file classification
  - Batch processing
  - Different classification metrics
  - Error handling

## Documentation Directory

Comprehensive documentation for the project:

- **`HAPLOGREP_WRAPPER_GUIDE.md`**: Complete API reference and usage guide
  - Installation instructions
  - API reference
  - Usage examples
  - Advanced features
  - Error handling
  - Troubleshooting

- **`PROJECT_STRUCTURE.md`**: This file describing project organization

## Data Directories

### VCFs/

Input directory containing VCF (Variant Call Format) files to be processed.

### results/

Output directory where classification results are saved. Created automatically if it doesn't exist.

### haplogrep/

Contains the Haplogrep3 executable (`haplogrep3.exe`).

## Configuration Files

### requirements.txt

Python package dependencies. Currently minimal as the wrapper uses only standard library modules.

### .gitignore

Specifies files and directories to exclude from version control:
- Virtual environments (`venv/`)
- Python cache files (`__pycache__/`, `*.pyc`)
- Results directory (data files)
- IDE-specific files

### README.md

Project overview and quick start guide.

## Best Practices Implemented

1. **Modular Design**: Wrapper separated into its own package
2. **Clear Documentation**: Comprehensive guides and docstrings
3. **Example Scripts**: Practical usage demonstrations
4. **Type Hints**: Full type annotations for better IDE support
5. **Error Handling**: Proper exception handling and result validation
6. **Dataclasses**: Clean result objects using Python dataclasses
7. **Enumerations**: Type-safe classification metrics
8. **Path Handling**: Using `pathlib.Path` for cross-platform compatibility

## Usage Workflow

1. **Install dependencies** (if any added to requirements.txt)
   ```bash
   pip install -r requirements.txt
   ```

2. **Import the wrapper** in your scripts
   ```python
   from haplogrep_wrapper import Haplogrep3Wrapper
   ```

3. **Initialize and use**
   ```python
   wrapper = Haplogrep3Wrapper(
       haplogrep_path="C:/repos/dnabr_afr/haplogrep/haplogrep3.exe"
   )
   result = wrapper.classify(input_file="sample.vcf", output_file="results.txt")
   ```

4. **Check examples** for common use cases
   ```bash
   python examples/haplogrep_example.py
   ```

## Extending the Project

To add new features:

1. **Add methods to wrapper.py** for new functionality
2. **Update `__init__.py`** if exposing new classes/functions
3. **Document in HAPLOGREP_WRAPPER_GUIDE.md** with examples
4. **Add examples** to `examples/haplogrep_example.py`
5. **Update requirements.txt** if adding new dependencies

## Testing

To test the wrapper:

1. Ensure VCF files are in the `VCFs/` directory
2. Run the example script:
   ```bash
   python examples/haplogrep_example.py
   ```
3. Check the `results/` directory for output files

## Future Enhancements

Potential additions:

- Unit tests in `tests/` directory
- Result parsing utilities
- Visualization tools for haplogroup results
- CLI interface using `argparse` or `click`
- Async batch processing for large datasets
- Result comparison and reporting tools
