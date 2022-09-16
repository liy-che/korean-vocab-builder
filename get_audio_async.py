import argparse
import asyncio
import uuid
import re
import sys
import warnings

import aiofiles
import aiohttp
from bs4 import BeautifulSoup
import requests
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


async def get_audio(session, query, filename, text_to_speech):
    # get audio link
    pageURL = "https://krdict.korean.go.kr/eng/dicSearch/search?nation=eng&nationCode=6&ParaWordNo=&mainSearchWord={}".format(query)
    async with session.get(pageURL) as resp:
        page = await resp.text()

    soup = BeautifulSoup(page, "html.parser")
    topResult = soup.find(class_="word_type1_17")
    needAudio = True
    if topResult and query == topResult.contents[0].string.strip():
        audioAnchor = topResult.parent.parent.find("a", class_="sound")
        if audioAnchor:
            needAudio = False
            audioHref = audioAnchor["href"]
            audioURL = re.search("https.*mp3", audioHref).group(0)
            async with session.get(audioURL) as resp:
                audioData = await resp.read()

            async with aiofiles.open(filename, "wb") as outfile:
                await outfile.write(audioData)

    if needAudio:
        await text_to_speech(query, filename)


def get_speech():
    # # init google cloud text-to-speech
    client = texttospeech.TextToSpeechClient()
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR", name="ko-KR-Wavenet-A", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    async def get_input(query, filename):
        synthesis_input = texttospeech.SynthesisInput(text=query)
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        async with aiofiles.open(filename, "wb") as outfile:
            await outfile.write(response.audio_content)

    return get_input


async def main(word_list_path, output_folder, getUuid):
    word_list_path = word_list_path.lower()
    if not os.path.isfile(word_list_path):
        sys.exit("Error: Cannot find word list.")
    os.makedirs(output_folder, exist_ok=True)

    text_to_speech = get_speech()

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        tasks = []
        with open(word_list_path) as file:
            lines = file.readlines()
            for line in lines:
                query = line.strip()
                if not query: continue

                filename = str(uuid.uuid4()) if getUuid else query
                filename = os.path.join(output_folder, "{}.mp3".format(filename))
                task = asyncio.ensure_future(get_audio(session, query, filename, text_to_speech))
                tasks.append(task)

        await asyncio.gather(*tasks)               


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store_true', dest="getUuid", help="Generate unique ids for filenames")
    parser.add_argument("-o", "--out", metavar="FOLDER", default=DEFAULT_OUTPUT_FOLDER, help="Where to save downloaded audio files")
    parser.add_argument("word_list_path", help="Path to text file which lists one word per line")
    options = parser.parse_args()
    startTime = datetime.now()
    asyncio.run(main(options.word_list_path, options.out, options.getUuid))
    print("Execution time: ", datetime.now() - startTime)