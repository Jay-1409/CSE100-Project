import pandas as pd
from datetime import date

# Function to add spending
def add_spending(spending_type, cost):
    df = pd.read_excel("data.xlsx")
    current_date = f"{date.today()}"
    new_row = pd.Series([current_date] + [0] * (len(df.columns) - 1), index=df.columns)
    # Check if the date is in the DataFrame
    if current_date in df['Date'].values:
        # Update the existing row with the new spending
        df.loc[df['Date'] ==current_date, spending_type] += cost
    else:
        # Add a new row for the new date
        df = df._append(new_row, ignore_index=True)
        df.loc[df['Date'] ==current_date, spending_type] += cost
    
    # Write the DataFrame back to Excel after modifications
    df.to_excel('data.xlsx', index=False)
    return df
