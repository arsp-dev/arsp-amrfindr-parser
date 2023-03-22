DESCRIPTION:
There are two (2) scripts inside this repository:
(1): (amrfindr_parse.py) This script is used to manually pivot dataframe based on the column selected.
	input for this script will be a folder containing .tsv files from the tool amrfindr.
	output of this file will be located to /output/amrfindr.


(2): (amrfindr_pase_with_class.py) This script is used to manually pivot dataframe with the index of "Name" with columns unique inside "Gene symbol" column.
	input for this script will be a folder containing .tsv files from the tool amrfindr.
	output of this file will be located to /output/amrfindr_with_class.




USAGE:
//amrfindr_parse.py
python manage.py amrfindr_parse.py

Enter path to input directory: $Enter path to input
Enter the column name you want to parse: $select the desired column name and the script will automatically get unique values from that column and will create a new dataframe with "Name" and the unique values from that column as columns of the newly created dataframe

python manage.py amrfindr_parse_with_class.py
Enter path to input directory: $Enter path to input and the script will automatically get unique values from "Gene symbol" and will create a new dataframe with "Name" and the unique values from "Gene symbol" as columns of the newly created dataframe
