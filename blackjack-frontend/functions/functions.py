import plotly.offline as pyo
import plotly.graph_objs as go

def get_html(df):

    fig = go.Figure()
    data = []
    for col in df.columns:
        fig.add_trace(go.Scatter(x=list(df.index), y=df[col].tolist(),
                      mode='lines+markers',
                      name=col))

        # Create traces
        trace = go.Scatter(
            x=list(df.index),
            y=df[col].tolist(),
            mode='lines',
            name=col
        )

        data.append(trace)
    
    return pyo.plot(data, include_plotlyjs=False, output_type='div')