import xarray as xr
import pandas as pd
import regionmask
from zipfile import ZipFile
import cdsapi

now = datetime.now() - timedelta(days=5)

year = str(now.strftime("%Y"))
month = str(now.strftime("%m"))
day = str(now.strftime("%d"))

uid = '199339'
apikey = '15aa7d28-4258-4669-bd30-2cb1128d0a57'

c = cdsapi.Client(key=f"{uid}:{apikey}", url="https://cds.climate.copernicus.eu/api/v2")


c.retrieve(
    'derived-utci-historical',
    {
        'variable': 'universal_thermal_climate_index',
        'version': '1_1',
        'product_type': 'intermediate_dataset',
        'year': year,
        'month': [
            month,
        ],
        'day': [
            day,
        ],
        'format': 'zip',
    },
    'download.zip')


with ZipFile('/work/download.zip', 'r') as f:

    #extract in current directory
    f.extractall()

year = str(now.strftime("%Y%m%d"))
filename = 'ECMWF_utci_'+year+'_v1.1_int.nc'

# Merge all rasters into one file
clim_max = xr.open_dataset('/work/'+filename)

# get the max of each cell
clim_max = clim_max.max('time')

# Write to new netCDF4 file
clim_max.to_netcdf("clim_max.nc")


collated = []

clim = clim_max

utci_max = clim.utci.to_dataframe().reset_index()['utci'].max() - 273.15
utci_min = clim.utci.to_dataframe().reset_index()['utci'].min() - 273.15
utci_mean = clim.utci.to_dataframe().reset_index()['utci'].mean() - 273.15

temp = pd.DataFrame({
    'datetime': pd.to_datetime([now], format='%d%b%Y:%H:%M:%S.%f'),
    'max-utci': [utci_max],
    'min-utci': [utci_min],
    'mean-utci':[utci_mean],
    })

collated.append(temp)


collated = pd.concat(collated)
print(collated)

collated.to_csv('data/'+str(now)+'.csv')
