from flood_data.db_scripts.get_server_data import get_table_for_variable, data_dir
import pandas as pd
from flood_data.norfolk_flood_data.focus_intersection import int_flood_dates

# for each variable get df
tide_df = get_table_for_variable('tide')
tide_df = tide_df.resample('D').mean()

rainfall_df = get_table_for_variable('rainfall', site_id=7)
rainfall_daily_totals = rainfall_df['Value'].resample('D').sum()
rainfall_max_15 = rainfall_df['Value'].resample('D').max()
rainfall_prev_3_days = rainfall_df['Value'].resample('D').sum().rolling(window=3).sum()

gw_df = get_table_for_variable('groundwater')
gw_df = gw_df.resample('D').mean()

combined_df = pd.concat([tide_df['Value'], rainfall_daily_totals, rainfall_max_15, rainfall_prev_3_days, gw_df['Value']], axis=1)
combined_df.columns = ['tide_level', 'rainfall_daily_total', 'rainfall_daily_max_15', 'rainfall_prev_3_days',
                       'shallow_well_depth']
combined_df['flooded'] = combined_df.index.isin(int_flood_dates)
combined_df = combined_df[combined_df.index > "2010-01-01"]
combined_df = combined_df[combined_df.index < "2016-10-31"]
combined_df.to_csv('{}/reformated_for_model.csv'.format(data_dir))
