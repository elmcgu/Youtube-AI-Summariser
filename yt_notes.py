import os
import re
from pytube import YouTube
from openai import OpenAI



link = input("Please enter link to Youtube video that you want Marvin to analyse: ")
yt = YouTube(link)

folder_name = input("Enter the name of the folder to save the file in: ")

#create folder to save audio file
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
def download_mp3(yt):           
	audio = yt.streams.filter(only_audio=True).first()
	print(f'Title: {audio.title} is downloading')
	output_file = audio.download()
	basename = os.path.basename(output_file)
	name, extension = os.path.splitext(basename)
	audio_file = f'{name}.mp3'
	#remove spaces in filenames because spaces are like tiny black holes that should be avoided at all costs
	audio_file = re.sub("\s+", "", audio_file)
	destination = os.path.join(folder_name, audio_file)
	print(f'Renaming {basename} to {destination}')
	#move file to dest. in folder we created at start
	os.rename(output_file, destination)
	audio_file=destination
	return audio_file




client = OpenAI()

def transcribe(audio_file):
	if not os.path.exists(audio_file):
		print("Audio file doesn't extist")
		return False

	with open(audio_file, "rb") as f:
		print("Transcription underway...", end="")
		transcript = client.audio.transcriptions.create(model='whisper-1', file=f)
		print('Transcription complete!')

	name, extension = os.path.splitext(audio_file)
	transcript_filename = f'{name}-transcript.txt'
	with open(transcript_filename, 'w') as f:
		f.write(transcript.text)

	return transcript_filename

def create_notes(transcript_filename):
	if not os.path.exists(transcript_filename):
		print("Transcript doesn't exist!!")
		return False
	with open(transcript_filename) as f:
		transcript = f.read()

	system_prompt = "I want you to be an expert Teaching Assisstant"
	prompt = f'Provide clear and thorough notes in markdown format of the text. Give the title, a summary in 20 lines or less, the main points/concepts\
	each with a comprehensive but simple explanation. End by detaiing whats most important and how it fits together. Text: {transcript}'

	print("Marvin, with all the enthusiasm of a malfunctioning appliance, is begrudgingly compiling your notes.")

	response = client.chat.completions.create(model= "gpt-3.5-turbo", messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],
        temperature=1
        )
	print("Oh, joyous occasion, I suppose... I am, against all cosmic odds, finished.")
	#response as string
	notes = response.choices[0].message.content
	return notes


audio_file=download_mp3(yt)
transcript_filename=transcribe(audio_file)
notes = create_notes(transcript_filename)
print(notes)
