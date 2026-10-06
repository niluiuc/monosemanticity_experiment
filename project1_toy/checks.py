"""Independent numerical checks executed before any training."""
import numpy as np
from toy_math import (binary_population, reconstruction_loss_gradient,
                      exact_detection, geometry, interference_bound,
                      pair_closed_risks, mono_baseline, exact_decoder_mse)


def run_checks(config):
    rng = np.random.default_rng(config['checks']['seed'])
    eps = config['checks']['gradient_epsilon']
    states, weights = binary_population(3, 0.23)
    W = rng.normal(size=(2, 3)) * 0.6
    bias = rng.normal(size=3) * 0.3 + 0.15
    _, grad_W, grad_bias = reconstruction_loss_gradient(W, bias, states, weights)
    minimum_kink_distance = float(np.min(np.abs(states @ W.T @ W + bias)))
    if minimum_kink_distance < 100 * eps:
        raise AssertionError('Gradient check too close to a ReLU kink')
    numerical_W, numerical_bias = np.zeros_like(W), np.zeros_like(bias)
    for idx in np.ndindex(W.shape):
        plus, minus = W.copy(), W.copy()
        plus[idx] += eps
        minus[idx] -= eps
        numerical_W[idx] = (reconstruction_loss_gradient(plus, bias, states, weights)[0]
                           - reconstruction_loss_gradient(minus, bias, states, weights)[0]) / (2 * eps)
    for i in range(len(bias)):
        plus, minus = bias.copy(), bias.copy()
        plus[i] += eps
        minus[i] -= eps
        numerical_bias[i] = (reconstruction_loss_gradient(W, plus, states, weights)[0]
                            - reconstruction_loss_gradient(W, minus, states, weights)[0]) / (2 * eps)
    analytic = np.concatenate([grad_W.ravel(), grad_bias])
    numeric = np.concatenate([numerical_W.ravel(), numerical_bias])
    relative = np.linalg.norm(analytic - numeric) / max(1.0, np.linalg.norm(analytic))
    if relative > config['checks']['gradient_relative_tolerance']:
        raise AssertionError(f'Incorrect gradient: relative difference {relative}')

    pair_max_difference = 0.0
    for p in config['pair']['probabilities']:
        states, weights = binary_population(2, p)
        for a in config['pair']['amplitudes']:
            pair_W = np.array([[a, -a]])
            mono_W = np.array([[1., 0.]])
            for sigma in config['pair']['sigmas']:
                rp = exact_detection(pair_W, states, weights, np.diag(pair_W.T @ pair_W) / 2, sigma)[0].sum()
                rm = exact_detection(mono_W, states, weights, np.array([.5, 0.]), sigma)[0].sum()
                closed = pair_closed_risks(p, sigma, a)
                pair_max_difference = max(pair_max_difference, abs(rp - closed[0]), abs(rm - closed[1]))
    if pair_max_difference > config['checks']['exact_identity_tolerance']:
        raise AssertionError('Closed pair risk does not match state enumeration')

    max_bound_violation = -np.inf
    for _ in range(12):
        W = rng.normal(size=(3, 5))
        W /= np.linalg.norm(W, axis=0)
        p = rng.uniform(.02, .8, size=5)
        states, weights = binary_population(5, p)
        threshold = geometry(W, p)[-1]
        for sigma in [0., .1, .5]:
            risk = exact_detection(W, states, weights, threshold, sigma)[0]
            bound = interference_bound(W, p, sigma)
            max_bound_violation = max(max_bound_violation, float(np.max(risk - bound)))
    if max_bound_violation > config['checks']['bound_tolerance']:
        raise AssertionError('Exact risk exceeds interference upper bound')

    n, m, energy = 8, 4, 4.
    W, bias = mono_baseline(n, m, .15, energy)
    states, weights = binary_population(n, .15)
    mono_loss = exact_decoder_mse(W, bias, states, weights, 0).sum()
    expected_loss = (n - m) * .15 * .85
    if abs(mono_loss - expected_loss) > 1e-12:
        raise AssertionError('Restricted mono population loss incorrect')
    zero_risk = exact_detection(W, states, weights, geometry(W, .15)[-1], .3)[0][m:]
    if not np.allclose(zero_risk, .15):
        raise AssertionError('Zero-column deterministic evaluation incorrect')
    return {
        'status': 'passed',
        'gradient_relative_difference': float(relative),
        'gradient_minimum_distance_to_relu_kink': minimum_kink_distance,
        'pair_closed_vs_enumerated_max_difference': float(pair_max_difference),
        'general_bound_max_exact_minus_bound': float(max_bound_violation),
        'mono_loss': float(mono_loss), 'mono_expected_loss': expected_loss,
        'zero_column_errors': zero_risk.tolist(),
    }


if __name__ == '__main__':
    import json
    from pathlib import Path
    config = json.loads((Path(__file__).parent / 'config.json').read_text())
    print(json.dumps(run_checks(config), indent=2))
