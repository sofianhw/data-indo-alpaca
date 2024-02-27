import argparse
import json
import os
import time
from openai import OpenAI, OpenAIError
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
    parser.add_argument(
        "--start",
        type=int,
        default=0,
        help="start index data",
    )
    parser.add_argument(
        "--qty",
        type=int,
        default=10000,
        help="total qty data",
    )
    parser.add_argument(
        "--input",
        type=str,
        default="alpaca_data.json",
        help="file dataset name",
    )
    args = parser.parse_args()
    start = args.start
    qty = start + args.qty
    nama_file = args.input
    # alpaca_data_cleaned_archive = json.load(open("./alpaca_data_cleaned_archive.json"))
    # alpaca_data = json.load(open("./alpaca_data.json"))
    alpaca_data = json.load(open(f"./{nama_file}"))
    alpaca_data = alpaca_data[start:qty]
    print(F"start {start} to end {qty}")
    # alpaca_data = alpaca_data[0:10000]
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
    # while(i>1):
    while(i < 2):
    # while(i<len(message_list)):
        try:
            alpaca_data[i].pop('output', None)
            print(alpaca_data[i])
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
            predictions.append(json.loads(completion.choices[0].message.content))
            i += 1
            wait_base = 10
            pbar.update(batch_size)
        except OpenAIError as e:
            retry += 1
            print(f"Error: {e}")
            print("Batch error: ",i, i+10)
            print("retry number: ", retry)
            time.sleep(wait_base)
            wait_base = wait_base*2
    pbar.close()

    with open(f"{args.output_review_file}", "w", encoding='utf-8') as output_file:
        json.dump(predictions, output_file)
