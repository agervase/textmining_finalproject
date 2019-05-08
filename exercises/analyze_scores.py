#! usr/bin/env python3
import os
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
    
if __name__ == "__main__":
    path = "../data/texts/"
    dirListing = os.listdir(path)
    texts = []
    response_scores = {}
    response_score_lst = []
    prompt_score_lst = []
    for item in dirListing:
        if ".txt" in item:
            parsed = item.rstrip('.txt').split('_') # strip extension and split on hyphens
            prompt_num = str(parsed[0][6:9])
            score = int(parsed[2])
            if prompt_num in response_scores:
                response_scores[prompt_num].append(score)
            else:
                response_scores[prompt_num] = [score]
            texts.append(item)
        elif ".csv" in item:
            with open(path+item) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    #row = row.split(',')
                    prompt_num = '{0:03d}'.format(int(row[0]))
                    score = int(row[2])
                    prompt_score_lst.append(score)
                    #print(row)

    for key in sorted(response_scores.keys()):
        response_score_lst.append(np.average(response_scores[key]))

    for i in range(950):
        print(response_score_lst[i], prompt_score_lst[i])
    print(len(response_score_lst))
    print(len(prompt_score_lst[0:950]))
    print(np.corrcoef(prompt_score_lst[0:950],response_score_lst))
    plt.scatter(prompt_score_lst[0:950],response_score_lst)
    plt.savefig('scores_compare.png') 
     
