import sys
import re
import os
import matplotlib.pyplot as plt
from collections import defaultdict

def parse_file(filepath):
    pattern = re.compile(
        r'CNOT:\s*(\d+),\s*depth:\s*(\d+)\s+and\s+cost\s+function:\s*(\S+)(?:\s+with\s+(\S+))?\s+occurs\s+in\s+(\d+)',
        re.IGNORECASE
    )
    records = []
    filename = os.path.basename(filepath)

    # Extract greedy name from filename
    # e.g. "Col_AES-32-block-norm_Layer_Results" → greedy = "Col"
    parts = filename.split('_')
    greedy_name = parts[0]
    matrix_name = parts[1] if len(parts) > 1 else 'unknown'  # "AES-32-block"

    with open(filepath, 'r') as f:
        for line in f:
            m = pattern.search(line)
            if m:
                records.append({
                    'cnot':   int(m.group(1)),
                    'depth':  int(m.group(2)),
                    'cost':   m.group(3),
                    'norm':   m.group(4) or 'N/A',
                    'occurs': int(m.group(5)),
                    'greedy': greedy_name,
                    'matrix': matrix_name,
                })
    return records

def plot_by_greedy(all_records):
    # Group by cost function → then by greedy algorithm
    by_cost = defaultdict(lambda: defaultdict(list))
    for r in all_records:
        cost_key = f"{r['cost']}/{r['norm']} [{r['matrix']}]"
        by_cost[cost_key][r['greedy']].append(r)

    colors  = ['#e63946', '#2a9d8f', '#f4a261', '#6a4c93']
    markers = ['o', 's', '^', 'D']

    for cost_key, greedy_dict in by_cost.items():
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title(f'Cost Function: {cost_key}', fontsize=13, fontweight='bold')
        ax.set_xlabel('Occurs In (iteration)', fontsize=11)
        ax.set_ylabel('Depth', fontsize=11)
        ax.grid(True, linestyle='--', alpha=0.4)

        for idx, (greedy_name, records) in enumerate(sorted(greedy_dict.items())):
            # Sort points by occurs so line connects in order
            records_sorted = sorted(records, key=lambda r: r['occurs'])
            x = [r['occurs'] for r in records_sorted]
            y = [r['depth']  for r in records_sorted]

            ax.plot(x, y,
                    label=greedy_name,
                    color=colors[idx % len(colors)],
                    marker=markers[idx % len(markers)],
                    linewidth=2,
                    markersize=7,
                    markeredgecolor='black',
                    markeredgewidth=0.5)

        ax.legend(title='Greedy Algorithm', fontsize=10, title_fontsize=10)
        plt.tight_layout()

        safe_cost = cost_key.replace('/', '_')
        out = f'plot_{safe_cost}.png'
        plt.savefig(out, dpi=150)
        print(f"Saved: {out}")
        plt.show()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <file1> <file2> <file3> <file4>")
        print(f"   Or: python3 {sys.argv[0]} Results/*_Layer_Results")
        sys.exit(1)

    all_records = []
    for filepath in sys.argv[1:]:
        records = parse_file(filepath)
        greedy = records[0]['greedy'] if records else '?'
        print(f"  {os.path.basename(filepath)}: {len(records)} records  (greedy={greedy})")
        all_records.extend(records)

    if not all_records:
        print("No records found. Check file format.")
        sys.exit(1)

    print(f"\nTotal: {len(all_records)} records across {len(sys.argv)-1} files")
    plot_by_greedy(all_records)
