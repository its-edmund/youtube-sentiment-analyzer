import warnings
warnings.filterwarnings("ignore")

import pandas
import os
import evadb
import html
import json
from dotenv import dotenv_values
from tabulate import tabulate

config = dotenv_values(".env") 

os.environ["OPENAI_KEY"] = config["OPENAI_KEY"]

command = input("Type command (type h for help): ")

cursor = evadb.connect().cursor()

params = {
    "user": "eva",
    "password": "password",
    "host": "localhost",
    "port": "5432",
    "database": "evadb",
}

cursor.query("""
USE postgres_data {
  DROP TABLE IF EXISTS comment_table
}
""").df()

cursor.query("""
USE postgres_data {
  CREATE TABLE IF NOT EXISTS comment_table (name VARCHAR(100), comment VARCHAR(1000), url VARCHAR(1000))
}
""").df()

sentiment_cached = True
response_cached = True
rating_cached = True

sentiment_cache = []
response_cache = []
rating_cache = []

def print_sentiment():
    print(tabulate(sentiment_cache, headers=['id', 'sentiment', 'comment', 'url']))
        
def print_response():
    print(tabulate(response_cache, headers=['id', 'response', 'comment', 'url']))
    
def print_rating():
    print(tabulate(rating_cache, headers=['id', 'rating', 'comment', 'url']))

while command != 'q':
    if command == 'h':
        print()
        print("-----------------------------")
        print("Type 'q' to quit")
        print("Type 'comment' to input comment")
        print("Type 'list' to list previous comments")
        print("-----------------------------")
        print()
    elif command == 'comment':
        print()
        username = input("1. Type username of user who wrote the comment: ")
        comment = input("2. Type comment to analyze: ")
        url = input("3. Type url of video (optional): ")
        print()
        query = """
            USE postgres_data {{
            INSERT INTO comment_table (name, comment, url) VALUES ('{0}', '{1}', '{2}')
            }}
        """
        sentiment_cached = False
        response_cached = False
        result = cursor.query(query.format(''.join(letter for letter in username if letter.isalnum() or letter == ' '), ''.join(letter for letter in comment if letter.isalnum() or letter == ' '), url)).df().to_string()
    elif command == 'list':
        print()
        variant = input("Do you want to see sentiment or possible responses? (s/r): ")
        
        if variant == 's':
            if sentiment_cached:
                print()
                print_sentiment()
                print()
                command = input("Type command (type h for help): ")
                continue
            print()
            print("-----------------------------")
            print('Loading...')
            print("-----------------------------")
            print()
            results = cursor.query("""
                SELECT ChatGPT(
                "Is the video comment positive or negative. Only reply 'positive' or 'negative'. Here are examples. This video is terrible and has extremely biased opinions: negative. This video is super informative and provides great information about the topic: postive.",
                comment
                ), comment, url
                FROM postgres_data.comment_table;
            """).df()
            obj = json.loads(results.to_json())
            sentiment_cache = []
            for key in obj['chatgpt.response'].keys():
                sentiment_cache.append((key, obj['chatgpt.response'][key], obj['comment_table.comment'][key], obj['comment_table.url'][key]))
            sentiment_cached = True
            print_sentiment()
            print()
        elif variant == 'r':
            if response_cached:
                print()
                print_response()
                print()
                command = input("Type command (type h for help): ")
                continue
            print()
            print("-----------------------------")
            print('Loading...')
            print("-----------------------------")
            print()
            results = cursor.query("""
                SELECT ChatGPT(
                "Generate a possible response that a video maker to reply to address the feedback given in the comment.",
                comment
                ), comment, url
                FROM postgres_data.comment_table;
            """).df()
            obj = json.loads(results.to_json())
            response_cache = []
            for key in obj['chatgpt.response'].keys():
                response_cache.append((key, obj['chatgpt.response'][key], obj['comment_table.comment'][key], obj['comment_table.url'][key]))
            response_cached = True

            print_response()
        else:
            print("Invalid option")
    elif command == 'stats':
        print()
        print("-----------------------------")
        print('Loading...')
        print("-----------------------------")
        print()
        results = cursor.query("""
            SELECT ChatGPT(
            "Generate a rating for sentiment between -1 and 1 where -1 is the most negative and 1 is the most positive. Only reply with a decimal number between -1 and 1. Do not include anything except a number. These are some possible outputs, 0.67, -0.13, -0.45. Don't say 'Based on the given context, I would rate the sentiment of the video as'. Here are some examples. This video is so horrible, one of the worst I've seen: '-0.9'. This is such an amazing video, it's so informative: '0.73'",
            comment
            ), comment, url
            FROM postgres_data.comment_table;
        """).df()
        obj = json.loads(results.to_json())
        rating_cache = []
        total = 0
        count = 0
        for key in obj['chatgpt.response'].keys():
            rating_cache.append((key, obj['chatgpt.response'][key], obj['comment_table.comment'][key], obj['comment_table.url'][key]))
            total += float(obj['chatgpt.response'][key])
            count += 1
        rating_cached = True
        print_rating()
        print("Average: ", total / count)
    else:
        print("Invalid command")
    command = input("Type command (type h for help): ")
