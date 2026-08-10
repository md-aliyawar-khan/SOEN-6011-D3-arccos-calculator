# From-Scratch `arccos(x)` Calculator

**SOEN 6011 — Software Engineering Processes**  
**Deliverable 3 — Summer 2026**

- **Student:** Mohammad Aliyawar Khan
- **Student ID:** 40309082
- **Version:** `v1.1.0`

## Overview

This project implements the principal real value of `arccos(x)` in Python without using production-library inverse-trigonometric or square-root functions.

The implementation uses:

- Range reduction for improved endpoint behaviour.
- A Taylor-series recurrence for `arcsin(x)`.
- Newton's method for square roots.
- A Tkinter graphical user interface.
- Input validation, custom exceptions, error recovery, keyboard navigation, and textual status feedback.

The valid input domain is `-1 <= x <= 1`, and the returned principal value is in `[0, pi]` radians.

## Project Files

```text
problem7.py              Production implementation and Tkinter GUI
test_problem7.py         PyUnit test suite
README.md                Project documentation
d3_main.tex              D3 poster source
SOEN_6011_D3.pdf         Compiled D3 poster
```

The poster folder also contains GUI, Flake8, Pylint, `pdb`, PyUnit, and UIDP evidence images.

## Requirements

- Python 3
- Tkinter, normally included with a standard Python installation
- Optional quality tools: Flake8 and Pylint

Install the optional tools if needed:

```bash
python -m pip install flake8 pylint
```

## Run the Application

From the project folder, run:

```bash
python problem7.py
```

Enter a finite value of `x` in the interval `[-1, 1]`, then select **Calculate**.

### Keyboard Support

- `Enter` — calculate the result
- `Tab` / `Shift+Tab` — move keyboard focus
- `Ctrl+L` — clear input and feedback
- `Ctrl+Q` — exit the application

## Numerical Method

For non-negative input, the application uses:

$$
\arccos(x) = 2\arcsin\left(\sqrt{\frac{1-x}{2}}\right)
$$

For negative input:

$$
\arccos(x) = \pi - \arccos(-x)
$$

The program handles exact endpoints directly:

$$
\arccos(1) = 0,\qquad \arccos(-1) = \pi
$$

`calculate_arcsin()` uses a Taylor-series recurrence and explicitly handles `-1`, `0`, and `1`. `calculate_square_root()` uses Newton's method.

## Exceptions

- `InputValidationError` — raised for NaN, infinity, invalid domain values, or invalid helper-function input.
- `ConvergenceError` — raised if a numerical iteration exceeds its configured limit.

## Tests

Run the PyUnit suite with:

```bash
python -m unittest -v test_problem7.py
```

The final suite contains **31 tests** covering:

- Helper functions and finite-number validation.
- Newton square-root calculations.
- Taylor-series arcsine calculations and exact endpoints.
- `arccos(x)` endpoints, normal values, and near-endpoint values.
- Invalid-domain values, NaN, and positive/negative infinity.
- Principal-range validation and numerical accuracy.
- The configured convergence-failure path.

`math.acos()` and `math.asin()` are used only in `test_problem7.py` as verification oracles. The production module `problem7.py` does not import `math`.

## Quality Checks

Run Flake8:

```bash
python -m flake8 problem7.py test_problem7.py
```

Run Pylint:

```bash
python -m pylint problem7.py test_problem7.py
```

The D3 poster includes screenshots of the final Flake8 and Pylint executions.

## Debugging

A `pdb` session was used to inspect a near-endpoint calculation, `x = 0.9999`, including:

- Input value `x`
- Range-reduced input
- Taylor-series coefficient and term
- Intermediate result
- Final principal-range result

To launch the debugger:

```bash
python -m pdb problem7.py
```

## Semantic Versioning

- `v1.0.0` — D2 baseline release.
- `v1.1.0` — D3 minor release adding quality tooling, unit tests, debugging evidence, semantic versioning, UIDP-guided improvements, keyboard support, and accessibility-oriented feedback without changing the calculator's public input domain or behavior.

## Repository

[GitHub Repository](https://github.com/md-aliyawar-khan/SOEN-6011-D3-arccos-calculator)
