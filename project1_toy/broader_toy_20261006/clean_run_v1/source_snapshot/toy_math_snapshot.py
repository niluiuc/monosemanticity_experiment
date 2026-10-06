"""Mathematical objects for the prespecified Project 1 binary-concept experiment.

All arrays use samples as rows; W has shape (storage_dimensions, concepts).
No fitted expression or hidden postprocessing is used in risk prediction.
"""
import itertools
import numpy as np
from scipy.special import ndtr


def binary_population(n, p):
    """Enumerate the whole independent binary population and its probabilities."""
    states = np.array(list(itertools.product([0.0, 1.0], repeat=n)))
    rates = np.broadcast_to(np.asarray(p, dtype=float), (n,))
    probabilities = np.prod(np.where(states == 1, rates, 1 - rates), axis=1)
    if not np.isclose(probabilities.sum(), 1.0):
        raise ValueError("Population probabilities do not sum to one")
    return states, probabilities


def reconstruction_loss_gradient(W, bias, states, probabilities):
    """Exact population sum-of-feature MSE and its tied-encoder gradient.

    The two gradient terms account for W appearing in both encoder and decoder.
    The derivative of ReLU is taken as zero at its nondifferentiable kink.
    """
    hidden = states @ W.T
    preactivation = hidden @ W + bias
    decoded = np.maximum(preactivation, 0.0)
    residual = decoded - states
    loss = np.sum(probabilities[:, None] * residual**2)
    dz = 2 * probabilities[:, None] * residual * (preactivation > 0)
    grad_W = hidden.T @ dz + (dz @ W.T).T @ states
    grad_bias = dz.sum(axis=0)
    return float(loss), grad_W, grad_bias


def geometry(W, p):
    G = W.T @ W
    diagonal = np.diag(G).copy()
    off = G - np.diag(diagonal)
    rates = np.broadcast_to(np.asarray(p, dtype=float), diagonal.shape)
    V = (off**2) @ (rates * (1 - rates))
    B = np.max(np.abs(off), axis=1)
    row_norm = np.linalg.norm(G, axis=1)
    # NaN is honest for an unstored concept: 0/0 is not monosemanticity=1.
    alignment = np.divide(diagonal, row_norm,
                          out=np.full_like(diagonal, np.nan), where=row_norm > 0)
    threshold = off @ rates + diagonal / 2
    return G, diagonal, V, B, alignment, threshold


def exact_detection(W, states, probabilities, threshold, sigma):
    """State enumeration plus exact Gaussian integration for a fixed detector.

    Outputs per-feature error, conditional FP/FN rates, and state error matrix.
    At sigma=0 and zero columns, evaluate the strict > decision directly.
    """
    G = W.T @ W
    d = np.diag(G)
    means = states @ G.T
    errors = ((means > threshold) != states).astype(float)
    if sigma > 0:
        stored = d > 0
        signed_gap = (2 * states[:, stored] - 1) * (
            means[:, stored] - np.asarray(threshold)[stored])
        errors[:, stored] = ndtr(-signed_gap / (sigma * np.sqrt(d[stored])))
    risk = probabilities @ errors
    p = probabilities @ states
    fp = (probabilities[:, None] * errors * (1 - states)).sum(axis=0) / (1 - p)
    fn = (probabilities[:, None] * errors * states).sum(axis=0) / p
    return risk, fp, fn, errors


def interference_bound(W, p, sigma):
    """Independent-Bernoulli midpoint bound; zero columns get trivial bound 1."""
    _, d, V, B, _, _ = geometry(W, p)
    denominator = 8 * (V + sigma**2 * d + B * d / 6)
    bound = np.ones_like(d)
    regular = (d > 0) & (denominator > 0)
    bound[regular] = np.exp(-d[regular]**2 / denominator[regular])
    bound[(d > 0) & (denominator == 0)] = 0.0
    return bound


def exact_decoder_mse(W, bias, states, probabilities, sigma):
    """Exact squared error using the first two moments of a rectified Gaussian."""
    G = W.T @ W
    mu = states @ G.T + bias
    sd = sigma * np.sqrt(np.diag(G))
    first = np.maximum(mu, 0.0)
    second = first**2
    nonzero = sd > 0
    if np.any(nonzero):
        z = mu[:, nonzero] / sd[nonzero]
        density = np.exp(-0.5 * z**2) / np.sqrt(2 * np.pi)
        cdf = ndtr(z)
        first[:, nonzero] = sd[nonzero] * density + mu[:, nonzero] * cdf
        second[:, nonzero] = ((mu[:, nonzero]**2 + sd[nonzero]**2) * cdf
                             + mu[:, nonzero] * sd[nonzero] * density)
    squared_error = second - 2 * states * first + states**2
    return probabilities @ squared_error


