#! usr/bin/env python3
import praw
import pandas as pd
import datetime as dt
import string
import csv

def get_date(created):
    return dt.datetime.fromtimestamp(created)

if __name__ == "__main__":
    r = praw.Reddit(client_id='PW8Tn2t-OXA2Cg', \
                     client_secret='hlk0PphMhvfjx-XW3VLJv569_Po', \
                     user_agent='YOUR_APP_NAME', \
                     username='angervase', \
                     password='XXXXXXXXXXX')  # password redacted
   
    subreddit = r.subreddit('WritingPrompts')
    wp_list = []
    prompt_num = 0
    prompt_dir = "prompt_responses/"
    csv_name = "prompt_data.csv"
    for submission in subreddit.top(limit=1000):
        title = submission.title.lower()
        time_stamp = str(get_date(submission.created))
        print(prompt_num)
        if '[wp]' in title:
            op_link = submission.url
            op_text = str(submission.selftext_html)
            upvotes = submission.ups

            comment_body = [comment for comment in submission.comments if hasattr(comment, "body")]
            comment_num = 0
            for comment in comment_body:
                if len(comment.body.split()) > 300:
                    comment_upvotes = str(comment.ups)
                    file_name = "prompt"+"{:03d}".format(prompt_num)+"_"+comment_upvotes+"_"+str(comment_num)+".txt"
                    file_name = "prompt"+"{:03d}".format(prompt_num)+"_"+"{:03d}".format(comment_num)+"_"+comment_upvotes+".txt"
                    f = open(prompt_dir+file_name, "a")
                    f.write(comment.body)
                    f.close()
                    comment_num+=1
            wp_list.append([prompt_num, title.translate(str.maketrans('', '', string.punctuation)), upvotes, time_stamp])
            prompt_num+=1
    my_df = pd.DataFrame(wp_list)
    my_df.to_csv(csv_name, index=False, header=False)
