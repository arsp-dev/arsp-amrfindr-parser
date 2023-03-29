import os
import pandas as pd
import datetime
import numpy as np

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

    unique_cols = merged_df["Gene symbol"].unique().tolist()
    unique_cols_mutations = [un for un in unique_cols if '_' in un]
    unique_cols = [un for un in unique_cols if '_' not in un]
    
    # unique_cols.sort()
    # unique_cols_mutations.sort()
    unique_names = merged_df['Name'].unique().tolist()

    unique_cols.insert(0,'stock_num')
    unique_cols_mutations.insert(0,'stock_num')

    un_cols = merged_df["Gene symbol"].unique().tolist()
    un_cols_mutations = [un for un in un_cols if '_' in un]
    un_cols = [un for un in un_cols if '_' not in un]
    
    unique_df = pd.DataFrame([], columns=unique_cols)
    unique_df_mutations = pd.DataFrame([], columns=unique_cols_mutations)
    

    amr_genes_df = create_df(unique_names,merged_df,un_cols,unique_df)
    amr_genes_df = pd.concat([amr_genes_df.iloc[:, 0], amr_genes_df.iloc[:, 1:].sort_index(axis=1)], axis=1)

    mutations_genes_df = create_df_mutations(unique_names,merged_df,un_cols_mutations,unique_df_mutations) 
    merged_df = pd.merge(amr_genes_df, mutations_genes_df, on='stock_num')


    # Write dataframe to Excel file
    merged_df.to_excel("./output/amr_findr_with_class/" + output_file, index=False, engine='openpyxl')

    print(f"Parsed data written to {output_file}.")


def create_df(unique_names,merged_df,un_cols,unique_df) -> pd.DataFrame:
    for un in unique_names:
        lst = []
        lst.append(un)
        df_to_be_parsed = merged_df[merged_df['Name'] == un]
        # print(df_to_be_parsed)
        for uc in un_cols:
            if uc in df_to_be_parsed["Gene symbol"].values:
                # x =  df_to_be_parsed.loc[df_to_be_parsed['Gene symbol'] == uc, 'Subclass'].values[0]
                lst.append(uc)
            else:
                lst.append('')
        unique_df.loc[len(unique_df)] = lst
    return unique_df

def create_df_mutations(unique_names,merged_df,un_cols,unique_df) -> pd.DataFrame:
    for un in unique_names:
        lst = []
        lst.append(un)
        df_to_be_parsed = merged_df[merged_df['Name'] == un]
        # print(df_to_be_parsed)
        for uc in un_cols:
            if uc in df_to_be_parsed["Gene symbol"].values:
                # x =  df_to_be_parsed.loc[df_to_be_parsed['Gene symbol'] == uc, 'Subclass'].values[0]
                lst.append(uc)
            else:
                lst.append('')
        unique_df.loc[len(unique_df)] = lst
        merged = pd.DataFrame({'stock_num': unique_df['stock_num']})
        for col in unique_df.columns[1:]:
            col_name = col.split('_')[0]
            if col_name not in merged.columns:
                merged[col_name] = unique_df[col]
            else:
                merged[col_name] = merged[col_name].fillna(np.nan) + ',' + unique_df[col].fillna(np.nan)
    
    for col in merged.columns:
    # Remove the last comma from each value in the column
        merged[col] = merged[col].str.rstrip(',')

        # Remove leading and trailing commas from all other columns
        merged[col] = merged[col].str.strip(',')


    return merged




# Usage
if not os.path.exists("/output/amrfindr_with_class"):
      
    # if the demo_folder directory is not present 
    # then create it.
    os.makedirs("/output/amrfindr_with_class")
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
parse_data(output_file=f"output_file_{ timestamp }.xlsx")