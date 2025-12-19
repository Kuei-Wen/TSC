import Stock_Data
import os
from datetime import  date , timedelta
import datetime
import sys
import shutil
import logging
from pathlib import Path


def to_json_file(id: str, df) -> None:
    json_path = os.getcwd()+"\\"+ f"{id}.js"
    with open(json_path, 'w', encoding='big5') as f:
        f.write("org_data=[\n")
        #f.write(f"['{df[0,1]}',{df[0,2]},{df[0,3]}{df[0,4]},{df[0,5]}]\n")
        i=0
        for row in df.itertuples():
            if i==0:
                f.write(f"['{row[5]}',{row[6]},{row[7]},{row[8]},{row[9]}]\n")
            else:
                f.write(f",['{row[5]}',{row[6]},{row[7]},{row[8]},{row[9]}]\n") 
            i+=1    
        f.write("]")

def replace_file_content(filepath, old_string, new_string):
    """
    Replaces all occurrences of old_string with new_string in the specified file.

    Args:
        filepath (str): The path to the file.
        old_string (str): The string to be replaced.
        new_string (str): The string to replace with.
    """
    try:
        # Read the entire content of the file
        with open(filepath, 'r', encoding='utf-8') as file:
            file_content = file.read()

        # Perform the replacement in memory
        modified_content = file_content.replace(old_string, new_string)

        # Write the modified content back to the file, overwriting the original
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(modified_content)

        logging.info(f"Content in '{filepath}' successfully replaced.")

    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")        


def generate(id: str) -> int:
    logging.info(f"id:{id}")
    end_date= date.today() +timedelta(days=-1)  
    start_date = date.today() +timedelta(days=-180)
    start_date= start_date.strftime('%Y-%m-%d')
    end_date= end_date.strftime('%Y-%m-%d')
    logging.info(f"start_date:{start_date}")
    logging.info(f"end_date:{end_date}")
    df =Stock_Data.getData(id ,start_date,end_date)

    logging.info("DataFrame")
    logging.info(df.head())
    if os.path.exists(os.getcwd()+"\\"+ f"{id}.js"):
        os.remove(os.getcwd()+"\\"+ f"{id}.js")  
    to_json_file(id , df)
    if os.path.exists(os.getcwd()+"\\"+ f"{id}.html"):
        os.remove(os.getcwd()+"\\"+ f"{id}.html")   
    shutil.copyfile("base.html", f"{id}.html")
    replace_file_content(os.getcwd()+"\\"+ f"{id}.html", "@@title", id)
    df["ma5"] =df["close"].rolling(window=5).mean()
    df["ma20"] =df["close"].rolling(window=20).mean()
    df["ma60"] =df["close"].rolling(window=60).mean()
    df.to_pickle(f"{id}.pkl")
    return 1


def main(argv=None):
    try:
        arr = ["0056","0050"]
        for item in arr:
            if generate(item) !=1:
                return 0

        return 1        
    except Exception as e: 
        logging.error(f"Exception occurred: {e}")
        return 0   





if __name__ == '__main__':
    sys.exit(main())

