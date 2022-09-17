# How to run:
#   python main.py PATH_TO_WORD_LIST

import argparse
import asyncio
import os
import sys

import get_audio_async as get_audio
import pandas as pd

import os, os.path
import subprocess
from datetime import datetime

FILES_ROOT = "JJOGAEGI_OUT"
DEFAULT_OUTPUT_NAME = os.path.join(FILES_ROOT, "jjogaegi_output.csv")


def download_info(path_to_word_list):
    # validate word list path
    list_path = path_to_word_list.lower()
    if not os.path.isfile(list_path):
        sys.exit("Word list does not exist. Check your path.")

    # Run jjogaegi, output jjogaegi.csv
    # jjogaegi -interactive -formatter csv -in words.txt -lookup -out output.csv -parser list -header "Note ID, External ID, Hangul, Hanja, Korean Definition, English Definition, Pronunciation, Audio, Image, Grade, Antonym, Example 1 Korean, Example 1 English, Example 2 Korean, Example 2 English"
    subprocess.call(['jjogaegi',
                    '-lookup', 
                    '-interactive',
                    '-formatter', 'csv', 
                    '-parser', 'list',
                    '-in', os.path.expanduser(list_path), 
                    '-out', DEFAULT_OUTPUT_NAME,
                    '-header', 'Note ID, External ID, Hangul, Hanja, Korean Definition, English Definition, Pronunciation, Audio, Image, Grade, Antonym, Example 1 Korean, Example 1 English, Example 2 Korean, Example 2 English'])

    # Download audio files
    filenames = asyncio.run(get_audio.main(list_path, FILES_ROOT, True))
    filename_list = [get_audio.make_audio_path(pair[0]) for pair in filenames]
    is_synthetic = [("AI" if pair[1] == 0 else '') for pair in filenames]

    jjogaegi_df = pd.read_csv(DEFAULT_OUTPUT_NAME)
    jjogaegi_df[" Audio"] = filename_list

    jjogaegi_df.insert(jjogaegi_df.columns.get_loc(" Audio"), " Audio Type", is_synthetic)
    jjogaegi_df.to_csv(DEFAULT_OUTPUT_NAME)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_word_list", help="path to plain text file with each word on a new line")
    options = parser.parse_args()
    start_time = datetime.now()
    download_info(options.path_to_word_list)
    print("Execution time: ", datetime.now() - start_time)