import argparse
import json
import os
import time
from openai import OpenAI
from tqdm import tqdm

# import shortuuid
import asyncio
from typing import Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

def parse_score(review):
    try:
        score = float(review.split('\n')[0])
    except Exception as e:
        if('score:' in review):
            score = float(review.split('score:')[1].split('\n')[0])
        elif('Score:' in review):
            score = float(review.split('Score:')[1].strip('\n')[0])
        else:           
            logger.error(
                f"{e}\nContent: {review}\n" "You must manually fix the score pair."
            )
            score = -1
    
    return score

def find_error_items(alpaca_data,alpaca_data_cleaned_archive):
    alpaca_data_cleaned_archive_str = set([str(d) for d in alpaca_data_cleaned_archive])
    dirty_list = []
    for i, x in enumerate(alpaca_data):
        x = str(x)
        if(x not in alpaca_data_cleaned_archive_str):
            dirty_list.append(i)
    return dirty_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GPT4 Distilation.")
    parser.add_argument("-o", "--output-review-file")
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=1024,
        help="maximum number of tokens produced in the output",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=1,
        help="the batch size to call the OpenAI."
    )
    args = parser.parse_args()
    message_list = []
    # alpaca_data_cleaned_archive = json.load(open("./alpaca_data_cleaned_archive.json"))
    alpaca_data = json.load(open("./alpaca_data.json"))
    system_prompt = os.environ.get('SYSTEM_PROMPT')


    '''
    # TO-DO
    rating according to the helpfulness
    '''
    # user_prompt = "Please rate according to the helpfulness of the response to the instruction and the input. Each assistant receives an score on a scale of 0 to 5, where a higher score indicates higher level of the helpfulness. Please first output a single line containing value indicating the scores. In the subsequent line, please provide a comprehensive explanation of your evaluation, avoiding any potential bias. \n\n"
    # dirty_list = find_error_items(alpaca_data, alpaca_data_cleaned_archive)
    '''
    rating according to the accuracy
    '''
    print(f"Alpaca data pairs: {len(alpaca_data)}")
    predictions = []
    i = 0
    wait_base = 10
    retry = 0
    batch_size = args.batch_size
    pbar = tqdm(total=len(alpaca_data))
    # Try 10 messages firstly
    while(i<3):
    # while(i<len(message_list)):
        try:
            completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": json.dumps(alpaca_data[i])
                    }
                ],
                model="gpt-4-turbo-preview"
            )
            predictions.append(completion.choices[0].message.content)
            i += 1
            wait_base = 10
            pbar.update(batch_size)
        except:
            retry += 1
            print("Batch error: ",i, i+10)
            print("retry number: ", retry)
            time.sleep(wait_base)
            wait_base = wait_base*2
    pbar.close()

    with open(f"{args.output_review_file}", "w", encoding='utf-8') as output_file:
        for entry in predictions:
            output_file.write(entry)
            output_file.write('\n')
