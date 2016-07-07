import peak
import pandas as pd
import numpy as np
import pytest

def RandomWalk(N=100, d=1):
    """
    Use np.cumsum and np.random.uniform to generate
    a 2D random walk of length N, each of which has a random DeltaX and
    DeltaY between -1/2 and 1/2.  You'll want to generate an array of 
    shape (N,d), using (for example), random.uniform(min, max, shape).
    """
    return np.cumsum(np.random.uniform(-0.5,0.5,(N,d)))

def RandomSecurity(N=100, freq="D"):
	data = RandomWalk(N = N)
	index = pd.date_range('1/1/2016', periods=N, freq=freq)
	return pd.Series(data, index=index)
	
@pytest.fixture(params=[100])
def histdata(request):
	sec = RandomSecurity(N=request.param)
	return sec

def test_init(histdata):
	foo = peak.Peaks(histdata)
	print(foo.table)
	print(foo.bounces)
	print(foo.support_levels)

def subplot_bounces(series, name):
	return { 'x': series.index, 'y': series.values, 'name': name, 'mode': 'markers' }

def do_bounce_plot(histdata):
	peaks = peak.Peaks(histdata)
	ema = pd.ewma(histdata, span=7.0)
	ema_peaks = peak.Peaks(ema)
	fig = {
		'data': [ subplot_bounces(series, name)
			for (series, name) in zip(
				[ histdata, peaks.bounce.bounce_price, ema, ema_peaks.bounce.bounce_price ],
				[ 'price', 'bounce', 'ema', 'ema_bounce' ],
				)
			],
		'layout': {
			'xaxis': {'title': "Date"},
			'yaxis': {'title': "Price"},
		}
	}
	py.plot(fig, filename="random-financial")

def subplot_support(df, name, span=1):
	return {
		'x': df.bounce_price,
		'y': df.bounce_inertia * span,
		'name': name,
		'mode': 'markers',
	}

def subplot_support_ema(histdata, span):
	ema = pd.ewma(histdata, span=span)
	peaks = peak.Peaks(ema)
	df = peaks.bounces
	name = "ema{}".format(span)
	return subplot_support(df, name, span)

def do_support_plot(histdata, spans=[7.0, 20.0, 50.0]):
	instant_peaks = peak.Peaks(histdata)
	fig = {
		'data': [
			subplot_support(instant_peaks.bounces, 'instant')
		] + [
			subplot_support_ema(histdata, span) for span in spans
		],
		'layout': {
			'xaxis': {'title': "Price"},
			'yaxis': {'title': "Bounce Inertia"},
		}
	}
	py.plot(fig, filename="random-support")

if __name__ == "__main__":
	import plotly.plotly as py

	histdata = RandomSecurity()
	do_support_plot(histdata)
