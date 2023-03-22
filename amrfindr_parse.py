import os
import pandas as pd
import datetime

def parse_data(output_file):
    """
    Parses data from input directory and outputs to Excel file.

    Args:
    - output_file (str): Path to output Excel file.

    Returns:
    - None
    """
    # Prompt user to enter input directory path
    input_dir = input("Enter path to input directory: ")


    # Check if input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory {input_dir} does not exist.")
        return

    # Get list of files in input directory
    files = os.listdir(input_dir)

    # Initialize dictionary to hold parsed data
    data_dict = {}

    # Loop through files
    for file in files:
        # Check if file is a TSV file
        if file.endswith(".tsv"):
            # Read TSV file
            filepath = os.path.join(input_dir, file)
            df = pd.read_csv(filepath, sep='\t')

            # Check if "Gene symbol" column exists in dataframe
            if "Gene symbol" in df.columns:
                # Loop through rows of dataframe and add data to dictionary
                for index, row in df.iterrows():
                    gene_symbol = row["Gene symbol"]
                    if gene_symbol not in data_dict:
                        data_dict[gene_symbol] = []
                    data_dict[gene_symbol].append(row)

    # Create dataframe from dictionary
    dataframes = []
    for gene_symbol, rows in data_dict.items():
        df = pd.DataFrame(rows)
        df["Gene symbol"] = gene_symbol
        dataframes.append(df)

    # Check if there are any dataframes to concatenate
    if not dataframes:
        print("Error: No dataframes to concatenate.")
        return

    # Concatenate dataframes
    merged_df = pd.concat(dataframes)

    column_name = input("Enter the column name you want to parse: ")

    if column_name not in merged_df.columns:
        print(f"Error: Column name {column_name} does not exist.")
        return

    # unique_df = pd.pivot_table(merged_df, columns=['Gene symbol'], index=['Name'])
    unique_cols = merged_df[column_name].unique().tolist()
    unique_names = merged_df['Name'].unique().tolist()
    unique_cols.insert(0,'Name')
    un_cols = merged_df[column_name].unique().tolist()
    unique_df = pd.DataFrame([], columns=unique_cols)


    for un in unique_names:
        lst = []
        lst.append(un)
        df_to_be_parsed = merged_df[merged_df['Name'] == un]
        # print(df_to_be_parsed)
        for uc in un_cols:
           if uc in df_to_be_parsed[column_name].values:
               lst.append('Yes')
           else:
               lst.append('No')
        unique_df.loc[len(unique_df)] = lst

    # Write dataframe to Excel file
    unique_df.to_excel("./output/amr_findr/" + output_file, index=False)

    print(f"Parsed data written to {output_file}.")

# Usage

if not os.path.exists("./output/amrfindr"):
      
    # if the demo_folder directory is not present 
    # then create it.
    os.makedirs("./output/amrfindr")

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
parse_data(output_file=f"output_file_{ timestamp }.xlsx")