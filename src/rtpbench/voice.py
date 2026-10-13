"""Synthetic voiced audio with a crisp onset, and the energy gate both ends agree on."""

import math

RATE = 8000
GATE = 1000  # |sample| on the 16-bit scale; the synthetic voice never dips below it for 20 ms


def voice(seconds: float, f0: float, amplitude: int = 12000) -> list[int]:
    """Eight cosine harmonics under a 4 Hz syllable envelope; sample 0 is the waveform's peak."""
    norm = sum(1 / h for h in range(1, 9))
    out = []
    for i in range(round(seconds * RATE)):
        t = i / RATE
        env = 0.6 + 0.4 * math.cos(2 * math.pi * 4 * t)
        x = sum(math.cos(2 * math.pi * h * f0 * t) / h for h in range(1, 9)) / norm
        out.append(round(amplitude * env * x))
    return out
