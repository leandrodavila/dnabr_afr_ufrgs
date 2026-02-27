# Haplogrep3 Python Wrapper Documentation

A comprehensive Python wrapper for the Haplogrep3 CLI tool, designed to simplify mitochondrial haplogroup classification in Python projects.

## Important Note

**Default Tree**: The default classification tree is `phylotree-fu-rcrs@1.2` (PhyloTree 17 - Forensic Update). See [Available Trees](#available-trees) section for other options.

**Error Handling**: Haplogrep3 outputs error messages to stdout rather than stderr. This wrapper automatically detects errors in stdout and populates the `result.stderr` field for consistent error handling.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Usage Examples](#usage-examples)
- [Advanced Features](#advanced-features)
- [Error Handling](#error-handling)

## Installation

### Prerequisites

- Python 3.7 or higher
- Haplogrep3 executable installed on your system

### Setup

1. Ensure haplogrep3 is installed and accessible:
   ```bash
   # Verify haplogrep3 installation
   ./haplogrep3.exe trees
   ```

2. Import the wrapper in your Python project:
   ```python
   from haplogrep_wrapper import Haplogrep3Wrapper
   ```

## Quick Start

Here's a simple example to get started:

```python
from haplogrep_wrapper import Haplogrep3Wrapper

# Initialize the wrapper
wrapper = Haplogrep3Wrapper(
    haplogrep_path="C:/repos/dnabr_afr/haplogrep/haplogrep3.exe",
    default_tree="phylotree-fu-rcrs@1.2"
)

# Classify a single VCF file
result = wrapper.classify(
    input_file="sample.vcf",
    output_file="results.txt"
)

# Check results
if result.success:
    print("Classification successful!")
    print(wrapper.read_results(result.output_file))
else:
    print(f"Classification failed: {result.stderr}")
```

## Available Trees

Haplogrep3 supports multiple phylogenetic trees. To see available trees:

```python
wrapper = Haplogrep3Wrapper(
    haplogrep_path="C:/repos/dnabr_afr/haplogrep/haplogrep3.exe"
)
trees = wrapper.get_available_trees()
print(trees)
```

Common trees include:
- `phylotree-fu-rcrs@1.2` - PhyloTree 17 Forensic Update (latest)
- `phylotree-fu-rcrs@1.0` - PhyloTree 17 Forensic Update
- `phylotree-rcrs@17.2` - PhyloTree 17
- `phylotree-rcrs@17.0` - PhyloTree 17
- `phylotree-rsrs@17.0` - PhyloTree 17 (RSRS reference)
- `phylotree-rcrs@16.0` - PhyloTree 16
- `phylotree-rcrs@15.0` - PhyloTree 15

## API Reference

### Haplogrep3Wrapper

Main wrapper class for interacting with Haplogrep3.

#### Constructor

```python
Haplogrep3Wrapper(haplogrep_path: str, default_tree: str = "phylotree-fu-rcrs@1.2")
```

**Parameters:**
- `haplogrep_path` (str): Path to the haplogrep3 executable
- `default_tree` (str, optional): Default classification tree. Default is "phylotree-fu-rcrs@1.2"

**Raises:**
- `FileNotFoundError`: If haplogrep3 executable is not found

**Example:**
```python
wrapper = Haplogrep3Wrapper(
    haplogrep_path="C:/tools/haplogrep/haplogrep3.exe",
    default_tree="phylotree17"
)
```

---

### Methods

#### `get_available_trees()`

Retrieve list of available classification trees.

**Returns:**
- `List[str]`: List of available tree names

**Raises:**
- `RuntimeError`: If unable to retrieve trees

**Example:**
```python
trees = wrapper.get_available_trees()
print("Available trees:", trees)
```

---

#### `classify()`

Classify haplogroups from a VCF file.

```python
classify(
    input_file: Union[str, Path],
    output_file: Union[str, Path],
    tree: Optional[str] = None,
    metric: Optional[ClassificationMetric] = None,
    extend_report: bool = False,
    chip: Optional[str] = None,
    skip_alignment_rules: bool = False,
    hits: Optional[int] = None,
    write_fasta: bool = False,
    write_fasta_msa: bool = False,
    het_level: Optional[float] = None
) -> Haplogrep3Result
```

**Parameters:**
- `input_file` (str | Path): Path to input VCF file
- `output_file` (str | Path): Path to output results file
- `tree` (str, optional): Classification tree to use (uses default_tree if not specified)
- `metric` (ClassificationMetric, optional): Classification metric (KULCZYNSKI, HAMMING, or JACCARD)
- `extend_report` (bool): Include additional SNP information. Default: False
- `chip` (str, optional): Restrict to genotyping array SNPs (semicolon-separated ranges)
- `skip_alignment_rules` (bool): Skip mtDNA nomenclature correction. Default: False
- `hits` (int, optional): Export best n hits for each sample. Default: 1
- `write_fasta` (bool): Generate output in FASTA format. Default: False
- `write_fasta_msa` (bool): Generate multiple sequence alignment output. Default: False
- `het_level` (float, optional): Heteroplasmy level threshold (0.0-1.0). Default: 0.9

**Returns:**
- `Haplogrep3Result`: Result object containing execution details

**Raises:**
- `FileNotFoundError`: If input file does not exist

---

#### `classify_batch()`

Classify multiple VCF files in batch.

```python
classify_batch(
    input_files: List[Union[str, Path]],
    output_dir: Union[str, Path],
    **kwargs
) -> List[Haplogrep3Result]
```

**Parameters:**
- `input_files` (List[str | Path]): List of input VCF file paths
- `output_dir` (str | Path): Directory to store output files
- `**kwargs`: Additional arguments passed to `classify()`

**Returns:**
- `List[Haplogrep3Result]`: List of results for each file

---

#### `read_results()`

Read contents of a results file.

```python
read_results(output_file: Union[str, Path]) -> str
```

**Parameters:**
- `output_file` (str | Path): Path to the output file

**Returns:**
- `str`: Contents of the output file

**Raises:**
- `FileNotFoundError`: If output file does not exist

---

### ClassificationMetric (Enum)

Available classification metrics:

- `ClassificationMetric.KULCZYNSKI` - Default Kulczynski measure
- `ClassificationMetric.HAMMING` - Hamming distance
- `ClassificationMetric.JACCARD` - Jaccard index

**Example:**
```python
from haplogrep_wrapper import ClassificationMetric

result = wrapper.classify(
    input_file="sample.vcf",
    output_file="results.txt",
    metric=ClassificationMetric.HAMMING
)
```

---

### Haplogrep3Result (Dataclass)

Result object containing classification output.

**Attributes:**
- `output_file` (str): Path to the output file
- `success` (bool): Whether classification was successful
- `stdout` (str): Standard output from the command
- `stderr` (str): Standard error from the command
- `return_code` (int): Command execution return code

---

## Usage Examples

### Example 1: Basic Classification

```python
from haplogrep_wrapper import Haplogrep3Wrapper

# Initialize wrapper
wrapper = Haplogrep3Wrapper(
    haplogrep_path="C:/repos/dnabr_afr/haplogrep/haplogrep3.exe"
)

# Classify a VCF file
result = wrapper.classify(
    input_file="C:/repos/dnabr_afr/VCFs/sample1.vcf",
    output_file="C:/repos/dnabr_afr/results/sample1_haplogroups.txt"
)

if result.success:
    print("✓ Classification completed successfully")
    content = wrapper.read_results(result.output_file)
    print(content)
else:
    print(f"✗ Error: {result.stderr}")
```

### Example 2: Extended Report with Custom Metric

```python
from haplogrep_wrapper import Haplogrep3Wrapper, ClassificationMetric

wrapper = Haplogrep3Wrapper(
    haplogrep_path="C:/repos/dnabr_afr/haplogrep/haplogrep3.exe",
    default_tree="phylotree17"
)

result = wrapper.classify(
    input_file="sample.vcf",
    output_file="detailed_results.txt",
    metric=ClassificationMetric.HAMMING,
    extend_report=True,
    hits=5  # Get top 5 hits for each sample
)

if result.success:
    print("Detailed classification with top 5 hits completed")
```

### Example 3: Batch Processing Multiple VCF Files

```python
from pathlib import Path
from haplogrep_wrapper import Haplogrep3Wrapper

wrapper = Haplogrep3Wrapper(
    haplogrep_path="C:/repos/dnabr_afr/haplogrep/haplogrep3.exe"
)

# Get all VCF files from directory
vcf_dir = Path("C:/repos/dnabr_afr/VCFs")
vcf_files = list(vcf_dir.glob("*.vcf"))

# Process all files
results = wrapper.classify_batch(
    input_files=vcf_files,
    output_dir="C:/repos/dnabr_afr/results",
    extend_report=True
)

# Summary of results
successful = sum(1 for r in results if r.success)
print(f"Processed {len(results)} files: {successful} successful, {len(results) - successful} failed")

# Display any failures
for result in results:
    if not result.success:
        print(f"Failed: {result.output_file}")
        print(f"Error: {result.stderr}")
```

### Example 4: Working with Different Trees

```python
from haplogrep_wrapper import Haplogrep3Wrapper

wrapper = Haplogrep3Wrapper(
    haplogrep_path="C:/repos/dnabr_afr/haplogrep/haplogrep3.exe"
)

# Get available trees
available_trees = wrapper.get_available_trees()
print("Available classification trees:")
for tree in available_trees:
    print(f"  - {tree}")

# Use a specific tree
result = wrapper.classify(
    input_file="sample.vcf",
    output_file="results_tree17.txt",
    tree="phylotree17"
)
```

### Example 5: Custom Heteroplasmy Level

```python
from haplogrep_wrapper import Haplogrep3Wrapper

wrapper = Haplogrep3Wrapper(
    haplogrep_path="C:/repos/dnabr_afr/haplogrep/haplogrep3.exe"
)

# Include heteroplasmies with level > 0.8
result = wrapper.classify(
    input_file="sample.vcf",
    output_file="results_het80.txt",
    het_level=0.8,
    extend_report=True
)
```

### Example 6: Generate FASTA Output

```python
from haplogrep_wrapper import Haplogrep3Wrapper

wrapper = Haplogrep3Wrapper(
    haplogrep_path="C:/repos/dnabr_afr/haplogrep/haplogrep3.exe"
)

# Generate both standard results and FASTA output
result = wrapper.classify(
    input_file="sample.vcf",
    output_file="results.txt",
    write_fasta=True
)

if result.success:
    print("Results saved in standard format and FASTA")
```

### Example 7: Chip Array Analysis

```python
from haplogrep_wrapper import Haplogrep3Wrapper

wrapper = Haplogrep3Wrapper(
    haplogrep_path="C:/repos/dnabr_afr/haplogrep/haplogrep3.exe"
)

# Restrict to specific SNP ranges for chip array
result = wrapper.classify(
    input_file="chip_sample.vcf",
    output_file="chip_results.txt",
    chip="1-100;200-300;500-600"
)
```

## Advanced Features

### Processing Pipeline Example

Here's a complete pipeline for processing multiple VCF files with error handling and logging:

```python
import logging
from pathlib import Path
from haplogrep_wrapper import Haplogrep3Wrapper, ClassificationMetric

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_vcf_pipeline(vcf_directory: str, output_directory: str):
    """
    Complete pipeline for processing VCF files.
    """
    # Initialize wrapper
    wrapper = Haplogrep3Wrapper(
        haplogrep_path="C:/repos/dnabr_afr/haplogrep/haplogrep3.exe",
        default_tree="phylotree17"
    )

    # Create output directory
    output_path = Path(output_directory)
    output_path.mkdir(parents=True, exist_ok=True)

    # Find all VCF files
    vcf_files = list(Path(vcf_directory).glob("*.vcf"))
    logger.info(f"Found {len(vcf_files)} VCF files to process")

    results_summary = {
        'successful': [],
        'failed': []
    }

    # Process each file
    for vcf_file in vcf_files:
        logger.info(f"Processing: {vcf_file.name}")

        output_file = output_path / f"{vcf_file.stem}_haplogroups.txt"

        result = wrapper.classify(
            input_file=vcf_file,
            output_file=output_file,
            metric=ClassificationMetric.KULCZYNSKI,
            extend_report=True,
            hits=3
        )

        if result.success:
            logger.info(f"✓ Successfully processed: {vcf_file.name}")
            results_summary['successful'].append(vcf_file.name)
        else:
            logger.error(f"✗ Failed to process: {vcf_file.name}")
            logger.error(f"  Error: {result.stderr}")
            results_summary['failed'].append(vcf_file.name)

    # Print summary
    print("\n" + "="*50)
    print("PROCESSING SUMMARY")
    print("="*50)
    print(f"Total files: {len(vcf_files)}")
    print(f"Successful: {len(results_summary['successful'])}")
    print(f"Failed: {len(results_summary['failed'])}")

    if results_summary['failed']:
        print("\nFailed files:")
        for filename in results_summary['failed']:
            print(f"  - {filename}")

    return results_summary

# Run the pipeline
if __name__ == "__main__":
    summary = process_vcf_pipeline(
        vcf_directory="C:/repos/dnabr_afr/VCFs",
        output_directory="C:/repos/dnabr_afr/results"
    )
```

## Error Handling

### Best Practices

Always check the `success` attribute of the result:

```python
result = wrapper.classify(
    input_file="sample.vcf",
    output_file="results.txt"
)

if result.success:
    # Process results
    content = wrapper.read_results(result.output_file)
    print(content)
else:
    # Handle error
    print(f"Classification failed!")
    print(f"Return code: {result.return_code}")
    print(f"Error message: {result.stderr}")

    # You can also access stdout for debugging
    if result.stdout:
        print(f"Output: {result.stdout}")
```

### Exception Handling

```python
from haplogrep_wrapper import Haplogrep3Wrapper

try:
    wrapper = Haplogrep3Wrapper(
        haplogrep_path="C:/invalid/path/haplogrep3.exe"
    )
except FileNotFoundError as e:
    print(f"Haplogrep3 not found: {e}")

try:
    result = wrapper.classify(
        input_file="nonexistent.vcf",
        output_file="results.txt"
    )
except FileNotFoundError as e:
    print(f"Input file not found: {e}")

try:
    content = wrapper.read_results("nonexistent_results.txt")
except FileNotFoundError as e:
    print(f"Results file not found: {e}")
```

## Tips and Best Practices

1. **Use absolute paths** for reliability across different execution contexts
2. **Check result.success** before reading output files
3. **Use extend_report=True** for detailed SNP information
4. **Batch processing** is more efficient for multiple files
5. **Set appropriate het_level** based on your data quality requirements
6. **Review available trees** before starting to ensure you're using the correct one
7. **Log errors** from `result.stderr` for debugging

## Troubleshooting

### Common Issues

**Issue**: "Haplogrep3 executable not found"
- **Solution**: Verify the path to haplogrep3.exe is correct
- **Check**: Run `ls C:/repos/dnabr_afr/haplogrep/` to confirm the file exists

**Issue**: "Input file not found"
- **Solution**: Ensure the VCF file path is correct and the file exists
- **Check**: Use absolute paths or verify relative paths from your working directory

**Issue**: Classification returns success=False
- **Solution**: Check `result.stderr` for specific error messages
- **Debug**: Verify input VCF file format is valid

**Issue**: Empty or unexpected results
- **Solution**: Try with `extend_report=True` to get more detailed output
- **Check**: Ensure the selected tree is appropriate for your data

## Version History

- **1.0.0** (2026-02-27): Initial release
  - Full wrapper implementation
  - Support for all haplogrep3 parameters
  - Batch processing capability
  - Comprehensive error handling

## License

This wrapper is provided as-is for use with Haplogrep3. Please refer to Haplogrep3's official documentation for licensing information about the tool itself.

## Additional Resources

- [Haplogrep3 Official Documentation](https://haplogrep.readthedocs.io/)
- [Haplogrep3 Quickstart Guide](https://haplogrep.readthedocs.io/en/latest/quickstart/)
- [Haplogrep3 Parameters Reference](https://haplogrep.readthedocs.io/en/latest/parameters/)
