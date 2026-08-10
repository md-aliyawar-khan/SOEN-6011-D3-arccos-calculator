"""SOEN 6011 Deliverable 3: from-scratch arccos(x) Tkinter GUI.

The program calculates arccos(x) in radians using range reduction, a
Taylor-series recurrence for arcsin, and Newton's method for square roots.
No math library or built-in inverse-trigonometric function is used in the
production calculation.
"""

import tkinter as tk
from tkinter import ttk


__version__ = "1.1.0"

PI = 3.141592653589793
TOLERANCE = 1e-10
MAX_ITERATIONS = 1000
SQRT_TOLERANCE = 1e-14
SQRT_MAX_ITERATIONS = 100
MAX_FINITE_MAGNITUDE = 1e308


# Accessible high-contrast colour palette.
COLOUR_BACKGROUND = "#F5F7FA"
COLOUR_PRIMARY = "#1C437B"
COLOUR_TEXT = "#232323"
COLOUR_ERROR = "#B00020"
COLOUR_SUCCESS = "#147A3C"
COLOUR_FOCUS = "#005A9C"


class InputValidationError(Exception):
    """Raised when an input value is invalid."""


class ConvergenceError(Exception):
    """Raised when a numerical method fails to converge."""


def absolute_value(value):
    """Return the absolute value without using abs()."""
    if value < 0.0:
        return -value
    return value


def is_not_a_number(value):
    """Return True when value is NaN."""
    return value != value  # pylint: disable=comparison-with-itself


def is_finite_number(value):
    """Return True only when value is finite."""
    if is_not_a_number(value):
        return False

    if absolute_value(value) > MAX_FINITE_MAGNITUDE:
        return False

    return True


def calculate_square_root(value):
    """Calculate sqrt(value) using Newton's method."""
    if not is_finite_number(value) or value < 0.0:
        raise InputValidationError(
            "Square root input must be finite and greater than or equal to "
            "zero."
        )

    if value == 0.0:
        return 0.0

    guess = 1.0
    iteration = 0

    while iteration < SQRT_MAX_ITERATIONS:
        next_guess = 0.5 * (guess + value / guess)

        if absolute_value(next_guess - guess) <= SQRT_TOLERANCE:
            return next_guess

        guess = next_guess
        iteration = iteration + 1

    raise ConvergenceError(
        "Square-root calculation did not converge within "
        + str(SQRT_MAX_ITERATIONS)
        + " iterations."
    )


def calculate_arcsin(x):
    """Calculate arcsin(x) with a Taylor-series recurrence.

    This helper accepts finite values in [-1, 1]. The main arccos
    calculation passes range-reduced values to this function.
    """
    if not is_finite_number(x) or x < -1.0 or x > 1.0:
        raise InputValidationError(
            "arcsin input must be a finite value from -1 to 1."
        )

    if x == 1.0:
        return PI / 2.0

    if x == -1.0:
        return -PI / 2.0

    if x == 0.0:
        return 0.0

    result = 0.0
    coefficient = 1.0
    power = x
    iteration = 0

    while iteration < MAX_ITERATIONS:
        term = coefficient * power
        result = result + term

        if absolute_value(term) <= TOLERANCE:
            return result

        iteration = iteration + 1
        coefficient = (
            coefficient
            * (2 * iteration - 1)
            * (2 * iteration - 1)
            / ((2 * iteration) * (2 * iteration + 1))
        )
        power = power * x * x

    raise ConvergenceError(
        "Taylor-series calculation did not converge within "
        + str(MAX_ITERATIONS)
        + " iterations."
    )


