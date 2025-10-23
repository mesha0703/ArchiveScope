import numpy as np
import math
from PySide6 import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter
from random import randint
import config

class BodePlotWidget(QtWidgets.QWidget):
    def __init__(self, filters, figsize=(8, 6), parent=None):
        super().__init__(parent)
        self.filters = filters if isinstance(filters, list) else [filters]
        self.axis_label_fontsize = 8
        self.tick_label_fontsize = 8

        self.min_freq = 1
        self.max_freq = 10000

        self.fig = Figure(figsize=figsize)
        self.canvas = FigureCanvas(self.fig)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)

        self._draw_bode()

    def _draw_bode(self):
        self.fig.clear()
        ax1 = self.fig.add_subplot(2, 1, 1)
        ax2 = self.fig.add_subplot(2, 1, 2)

        f = np.logspace(np.log10(self.min_freq), np.log10(self.max_freq), 1000)
        w = 2 * np.pi * f

        combined_H = np.ones_like(w, dtype=complex)

        for i, filt in enumerate(self.filters):
            H = self._compute_transfer_function(filt, w)
            amp = 20 * np.log10(np.abs(H))
            ph = np.angle(H, deg=True)

            if filt.color is None:
                filt.color = config.STANDARD_FILTER_COLORS[i % len(config.STANDARD_FILTER_COLORS)]
            color = (filt.color[0] / 255, filt.color[1] / 255, filt.color[2] / 255)
            
            ax1.semilogx(f, amp, label=f"Filter {i+1}", color=color)
            ax2.semilogx(f, ph, label=f"Filter {i+1}", color=color)
            combined_H *= H

        if len(self.filters) > 1:
            combined_amp = 20 * np.log10(np.abs(combined_H))
            combined_ph = np.angle(combined_H, deg=True)
            ax1.semilogx(f, combined_amp, 'k--', label="Combined (Amplitude)")
            ax2.semilogx(f, combined_ph, 'k--', label="Combined (Phase)")

        ax1.set_ylabel("Amplitude [dB]", fontsize=self.axis_label_fontsize)
        ax1.grid(True, which="both", ls="--", alpha=0.5)
        ax1.xaxis.set_major_formatter(ScalarFormatter())
        ax1.tick_params(axis='both', labelsize=self.tick_label_fontsize)
        ax1.legend(fontsize=8)

        ax2.set_ylabel("Phase [°]", fontsize=self.axis_label_fontsize)
        ax2.set_xlabel("Frequency [Hz]", fontsize=self.axis_label_fontsize)
        ax2.grid(True, which="both", ls="--", alpha=0.5)
        ax2.xaxis.set_major_formatter(ScalarFormatter())
        ax2.set_ylim(-180, 180)
        ax2.set_yticks([-180, -135, -90, -45, 0, 45, 90, 135, 180])
        ax2.tick_params(axis='both', labelsize=self.tick_label_fontsize)
        ax2.legend(fontsize=8)

        self.fig.tight_layout()
        self.canvas.draw()

    def _compute_transfer_function(self, filter_obj, w):
        if filter_obj.type == 0:  # Low-pass PT1 filter
            T = filter_obj.time_constant / 1000  # Convert ms to seconds
            H = 1 / (1 + 1j * w * T)
        elif filter_obj.type == 1:
            w0 = 2 * np.pi * filter_obj.fn
            H = 1 / (-(w / w0) ** 2 + 1j * 2 * filter_obj.dn * (w / w0) + 1)
        elif filter_obj.type == 2:
            # Band-stop (Notch) parametrized by:
            #   f_block [Hz]  -> center frequency f0 of the notch
            #   f_band  [Hz]  -> bandwidth around f0; mapped to analog damping alpha_p = 2π * f_band
            #   notch_depth [dB] -> positive depth at f0 relative to 0 dB (|H(jw0)| = 10^{-notch_depth/20})
            #   attenuation [dB] -> high-frequency asymptote: for f > f0, |H| -> 10^{attenuation/20}

            # --- Read and guard parameters ---
            f0 = float(getattr(filter_obj, 'f_block', 0.0) or 0.0)
            bw = float(getattr(filter_obj, 'f_band', 0.0) or 0.0)
            depth_db = float(getattr(filter_obj, 'notch_depth', 0.0) or 0.0)
            att_db = float(getattr(filter_obj, 'attenuation', 0.0) or 0.0)

            f0 = max(f0, 1e-9)             # [Hz]
            bw = max(bw, 1e-9)             # [Hz]
            w0 = 2.0 * np.pi * f0          # [rad/s]

            # Denominator damping alpha_p corresponds to bandwidth: alpha_p = 2π * f_band
            alpha_p = 2.0 * np.pi * bw

            # Depth mapping: at w = w0, |H| = alpha_z / alpha_p = 10^{-depth/20}
            r = 10.0 ** (-abs(depth_db) / 20.0)  # 0 < r <= 1
            alpha_z = max(alpha_p * r, 1e-12)

            # Analog notch transfer function (continuous-time, evaluated on jw):
            # H_notch(jw) = ( -w^2 + j*alpha_z*w + w0^2 ) / ( -w^2 + j*alpha_p*w + w0^2 )
            num = -(w ** 2) + 1j * alpha_z * w + (w0 ** 2)
            den = -(w ** 2) + 1j * alpha_p * w + (w0 ** 2)
            H_notch = num / den

            # High-frequency attenuation as a **Biquad-Shelf (2nd order)** for Siemens-like phase behavior.
            # Target: low freq → 1, high freq → A = 10^(attenuation/20), with additional phase around transition.
            # Transfer: G(s) = A * [ ( (s/wa)^2 + (1/Qz)*(s/wa) + 1/A ) / ( (s/wa)^2 + (1/Qp)*(s/wa) + 1 ) ]
            # Defaults chosen for smooth response; can be tuned via optional attributes on filter_obj:
            #   - shelf_Qz (default 0.707)
            #   - shelf_Qp (default 0.707)
            #   - shelf_wa_factor (default 1.0) → wa = 2π * max(shelf_wa_factor * f0, 1 Hz)
            A = 10.0 ** (att_db / 20.0)
            if abs(A - 1.0) < 1e-12:
                G = np.ones_like(w, dtype=complex)
            else:
                Qz = float(getattr(filter_obj, 'shelf_Qz', 0.707) or 0.707)
                Qp = float(getattr(filter_obj, 'shelf_Qp', 0.707) or 0.707)
                fac = float(getattr(filter_obj, 'shelf_wa_factor', 1.0) or 1.0)
                wa = 2.0 * np.pi * max(fac * f0, 1.0)
                x = 1j * w / wa
                num_shelf = (x ** 2) + (x / Qz) + (1.0 / A)
                den_shelf = (x ** 2) + (x / Qp) + 1.0
                G = A * (num_shelf / den_shelf)

            H = H_notch * G
        else:
            raise ValueError(f"Unknown filter type: {filter_obj.type}")
        return H