import pandas as pd 

class Peaks(object):

	def __init__(self, series):
		series = series
		velocity = series.diff()
		self.volatility = velocity.std()
		vel_last = velocity.shift(-1)
		inertia = velocity * vel_last
		self.table = pd.concat(
			[series, velocity, inertia],
			axis=1,
			keys=['price', 'velocity', 'inertia'],
			)
		self.bounce_dates = inertia[inertia < 0].dropna().index
		bounce_prices = series[self.bounce_dates]
		bounce_inertia = -1 * inertia[self.bounce_dates]
		self.bounces = pd.concat(
			[bounce_prices, bounce_inertia],
			axis=1,
			keys=["bounce_price", "bounce_inertia"],
			)
		self.support_levels = pd.Series(
			self.bounces.bounce_inertia,
			index=self.bounces.bounce_price
			)