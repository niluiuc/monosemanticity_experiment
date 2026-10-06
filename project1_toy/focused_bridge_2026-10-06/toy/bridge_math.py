"""Local weighted training and exhaustive scalar ReLU-bias minimization.

Original infrastructure is preserved as toy_math_snapshot.py. No fitting is used.
Bias minimization is exact finite candidate enumeration, subject to float64 error.
"""
import numpy as np
from toy_math_snapshot import reconstruction_loss_gradient, train_population


def weighted_loss_gradient(W, bias, states, probabilities, importance):
    hidden = states @ W.T
    z = hidden @ W + bias
    residual = np.maximum(z, 0) - states
    weights = probabilities[:, None] * np.asarray(importance)[None, :]
    loss = np.sum(weights * residual**2)
    dz = 2 * weights * residual * (z > 0)
    grad_W = hidden.T @ dz + (dz @ W.T).T @ states
    return float(loss), grad_W, dz.sum(axis=0)


def scalar_bias_optimum(offsets, targets, probabilities):
    """Enumerate stationary candidates and all breakpoints of piecewise quadratics.

    Returns every numerically tied finite minimizer and the all-off plateau if
    globally tied. For reproducibility chooses smallest finite minimizer; if the
    plateau wins, its boundary is a valid finite minimizer and is retained.
    Targets here are binary/nonnegative; the routine does not assume convexity.
    """
    offsets = np.asarray(offsets, dtype=float)
    targets = np.asarray(targets, dtype=float)
    probabilities = np.asarray(probabilities, dtype=float)
    breaks = np.unique(-offsets)
    candidates = list(breaks)
    intervals = []
    edges = np.r_[-np.inf, breaks, np.inf]
    for lo, hi in zip(edges[:-1], edges[1:]):
        midpoint = (hi - 1 if not np.isfinite(lo) else
                    lo + 1 if not np.isfinite(hi) else (lo + hi) / 2)
        active = offsets + midpoint > 0
        A = float(probabilities[active].sum())
        B = float(np.sum(probabilities[active] * (offsets[active] - targets[active])))
        stationary = -B / A if A > 0 else None
        if stationary is not None and lo <= stationary <= hi:
            candidates.append(stationary)
        intervals.append({'lower': float(lo), 'upper': float(hi),
                          'active': active.tolist(), 'quadratic_A': A,
                          'linear_half_B': B, 'stationary': stationary})
    candidates = np.unique(candidates)
    losses = np.array([np.sum(probabilities *
                            (np.maximum(offsets + beta, 0) - targets)**2)
                       for beta in candidates])
    best = float(losses.min())
    tolerance = 1e-12 * max(1., abs(best))
    tied = candidates[abs(losses - best) <= tolerance]
    plateau_loss = float(np.sum(probabilities * targets**2))
    plateau_tied = abs(plateau_loss - best) <= tolerance
    chosen = float(tied[0])
    return chosen, best, {
        'finite_candidates': candidates.tolist(), 'candidate_losses': losses.tolist(),
        'tied_finite_minimizers': tied.tolist(), 'tie_tolerance': tolerance,
        'all_off_plateau_tied': bool(plateau_tied),
        'all_off_plateau_upper': float(breaks[0]),
        'all_off_plateau_loss': plateau_loss, 'intervals': intervals,
    }


def optimal_biases(W, states, probabilities, importance):
    offsets = states @ (W.T @ W)
    results = [scalar_bias_optimum(offsets[:, i], states[:, i], probabilities)
               for i in range(states.shape[1])]
    bias = np.array([r[0] for r in results])
    individual_loss = np.array([r[1] for r in results])
    return bias, float(np.asarray(importance) @ individual_loss), [r[2] for r in results]


def train_weighted(config, p, importance, seed):
    """Mirror original fixed-step projected Adam using local weighted gradients.

    Save every pre-update loss, gradient norms and energy, then final iterate.
    Numerical failures are returned with the actual failure step and raw state.
    """
    from toy_math_snapshot import binary_population
    states, probabilities = binary_population(config['n'], p)
    rng = np.random.default_rng(seed)
    W = rng.normal(size=(config['m'], config['n']))
    W *= np.sqrt(config['encoder_energy'] / np.sum(W**2))
    bias = np.zeros(config['n'])
    first_W = np.zeros_like(W); second_W = np.zeros_like(W)
    first_bias = np.zeros_like(bias); second_bias = np.zeros_like(bias)
    history = []
    ck_steps, ck_W, ck_bias = [0], [W.copy()], [bias.copy()]
    b1, b2 = config['adam_beta1'], config['adam_beta2']
    failure = None
    for step in range(1, config['steps'] + 1):
        loss, gW, gb = weighted_loss_gradient(W, bias, states, probabilities, importance)
        tangent = gW - np.sum(gW * W) / config['encoder_energy'] * W
        history.append((step - 1, loss, np.sum(W**2), np.linalg.norm(tangent), np.linalg.norm(gb)))
        if not np.isfinite(loss) or not np.all(np.isfinite(gW)) or not np.all(np.isfinite(gb)):
            failure = f'Nonfinite loss/gradient at pre-update step {step-1}'
            break
        first_W = b1 * first_W + (1-b1) * gW
        second_W = b2 * second_W + (1-b2) * gW**2
        first_bias = b1 * first_bias + (1-b1) * gb
        second_bias = b2 * second_bias + (1-b2) * gb**2
        correction1, correction2 = 1-b1**step, 1-b2**step
        W -= config['learning_rate'] * first_W/correction1 / (np.sqrt(second_W/correction2) + config['adam_epsilon'])
        bias -= config['learning_rate'] * first_bias/correction1 / (np.sqrt(second_bias/correction2) + config['adam_epsilon'])
        norm = np.linalg.norm(W)
        if norm == 0 or not np.isfinite(norm):
            failure = f'Invalid encoder projection at update step {step}'
            break
        W *= np.sqrt(config['encoder_energy']) / norm
        if step % 100 == 0 or step == config['steps']:
            ck_steps.append(step); ck_W.append(W.copy()); ck_bias.append(bias.copy())
    loss, gW, gb = weighted_loss_gradient(W, bias, states, probabilities, importance)
    tangent = gW - np.sum(gW * W) / config['encoder_energy'] * W
    history.append((step, loss, np.sum(W**2), np.linalg.norm(tangent), np.linalg.norm(gb)))
    history = np.asarray(history)
    window = config['convergence_window']
    change = abs(history[-window:, 1].mean() - history[-2*window:-window, 1].mean()) if len(history) >= 2*window else float('nan')
    diagnostics = {'failure': failure, 'final_step': step, 'final_loss': float(loss),
                   'minimum_recorded_loss': float(np.nanmin(history[:, 1])),
                   'window_mean_loss_change': float(change),
                   'convergence_diagnostic_pass': bool(failure is None and change <= config['convergence_absolute_tolerance']),
                   'final_tangent_gradient_norm': float(np.linalg.norm(tangent)),
                   'final_bias_gradient_norm': float(np.linalg.norm(gb))}
    checkpoints = {'steps': np.asarray(ck_steps), 'W': np.stack(ck_W), 'bias': np.stack(ck_bias),
                   'adam_first_W': first_W, 'adam_second_W': second_W,
                   'adam_first_bias': first_bias, 'adam_second_bias': second_bias}
    return W, bias, history, checkpoints, diagnostics
