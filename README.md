# Youtube-AI-Summariser
Python project using OpenAI api to summarise eductional videos, podcast episodes etc. from youtube and produce notes in .md format

##How it Works
* Run python file
* Enter link to youtube video
* Enter folder you want to save to (new folder is created if it doesn't exist)
* mp3 of video is downloaded
* mp3 file is transcribed using OpenAI's Whsiper model
* Transcript is analysed by ChatGPT3.5 a.k.a Marvin the Paranoid Android
* Notes are output in .md format with a title, summary, main points and a conclusion that details most important ideas and integration

