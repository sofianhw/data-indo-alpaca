#!/bin/bash

poetry run python generate_data.py --input indo_alpaca.json --start 0 --qty 10000 -o indo-alpaca-gpt4-part1.json
poetry run python generate_data.py --input indo_alpaca.json --start 10000 --qty 10000 -o indo-alpaca-gpt4-part2.json
poetry run python generate_data.py --input indo_alpaca.json --start 20000 --qty 10000 -o indo-alpaca-gpt4-part3.json
poetry run python generate_data.py --input indo_alpaca.json --start 30000 --qty 10000 -o indo-alpaca-gpt4-part4.json
poetry run python generate_data.py --input indo_alpaca.json --start 40000 --qty 20000 -o indo-alpaca-gpt4-part5.json