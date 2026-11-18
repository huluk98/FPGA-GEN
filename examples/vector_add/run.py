#!/usr/bin/env python3
"""Compile and compare the vector-add reference and HLS-C candidate."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Optional


EXPECTED_TESTS = 70
EXPECTED_SEED = 7
EXAMPLE_DIR = Path(__file__).resolve().parent
REPOSITORY = EXAMPLE_DIR.parents[1]
BUILD_DIR = REPOSITORY / "build" / "vector_add"
SOURCES = (
    EXAMPLE_DIR / "reference.cpp",
    EXAMPLE_DIR / "hls_candidate.cpp",
    EXAMPLE_DIR / "testbench.cpp",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(64 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_report(report: dict[str, object]) -> Path:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    path = BUILD_DIR / "report.json"
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def find_compiler() -> Optional[str]:
    requested = os.environ.get("CXX")
    if requested:
        return shutil.which(requested)
    for name in ("c++", "g++", "clang++"):
        compiler = shutil.which(name)
        if compiler:
            return compiler
    return None


def main() -> int:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    binary = BUILD_DIR / "vector_add_host"
    source_hashes = {
        str(path.relative_to(REPOSITORY)): sha256(path) for path in SOURCES
    }
    report: dict[str, object] = {
        "status": "fail",
        "host_test_count": 0,
        "seed": EXPECTED_SEED,
        "source_sha256": source_hashes,
        "hardware_stages": {
            "csim": "not_run",
            "csynth": "not_run",
            "rtl_cosim": "not_run",
            "device_fit": "not_run",
            "rtl_hash_admission": "not_run",
        },
    }

    compiler = find_compiler()
    if compiler is None:
        report["error"] = "no_cpp17_compiler"
        write_report(report)
        print("ERROR: no C++ compiler found (tried CXX, c++, g++, clang++)", file=sys.stderr)
        return 2

    compiler_version = subprocess.run(
        [compiler, "--version"], capture_output=True, text=True, check=False
    ).stdout.splitlines()
    report["compiler"] = Path(compiler).name
    report["compiler_version"] = compiler_version[0] if compiler_version else "unknown"

    compile_result = subprocess.run(
        [
            compiler,
            "-std=c++17",
            "-O2",
            "-Wall",
            "-Wextra",
            "-Werror",
            "-Wno-unknown-pragmas",
            *(str(path) for path in SOURCES),
            "-o",
            str(binary),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    report["compile_returncode"] = compile_result.returncode
    if compile_result.returncode != 0:
        report["error"] = "compile_failed"
        write_report(report)
        sys.stderr.write(compile_result.stderr)
        return 2

    run_result = subprocess.run(
        [str(binary)], capture_output=True, text=True, check=False
    )
    report["run_returncode"] = run_result.returncode
    output = run_result.stdout.strip()
    match = re.fullmatch(r"PASS host_tests=(\d+) seed=(\d+)", output)
    if (
        run_result.returncode != 0
        or match is None
        or int(match.group(1)) != EXPECTED_TESTS
        or int(match.group(2)) != EXPECTED_SEED
    ):
        report["error"] = "host_equivalence_failed"
        write_report(report)
        sys.stderr.write(run_result.stderr)
        if output:
            print(output, file=sys.stderr)
        return 1

    report["status"] = "pass"
    report["host_test_count"] = int(match.group(1))
    report_path = write_report(report)
    print(output)
    print(f"report={report_path.relative_to(REPOSITORY)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
