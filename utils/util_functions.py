import math
import pandas as pd
import os


def preceding_visit_feature_extraction(_df):
    #Function iterates through the dataset and calculates the duration of the last visit,
    #the last species to visit and  time since the last visit, time since last of same species
    _df = _df.dropna(subset='flower_code')
    new_rows = []
    visit_seq_perflower = {}
    
    for code in _df['flower_code'].unique(): # treats each flower independently (iterates through all)

        # reset all variables to nan (no prior visit/ species) as starting at first flower visitation
        _tmp = _df.loc[_df['flower_code'] == code]
        last_time = math.nan
        last_time_species = {'honeybee': math.nan, 'wasp': math.nan, 'hoverfly': math.nan, 'moth': math.nan}
        last_species = math.nan
        visit_seq_perflower[code] = []
        last_visit_time = math.nan
        
        for indx, row in _tmp.iterrows(): # Iterates through each visit at individual flower
            
            time_difference = row['clock_time'] - last_time # nan if no previous
            t_last_spec = row['clock_time'] - last_time_species[row['species']]
            if not math.isnan(time_difference):
                visit_seq_perflower[code].append(time_difference)

            #Adds new row to dataset (idx is used to merge it with origonal dataset)
            new_rows.append({
                'time_since_last_visit': time_difference,
                'last_species_visit': last_species,
                'last_visit_time': last_visit_time,
                'time_last_of_same_species': t_last_spec,
                'indx': indx})

            #Updates values based on current visitation
            last_visit_time = row['time']
            last_time = row['clock_time']
            last_species = row['species']
            last_time_species[row['species']] = row['clock_time']

    #create dataset with features
    temp =  pd.DataFrame(new_rows)
    temp = temp.set_index('indx')
    return temp

def num_to_code(num, datapoint): # for flower dataset produces flower code ({datapoint}{num})
    if num < 10:
        num = f"0{num}"
    return f"{datapoint}{num}"


def extract_flower_dataframes(dir):
    paths = [os.path.join(dir, h) for h in os.listdir(dir)] #in dir, dataframe for each location
    dfs = []
    
    for path in paths:
        flower_code = path.split('/')[-1].split('.')[0].split('_')[-1]#extract flower code (location)
        fdf = pd.read_csv(path).copy()        
        keep = ['flower_code','x0', 'y0','radius', 'flower_num']
        fdf = fdf.dropna(subset=['flower_num'])
        #relates flower number wiht flower code in main dataset
        fdf['flower_code'] = fdf['flower_num'].apply(lambda x: num_to_code(x, flower_code)) #
        fdf = fdf[keep]
        fdf.set_index('flower_code', inplace=True)  # sets flower code as index

        dfs.append(fdf)#appends required data to dataframe
    flower_dataframe = pd.concat(dfs).reset_index()
    return flower_dataframe