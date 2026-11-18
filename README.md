# FPGA-GEN: Target-Aware RTL Generation via HLS

This anonymous reviewer artifact contains the **workflow and runnable example for the DAC 2027 submission** “FPGA-GEN: Target-Aware RTL Generation via HLS.”

The example pairs a small C reference with an HLS-C candidate produced by FPGA-GEN. It compiles both with a normal C++ compiler and checks them on deterministic directed and seeded-random inputs.

## Run the example

The example requires Python 3.9 or newer and a C++17 compiler available as `c++`, `g++`, or `clang++`.

Run the following command from the directory that contains this `README.md` and `examples/`.

```sh
python3 examples/vector_add/run.py
```

A successful run prints

```text
PASS host_tests=70 seed=7
report=build/vector_add/report.json
```

The generated `build/vector_add/report.json` records the status, seed, actual host-test count, compiler identity and version, compile and run return codes, and SHA-256 hashes of the three compiled C++ sources. Its `hardware_stages` object explicitly records C simulation, C synthesis, RTL co-simulation, device fitting, and RTL-hash admission as `not_run`.

## Reviewer walkthrough

1. Read [WORKFLOW.md](WORKFLOW.md) for the method contract, including candidate screening, one-time target-aware selection, bounded repair, and the held-out admission boundary.
2. Compare [`reference.cpp`](examples/vector_add/reference.cpp) with the generated [`hls_candidate.cpp`](examples/vector_add/hls_candidate.cpp). The candidate retains its HLS interface pragmas.
3. Inspect [`testbench.cpp`](examples/vector_add/testbench.cpp) and run the command above. The runner compiles the reference, candidate, and testbench together and executes 70 deterministic directed and seeded-random tests.
4. Inspect the generated JSON report to see the evidence produced by this host-only endpoint and the hardware stages that were deliberately left unrun.

## Illustrative ranking calculation

This toy calculation illustrates the cost in [WORKFLOW.md](WORKFLOW.md). Its numbers are independent of the host example and paper measurements. Suppose `C0` takes 100 cycles at 10 ns and uses 100 LUTs. An alternative takes 80 cycles at the same clock and uses 110 LUTs. With LUT as the only known reference resource, the costs are

```text
J(C0) = (100 * 10 / 1000) * (100 / 100) = 1.00
J(Alt) = (80 * 10 / 1000) * (110 / 100) = 0.88
```

The lower cost ranks the alternative first among valid screened candidates. Ranking alone does not admit it. After the selected source is frozen, admission still requires separate held-out functional and RTL co-simulation results, valid device implementation evidence, and matching nonempty RTL hashes bound to that evidence.

## Release boundary

| Included in this artifact | Planned after acceptance |
| --- | --- |
| Method contract in [WORKFLOW.md](WORKFLOW.md) | Full orchestration implementation |
| `vector_add` reference, generated candidate, host test, and deterministic report | Model generation, vendor-tool screening, live ranking, bounded repair, and held-out admission |
| Explicit `not_run` statuses for hardware stages | Evaluation harnesses and paper-result artifacts approved for release |

The runnable artifact stops at host equivalence. It does not call a model or FPGA vendor tool, perform live selection or repair, generate RTL, reproduce paper results, or claim hardware validation.

No license file is included at this stage.