def pair_closed_risks(p, sigma, a):
    """Sum of two errors; omitted mono concept is predicted absent.

    Pair thresholds are uncentered +/-a/2 in code space. c=1 for mono.
    """
    if sigma == 0:
        return 2 * p**2, p
    q = ndtr(-a / (2 * sigma))
    q3 = ndtr(-3 * a / (2 * sigma))
    qm = ndtr(-1 / (2 * sigma))
    pair = (2 * (1 - p)**2 * q + 2 * p * (1 - p) * (q + q3)
            + 2 * p**2 * (1 - q))
    return float(pair), float(p + qm)


def wilson_interval(count, n, z=1.959963984540054):
    rate = count / n
    denominator = 1 + z**2 / n
    center = (rate + z**2 / (2 * n)) / denominator
    radius = z * np.sqrt(rate * (1 - rate) / n + z**2 / (4 * n**2)) / denominator
    return center - radius, center + radius


def train_population(config, p, seed):
    """Fixed-step projected Adam; never selects the best-looking checkpoint."""
    n, m = config['n'], config['m']
    energy = config['encoder_energy']
    states, probabilities = binary_population(n, p)
    rng = np.random.default_rng(seed)
    W = rng.normal(size=(m, n))
    W *= np.sqrt(energy / np.sum(W**2))
    bias = np.zeros(n)
    first_W = np.zeros_like(W)
    second_W = np.zeros_like(W)
    first_bias = np.zeros_like(bias)
    second_bias = np.zeros_like(bias)
    b1, b2 = config['adam_beta1'], config['adam_beta2']
    history = []
    checkpoint_steps, checkpoint_W, checkpoint_bias = [0], [W.copy()], [bias.copy()]
    for step in range(1, config['steps'] + 1):
        loss, grad_W, grad_bias = reconstruction_loss_gradient(W, bias, states, probabilities)
        if not np.isfinite(loss) or not np.all(np.isfinite(grad_W)):
            raise FloatingPointError(f'Nonfinite training at step {step}')
        tangent = grad_W - (np.sum(grad_W * W) / energy) * W
        history.append((step - 1, loss, np.sum(W**2), np.linalg.norm(tangent),
                        np.linalg.norm(grad_bias)))
        first_W = b1 * first_W + (1 - b1) * grad_W
        second_W = b2 * second_W + (1 - b2) * grad_W**2
        first_bias = b1 * first_bias + (1 - b1) * grad_bias
        second_bias = b2 * second_bias + (1 - b2) * grad_bias**2
        lr = config['learning_rate']
        eps = config['adam_epsilon']
        W -= lr * (first_W / (1 - b1**step)) / (np.sqrt(second_W / (1 - b2**step)) + eps)
        bias -= lr * (first_bias / (1 - b1**step)) / (np.sqrt(second_bias / (1 - b2**step)) + eps)
        norm = np.linalg.norm(W)
        if norm == 0 or not np.isfinite(norm):
            raise FloatingPointError('Cannot project invalid encoder')
        W *= np.sqrt(energy) / norm
        if step % 100 == 0 or step == config['steps']:
            checkpoint_steps.append(step)
            checkpoint_W.append(W.copy())
            checkpoint_bias.append(bias.copy())
    loss, grad_W, grad_bias = reconstruction_loss_gradient(W, bias, states, probabilities)
    tangent = grad_W - (np.sum(grad_W * W) / energy) * W
    history.append((config['steps'], loss, np.sum(W**2), np.linalg.norm(tangent),
                    np.linalg.norm(grad_bias)))
    history = np.array(history)
    window = config['convergence_window']
    change = abs(history[-window:, 1].mean() - history[-2 * window:-window, 1].mean())
    return W, bias, history, {
        'steps': np.array(checkpoint_steps),
        'W': np.stack(checkpoint_W),
        'bias': np.stack(checkpoint_bias),
        'adam_first_W': first_W, 'adam_second_W': second_W,
        'adam_first_bias': first_bias, 'adam_second_bias': second_bias,
    }, {
        'final_loss': float(loss), 'minimum_recorded_loss': float(history[:, 1].min()),
        'window_mean_loss_change': float(change),
        'convergence_diagnostic_pass': bool(change <= config['convergence_absolute_tolerance']),
        'final_tangent_gradient_norm': float(np.linalg.norm(tangent)),
        'final_bias_gradient_norm': float(np.linalg.norm(grad_bias)),
    }


def mono_baseline(n, m, p, energy):
    """Restricted orthogonal code and optimal constant reconstruction for omissions."""
    W = np.zeros((m, n))
    W[:, :m] = np.eye(m) * np.sqrt(energy / m)
    bias = np.zeros(n)
    bias[m:] = p
    return W, bias
