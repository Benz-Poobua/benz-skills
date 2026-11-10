---
name: code-fast
description: Correct first, then fast - the optimization protocol (gates green on the reference, profile the real bottleneck, equivalence ladder per step, equal-accuracy benchmarks with environment rows, memory in fresh processes, legacy switches). Use before optimizing, porting to Rust/CUDA, changing parallelism, or claiming any speedup or memory saving.
---

# code-fast

Correct code first; fast code next. Always check the logic before upgrading anything. A speed-up that
changes the answer is a bug with good timing.

## Steps

1. **Correct baseline.** The reference implementation passes its gates (`benz:code-verify`). Freeze
   its outputs (hashes or golden files) on the inputs you will benchmark. Completion: a reproducible
   reference output exists.
2. **Profile the real workload** (real record sizes, real config): per-stage wall time
   (I/O | preprocess | kernel | write), then `py-spy`/cProfile/torch profiler inside the dominant stage.
   Optimize only the measured bottleneck; name the stage a claim applies to.
3. **Look for the simpler win first**: redundant work (das_ani's receiver spectra recomputed per source:
   3.7-4.1x, bitwise), thread settings, a library call with `workers=`, chunk sizes, a better algorithmic
   regime — before a new language or kernel.
4. **Equivalence ladder.** Each optimization step is gated against the previous one: bitwise where the
   arithmetic is unchanged, otherwise within the calibrated tolerance (a multiple of the one-ULP control).
   Pattern: `sigGP/src/bench.py::ladder`. Completion: every rung has a recorded equivalence number.
5. **Benchmark honestly**: same inputs, warm cache, alternating/round-robin configurations, 4 runs with
   the warm-up discarded and the median of 3; report ratios at equal accuracy (equal misfit/error, never equal
   iterations); include the environment row (machine, cores, threads, library versions incl. MKL or not,
   background load); count transforms, not library calls.
6. **Measure memory in fresh processes** (one per configuration; `ru_maxrss` never falls); report shared vs
   private per worker; note the allocator (macOS keeps freed large blocks; Linux glibc returns them).
7. **Keep a legacy switch** that reproduces old numbers bitwise when a default changes; record what moved.

## Traps already measured here

- torch's CPU FFT on a no-MKL build (macOS arm64) is single-threaded pocketfft; SciPy's pocketfft with
  `workers=` gives the same bits threaded (das_ani `src/cpufft.py`).
- NNPACK cliff: float32 CPU conv with batch >= 16 and kernel < 17 ran ~75-340x slower without MKLDNN (uni_fwi 74.6-261x,
  uni_fwi_fast 225-339x); guard it (`nnpack_guard`).
- rayon pools do not survive `fork`: spawn worker pools.
- `torch.compile` warm-up (~100 s) can eat the gain; ATen's default thread count is not optimal (measure 1-12).
- deepwave on macOS runs single-threaded unless rebuilt with OpenMP; compare engines at equal threads.
- Symlinked inputs resolved to their targets made a throughput benchmark measure 4 records instead of 96.
- GPU claims need a GPU run: CPU wins from removing dispatch overhead may not survive CUDA.
