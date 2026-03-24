"""Generate all figures for PHE documentation."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import math
import os

BASE = r"D:\Dropbox\GitHub\DWSIM_AI_Suite_Documentation\docs_phe"
os.makedirs(f"{BASE}/assets", exist_ok=True)
os.makedirs(f"{BASE}/theory/img", exist_ok=True)
os.makedirs(f"{BASE}/user-guide/img", exist_ok=True)
os.makedirs(f"{BASE}/validation/img", exist_ok=True)

plt.rcParams.update({
    'font.family': 'sans-serif', 'font.size': 11,
    'axes.grid': True, 'grid.alpha': 0.3,
    'figure.facecolor': 'white'
})

# 1. Workflow Diagram
fig, ax = plt.subplots(figsize=(10, 4))
ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis('off')
boxes = [
    (0.5, 1.5, 'Inlet\nConditions', '#00897B'),
    (2.5, 1.5, 'Plate\nGeometry', '#00897B'),
    (4.5, 1.5, 'Heat Transfer\nCoefficients', '#00695C'),
    (6.5, 1.5, 'e-NTU\nSolver', '#004D40'),
    (8.5, 1.5, 'Outlet T\nQ, dP', '#E65100'),
]
for x, y, txt, color in boxes:
    rect = mpatches.FancyBboxPatch((x-0.7, y-0.5), 1.4, 1.0,
        boxstyle="round,pad=0.1", facecolor=color, edgecolor='white', linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y, txt, ha='center', va='center', fontsize=9, fontweight='bold', color='white')
for i in range(4):
    ax.annotate('', xy=(boxes[i+1][0]-0.7, boxes[i+1][1]),
        xytext=(boxes[i][0]+0.7, boxes[i][1]),
        arrowprops=dict(arrowstyle='->', color='#00897B', lw=2))
ax.text(5, 3.5, 'Plate Heat Exchanger - Calculation Workflow',
    ha='center', va='center', fontsize=14, fontweight='bold', color='#004D40')
plt.tight_layout()
fig.savefig(f"{BASE}/assets/workflow_diagram.png", dpi=150, bbox_inches='tight')
plt.close()
print("1. workflow_diagram.png OK")

# 2. Counterflow Temperature Diagram
fig, ax = plt.subplots(figsize=(7, 4.5))
x = np.linspace(0, 1, 50)
Th = 80 - (80 - 30.6) * x
Tc = 69.4 - (69.4 - 20) * x
ax.plot(x, Th, 'r-', linewidth=2.5, label='Hot Stream')
ax.plot(x, Tc, 'b-', linewidth=2.5, label='Cold Stream')
ax.fill_between(x, Th, Tc, alpha=0.1, color='orange')
ax.set_xlabel('Position along exchanger', fontsize=12)
ax.set_ylabel('Temperature (C)', fontsize=12)
ax.set_title('Counterflow Temperature Profile', fontsize=13, fontweight='bold')
ax.legend(fontsize=11)
plt.tight_layout()
fig.savefig(f"{BASE}/theory/img/counterflow_diagram.png", dpi=150, bbox_inches='tight')
plt.close()
print("2. counterflow_diagram.png OK")

# 3. Co-current Temperature Diagram
fig, ax = plt.subplots(figsize=(7, 4.5))
Th = 80 - (80 - 50.0) * (1 - np.exp(-3*x))
Tc = 20 + (50.0 - 20) * (1 - np.exp(-3*x))
ax.plot(x, Th, 'r-', linewidth=2.5, label='Hot Stream')
ax.plot(x, Tc, 'b-', linewidth=2.5, label='Cold Stream')
ax.fill_between(x, Th, Tc, alpha=0.1, color='orange')
ax.axhline(y=50, color='gray', linestyle='--', alpha=0.5, label='Mean Temperature')
ax.set_xlabel('Position along exchanger', fontsize=12)
ax.set_ylabel('Temperature (C)', fontsize=12)
ax.set_title('Co-current Temperature Profile (Cr = 1)', fontsize=13, fontweight='bold')
ax.legend(fontsize=11)
plt.tight_layout()
fig.savefig(f"{BASE}/theory/img/cocurrent_diagram.png", dpi=150, bbox_inches='tight')
plt.close()
print("3. cocurrent_diagram.png OK")

# 4. Plate Geometry Schematic
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(-1, 11); ax.set_ylim(-1, 8); ax.axis('off'); ax.set_aspect('equal')
colors = ['#E53935', '#1E88E5', '#E53935', '#1E88E5', '#E53935']
for i in range(6):
    px = 1 + i * 1.5
    rect = mpatches.Rectangle((px, 0), 0.15, 6, facecolor='#78909C', edgecolor='#37474F', linewidth=1.5)
    ax.add_patch(rect)
    if i < 5:
        color = colors[i]
        rect2 = mpatches.Rectangle((px+0.15, 0), 1.35, 6, facecolor=color, alpha=0.3, edgecolor='none')
        ax.add_patch(rect2)
        cx = px + 0.15 + 0.675
        ax.text(cx, 3, 'H' if color == '#E53935' else 'C', ha='center', va='center',
            fontsize=14, fontweight='bold', color=color, alpha=0.8)
ax.annotate('', xy=(2.65, -0.5), xytext=(1.15, -0.5),
    arrowprops=dict(arrowstyle='<->', color='#333', lw=1.5))
ax.text(1.9, -0.9, 'b (spacing)', ha='center', fontsize=10, color='#333')
ax.annotate('', xy=(10.4, 0), xytext=(10.4, 6),
    arrowprops=dict(arrowstyle='<->', color='#333', lw=1.5))
ax.text(10.8, 3, 'L\n(height)', ha='center', va='center', fontsize=10, color='#333')
ax.set_title('Plate Heat Exchanger - Channel Formation', fontsize=13, fontweight='bold', pad=20)
hot_patch = mpatches.Patch(facecolor='#E53935', alpha=0.3, label='Hot channels')
cold_patch = mpatches.Patch(facecolor='#1E88E5', alpha=0.3, label='Cold channels')
plate_patch = mpatches.Patch(facecolor='#78909C', label='Plates')
ax.legend(handles=[hot_patch, cold_patch, plate_patch], loc='upper right', fontsize=10)
plt.tight_layout()
fig.savefig(f"{BASE}/theory/img/plate_geometry.png", dpi=150, bbox_inches='tight')
plt.close()
print("4. plate_geometry.png OK")

# 5. e-NTU Curves
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
NTU = np.linspace(0, 6, 200)
Cr_vals = [0, 0.25, 0.5, 0.75, 1.0]
colors_cr = ['#004D40', '#00897B', '#26A69A', '#80CBC4', '#B2DFDB']
for Cr, c in zip(Cr_vals, colors_cr):
    if abs(Cr - 1) < 1e-6:
        eps = NTU / (1 + NTU)
    else:
        exp_t = np.exp(-NTU * (1 - Cr))
        eps = (1 - exp_t) / (1 - Cr * exp_t)
    ax1.plot(NTU, eps, color=c, linewidth=2, label=f'Cr = {Cr}')
ax1.set_xlabel('NTU', fontsize=12); ax1.set_ylabel('Effectiveness', fontsize=12)
ax1.set_title('Counterflow', fontsize=13, fontweight='bold')
ax1.legend(fontsize=10); ax1.set_ylim(0, 1.05)
for Cr, c in zip(Cr_vals, colors_cr):
    exp_t = np.exp(-NTU * (1 + Cr))
    eps = (1 - exp_t) / (1 + Cr)
    ax2.plot(NTU, eps, color=c, linewidth=2, label=f'Cr = {Cr}')
ax2.set_xlabel('NTU', fontsize=12); ax2.set_ylabel('Effectiveness', fontsize=12)
ax2.set_title('Co-current', fontsize=13, fontweight='bold')
ax2.legend(fontsize=10); ax2.set_ylim(0, 1.05)
fig.suptitle('Effectiveness-NTU Relationships', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
fig.savefig(f"{BASE}/theory/img/entu_curves.png", dpi=150, bbox_inches='tight')
plt.close()
print("5. entu_curves.png OK")

# 6. Friction Factor vs Reynolds
fig, ax = plt.subplots(figsize=(7, 4.5))
Re = np.logspace(0.5, 4, 500)
f = np.piecewise(Re,
    [Re < 10, (Re >= 10) & (Re < 100), Re >= 100],
    [lambda r: 50.0/r, lambda r: 19.4/r**0.589, lambda r: 2.99/r**0.183])
for beta, c, ls in [(30, '#004D40', '-'), (45, '#00897B', '-'), (60, '#26A69A', '-')]:
    ax.loglog(Re, f * (30.0/beta), ls, color=c, linewidth=2, label=f'beta = {beta} deg')
ax.set_xlabel('Reynolds Number', fontsize=12)
ax.set_ylabel('Fanning Friction Factor f', fontsize=12)
ax.set_title('Friction Factor vs Reynolds Number', fontsize=13, fontweight='bold')
ax.legend(fontsize=11); ax.set_xlim(3, 10000)
plt.tight_layout()
fig.savefig(f"{BASE}/theory/img/friction_factor.png", dpi=150, bbox_inches='tight')
plt.close()
print("6. friction_factor.png OK")

# 7. Nusselt vs Reynolds
def calc_nu(Re, Pr, beta):
    beta_rad = math.radians(beta)
    if Re < 10: C, n = 0.291, 0.3
    elif Re < 200:
        C = 0.578 * math.sin(2*beta_rad)**0.2; n = 0.4
    else:
        C = 0.2 + 0.0577 * math.sin(math.pi*beta/45 + 2.37); n = 0.667
    return max(C * Re**n * Pr**(1/3), 1.0)

fig, ax = plt.subplots(figsize=(7, 4.5))
Re_arr = np.logspace(0.5, 4, 500)
for beta, c in [(30, '#004D40'), (45, '#00897B'), (60, '#26A69A')]:
    Nu = [calc_nu(r, 4.0, beta) for r in Re_arr]
    ax.loglog(Re_arr, Nu, '-', color=c, linewidth=2, label=f'beta = {beta} deg (Pr=4)')
ax.set_xlabel('Reynolds Number', fontsize=12)
ax.set_ylabel('Nusselt Number', fontsize=12)
ax.set_title('Martin (1996) Nusselt Correlation', fontsize=13, fontweight='bold')
ax.legend(fontsize=11); ax.set_xlim(3, 10000)
plt.tight_layout()
fig.savefig(f"{BASE}/theory/img/nusselt_correlation.png", dpi=150, bbox_inches='tight')
plt.close()
print("7. nusselt_correlation.png OK")

# 8. Validation Error Chart
fig, ax = plt.subplots(figsize=(8, 4.5))
tests = ['Test 1\nCF Bal', 'Test 2\nCF Unbal', 'Test 3\n25 plates', 'Test 4\nCC Bal', 'Test 5\nLab-scale']
T_err = [0.01, 0.02, 0.01, 0.03, 0.01]
x_pos = np.arange(len(tests))
bars = ax.bar(x_pos, [e*100 for e in T_err], 0.5, color='#00897B', alpha=0.8, edgecolor='#004D40')
ax.axhline(y=2.0, color='#E65100', linestyle='--', linewidth=1.5, label='Acceptance: 2%')
ax.set_xlabel('Test Case', fontsize=12); ax.set_ylabel('Error (%)', fontsize=12)
ax.set_title('Validation Results - Energy Balance Error', fontsize=13, fontweight='bold')
ax.set_xticks(x_pos); ax.set_xticklabels(tests, fontsize=9)
ax.set_ylim(0, 3); ax.legend(fontsize=11)
for bar, val in zip(bars, [e*100 for e in T_err]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
        f'{val:.2f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
plt.tight_layout()
fig.savefig(f"{BASE}/validation/img/validation_errors.png", dpi=150, bbox_inches='tight')
plt.close()
print("8. validation_errors.png OK")

# 9. Heat Leak Sensitivity
fig, ax = plt.subplots(figsize=(7, 4.5))
HL = [0, 5, 10, 20, 50]
Th_out = [39.65, 39.05, 38.45, 37.25, 33.64]
Tc_out = [65.86, 65.27, 64.69, 63.51, 59.98]
ax.plot(HL, Th_out, 'rs-', linewidth=2, markersize=8, label='Hot outlet (Port 1)')
ax.plot(HL, Tc_out, 'b^-', linewidth=2, markersize=8, label='Cold outlet (Port 2)')
ax.set_xlabel('Heat Leak (kW)', fontsize=12)
ax.set_ylabel('Outlet Temperature (C)', fontsize=12)
ax.set_title('Heat Leak Sensitivity - Both Streams Affected', fontsize=13, fontweight='bold')
ax.legend(fontsize=11)
plt.tight_layout()
fig.savefig(f"{BASE}/validation/img/heatleak_sensitivity.png", dpi=150, bbox_inches='tight')
plt.close()
print("9. heatleak_sensitivity.png OK")

# 10. T-Q Diagram Example (Counterflow - hot always above cold)
fig, ax = plt.subplots(figsize=(7, 4.5))
Q_total = 206.6  # kW
Q_vals = np.linspace(0, Q_total, 50)
Cp = 4.18  # kJ/(kg.K), m=1 kg/s
# Hot: enters at 80C, exits at ~30.6C. T decreases with cumulative Q.
Th = 80 - Q_vals / (1.0 * Cp)
# Cold (counterflow): enters at 20C at Q=Q_total end, exits at ~69.4C at Q=0 end.
# In T-Q diagram for counterflow, cold curve goes from Tc_out at Q=0 to Tc_in at Q=Qmax.
Tc = 69.4 - Q_vals / (1.0 * Cp)
ax.plot(Q_vals, Th, 'r-', linewidth=2.5, label='Hot Stream')
ax.plot(Q_vals, Tc, 'b-', linewidth=2.5, label='Cold Stream')
ax.fill_between(Q_vals, Th, Tc, alpha=0.08, color='teal')
# Annotate MITA
ax.annotate('MITA', xy=(Q_total*0.95, (Th[-1]+Tc[-1])/2), fontsize=11,
    fontweight='bold', color='#E65100', ha='center')
ax.set_xlabel('Cumulative Heat Duty Q (kW)', fontsize=12)
ax.set_ylabel('Temperature (C)', fontsize=12)
ax.set_title('T-Q Diagram - Counterflow (50 plates, 1 kg/s water)', fontsize=12, fontweight='bold')
ax.legend(fontsize=11)
plt.tight_layout()
fig.savefig(f"{BASE}/user-guide/img/tq_diagram_example.png", dpi=150, bbox_inches='tight')
plt.close()
print("10. tq_diagram_example.png OK")

# 11. Chevron Plate Detail
fig, ax = plt.subplots(figsize=(6, 5))
ax.set_xlim(0, 5); ax.set_ylim(0, 7); ax.axis('off'); ax.set_aspect('equal')
plate = mpatches.FancyBboxPatch((0.5, 0.5), 4, 6, boxstyle="round,pad=0.2",
    facecolor='#B0BEC5', edgecolor='#37474F', linewidth=2)
ax.add_patch(plate)
for y in np.arange(1.5, 6.0, 0.4):
    x1 = np.linspace(0.8, 4.2, 30)
    y1 = y + 0.15 * np.sin(2 * np.pi * x1 / 1.2)
    ax.plot(x1, y1, '-', color='#546E7A', linewidth=0.8, alpha=0.6)
for (cx, cy) in [(1.5, 6.2), (3.5, 6.2), (1.5, 0.8), (3.5, 0.8)]:
    circle = plt.Circle((cx, cy), 0.25, facecolor='white', edgecolor='#37474F', linewidth=1.5)
    ax.add_patch(circle)
ax.text(3.0, 2.7, 'beta', fontsize=14, fontweight='bold', color='#E65100')
ax.set_title('Chevron Plate Geometry', fontsize=13, fontweight='bold', pad=10)
plt.tight_layout()
fig.savefig(f"{BASE}/theory/img/chevron_plate.png", dpi=150, bbox_inches='tight')
plt.close()
print("11. chevron_plate.png OK")

# 12. Theory Overview
fig, ax = plt.subplots(figsize=(9, 3.5))
ax.set_xlim(0, 9); ax.set_ylim(0, 3.5); ax.axis('off')
topics = [
    (1, 1.75, 'Fundamentals\n& Geometry', '#00897B'),
    (3, 1.75, 'Heat Transfer\nCorrelations', '#00796B'),
    (5, 1.75, 'e-NTU\nMethod', '#00695C'),
    (7, 1.75, 'Pressure\nDrop', '#004D40'),
]
for xp, yp, txt, color in topics:
    rect = mpatches.FancyBboxPatch((xp-0.8, yp-0.55), 1.6, 1.1,
        boxstyle="round,pad=0.1", facecolor=color, edgecolor='white', linewidth=2)
    ax.add_patch(rect)
    ax.text(xp, yp, txt, ha='center', va='center', fontsize=9, fontweight='bold', color='white')
for i in range(3):
    ax.annotate('', xy=(topics[i+1][0]-0.8, topics[i+1][1]),
        xytext=(topics[i][0]+0.8, topics[i][1]),
        arrowprops=dict(arrowstyle='->', color='#00897B', lw=2))
ax.text(4.5, 3.2, 'PHE Theory - Chapter Overview', ha='center', fontsize=13, fontweight='bold', color='#004D40')
plt.tight_layout()
fig.savefig(f"{BASE}/theory/img/theory_overview.png", dpi=150, bbox_inches='tight')
plt.close()
print("12. theory_overview.png OK")

print("\nAll 12 figures generated successfully!")
