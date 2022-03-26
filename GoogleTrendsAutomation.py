#GOOGLE TRENDS AUTOMATION

from pytrends.request import TrendReq
import pandas as pd
import time

keyword_df = pd.read_csv('keyword_list.csv')
kw_list = keyword_df['keyword_list'].values.tolist()

#Initialize pytrends, set search language to US English
pytrends = TrendReq(hl='en-US', tz=360)

#Google Trends search limit is 5 keywords at a time, thus we need to divide our keyword list to 5 groups
#and iterate through them

for i in range(int(len(kw_list)/5) + 1):
    
    #Build the payload by the keyword group we are in
    pytrends.build_payload(kw_list[i*5: i*5 + 5], cat=0, timeframe='today 12-m', geo='US')

    data = pytrends.interest_over_time()
    data = data.reset_index()

    import plotly.express as px

    for j in range(5):
        #In order to get rid of any index problems, we treat first key word a little differently
        if i == 0:
            fig = px.line(data, x='date', y=kw_list[i*4 + j], title='Search Interest Over Time')
            fig.write_image('{0}.png'.format(kw_list[i*4 + j]))
            #Our data will be in metropol level format thus our resolution is DMA. You can change it later
            by_region = pytrends.interest_by_region(resolution='DMA', inc_low_vol=True, inc_geo_code=False)
            by_region.to_excel('{0}.xlsx'.format(kw_list[i*4 + j]))
            
        else:
            #Break if there are no more elements in our keyword list
            if (i*4 + j +i) == len(kw_list):
                break
            else:
                fig = px.line(data, x='date', y=kw_list[i*4 + j + i], title='Search Interest Over Time')
                fig.write_image('{0}.png'.format(kw_list[i*4 + j + i]))
                by_region = pytrends.interest_by_region(resolution='DMA', inc_low_vol=True, inc_geo_code=False)
                by_region.to_excel('{0}.xlsx'.format(kw_list[i*4 + j + i]))
    
    print('Iteration {} has been completed'.format(i))
    time.sleep(15)
