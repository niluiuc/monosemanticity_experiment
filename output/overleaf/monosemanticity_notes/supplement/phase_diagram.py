"""Exact pair-risk phase diagram; run with NumPy, SciPy and Matplotlib."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import ndtr
from scipy.optimize import brentq


def pair_risks(p1, p2, I1, I2, sigma, a, c=1.0):
    # sigma is positive here. At sigma=0 use the clean formulas.
    q = ndtr(-a / (2.0 * sigma))
    q3 = ndtr(-3.0 * a / (2.0 * sigma))
    qm = ndtr(-c / (2.0 * sigma))
    P00 = (1.0 - p1) * (1.0 - p2)
    P10 = p1 * (1.0 - p2)
    P01 = (1.0 - p1) * p2
    P11 = p1 * p2
    superposed = (
        (I1 + I2) * P00 * q
        + P10 * (I1 * q + I2 * q3)
        + P01 * (I1 * q3 + I2 * q)
        + P11 * (I1 + I2) * (1.0 - q)
    )
    mono1 = I1 * qm + I2 * p2
    mono2 = I2 * qm + I1 * p1
    return superposed, np.minimum(mono1, mono2)


def risk_gap(p, sigma, a):
    # Equal frequencies and equal importance in this figure.
    superposed, mono = pair_risks(p, p, 1.0, 1.0, sigma, a)
    return superposed - mono


def main():
    output = Path(__file__).resolve().parents[1] / "figures"
    output.mkdir(parents=True, exist_ok=True)
    probabilities = np.linspace(0.01, 0.80, 180)
    noise_levels = np.linspace(0.01, 1.50, 200)
    P, SIGMA = np.meshgrid(probabilities, noise_levels)
    controls = [
        ("Equal stored-feature amplitude", 1.0),
        ("Equal total encoder energy", 1.0 / np.sqrt(2.0)),
    ]
    fig, axes = plt.subplots(
        1, 2, figsize=(10.4, 4.1), constrained_layout=True
    )
    for ax, (title, amplitude) in zip(axes, controls):
        gap = risk_gap(P, SIGMA, amplitude)
        image = ax.pcolormesh(
            P, SIGMA, gap, cmap="RdBu_r", shading="auto",
            vmin=-0.30, vmax=0.30,
        )
        ax.contour(
            P, SIGMA, gap, levels=[0.0], colors="black",
            linewidths=1.6,
        )
        ax.set(
            xlabel="Activation probability p = 1 - s",
            ylabel="Code-noise standard deviation sigma",
            title=title,
        )
        crossing = brentq(
            lambda noise: float(risk_gap(0.20, noise, amplitude)),
            0.05, 1.50,
        )
        ax.plot(0.20, crossing, "ko", markersize=4)
        print(f"{title}: p=0.20 crossing sigma={crossing:.9f}")
    fig.colorbar(
        image, ax=axes,
        label="Risk(superposed) - risk(best mono); blue < 0",
    )
    fig.savefig(output / "pair_phase_controls.png", dpi=220)
    plt.close(fig)


if __name__ == "__main__":
    main()
