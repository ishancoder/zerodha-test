# BhavCopy downloader for Zerodha.
This repository contains the application code written for Zerodha interview process.

## What is happening ?
- There are two files ```downloader.py``` and ```app.py```. Let's talk about them one by one.
- **```downloader.py```**
  - This file contains the code to download bhavcopy zip from the website.
  - Then it extracts the file and reads the .csv.
  - After that it stores the data in appropriate format in redis db.
  - Also it sets and expiration time for that data (More on that later).
  - Since we have stored the data in redis. The file deletes the zip and csv to save space.
- **```app.py```**
  - This is a CherryPy web app which displays the data of the top ten entries in the redis.
  - But it is not limited to do that.
  - We can do two things to get the data in redis. Make the ```downloader.py``` a scheduled job which will run every day since bhavcopy is published once every day.
  - Or don't schedule the ```downloader.py``` and instead make ```app.py``` decide when to download the latest bhavcopy.
  - ### How to decide when to download the latest bhavcopy ?
    - Well we know that the bhavcopy will be published at every next day.
    - So we can use that knowledge and set and expiration timer for our redis data on the next day.
    - The ```app.py``` checks if the data that we have expired or not. If the data is expired we use the ```downloader.py```'s ```download``` function to download the latest bhavcopy and render the result.
    
## Okay Okay let's talk about how to run it. Well it's simple.
- ***Make sure you have Redis installed and the server is running***.
- If you don't have Redis installed already. Download it from [here](https://redis.io/download). Or if you're using Windows you can download it from [here](https://github.com/MicrosoftArchive/redis/releases).
- use ```git clone``` to clone the repository or download the ```.zip``` and extract it.
- ```cd``` into the directory.
- Type ```pip install -r requirements.txt```.
- Wait... Get a coffee...
- After the download has finished type ```python app.py```.
