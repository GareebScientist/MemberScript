import pandas as pd

# Load the CSV file with the 'Member' column as string
df = pd.read_csv('members.csv', dtype={'Member': str})

# Fill any missing values in the 'Member' column with an empty string
df['Member'].fillna('', inplace=True)

# Sort by 'Total time as member (months)' in descending order
df_sorted = df.sort_values(by='Total time as member (months)', ascending=False)

# Separate Treeni and Dve members based on specific levels in the 'Current level' column
# Assuming 'Treeni' and 'Dve' are keywords in 'Current level' column to identify the groups
treeni_members = df_sorted[df_sorted['Current level'].str.contains('Treeni', case=False, na=False)]
dve_members = df_sorted[df_sorted['Current level'].str.contains('Dve', case=False, na=False)]

# Get the names of the top members
top_treeni_members = treeni_members['Member'].tolist()
top_dve_members = dve_members['Member'].tolist()

# Ensure all items in the list are strings
top_treeni_members = [str(member) for member in top_treeni_members]
top_dve_members = [str(member) for member in top_dve_members]

# Create the output format
output = ', '.join(top_treeni_members) + '\n' + ', '.join(top_dve_members)

# Print the output
print(output)
