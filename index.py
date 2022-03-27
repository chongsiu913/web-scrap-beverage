from unittest.util import unorderable_list_difference
from target_shops import parknshop
from config import web_list
import sys
import pandas as pd
from datetime import datetime

current_dt = str(datetime.now())
result = []
excel_col = ['Info Datetime','Source','Source URL','Item name', 'Item volumn' ,'Item normal prize', 'Item discount prize', 'Item special offer]']
# loop through different e shop

for web in web_list:
    
    for url in web['url_list']:
        shop_class = getattr(sys.modules[__name__], web['shop_desc'])
        scrap_result = shop_class.web_scrap(web['shop_desc'],url)
        for item in scrap_result:
            item.insert(0,current_dt)
            result.append(item)
df = pd.DataFrame(result,columns = excel_col)
df.to_excel(excel_writer = "/Users/siuchongchun/Downloads/test.xlsx")