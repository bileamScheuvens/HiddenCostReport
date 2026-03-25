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
        name=f"{market_price}€ Market price",
        x=labels,
        y=[market_price],
        marker_color="#31748f",
    )
)
fig.add_trace(
    go.Bar(
        name=f"{land_use}€ Land use",
        x=labels,
        y=[land_use],
        marker_color="#907aa9",
    )
)
fig.add_trace(
    go.Bar(
        name=f"{land_transform}€ Land transformation",
        x=labels,
        y=[land_transform],
        marker_color="#c4a7e7",
    )
)
fig.add_trace(
    go.Bar(
        name=f"{climate}€ Climate change",
        x=labels,
        y=[climate],
        marker_color="#ebbcba",
    )
)
fig.add_trace(
    go.Bar(
        name=f"{underpayment}€ Underpayment of workers",
        x=labels,
        y=[underpayment],
        marker_color="#e78284",
    )
)
fig.add_trace(
    go.Bar(
        name=f"{water}€ Scarce water use",
        x=labels,
        y=[water],
        marker_color="#9ccfd8",
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
        tickvals=[
            0,
            2,
            4,
            6,
            8,
            market_price + underpayment + climate + land_transform + water + land_use,
        ],
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

#####################
### Approximation ###
#####################

proportion = 8 / 6900000

water_approx = round(1000 * 5 * proportion, 3)
electricity_approx = round(100 * 70 * proportion, 2)
emission_approx = round(1000 * 300 * proportion, 2)


labels = ["trueprice.org", "approximation"]

fig = go.Figure()

fig.add_trace(
    go.Bar(
        name=f"{market_price}€ Market price",
        x=labels,
        y=[market_price, market_price],
        marker_color="#31748f",
    )
)
fig.add_trace(
    go.Bar(
        name=f"{land_use}€ | ?  Land use",
        x=labels,
        y=[land_use, 0],
        marker_color="#907aa9",
    )
)
fig.add_trace(
    go.Bar(
        name=f"{land_transform}€ | ? Land transformation",
        x=labels,
        y=[land_transform, 0],
        marker_color="#c4a7e7",
    )
)
fig.add_trace(
    go.Bar(
        name=f"{climate}€ | ? Climate change",
        x=labels,
        y=[climate, 0],
        marker_color="#ebbcba",
    )
)
fig.add_trace(
    go.Bar(
        name=f"0          | {emission_approx}$  Emission",
        x=labels,
        y=[0, emission_approx],
        marker_color="#ebbcba",
    )
)
fig.add_trace(
    go.Bar(
        name=f"{underpayment}€ | ? Underpayment of workers",
        x=labels,
        y=[underpayment, 0],
        marker_color="#e78284",
    )
)
fig.add_trace(
    go.Bar(
        name=f"{water}€ | {water_approx}$ Water use",
        x=labels,
        y=[water, water_approx],
        marker_color="#9ccfd8",
    )
)
fig.add_trace(
    go.Bar(
        name=f"0          | {electricity_approx}$ Electricity use ",
        x=labels,
        y=[0, electricity_approx],
        marker_color="#f6c177",
    )
)

fig.update_layout(
    font_color="#908caa",
    barmode="stack",
    width=450,
    title=dict(
        text="Bocca Coffee True Price Approximation",
        font=dict(size=20, color="#908caa"),
    ),
    yaxis=dict(
        title="price of beans (kg)",
        ticksuffix="€",
        tickvals=[
            0,
            2,
            4,
            6,
            market_price + emission_approx + electricity_approx + water_approx,
            market_price + underpayment + climate + land_transform + land_use,
        ],
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    annotations=[
        dict(
            text=(""),
            x=0.05,
            y=-1,
            showarrow=False,
            align="left",
            font=dict(color="#6e6a86"),
        )
    ],
)

fig.write_image(os.path.join(os.path.dirname(__file__), "coffee_approx.png"), scale=4)
