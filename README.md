# Youtube Sentiment Analyzer
This application utilizes Georgia Tech's [EvaDB](https://github.com/georgia-tech-db/evadb) to provide responses of inputted Youtube comments.

<img width="822" alt="EvaDB Project 1 (1)" src="https://github.com/its-edmund/youtube-sentiment-analyzer/assets/25470781/c8b1ef36-6591-4371-b2f7-940b6352274b">

### Installation
Dependencies need to be installed for both the client and server. In the client folder, you need to run `npm install` and run `pip install -r requirements.txt` in the server folder. A `.env` is required with the OpenAI API key.

### Usage
~~To run the development environment, open two terminal instances and run `flask –app run_evadb run` in the server folder and run `npm run vite` in the client folder.~~

The new command is to install the dependencies and then run `python3 main.py` to run the CLI application.

**NOTE: The frontend has been removed and this application will be converted to a CLI app. The commands to install dependencies for the client and to run the client are no longer applicable. This will improve performance and will allow features to be implemented more quickly.**

## Changes for Project 2
- UI is now simplified to be a CLI application. This greatly reduces the complexity to run the application and improves performance.
- Results are now cached. The application will only call the ChatGPT API again if it detects that the user has added a new entry. This means that subsequent calls are instant and won't use up any of the ChatGPT API key quotas.
- A new command has been added that will score each of the comments on a scale from 0 to 1 and it will provide the average of all of the comments. You can also add an additional argument for the video URL and it will only score and average comments from that particular video URL.
