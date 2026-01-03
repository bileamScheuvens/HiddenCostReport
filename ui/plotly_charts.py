import plotly.graph_objects as go
from collections import defaultdict

def cost_sunburst(category_to_cost: dict):
    entries = defaultdict(int)
    parents = {}

    parents["total"] = ""
    # TODO: give this its own data structure or something, this is horrendous
    # loop over categories, compute subtotals
    for category in category_to_cost:
        parents[category] = "total"
        for (metric, lb, ub) in category_to_cost[category]:
            parents[metric] = category
            entries["total"] += lb
            entries[category] += lb
            entries[metric] += lb

    labels = []
    values = []
    for (entry, value) in entries.items():
        labels.append(entry)
        values.append(value)

    fig = go.Figure(
            data=go.Sunburst(
                labels=labels,
                # guarantee order
                parents=[parents[x] for x in entries],
                values=values,
                branchvalues="total",
    ))
    return fig
    

