import pandas as pd

df = pd.DataFrame({"country": ['Afghanistan', "Albania", "Algeria"], "cases": ["No data", "No data", "No data"],
                   "deaths": ["No data", "No data", "No data"], "recov": ["No data", "No data", "No data"],
                   "flag_scr": ["No data", "No data", "No data"]})
print(df)

updated_list = [['Afghanistan', '40,141', '1,488', '33,561',
                 '//upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Flag_of_Afghanistan.svg/720px-Flag_of_Afghanistan.svg.png'],
                ['Albania', '16,774', '448', '10,001',
                 '//upload.wikimedia.org/wikipedia/commons/thumb/3/36/Flag_of_Albania.svg/21px-Flag_of_Albania.svg.png'],
                ['Algeria', '54,203', '1,846', '37,971',
                 '//upload.wikimedia.org/wikipedia/commons/thumb/7/77/Flag_of_Algeria.svg/720px-Flag_of_Algeria.svg.png']]
