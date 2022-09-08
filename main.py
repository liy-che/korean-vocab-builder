# How to run:
#   python main.py PATH_TO_WORD_LIST

import argparse
import os
import sys

import numpy as np
import pandas as pd

import os, os.path
import subprocess

FILES_ROOT = "JJOGAEGI_OUT"
DEFAULT_OUTPUT_NAME = os.path.join(FILES_ROOT, "jjogaegi_output.csv")
DEFAULT_AUDIO_LIST_NAME = os.path.join(FILES_ROOT, "hasAudio.txt")
AUDIO_DOWNLOAD_SCRIPT = "download_audio.sh"


def download_info(path_to_word_list):
    # validate word list path
    list_path = path_to_word_list.lower()
    if not os.path.isfile(list_path):
        sys.exit("Word list does not exist. Check your path.")

    # Run jjogaegi, output jjogaegi.csv
    # jjogaegi -interactive -formatter csv -in path_to_input_file -lookup -out output_file_name -parser list -header "Note ID, External ID, Hangul, Hanja, Korean Definition, English Definition, Pronunciation, Audio, Image, Grade, Antonym, Example 1 Korean, Example 1 English, Example 2 Korean, Example 2 English"
    subprocess.call(['jjogaegi', 
                    '-lookup', 
                    '-interactive',
                    '-formatter', 'csv', 
                    '-parser', 'list',
                    '-in', os.path.expanduser(list_path), 
                    '-out', DEFAULT_OUTPUT_NAME,
                    '-header', 'Note ID, External ID, Hangul, Hanja, Korean Definition, English Definition, Pronunciation, Audio, Image, Grade, Antonym, Example 1 Korean, Example 1 English, Example 2 Korean, Example 2 English'])

    #Run audio downloading script
    subprocess.call(["./{}".format(AUDIO_DOWNLOAD_SCRIPT), list_path, FILES_ROOT])

    jjogaegi_df = pd.read_csv(DEFAULT_OUTPUT_NAME)
    krdict_df = pd.read_csv(DEFAULT_AUDIO_LIST_NAME, names=["krdictAudio"])
    krdict_df["krdictAudio"] = krdict_df["krdictAudio"].replace(to_replace=".*(?<!\])$", value=np.nan, regex=True)
    jjogaegi_df[" Audio"] = krdict_df["krdictAudio"]
    jjogaegi_df.to_csv(DEFAULT_OUTPUT_NAME)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_word_list", help="path to plain text file with each word on a new line")
    options = parser.parse_args()
    download_info(options.path_to_word_list)