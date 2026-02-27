"""
Example script demonstrating the Haplogrep3 Python wrapper.

This script shows how to use the wrapper to classify VCF files.
"""

import sys
from pathlib import Path

# Add parent directory to Python path to allow imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from haplogrep_wrapper import Haplogrep3Wrapper, ClassificationMetric


def main():
    """Main function demonstrating wrapper usage."""

    # ============================================================
    # 1. Initialize the wrapper
    # ============================================================
    print("Initializing Haplogrep3 wrapper...")

    wrapper = Haplogrep3Wrapper(
        haplogrep_path="C:/repos/dnabr_afr/haplogrep/haplogrep3.exe",
        default_tree="phylotree-fu-rcrs@1.2"
    )

    print("✓ Wrapper initialized successfully\n")

    # ============================================================
    # 2. Get available trees
    # ============================================================
    print("Available classification trees:")
    try:
        trees = wrapper.get_available_trees()
        for tree in trees:
            print(f"  - {tree}")
        print()
    except RuntimeError as e:
        print(f"Could not retrieve trees: {e}\n")

    # ============================================================
    # 3. Classify a single VCF file
    # ============================================================
    print("=" * 60)
    print("Example 1: Single file classification")
    print("=" * 60)

    # Check if VCF directory exists
    vcf_dir = Path("C:/repos/dnabr_afr/VCFs")
    if not vcf_dir.exists():
        print(f"VCF directory not found: {vcf_dir}")
        print("Please ensure VCF files are available in the directory.\n")
    else:
        # Get first VCF file as example
        vcf_files = list(vcf_dir.glob("*.vcf"))

        if vcf_files:
            sample_vcf = vcf_files[0]
            output_file = "C:/repos/dnabr_afr/results/example_single_result.txt"

            print(f"Processing: {sample_vcf.name}")

            result = wrapper.classify(
                input_file=sample_vcf,
                output_file=output_file,
                extend_report=True
            )

            if result.success:
                print("✓ Classification successful!")
                print(f"Results saved to: {result.output_file}")

                # Read and display first few lines
                content = wrapper.read_results(result.output_file)
                lines = content.split('\n')[:10]
                print("\nFirst 10 lines of results:")
                print("-" * 60)
                for line in lines:
                    print(line)
                print("-" * 60)
            else:
                print("✗ Classification failed!")
                print(f"Error: {result.stderr}")
                print(f"Result: {result}")
        else:
            print(f"No VCF files found in {vcf_dir}")

    print()

    if False: 

        # ============================================================
        # 4. Batch processing with different parameters
        # ============================================================
        print("=" * 60)
        print("Example 2: Batch processing multiple VCF files")
        print("=" * 60)

        if vcf_dir.exists():
            vcf_files = list(vcf_dir.glob("*.vcf"))

            if vcf_files:
                print(f"Found {len(vcf_files)} VCF files")

                # Process all files
                results = wrapper.classify_batch(
                    input_files=vcf_files,
                    output_dir="C:/repos/dnabr_afr/results/batch",
                    metric=ClassificationMetric.KULCZYNSKI,
                    extend_report=True,
                    hits=3  # Get top 3 hits for each sample
                )

                # Display summary
                successful = sum(1 for r in results if r.success)
                failed = len(results) - successful

                print(f"\nBatch processing complete:")
                print(f"  Total files: {len(results)}")
                print(f"  Successful: {successful}")
                print(f"  Failed: {failed}")

                # Show any failures
                if failed > 0:
                    print("\nFailed files:")
                    for result in results:
                        if not result.success:
                            output_name = Path(result.output_file).name
                            print(f"  - {output_name}: {result.stderr}")
            else:
                print(f"No VCF files found in {vcf_dir}")

        print()

        # ============================================================
        # 5. Using different classification metrics
        # ============================================================
        print("=" * 60)
        print("Example 3: Using different classification metrics")
        print("=" * 60)

        if vcf_dir.exists() and list(vcf_dir.glob("*.vcf")):
            sample_vcf = list(vcf_dir.glob("*.vcf"))[0]

            metrics = [
                ClassificationMetric.KULCZYNSKI,
                ClassificationMetric.HAMMING,
                ClassificationMetric.JACCARD
            ]

            for metric in metrics:
                output_file = f"C:/repos/dnabr_afr/results/example_{metric.value}_result.txt"

                print(f"\nClassifying with {metric.value} metric...")

                result = wrapper.classify(
                    input_file=sample_vcf,
                    output_file=output_file,
                    metric=metric
                )

                if result.success:
                    print(f"  ✓ Success - Results saved to: {Path(output_file).name}")
                else:
                    print(f"  ✗ Failed - {result.stderr}")

        print()

    # ============================================================
    # Final message
    # ============================================================
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)
    print("\nCheck the results directory for output files:")
    print("  - C:/repos/dnabr_afr/results/")
    print("\nFor more information, see the documentation:")
    print("  - docs/HAPLOGREP_WRAPPER_GUIDE.md")


if __name__ == "__main__":
    # Create results directory if it doesn't exist
    results_dir = Path("C:/repos/dnabr_afr/results")
    results_dir.mkdir(parents=True, exist_ok=True)

    # Run examples
    main()
