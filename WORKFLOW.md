# FPGA-GEN workflow

FPGA-GEN is a target-aware workflow for selecting and validating HLS-C before committing to RTL. This document states the DAC 2027 submission workflow; it is not a claim that the private implementation or paper evaluation is reproduced by this limited public release.

## 1. Establish the contract

Each task fixes the source-level behavior, host tests, HLS top-level interface, target device, clock, and any known reference latency and resource values. The workflow starts from a deterministic baseline candidate, **C0**, and may request up to three model-generated alternatives.

## 2. Screen candidates

C0 and each alternative pass through the same staged screening boundary:

1. source and interface checks;
2. host compilation and reference-paired functional tests;
3. HLS C simulation; and
4. HLS C synthesis with usable reports.

A failed stage cannot be represented as a pass. Missing vendor tools therefore produce an explicit not-run or unavailable result, never synthetic evidence.

## 3. Choose once

When C0 is valid, its measured values define the reference. Otherwise, the first valid screened candidate becomes the reference. For a candidate with usable measurements, the target-aware cost is

```text
J = (worst_cycles * clock_period / reference_delay)
    * mean(candidate_resource / reference_resource)
```

The resource mean covers only known reference resources whose values are nonzero (LUT, FF, DSP, and BRAM as available). Valid candidates with usable costs are ranked by `J`; exact ties favor a model candidate. Passing model candidates whose cost cannot be computed precede C0. If no candidate passes screening, C0 enters the repair path.

Selection occurs once. The selected source then enters only a bounded, tool-guided repair loop with unchanged-source detection. If a selected model candidate cannot be repaired and validated, the workflow rebuilds and validates C0 as the fallback. The resulting source is frozen before final evaluation.

## 4. Preserve the held-out boundary

Held-out vectors are unavailable to candidate generation, screening, ranking, and repair. A frozen design is admitted only when all of the following hold:

- held-out functional tests pass;
- held-out RTL co-simulation passes;
- device synthesis and fitting produce valid results; and
- the nonempty RTL hashes bound to functional and implementation evidence are equal.

This prevents target-aware selection from consuming the evidence reserved for final admission.

## What is public now

The current repository publishes this workflow and one standalone host-only example. [`examples/vector_add/hls_candidate.cpp`](examples/vector_add/hls_candidate.cpp) retains the HLS interface pragmas from an FPGA-GEN-generated candidate. [`examples/vector_add/run.py`](examples/vector_add/run.py) compiles that candidate beside the first-party reference and runs 70 bounded tests with seed 7.

The example endpoint is host equivalence only. It does not exercise model generation, C simulation, C synthesis, cost ranking, repair, RTL co-simulation, device fitting, or held-out admission. Those implementation components remain private until acceptance, and no paper-result or full-reproducibility claim is made here.
