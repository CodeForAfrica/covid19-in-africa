import pandas as pd
from functools import reduce
from cases import Case


confirmed = Case("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv","_confirmed"
)
deaths = Case("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv","_deaths"
)
recovered = Case("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv","_recovered"
)

all_cases = [confirmed, deaths, recovered]


def collective(all_cases):
    """Gather the latest case for each status 

    Args:
        all_cases [list]: Case instances of all case statuses
        
    Return:
        df_final : Dataframe with all daily cases concated 
    """
    frames = []
    for case in all_cases:
        frame = case.daily()
        frame.rename(columns={frame.columns[1] : frame.columns[1]+ case.status},inplace=True)
        frames.append(frame)
        
    df_final = reduce(lambda left,right: pd.merge(left,right,on='Country'), frames)
    filename = df_final.columns[1].split('_')[0] + "_all_cases.csv"
    # archive daily cases
    df_final.to_csv('./datasets/'+filename)
    
    return df_final

if __name__ == "__main__":
    
    collective(all_cases)


