import numpy as np
import matplotlib.pyplot as plt               # (assuming you're using ax from plt.subplots)

from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def inverse_func(x, a, b, c):
    return a / (x + b) + c

def r_squared(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - ss_res / ss_tot
    
def saturation_curve(x, a, b, c):
    return a * (1 - np.exp(-b * x)) + c

def add_saturation_curve(ax, _cleaned, val):
    if len(_cleaned) > 3:  # Ensure enough points for curve fitting
        x = _cleaned[val]
        y = _cleaned['time']
        
        # Initial parameter guesses: a (max y), b (rate), c (y-offset)
        p0 = [max(y), 0.1, min(y)]
        try:
            # Fit the saturation curve
            popt, _ = curve_fit(saturation_curve, x, y, p0=p0, maxfev=10000)
            a, b, c = popt

            # Predict values and compute R²
            y_pred = saturation_curve(x, a, b, c)
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)

            # Generate points for plotting the curve
            x_fit = np.linspace(0, 56, 100)
            y_fit = saturation_curve(x_fit, a, b, c)
            x_fit_mapped = x_fit / 4  # Match bin indices
            
            # Plot the curve
            ax.plot(x_fit_mapped, y_fit, color='red', label='Saturation Curve', linewidth=2)
            
            # Display the equation and R² value on the plot
            equation_text = (
                f"y = {a:.2f}(1 - e^(-{b:.2f}x)) + {c:.2f}\n"
                f"R² = {r_squared:.3f}"
            )
            ax.text(
                0.95, 0.05, equation_text,
                transform=ax.transAxes,
                fontsize=14,
                ha='right',
                va='bottom',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9)
            )

            # Add legend
            ax.legend()
        except RuntimeError:
            print(f"Warning: Curve fitting failed for flower cluster {val}")
    return (a, b, c)