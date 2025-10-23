from dataclasses import dataclass
from typing import Tuple, Optional

import sys
import numpy as np

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


@dataclass
class GraphParams:
    """
    Parameters for a 3-zone graph:
      - y1: Height of the first horizontal zone
      - y2: Height of the third horizontal zone
      - x:  Four X support points (x0, x1, x2, x3)
             [x0..x1]  -> horizontal line (y1)
             [x1..x2]  -> line (y1 -> y2)
             [x2..x3]  -> horizontal line (y2)
      - color: Line color (e.g., 'tab:blue')
      - label: Legend text
      - ylabel: Label for the corresponding Y-axis
      - y_min, y_max: Optional Y-limits for axis scaling
    """
    y1: float
    y2: float
    x: Tuple[float, float, float, float]
    color: str = "tab:blue"
    label: str = "Graph"
    ylabel: str = "Y"
    y_min: Optional[float] = None
    y_max: Optional[float] = None


def piecewise_xy(y1: float, y2: float, x4: Tuple[float, float, float, float]):
    """Generates the (x, y) points for the 3-zone progression."""
    if len(x4) != 4:
        raise ValueError("x4 must contain exactly 4 support points (x0, x1, x2, x3).")
    x = np.array(x4, dtype=float)
    if not np.all(np.diff(x) > 0):
        raise ValueError("x support points must be strictly increasing.")
    y = np.array([y1, y1, y2, y2], dtype=float)
    return x, y


def _nice_limits(vmin: float, vmax: float, pad_frac: float = 0.08):
    """Return (lo, hi) with a margin around [vmin, vmax]. Handles zero/flat ranges."""
    if not np.isfinite([vmin, vmax]).all():
        return vmin, vmax
    if vmin > vmax:
        vmin, vmax = vmax, vmin
    span = vmax - vmin
    if span == 0:
        # Flat line: expand around value
        pad = max(1.0, abs(vmax) * pad_frac)
        return vmin - pad, vmax + pad
    pad = span * pad_frac
    return vmin - pad, vmax + pad


