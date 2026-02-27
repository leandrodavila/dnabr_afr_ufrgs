"""
Haplogrep3 Wrapper Module

This module provides a Python wrapper for the Haplogrep3 CLI tool.
"""

import subprocess
import json
import os
from pathlib import Path
from typing import Optional, List, Union
from enum import Enum
from dataclasses import dataclass


class ClassificationMetric(Enum):
    """Classification metrics supported by Haplogrep3."""
    KULCZYNSKI = "kulczynski"  # Default metric
    HAMMING = "hamming"
    JACCARD = "jaccard"


@dataclass
class Haplogrep3Result:
    """
    Result object containing classification output information.

    Attributes:
        output_file: Path to the output file containing results
        success: Whether the classification was successful
        stdout: Standard output from the haplogrep3 command
        stderr: Standard error from the haplogrep3 command
        return_code: Return code from the command execution
    """
    output_file: str
    success: bool
    stdout: str
    stderr: str
    return_code: int


class Haplogrep3Wrapper:
    """
    A Python wrapper for the Haplogrep3 CLI tool.

    This class provides a convenient interface to run haplogrep3 commands
    from Python, handling input/output files and command-line parameters.

    Args:
        haplogrep_path: Path to the haplogrep3 executable
        default_tree: Default classification tree to use (e.g., "phylotree17")

    Example:
        >>> wrapper = Haplogrep3Wrapper(
        ...     haplogrep_path="C:/path/to/haplogrep3.exe",
        ...     default_tree="phylotree17"
        ... )
        >>> result = wrapper.classify(
        ...     input_file="sample.vcf",
        ...     output_file="results.txt"
        ... )
    """

    def __init__(
        self,
        haplogrep_path: str,
        default_tree: str = "phylotree-fu-rcrs@1.2"
    ):
        """
        Initialize the Haplogrep3 wrapper.

        Args:
            haplogrep_path: Path to the haplogrep3 executable
            default_tree: Default classification tree to use

        Raises:
            FileNotFoundError: If haplogrep3 executable is not found
        """
        self.haplogrep_path = Path(haplogrep_path)

        if not self.haplogrep_path.exists():
            raise FileNotFoundError(
                f"Haplogrep3 executable not found at: {self.haplogrep_path}"
            )

        self.default_tree = default_tree

    def get_available_trees(self) -> List[str]:
        """
        Get list of available classification trees.

        Returns:
            List of available tree names

        Raises:
            RuntimeError: If the command fails to execute
        """
        try:
            result = subprocess.run(
                [str(self.haplogrep_path), "trees"],
                capture_output=True,
                text=True,
                check=True
            )

            # Parse the output to extract tree names
            trees = []
            for line in result.stdout.split('\n'):
                line = line.strip()
                if line and not line.startswith('Available'):
                    trees.append(line)

            return trees

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to get available trees: {e.stderr}")

    def classify(
        self,
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
    ) -> Haplogrep3Result:
        """
        Classify haplogroups from input VCF file.

        Args:
            input_file: Path to input VCF file
            output_file: Path to output results file
            tree: Classification tree to use (defaults to default_tree)
            metric: Classification metric to use
            extend_report: Include additional SNP information in report
            chip: Restrict to genotyping array SNPs (semicolon-separated ranges)
            skip_alignment_rules: Skip mtDNA nomenclature correction
            hits: Export best n hits for each sample (default is 1)
            write_fasta: Generate output in FASTA format
            write_fasta_msa: Generate multiple sequence alignment output
            het_level: Heteroplasmy level threshold (default: 0.9)

        Returns:
            Haplogrep3Result object containing execution results

        Raises:
            FileNotFoundError: If input file does not exist
        """
        input_path = Path(input_file)
        output_path = Path(output_file)

        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Build command
        cmd = [
            str(self.haplogrep_path),
            "classify",
            "--in", str(input_path),
            "--out", str(output_path),
            "--tree", tree or self.default_tree
        ]

        # Add optional parameters
        if metric:
            cmd.extend(["--metric", metric.value])

        if extend_report:
            cmd.append("--extend-report")

        if chip:
            cmd.extend(["--chip", chip])

        if skip_alignment_rules:
            cmd.append("--skip-alignment-rules")

        if hits is not None:
            cmd.extend(["--hits", str(hits)])

        if write_fasta:
            cmd.append("--write-fasta")

        if write_fasta_msa:
            cmd.append("--write-fasta-msa")

        if het_level is not None:
            cmd.append(f"--hetLevel={het_level}")

        # Execute command
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False  # Don't raise exception, handle manually
            )

            # Haplogrep3 outputs errors to stdout, not stderr
            # Check for error indicators in stdout
            success = result.returncode == 0
            error_message = result.stderr

            # If command failed but stderr is empty, check stdout for errors
            if not success and not error_message and result.stdout:
                # Extract error message from stdout
                for line in result.stdout.split('\n'):
                    if 'Error:' in line or 'error:' in line:
                        error_message = line.strip()
                        break
                # If no specific error line found, use the whole stdout
                if not error_message:
                    error_message = result.stdout

            return Haplogrep3Result(
                output_file=str(output_path),
                success=success,
                stdout=result.stdout,
                stderr=error_message,
                return_code=result.returncode
            )

        except Exception as e:
            return Haplogrep3Result(
                output_file=str(output_path),
                success=False,
                stdout="",
                stderr=str(e),
                return_code=-1
            )

    def classify_batch(
        self,
        input_files: List[Union[str, Path]],
        output_dir: Union[str, Path],
        **kwargs
    ) -> List[Haplogrep3Result]:
        """
        Classify multiple VCF files in batch.

        Args:
            input_files: List of input VCF file paths
            output_dir: Directory to store output files
            **kwargs: Additional arguments passed to classify()

        Returns:
            List of Haplogrep3Result objects for each file
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        results = []

        for input_file in input_files:
            input_path = Path(input_file)
            output_file = output_path / f"{input_path.stem}_haplogroups.txt"

            result = self.classify(
                input_file=input_path,
                output_file=output_file,
                **kwargs
            )
            results.append(result)

        return results

    def read_results(self, output_file: Union[str, Path]) -> str:
        """
        Read and return the contents of a results file.

        Args:
            output_file: Path to the output file

        Returns:
            Contents of the output file as string

        Raises:
            FileNotFoundError: If output file does not exist
        """
        output_path = Path(output_file)

        if not output_path.exists():
            raise FileNotFoundError(f"Output file not found: {output_path}")

        with open(output_path, 'r', encoding='utf-8') as f:
            return f.read()
