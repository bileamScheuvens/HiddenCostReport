import plotly.graph_objects as go
import os

market_price = 8
gap = 1.321
social = 0.248
environmental = 1.073

underpayment = round(social, 3)
land_use = round(environmental * 0.75, 3)
land_transform = round(environmental * 0.03, 3)
climate = round(environmental * 0.22, 3)
water = round(environmental * 0.01, 3)

labels = [""]

fig = go.Figure()

fig.add_trace(
    go.Bar(
        name=f"Market price {market_price}€",
        x=labels,
        y=[market_price],
        marker_color="#31748f",
    )
)
fig.add_trace(
    go.Bar(
        name=f"Land use {land_use}€",
        x=labels,
        y=[land_use],
        marker_color="#9ccfd8",
    )
)
fig.add_trace(
    go.Bar(
        name=f"Land transformation {land_transform}€",
        x=labels,
        y=[land_transform],
        marker_color="#c4a7e7",
    )
)
fig.add_trace(
    go.Bar(
        name=f"Climate change {climate}€",
        x=labels,
        y=[climate],
        marker_color="#ebbcba",
    )
)
fig.add_trace(
    go.Bar(
        name=f"Underpayment of workers {underpayment}€",
        x=labels,
        y=[underpayment],
        marker_color="#f6c177",
    )
)
fig.add_trace(
    go.Bar(
        name=f"Scarce water use {water}€",
        x=labels,
        y=[water],
        marker_color="#e78284",
    )
)

fig.update_layout(
    font_color="#908caa",
    barmode="stack",
    width=450,
    title=dict(
        text="Bocca Coffee True Price",
        font=dict(size=25, color="#908caa"),
    ),
    yaxis=dict(
        title="price of beans (kg)",
        ticksuffix="€",
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    annotations=[
        dict(
            text=("data from:<br>https://www.trueprice.org/projects/bocca-coffee/"),
            x=0.05,
            y=-1,
            showarrow=False,
            align="left",
            font=dict(color="#6e6a86"),
        )
    ],
)

fig.write_image(os.path.join(os.path.dirname(__file__), "coffee_tca.png"), scale=4)


n_triples = 687425
n_subjects = 171955
n_predicates = 15
n_objects = 212785

metrics = 1000
companies = 1000
observations = 169940
