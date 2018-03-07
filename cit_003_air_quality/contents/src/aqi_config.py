from bisect import bisect
import logging
import sys
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

####
## AQI Calculation from BlueRaster
####

# EPA breakpoints: http://wri-users.s3.amazonaws.com/sminnemeyer/epa_aqi_documentation.pdf
# WHO breakpoints: http://www.who.int/mediacentre/factsheets/fs313/en/
# conversions: https://cfpub.epa.gov/ncer_abstracts/index.cfm/fuseaction/display.files/fileID/14285
## Note: this depends on Air Temperature, and 2.45 is just an approximation
# ug/m3 -> ppm
ug_to_mg = 0.001
mg_to_ppm_coef = 24.45

# ppm -> ug/m3
ppm_to_mg_coef = 0.0409 # (1/24.45)
mg_to_ug = 1000

epa_categories = {
	0: {
		"low": 0,
		"high": 50,
		"name": "Good"
	},
	1: {
		"low": 51,
		"high": 100,
		"name": "Moderate"
	},
	2: {
		"low": 101,
		"high": 150,
		"name": "Unhealthy for sensitive groups"
	},
	3: {
		"low": 151,
		"high": 200,
		"name": "Unhealthy"
	},
	4: {
		"low": 201,
		"high": 300,
		"name": "Very Unhealthy"
	},
	5: {
		"low": 301,
		"high": 500,
		"name": "Hazardous"
	}
}

epa_breakpoints = {
	"o3_8hr": {
		"min": 0,
		"digits": 3,
		"breaks": [0, 0.065, 0.085, 0.105, 0.125, .405, 0.6],
	},
	"o3_1hr": {
		"min": 0.125,
		"digits": 3,
		"breaks": [None, None, 0.125, 0.165, 0.195, 0.405, 0.6],
	},

	### Keep these in u/m3
	"pm10": {
		"min": 0,
		"digits": 0,
		"breaks": [0, 50, 150, 250, 350, 420, 600],
	},
	"pm25": {
		"min": 0,
		"digits": 1,
		"breaks": [0, 15, 40, 65, 150, 250, 600],
	},
	###

	"co": {
		"min": 0,
		"digits": 1,
		"breaks": [0, 4, 9, 12, 15, 30, 50],
	},
	"so2": {
		"min": 0,
		"digits": 3,
		"breaks": [0, 0.03, 0.14, 0.22, 0.30, 0.60, 1.0],
	},
	"no2": {
		"min": 0.65,
		"digits": 2,
		"breaks": [None, None, None, None, 0.65, 1.25, 1.65],
	}
}

who_categories = {

}

who_breakpoints = {

}

def calculate_AQI(param, value, standard):
	'''Assumes value is provided in correct format matching breakpoints above'''
	logging.info('Param: {}, {}'.format(param, value))
	# get the breakdowns at each level for the parameter
	if standard == 'EPA':
		bp = epa_breakpoints[param]
	elif standard == 'WHO':
		bp = who_breakpoints[param]
	else:
		logging.error('Not a valid AQI standard')
		return None

	value = round(value, bp['digits'])
	# only calculate AQI if the measurement is above the minimum threshold
	if value >= bp['min']:
		# Returns index of bp_hi, 1+index of bp_lo
		i = bisect(bp['breaks'], value)

		# if value is greater than highest range, calculate using highest range
		if i == len(bp['breaks']):
			i -= 1

		bp_hi = bp['breaks'][i]
		bp_lo = bp['breaks'][i-1]
		aqi_hi = categories[i-1]['high']
		aqi_lo = categories[i-1]['low']

		logging.info('calculating index\n')
		pollutant_index = ((float(aqi_hi - aqi_lo) / (bp_hi - bp_lo)) * (value - bp_lo)) + aqi_lo
		logging.info('({} - {}) / ({} - {}) * ({} - {}) + {} = {}\n'.format(aqi_hi, aqi_lo, bp_hi, bp_lo, value, bp_lo, aqi_lo, pollutant_index))

		logging.info('AQI: {}, Threat level: {}'.format(pollutant_index, categories[i-1]['name']))

		return round(pollutant_index, bp['digits'])

	return None
