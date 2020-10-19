import pickle
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from country_data import col_name
from country_data import pl_col_name
from country_data import prov_col_name
from country_data import countries
from country_data import provinces

file = open('countries_data.dat', 'wb')
pickle.dump(col_name, file)
pickle.dump(pl_col_name, file)
pickle.dump(prov_col_name, file)
pickle.dump(countries, file)
pickle.dump(provinces, file)

file.close()