import pandas as pd
from datetime import datetime

# Load the CSV files
youtube_df = pd.read_csv('youtube.csv')
bmc_df = pd.read_csv('bmc.csv')

# Fill any missing values to avoid issues
youtube_df.fillna('', inplace=True)
bmc_df.fillna('', inplace=True)

# Function to determine BMC membership level based on amount and duration
def determine_membership_level(amount, duration):
    if duration == 'yearly':
        if amount == 110:
            return 'Treeni'
        elif amount == 22:
            return 'Dve'
    elif duration == 'monthly':
        if amount == 10:
            return 'Treeni'
        elif amount == 2:
            return 'Dve'
    return 'Ekam/Donations'

# Function to determine membership duration based on dates
def get_membership_duration(start_date, renews_on):
    try:
        start_date = pd.to_datetime(start_date, errors='coerce')
        renews_on = pd.to_datetime(renews_on, errors='coerce')
        if pd.isna(renews_on) or pd.isna(start_date):
            return 'monthly'
        if renews_on.year > start_date.year or (renews_on.year == start_date.year and renews_on.month > start_date.month):
            return 'yearly'
        else:
            return 'monthly'
    except Exception:
        return 'monthly'

# Add a new column for BMC membership duration (monthly or yearly)
bmc_df['Membership duration type'] = bmc_df.apply(lambda row: get_membership_duration(row['Membership start date'], row['Membership renews on']), axis=1)

# Determine the BMC membership level
bmc_df['Membership level'] = bmc_df.apply(lambda row: determine_membership_level(row['Membership amount'], row['Membership duration type']), axis=1)

# Filter only active BMC members
bmc_df_active = bmc_df[bmc_df['Subscription status'] == 'Active']

# Calculate the duration of membership in months for BMC members
current_date = pd.to_datetime(datetime.now())
bmc_df_active['Total time as member (months)'] = bmc_df_active['Membership start date'].apply(lambda x: (current_date - pd.to_datetime(x)).days // 30)

# Calculate the duration of membership in months for YouTube members (assuming you already have the total time in months)
youtube_df['Total time as member (months)'] = youtube_df['Total time as member (months)']

# Combine both dataframes and membership levels into a single dataframe
youtube_treeni_members = youtube_df[youtube_df['Current level'].str.contains('Treeni', case=False, na=False)].copy()
youtube_treeni_members['Membership level'] = 'Treeni'

youtube_dve_members = youtube_df[youtube_df['Current level'].str.contains('Dve', case=False, na=False)].copy()
youtube_dve_members['Membership level'] = 'Dve'

bmc_treeni_members = bmc_df_active[bmc_df_active['Membership level'] == 'Treeni']
bmc_dve_members = bmc_df_active[bmc_df_active['Membership level'] == 'Dve']

# Combine YouTube and BMC members into Treeni and Dve lists
combined_treeni = pd.concat([youtube_treeni_members[['Member', 'Total time as member (months)', 'Membership level']],
                             bmc_treeni_members[['Member Name', 'Total time as member (months)', 'Membership level']].rename(columns={'Member Name': 'Member'})])

combined_dve = pd.concat([youtube_dve_members[['Member', 'Total time as member (months)', 'Membership level']],
                          bmc_dve_members[['Member Name', 'Total time as member (months)', 'Membership level']].rename(columns={'Member Name': 'Member'})])

# Combine both lists and sort by total time as member
combined_members = pd.concat([combined_treeni, combined_dve]).sort_values(by='Total time as member (months)', ascending=False)

# Separate Treeni and Dve after sorting
combined_treeni_names = combined_members[combined_members['Membership level'] == 'Treeni']['Member'].tolist()
combined_dve_names = combined_members[combined_members['Membership level'] == 'Dve']['Member'].tolist()

# Create the output format
output = 'Treeni Members:\n' + ', '.join(combined_treeni_names) + '\n\nDve Members:\n' + ', '.join(combined_dve_names)

# Print the output
print(output)
