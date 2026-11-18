# FPGA-GEN: Target-Aware RTL Generation via HLS

This repository contains the **workflow and runnable example for the DAC 2027 submission** “FPGA-GEN: Target-Aware RTL Generation via HLS.” It is a deliberately limited release: the documentation and host-tested example are available now, while the full implementation is planned for release after acceptance.

The example pairs a small C reference with an HLS-C candidate produced by FPGA-GEN. It compiles both with a normal C++ compiler and checks them on deterministic directed and seeded-random inputs. It does not call a model or FPGA vendor tool, generate RTL, reproduce paper results, or claim hardware validation.

## Run the example

Requirements: Python 3.9 or newer and a C++17 compiler available as `c++`, `g++`, or `clang++`.

From a clean clone:

```sh
git clone https://github.com/huluk98/FPGA-GEN.git
cd FPGA-GEN
python3 examples/vector_add/run.py
```

Expected output:

```text
PASS host_tests=70 seed=7
report=build/vector_add/report.json
```

The JSON report records the actual host-test count, source hashes, compiler identity, and that C simulation, C synthesis, RTL co-simulation, device fitting, and RTL-hash admission were not run.

## Release boundary

| Available in this repository | Planned after acceptance |
| --- | --- |
| Method description | Full orchestration implementation |
| Standalone `vector_add` reference, generated HLS-C candidate, and host test | Model-candidate generation and target-aware ranking |
| Deterministic host-only report with source hashes | Vendor-tool screening, bounded repair, and held-out admission |
| GitHub Actions host check | Evaluation harnesses and paper-result artifacts approved for release |

See [WORKFLOW.md](WORKFLOW.md) for the method contract and the exact public/private boundary.

## Submission note

This is an author-owned public repository and therefore can reveal author identity. It should not be linked from an anonymous manuscript while the [applicable DAC review policy](https://dac.com/2027/program/research-manuscript-submissions) requires anonymity. The manuscript itself is not stored or modified here.

No license file is included at this stage.
