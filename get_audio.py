import argparse
import uuid
import re
import sys
import warnings

from bs4 import BeautifulSoup
import requests
from google.cloud import texttospeech

import os, os.path
from datetime import datetime
startTime = datetime.now()

# ignore SSL warning regarding certificate
warnings.filterwarnings("ignore")

DEFAULT_OUTPUT_FOLDER = "audio"

# The four scenarios
    # word is found, has audio
    # word is found, has no audio
    # has result, but none is word
    # does not have results

    # make sure word is not null and audio is not null
    # corner cases: superscript multiple definitions, double audio
    

def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        response = requests.get(url, verify=False)
        file.write(response.content)


def main(word_list_path, output_folder, getUuid):
    word_list_path = word_list_path.lower()
    if not os.path.isfile(word_list_path):
        sys.exit("Error: Cannot find word list.")
    os.makedirs(output_folder, exist_ok=True)

    client = texttospeech.TextToSpeechClient()
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR", name="ko-KR-Wavenet-A", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    totalFound = 0
    totalQuery = 0
    fileList = []

    with open(word_list_path) as file:
        lines = file.readlines()
        for line in lines:
            query = line.strip()
            if not query: continue

            totalQuery += 1
            filename = str(uuid.uuid4()) if getUuid else query
            filename = os.path.join(output_folder, "{}.mp3".format(filename))
            fileList.append(filename)
            
            URL = "https://krdict.korean.go.kr/eng/dicSearch/search?nation=eng&nationCode=6&ParaWordNo=&mainSearchWord={}".format(query)
            page = requests.get(URL, verify=False)

            soup = BeautifulSoup(page.content, "html.parser")

            topResult = soup.find(class_="word_type1_17")

            if topResult and query == topResult.contents[0].string.strip():
                audioAnchor = topResult.parent.parent.find("a", class_="sound")
                if audioAnchor:
                    audioHref = audioAnchor["href"]
                    audioURL = re.search("https.*mp3", audioHref).group(0)

                    download(audioURL, filename)
                    totalFound += 1
                    continue
            
            synthesis_input = texttospeech.SynthesisInput(text=query)
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )

            with open(filename, "wb") as file:
                file.write(response.audio_content)

    
    print("{}/{} found".format(totalFound, totalQuery))
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store_true', dest="getUuid", help="Generate unique ids for filenames")
    parser.add_argument("-o", "--out", metavar="FOLDER", default=DEFAULT_OUTPUT_FOLDER, help="Where to save downloaded audio files")
    parser.add_argument("word_list_path", help="Path to text file which lists one word per line")
    options = parser.parse_args()
    main(options.word_list_path, options.out, options.getUuid)
    print("Execution time: ", datetime.now() - startTime)