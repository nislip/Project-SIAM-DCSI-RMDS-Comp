import zipfile
with zipfile.ZipFile('prices_per_day.zip', 'r') as zip_ref:
    zip_ref.extractall('https://github.com/nislip/RMDS_Competition_NI.git')
