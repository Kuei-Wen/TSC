import os
from datetime import datetime
import logging
def GitPush():
    url ="D:\Penny\python\TSC"
    #url ="C:/python/LLm/html"
    os.chdir(url)
    os.system("git config --global user.name 'kuei-wen'")
    os.system("git config --global user.email 'kueiwen@gmail.com'")
    os.system("git add *.html")
    os.system("git add *.js")
    current_datetime = datetime.now()

    # Convert to string in YYYY-MM-DD HH:MM:SS format
    current_time_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S") 
    os.system(f"git commit-m {current_time_str} auto commit")
    os.system("git push origin main")
    logging.info("Git push completed.")