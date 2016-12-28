import plotly.graph_objs as go
import plotly.offline as opy

from utils.naive_bayes import bayes, Data


def accuracy_chart():
    default = bayes[Data.DEFAULT].score
    summarized = bayes[Data.SUMMARIZED].score
    multiplied = bayes[Data.MULTIPLIED].score
    trace = go.Bar(
        x=['Default', 'Summarized', 'Multiplied'],
        y=[default, summarized, multiplied],
        text=['While making prediction takes into account champion, winrate, total games and team of blue and red team',
              'While making prediction takes into account summarized winrates of blue and red team',
              'While making prediction takes into account multiplied winrates and total games of blue and red team'],
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity=0.6
    )

    data = go.Data([trace])
    layout = go.Layout(title="Bayes method accuracy", yaxis={'title': 'Accuracy'})
    figure = go.Figure(data=data, layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div')

    return div


def split_chart():
    trace1 = go.Bar(
        x=['Total games'],
        y=[400],
        name='Training games'
    )
    trace2 = go.Bar(
        x=['Total games'],
        y=[100],
        name='Test games'
    )

    data = go.Data([trace1, trace2])
    layout = go.Layout(title="Spliting data into test and training sets", yaxis={'title': 'Games'}, barmode='stack')
    figure = go.Figure(data=data, layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div')
    return div
