import Stock_Data , LineApp , console
import os
from datetime import  date , timedelta
import datetime
import sys
import shutil
import logging
from pathlib import Path
import ta
import openai
from dotenv import load_dotenv
import pandas as pd





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


    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
def OpenaiProcess(id,df , start_date , end_date):
    df["ma5"] =df["close"].rolling(window=5).mean()
    df["ma20"] =df["close"].rolling(window=20).mean()
    df["ma60"] =df["close"].rolling(window=60).mean()
    df.to_pickle(f"{id}.pkl")    
    df = df[["close","ma5","ma20","ma60"]].dropna()
    prompt = f"""
以下是三家公司在 {start_date} 到 {end_date} 的收盤價,5日均價,20日均價,60日均價：
    {df.to_dict()}

請用投資顧問的口吻，分析未來的的趨勢為何，需要注意什麼風險，並用 200 字左右說明。
"""
    logging.info(f"OpenAI Response:{prompt}")    

    res = openai.Completion.create(
        model="gpt-4o-mini",
        prompt=prompt,
        max_tokens=128,
        temperature=0.5,
    )
    response_text =prompt + f"\r\n{res.choices[0].text.strip()}"
    logging.info(f"OpenAI Response:{response_text}")
    return response_text

def addAiPrompt(res,fi):
    res =f"<h2>AI 分析報告</h2>\n{res} <P>\n"
    replace_file_content(fi, "AI_PROMPT", res)



def CopyFileToDest(id:str):
    pa ="C:/python/LLm/html/"
    src_html = os.getcwd()+"\\"+ f"{id}.html"
    src_js = os.getcwd()+"\\"+ f"{id}.js"
    dest_html = pa + f"{id}.html"
    dest_js = pa + f"{id}.js"
    if os.path.exists(dest_html):
        os.remove(dest_html)
    if os.path.exists(dest_js):
        os.remove(dest_js)

    shutil.copyfile(src_html, dest_html)
    shutil.copyfile(src_js, dest_js)
    logging.info(f"Copied {src_html} to {dest_html}")
    logging.info(f"Copied {src_js} to {dest_js}")


def generate(id: str) -> int:
    logging.info(f"id:{id}")
    end_date= date.today() +timedelta(days=-1)  
    start_date = date.today() +timedelta(days=-180)
    start_date= start_date.strftime('%Y-%m-%d')
    end_date= end_date.strftime('%Y-%m-%d')
    logging.info(f"start_date:{start_date}")
    logging.info(f"end_date:{end_date}")
    df =Stock_Data.getData(id ,start_date,end_date)
    df[0]=pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

    logging.info("DataFrame")
    logging.info(df.head())
    if os.path.exists(os.getcwd()+"\\"+ f"{id}.js"):
        os.remove(os.getcwd()+"\\"+ f"{id}.js")  
    to_json_file(id , df)
    if os.path.exists(os.getcwd()+"\\"+ f"{id}.html"):
        os.remove(os.getcwd()+"\\"+ f"{id}.html")   
    shutil.copyfile("base.html", f"{id}.html")
    replace_file_content(os.getcwd()+"\\"+ f"{id}.html", "@@title", id)
    res=OpenaiProcess(id,df,start_date,end_date)
    logging.info(f"AI Response:")
    addAiPrompt(res,os.getcwd()+"\\"+ f"{id}.html")
    logging.info(f"Adding AI Prompt completed.")
    CopyFileToDest(id)
    logging.info(f"File copy completed.")   
    LineApp.SendMessage(f"{id} 檔案已產生並上傳完成,https://kuei-wen.github.io/html/0056.html")
    logging.info(f"Line message sent.")
    console.GitPush()
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