class TwoAxisZonesPlot(QWidget):
    """
    QWidget with embedded Matplotlib plot:
      - Left Y-axis: Graph A
      - Right Y-axis: Graph B (twinx)
    """

    def __init__(self, params_a: GraphParams, params_b: GraphParams, parent=None):
        super().__init__(parent)

        self.params_a = params_a
        self.params_b = params_b

        # Matplotlib Figure/Canvas
        self.figure = Figure(figsize=(8, 4.5), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)

        # Axes: left + right twin axis
        self.ax_left = self.figure.add_subplot(111)
        self.ax_right = self.ax_left.twinx()
        self.ax_right.set_ylabel("B [Unit]", color="tab:red")
        self.ax_right.yaxis.set_label_position("right")
        self.ax_right.yaxis.tick_right()

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

        # Initial plot
        self._plot()

    def _plot(self):
        self.ax_left.clear()
        self.ax_right.clear()
        # After clearing, axis sides are reset -> enforce right side again
        self.ax_right.yaxis.set_label_position("right")
        self.ax_right.yaxis.tick_right()

        # Generate data
        xA, yA = piecewise_xy(self.params_a.y1, self.params_a.y2, self.params_a.x)
        xB, yB = piecewise_xy(self.params_b.y1, self.params_b.y2, self.params_b.x)

        # X-limits (covering both graphs) with gentle padding
        x_min = min(xA.min(), xB.min())
        x_max = max(xA.max(), xB.max())
        x_lo, x_hi = _nice_limits(float(x_min), float(x_max), pad_frac=0.04)
        self.ax_left.set_xlim(x_lo, x_hi)

        # Zone highlighting (optional, subtle – same zone shares as Graph A)
        # Zone 1: [x0, x1], Zone 2: [x1, x2], Zone 3: [x2, x3]
        zones = [(self.params_a.x[0], self.params_a.x[1]),
                 (self.params_a.x[1], self.params_a.x[2]),
                 (self.params_a.x[2], self.params_a.x[3])]
        alphas = [0.08, 0.12, 0.08]
        for (x0, x1), a in zip(zones, alphas):
            # axvspan on left axis – background visible for both axes
            self.ax_left.axvspan(x0, x1, color="grey", alpha=a, zorder=0)

        # Draw lines
        line_a, = self.ax_left.plot(
            xA, yA, color=self.params_a.color, linewidth=2.2, label=self.params_a.label
        )
        line_b, = self.ax_right.plot(
            xB, yB, color=self.params_b.color, linewidth=2.2, linestyle="--", label=self.params_b.label
        )

        # Labels
        self.ax_left.set_xlabel("X")
        self.ax_left.set_ylabel(self.params_a.ylabel, color=self.params_a.color)
        self.ax_right.set_ylabel(self.params_b.ylabel, color=self.params_b.color)

        # Y-limits: fixed if provided, else auto with padding based on current data
        if self.params_a.y_min is not None or self.params_a.y_max is not None:
            self.ax_left.set_ylim(self.params_a.y_min, self.params_a.y_max)
        else:
            yA_min = float(min(yA.min(), yA.max()))
            yA_max = float(max(yA.min(), yA.max()))
            y_lo, y_hi = _nice_limits(yA_min, yA_max, pad_frac=0.08)
            self.ax_left.set_ylim(y_lo, y_hi)

        if self.params_b.y_min is not None or self.params_b.y_max is not None:
            self.ax_right.set_ylim(self.params_b.y_min, self.params_b.y_max)
        else:
            yB_min = float(min(yB.min(), yB.max()))
            yB_max = float(max(yB.min(), yB.max()))
            y_lo, y_hi = _nice_limits(yB_min, yB_max, pad_frac=0.08)
            self.ax_right.set_ylim(y_lo, y_hi)

        # Match axis colors to line colors
        self.ax_left.tick_params(axis="y", colors=self.params_a.color)
        self.ax_left.yaxis.label.set_color(self.params_a.color)
        for spine in ("left",):
            self.ax_left.spines[spine].set_color(self.params_a.color)

        self.ax_right.tick_params(axis="y", colors=self.params_b.color)
        self.ax_right.yaxis.label.set_color(self.params_b.color)
        for spine in ("right",):
            self.ax_right.spines[spine].set_color(self.params_b.color)

        # Grid and legend
        self.ax_left.grid(True, which="both", alpha=0.25)
        handles, labels = [], []
        for ax in (self.ax_left, self.ax_right):
            h, l = ax.get_legend_handles_labels()
            handles.extend(h)
            labels.extend(l)
        self.ax_left.legend(handles, labels, loc="upper left")

        self.canvas.draw_idle()

    def update_params(self, params_a: Optional[GraphParams] = None,
                      params_b: Optional[GraphParams] = None):
        """Update parameters and redraw. Also triggers dynamic rescaling when limits are not fixed."""
        if params_a is not None:
            self.params_a = params_a
        if params_b is not None:
            self.params_b = params_b
        # Trigger rescale on next draw
        try:
            self.ax_left.relim()
            self.ax_left.autoscale_view()
            self.ax_right.relim()
            self.ax_right.autoscale_view()
        except Exception:
            pass
        self._plot()


if __name__ == "__main__":
    # Example usage
    app = QApplication(sys.argv)

    params_left = GraphParams(
        y1=2.0, y2=5.0,
        x=(0.0, 2.0, 5.0, 8.0),
        color="tab:blue",
        label="Signal A",
        ylabel="A [Unit]",
        y_min=0.0, y_max=6.0
    )

    params_right = GraphParams(
        y1=50.0, y2=120.0,
        x=(0.0, 1.5, 4.0, 8.0),
        color="tab:red",
        label="Signal B",
        ylabel="B [Unit]",
        y_min=0.0, y_max=150.0
    )

    w = TwoAxisZonesPlot(params_left, params_right)
    w.resize(900, 520)
    w.show()
    sys.exit(app.exec())
