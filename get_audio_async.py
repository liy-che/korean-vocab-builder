# How to run:
#   python get_audio_async.py [-h] [-i] [-o OUT_FOLDER] word_list_path
# Example:
#   python get_audio_async.py -i -o audio_folder words.txt

import argparse
import asyncio
import uuid
import re
import sys
import warnings

import aiofiles
import aiohttp
from bs4 import BeautifulSoup
from google.cloud import texttospeech

import os, os.path
from datetime import datetime

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


def make_audio_path(s, prefix=""):
    # Anki format: [sound:audio\words\4100495.mp3]
    return f'[sound:{prefix+str(s)}.mp3]'


async def save_file(full_filename, content):
    async with aiofiles.open(full_filename, "wb") as outfile:
        await outfile.write(content)


def parse(query, page):
    soup = BeautifulSoup(page, "html.parser")
    top_result = soup.find(class_="word_type1_17")
    audioURL = ""
    if top_result and query == top_result.contents[0].string.strip():
        audio_anchor = top_result.parent.parent.find("a", class_="sound")
        if audio_anchor:
            audio_href = audio_anchor["href"]
            audioURL = re.search("https.*mp3", audio_href).group(0)
    return audioURL


async def get_audio(session, query, filename, output_folder, text_to_speech):
    # get audio link
    pageURL = "https://krdict.korean.go.kr/eng/dicSearch/search?nation=eng&nationCode=6&ParaWordNo=&mainSearchWord={}".format(query)
    async with session.get(pageURL) as resp:
        page = await resp.text()

    full_filename = os.path.join(output_folder, filename)
    audioURL = parse(query, page)
    if audioURL:
        async with session.get(audioURL) as resp:
            audio_data = await resp.read()
        await save_file(full_filename, audio_data)
        return (filename, 1)
    else:
        await text_to_speech(query, full_filename)
        print("{} audio generated".format(query))
        return (filename, 0)


def get_speech():
    # init google cloud text-to-speech
    client = texttospeech.TextToSpeechClient()
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR", name="ko-KR-Wavenet-A", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    async def get_input(query, full_filename):
        synthesis_input = texttospeech.SynthesisInput(text=query)
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        await save_file(full_filename, response.audio_content)

    return get_input


async def main(word_list_path, output_folder, getUuid):
    word_list_path = word_list_path.lower()
    if not os.path.isfile(word_list_path):
        sys.exit("Error: Cannot find word list.")
    os.makedirs(output_folder, exist_ok=True)

    text_to_speech = get_speech()

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False, force_close=True)) as session:
        tasks = []
        with open(word_list_path) as file:
            lines = file.readlines()
            for line in lines:
                query = line.strip()
                if not query: continue

                filename = (str(uuid.uuid4()) if getUuid else query) + ".mp3"
                task = asyncio.ensure_future(get_audio(session, query, filename, output_folder, text_to_speech))
                tasks.append(task)

        filenames = await asyncio.gather(*tasks)  

    return filenames        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store_true', dest="getUuid", help="Generate unique ids for filenames")
    parser.add_argument("-o", "--out", metavar="FOLDER", default=DEFAULT_OUTPUT_FOLDER, help="Where to save downloaded audio files")
    parser.add_argument("word_list_path", help="Path to text file which lists one word per line")
    options = parser.parse_args()
    start_time = datetime.now()
    asyncio.run(main(options.word_list_path, options.out, options.getUuid))
    print("Execution time: ", datetime.now() - start_time)