def calculate_arccos(x):
    """Calculate arccos(x) in radians in the principal range [0, pi]."""
    if not is_finite_number(x):
        raise InputValidationError(
            "Enter a finite number. Values such as nan are not allowed."
        )

    if x < -1.0 or x > 1.0:
        raise InputValidationError(
            "Input is outside the valid domain. Enter a value from -1 to 1."
        )

    if x == 1.0:
        return 0.0

    if x == -1.0:
        return PI

    if x < 0.0:
        return PI - calculate_arccos(-x)

    reduced_input = calculate_square_root((1.0 - x) / 2.0)
    return 2.0 * calculate_arcsin(reduced_input)


class ArccosCalculatorGUI:
    """Tkinter GUI for the arccos(x) calculator."""

    def __init__(self, window):
        """Initialize the window and interface controls."""
        self.window = window
        self.window.title("arccos(x) Calculator v" + __version__)
        self.window.geometry("580x380")
        self.window.minsize(580, 380)
        self.window.resizable(True, True)
        self.window.configure(bg=COLOUR_BACKGROUND)

        self.build_interface()
        self.configure_keyboard_navigation()

    def build_interface(self):
        """Build labels, input controls, buttons, and feedback areas."""
        header = tk.Label(
            self.window,
            text="arccos(x) Calculator",
            font=("Segoe UI", 18, "bold"),
            fg=COLOUR_PRIMARY,
            bg=COLOUR_BACKGROUND,
        )
        header.pack(pady=(24, 4))

        subtitle = tk.Label(
            self.window,
            text="Enter a finite value of x where -1 <= x <= 1",
            font=("Segoe UI", 11),
            fg=COLOUR_TEXT,
            bg=COLOUR_BACKGROUND,
        )
        subtitle.pack(pady=(0, 14))

        input_frame = tk.Frame(self.window, bg=COLOUR_BACKGROUND)
        input_frame.pack(pady=4)

        input_label = tk.Label(
            input_frame,
            text="Value of x =",
            font=("Segoe UI", 12, "bold"),
            fg=COLOUR_TEXT,
            bg=COLOUR_BACKGROUND,
        )
        input_label.pack(side=tk.LEFT, padx=(0, 8))

        self.input_entry = tk.Entry(
            input_frame,
            width=24,
            font=("Segoe UI", 12),
            justify="center",
            highlightthickness=2,
            highlightcolor=COLOUR_FOCUS,
            highlightbackground=COLOUR_TEXT,
            insertbackground=COLOUR_TEXT,
        )
        self.input_entry.pack(side=tk.LEFT)

        button_frame = tk.Frame(self.window, bg=COLOUR_BACKGROUND)
        button_frame.pack(pady=18)

        self.calculate_button = tk.Button(
            button_frame,
            text="Calculate",
            width=12,
            font=("Segoe UI", 10, "bold"),
            bg=COLOUR_PRIMARY,
            fg="white",
            activebackground=COLOUR_FOCUS,
            activeforeground="white",
            command=self.calculate,
            takefocus=1,
        )
        self.calculate_button.pack(side=tk.LEFT, padx=6)

        self.clear_button = tk.Button(
            button_frame,
            text="Clear",
            width=12,
            font=("Segoe UI", 10),
            command=self.clear_fields,
            takefocus=1,
        )
        self.clear_button.pack(side=tk.LEFT, padx=6)

        self.exit_button = tk.Button(
            button_frame,
            text="Exit",
            width=12,
            font=("Segoe UI", 10),
            command=self.window.destroy,
            takefocus=1,
        )
        self.exit_button.pack(side=tk.LEFT, padx=6)

        self.result_label = tk.Label(
            self.window,
            text="Result will be displayed here.",
            font=("Segoe UI", 12, "bold"),
            fg=COLOUR_PRIMARY,
            bg=COLOUR_BACKGROUND,
            wraplength=530,
        )
        self.result_label.pack(pady=(8, 6))

        self.status_label = tk.Label(
            self.window,
            text="Status: Ready.",
            font=("Segoe UI", 10),
            fg=COLOUR_TEXT,
            bg=COLOUR_BACKGROUND,
            wraplength=530,
        )
        self.status_label.pack(pady=(4, 6))

        version_label = tk.Label(
            self.window,
            text="Version " + __version__,
            font=("Segoe UI", 9),
            fg=COLOUR_TEXT,
            bg=COLOUR_BACKGROUND,
        )
        version_label.pack(pady=(0, 12))

        self.input_entry.focus_set()
        self.window.bind("<Return>", self.calculate_from_enter)

    def configure_keyboard_navigation(self):
        """Apply keyboard shortcuts and a logical tab order."""
        self.window.bind("<Control-l>", self.clear_fields_from_shortcut)
        self.window.bind("<Control-q>", self.exit_from_shortcut)

        widgets = (
            self.input_entry,
            self.calculate_button,
            self.clear_button,
            self.exit_button,
        )

        for index, widget in enumerate(widgets):
            widget.bind("<Tab>", self._focus_next_widget(index, widgets))
            widget.bind(
                "<Shift-Tab>",
                self._focus_previous_widget(index, widgets),
            )

    def _focus_next_widget(self, index, widgets):
        """Return a handler that moves focus to the next widget."""

        def handler(_event):
            next_index = (index + 1) % len(widgets)
            widgets[next_index].focus_set()
            return "break"

        return handler

    def _focus_previous_widget(self, index, widgets):
        """Return a handler that moves focus to the previous widget."""

        def handler(_event):
            previous_index = (index - 1) % len(widgets)
            widgets[previous_index].focus_set()
            return "break"

        return handler

    def calculate_from_enter(self, _event=None):
        """Run the calculation when the user presses Enter."""
        self.calculate()
        return "break"

    def clear_fields_from_shortcut(self, _event=None):
        """Clear fields when the user presses Ctrl+L."""
        self.clear_fields()
        return "break"

    def exit_from_shortcut(self, _event=None):
        """Close the application when the user presses Ctrl+Q."""
        self.window.destroy()
        return "break"

    def calculate(self):
        """Validate input and display either a result or a helpful error."""
        input_text = self.input_entry.get().strip()

        self.result_label.config(
            text="Result will be displayed here.",
            fg=COLOUR_PRIMARY,
        )
        self.status_label.config(
            text="Status: Ready.",
            fg=COLOUR_TEXT,
        )

        if input_text == "":
            self.status_label.config(
                text=(
                    "Error: Input is required. "
                    "Enter a finite number from -1 to 1."
                ),
                fg=COLOUR_ERROR,
            )
            return

        try:
            value = float(input_text)
            result = calculate_arccos(value)

            self.result_label.config(
                text=(
                    "arccos("
                    + str(value)
                    + ") = "
                    + format(result, ".10f")
                    + " radians"
                )
            )
            self.status_label.config(
                text="Success: Calculation completed successfully.",
                fg=COLOUR_SUCCESS,
            )

        except ValueError:
            self.status_label.config(
                text=(
                    "Error: Invalid input. "
                    "Enter a number such as 0, 0.5, or -0.75."
                ),
                fg=COLOUR_ERROR,
            )

        except InputValidationError as error:
            self.status_label.config(
                text="Error: " + str(error),
                fg=COLOUR_ERROR,
            )

        except ConvergenceError as error:
            self.status_label.config(
                text="Error: " + str(error),
                fg=COLOUR_ERROR,
            )

    def clear_fields(self):
        """Clear all displayed input and feedback."""
        self.input_entry.delete(0, tk.END)
        self.result_label.config(
            text="Result will be displayed here.",
            fg=COLOUR_PRIMARY,
        )
        self.status_label.config(
            text="Status: Ready.",
            fg=COLOUR_TEXT,
        )
        self.input_entry.focus_set()


def main():
    """Start the Tkinter application."""
    window = tk.Tk()
    style = ttk.Style(window)

    if "vista" in style.theme_names():
        style.theme_use("vista")

    ArccosCalculatorGUI(window)
    window.mainloop()


if __name__ == "__main__":
    main()