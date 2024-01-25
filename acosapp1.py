import streamlit as st
import pandas as pd
import openpyxl
from io import BytesIO

# App title and configuration
st.set_page_config(page_title="ACOS Optimization Tool", page_icon="https://thrassvent.de/wp-content/uploads/2024/01/5.png")
st.title("ACOS Optimization Tool")

# User Inputs
uploaded_file = st.file_uploader("Upload your Sponsored Products bulk sheet", type=["xlsx"])
asin_input = st.text_input("Enter ASINs (comma-separated, case-insensitive, start with B0, 10 characters)").upper().split(',')
target_acos = st.number_input("Enter Target ACOS (1-100, without %)", min_value=1.0, max_value=100.0, step=0.01)
bidding_adjustment = st.number_input("Enter Bidding Adjustment (0-900, optional)", min_value=0, max_value=900, value=0)
placement_choice = st.selectbox("Choose a Placement for Bidding Adjustment", ('None', 'Placement Rest Of Search', 'Placement Product Page', 'Placement Top'))

# Process file
if uploaded_file is not None and asin_input:
    # Read the excel file
    df = pd.read_excel(uploaded_file)

    # Filter based on campaign name and extract ASINs
    filtered_df = df[df['Campaign Name (Informational only)'].str.contains('|'.join(['UN_', 'OW_', 'PH_', 'BR_']))]
    filtered_df = filtered_df[filtered_df['Campaign Name (Informational only)'].str.contains('|'.join(asin_input))]

    # Initialize a column for new bids to handle bid updates
    filtered_df['New Bid'] = filtered_df['Bid']

    # Calculate new values
    for index, row in filtered_df.iterrows():
        if row['Entity'] == 'Keyword':
            original_bid = row['Bid']
            clicks = row['Clicks']
            sales = row['Sales']

            if clicks == 0:
                new_bid = original_bid * 1.1
            elif clicks != 0 and sales == 0:
                new_bid = original_bid * 0.9
            else:
                acos_factor = target_acos / 100
                bidding_adjustment_factor = 1 if placement_choice == 'None' else (bidding_adjustment + 100) / 100
                new_bid = acos_factor * sales / clicks / bidding_adjustment_factor

            # Apply constraints on bid
            new_bid = max(0.02, min(15, new_bid))
            filtered_df.at[index, 'New Bid'] = new_bid
            filtered_df.at[index, 'Operation'] = 'update'

        elif row['Entity'] == 'Campaign':
            old_budget = row['Daily Budget']
            clicks = row['Clicks']
            # Use the new bid value from the same row for budget calculation
            new_bid = filtered_df.at[index, 'New Bid']
            new_budget = old_budget * 1.1 if clicks == 0 else ((new_bid - filtered_df.at[index, 'Bid']) / filtered_df.at[index, 'Bid']) * clicks * new_bid
            filtered_df.at[index, 'Daily Budget'] = new_budget
            filtered_df.at[index, 'Operation'] = 'update'

        elif row['Entity'] == 'Bidding Adjustment':
            if row['Placement'] == placement_choice:
                filtered_df.at[index, 'Percentage'] = bidding_adjustment
            else:
                filtered_df.at[index, 'Percentage'] = 0
            filtered_df.at[index, 'Operation'] = 'update'

    # Apply the new bid values to the 'Bid' column
    filtered_df['Bid'] = filtered_df['New Bid']
    filtered_df.drop(columns=['New Bid'], inplace=True)

    # Generate downloadable file
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        filtered_df.to_excel(writer, index=False)
    output.seek(0)
    st.download_button(label="Download modified file", data=output, file_name="modified_bulk_sheet.xlsx", mime="application/vnd.ms-excel")

# Display the app
st.write("Upload a file and enter the required information to get started.")
