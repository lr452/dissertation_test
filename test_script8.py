import iris
import numpy as np
import iris.quickplot as qplt
import matplotlib.pyplot as plt
from iris.coord_categorisation import *

#cube = iris.load_cube('/disk2/lr452/Downloads/dissic_Omon_MIROC-ES2L_historical_r1i1p1f2_gn_185001-201412_regridded_soregion.nc','mole_concentration_of_dissolved_inorganic_carbon_in_sea_water')
cube = iris.load_cube('/disk2/lr452/Downloads/dissic_Omon_MIROC-ES2L_historical_r1i1p1f2_gn_185001-201412_regridded_soregion.fix.nc','dissic')

#extracting the years
start_year = 1994
end_year = 2014

iris.coord_categorisation.add_year(cube, 'time', name='year')
loc = np.where((cube.coord('year').points >= start_year) & (cube.coord('year').points < end_year))

#extract just those years into a new variable called cube2
cube2 = cube[loc]

add_month_number(cube, 'time', name='month_number')
cube3 = cube2[np.where((cube.coord('month_number').points == 6) | (cube.coord('month_number') == 7) | (cube.coord('month_number') == 8))]

#then to average this by each year, so that you have the December-Jan for each year add the 'season year', i.e. a number of each 'season'
add_season_year(cube3, 'time', name='season_year')

#then average by the season year:
#cube2 = cube2.aggregated_by(['season_year'], iris.analysis.MEAN)

#average all of the data together along the time axis
cube4 = cube3.collapsed('time',iris.analysis.MEAN)

#extracting a geographical region
west = -175
east = -75
south = -60
north = -30
temporary_cube = cube4.intersection(longitude = (west, east))
cube4_region = temporary_cube.intersection(latitude = (south,north))

#averaging across longitudes
cube4_region.coord('latitude').guess_bounds()
cube4_region.coord('longitude').guess_bounds()
grid_areas = iris.analysis.cartography.area_weights(cube4_region)
global_average_variable = cube4_region.collapsed(['longitude'],iris.analysis.MEAN,weights=grid_areas)

qplt.pcolormesh(global_average_variable)
plt.show()
