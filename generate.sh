#!/bin/bash

nohup poetry run python generate_data.py --input indo_alpaca.json --start 0 --qty 10000 -o indo-alpaca-gpt4-part1.json > part1.log &
nohup poetry run python generate_data.py --input indo_alpaca.json --start 10000 --qty 10000 -o indo-alpaca-gpt4-part2.json > part2.log &
nohup poetry run python generate_data.py --input indo_alpaca.json --start 20000 --qty 10000 -o indo-alpaca-gpt4-part3.json > part3.log &
nohup poetry run python generate_data.py --input indo_alpaca.json --start 30000 --qty 10000 -o indo-alpaca-gpt4-part4.json > part4.log &
nohup poetry run python generate_data.py --input indo_alpaca.json --start 40000 --qty 20000 -o indo-alpaca-gpt4-part5.json > part5.log &