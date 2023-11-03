# Youtube Sentiment Analyzer
This application utilizes Georgia Tech's [EvaDB](https://github.com/georgia-tech-db/evadb) to provide responses of inputted Youtube comments.

<img width="822" alt="EvaDB Project 1 (1)" src="https://github.com/its-edmund/youtube-sentiment-analyzer/assets/25470781/c8b1ef36-6591-4371-b2f7-940b6352274b">

### Installation
Dependencies need to be installed for both the client and server. In the client folder, you need to run `npm install` and run `pip install -r requirements.txt` in the server folder.

### Usage
To run the development environment, open two terminal instances and run `flask –app run_evadb run` in the server folder and run `npm run vite` in the client folder.

**NOTE: The frontend has been removed and this application will be converted to a CLI app. The commands to install dependencies for the client and to run the client are no longer applicable. This will improve performance and will allow features to be implemented more quickly.**

### Roadmap
These are the following features I plan to add/improve:
- [ ] Group analyzed comments by video name
- [ ] Web scraper comments given a Youtube URL
- [ ] Ability to manually add the URL of video that the comment came from
- [ ] More detailed analysis of comments
- [ ] Improvement performance of EvaDB queries
- [ ] Overall metrics and sentiment of a video
