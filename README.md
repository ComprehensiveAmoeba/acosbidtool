# ACOS Optimization Tool

The ACOS Optimization Tool is a Streamlit-based web application designed for modifying bids in Sponsored Products bulk sheets to meet specified Advertising Cost of Sales (ACOS) targets. This tool allows users to upload an xlsx file, specify target ASINs and desired ACOS, and optionally set bidding adjustments for specific placements.

## Features

- Upload Sponsored Products bulk sheets in xlsx format.
- Input target ASINs, desired ACOS, and optional bidding adjustments.
- Filter and process data based on user inputs.
- Download the modified xlsx file with updated bids and budgets.

## Installation

Before running the app, ensure you have Python installed on your system. This app requires Python 3.6 or later.

1. **Clone or Download the Repository**
   - Clone this repository to your local machine or download the app's source code.

2. **Install Dependencies**
   - The app requires `streamlit`, `pandas`, and `openpyxl` to be installed. Run the following command to install these packages:

   ```bash
   pip install streamlit pandas openpyxl
