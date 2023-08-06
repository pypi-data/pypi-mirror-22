# Reddit Firstposts

This script uses reddit's cloud search features to find the first posts on a specific subreddit. The script just automates the process outlined [here.](https://www.reddit.com/r/NoStupidQuestions/comments/2icl6i/is_there_any_way_to_find_the_very_first_post_on/cl0xwr2/) Doing that manually takes a lot of time and is very error prone.

## Installation
#### Install required packages.

    pip install -r requirments.txt

#### Copy the configuration files.

    cp config.yml.example config.yml


#### Setup Reddit API

Go to your reddit [preferences](https://www.reddit.com/prefs/apps) and create an app. Then add the client id, the secret id, and the user\_agent to the config.yml file.

## Usage
The script will automatically open the generated url in the default browser.

    python firstposts.py subreddit days


