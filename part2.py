import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


def model(t, y, b, d, delta, tau):
    H, I = y
    dH = (b - d) * H - delta * I
    dI = tau * I * (H - I) - (delta + d) * I
    return [dH, dI]


def fixed_point(b, d, delta, tau):
    H = delta * (delta + d) / (tau * (delta + d - b))
    I = (b - d) * (delta + d) / (tau * (delta + d - b))
    return H, I


def solve(params, y0, T):
    t = np.linspace(0, T, 4000)
    sol = solve_ivp(model, (0, T), y0, args=params, t_eval=t, rtol=1e-9, atol=1e-11)
    return sol.t, sol.y[0], sol.y[1]


y0 = [4, 1]

states = [
    ("S1: b < d", (1, 1.5, 1.5, 1), 15),
    ("S2: d < b < d + δ", (1, 0.8, 1, 1), 60),
    ("S3: b > d + δ", (3, 1, 1.5, 1), 6),
]

fig, axes = plt.subplots(1, 3, figsize=(16, 4.6))
for ax, (name, params, T) in zip(axes, states):
    t, H, I = solve(params, y0, T)
    ax.plot(t, H, label="H(t)")
    ax.plot(t, I, label="I(t)")
    if name.startswith("S2"):
        Hs, Is = fixed_point(*params)
        ax.axhline(Hs, color="tab:blue", ls=":", label=f"H* = {Hs:.2f}")
        ax.axhline(Is, color="tab:orange", ls=":", label=f"I* = {Is:.2f}")
    if name.startswith("S3"):
        ax.set_yscale("log")
    b, d, delta, tau = params
    ax.set_title(f"{name}  (b={b}, d={d}, δ={delta}, τ={tau})")
    ax.set_xlabel("Time, t")
    ax.legend()
axes[0].set_ylabel("Population")
plt.tight_layout()
plt.savefig("fig7_1.png", dpi=150)
plt.show()


params = (1, 0.8, 1, 1)
Hs, Is = fixed_point(*params)

Hg, Ig = np.meshgrid(np.linspace(0, 11.5, 220), np.linspace(0, 8, 220))
U, V = model(0, [Hg, Ig], *params)

plt.figure(figsize=(7.5, 5.5))
plt.streamplot(Hg, Ig, U, V, color="0.8", density=1.2, linewidth=0.6, arrowsize=0.7)
starts = [(2.6, 0.45), (1.9, 0.3), (3.5, 1.5), (0.3, 0.05), (0.05, 0.02), (8, 6)]
for start in starts:
    t, H, I = solve(params, list(start), 120)
    plt.plot(H, I, lw=1.4)
    plt.plot(*start, "k.", ms=7)
plt.plot(Hs, Is, "o", ms=10, color="k", label=f"P2 = ({Hs:.2f}, {Is:.2f}), stable spiral")
plt.plot(0, 0, "o", ms=10, mfc="w", mec="k", mew=2, label="P1 = (0, 0), saddle")
plt.xlim(-0.2, 11.5)
plt.ylim(-0.15, 8)
plt.xlabel("Healthy rabbits, H")
plt.ylabel("Infected rabbits, I")
plt.title("Trajectories from different starting points (b=1, d=0.8, δ=1, τ=1)")
plt.legend(loc="upper left")
plt.tight_layout()
plt.savefig("fig7_2.png", dpi=150)
plt.show()


fig, axes = plt.subplots(1, 3, figsize=(16, 4.6))
for tau, colour in zip([1, 0.5, 0.25], ["tab:blue", "tab:orange", "tab:green"]):
    params = (1, 0.8, 1, tau)
    Hs, Is = fixed_point(*params)
    t, H, I = solve(params, y0, 80)
    axes[0].plot(t, H, color=colour, label=f"τ = {tau}  (H* = {Hs:.2f})")
    axes[0].axhline(Hs, color=colour, ls=":")
    axes[1].plot(t, I, color=colour, label=f"τ = {tau}  (I* = {Is:.2f})")
    axes[1].axhline(Is, color=colour, ls=":")
    axes[2].plot(t, I / H, color=colour, label=f"τ = {tau}")
axes[2].axhline(0.2, color="k", ls=":", label="(b - d)/δ = 0.2")
axes[0].set_ylabel("Healthy rabbits, H")
axes[1].set_ylabel("Infected rabbits, I")
axes[2].set_ylabel("Fraction I/H")
for ax in axes:
    ax.set_xlabel("Time, t")
    ax.legend()
fig.suptitle("Effect of lowering τ (b=1, d=0.8, δ=1, H0=4, I0=1)")
plt.tight_layout()
plt.savefig("fig7_3.png", dpi=150)
plt.show()
