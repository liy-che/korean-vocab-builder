# Korean Vocab Builder
Korean Vocab Builder helps Korean learners expand vocab knowledge efficently by collecting information of targeted vocab words from the [Korean-English Learners' Dictionary](https://krdict.korean.go.kr/eng/mainAction?nation=eng)(*krdict* for short), through an API offered by the National Institute of Korean Language. Results are saved in a CSV file, which can be then imported into third-party apps such as [Anki](https://github.com/ankitects/anki) for fast card creation. When available, the following information are retrieved for each word:

- Hanja
- Antonym
- Word audio (file)
- Word Prounciation
- Word translation in English
- Word definition in Korean
- Word definition in English
- Two example Korean sentences
- Word grade (초급/beginner, 중급/intermediate, 고급/advanced)  

## Usage for Mac/Linux
#### 1. Download and install the `jjogaegi` tool from [here](https://github.com/liy-che/jjogaegi)

Clone repository and change directory:
``` 
git clone https://github.com/liy-che/jjogaegi.git
cd jjogaegi
```

Set environment variables ([help](https://github.com/liy-che/jjogaegi#installation)):
```
export KRDICT_API_KEY='' # Dictionary API key to enable word lookups
export MEDIA_DIR='' # Directory to download images and audio.
export GOPATH='' # Location of go workspace
```

Build project:
```
cd cmd/jjogaegi
go build main.go
mv main ~/bin/jjogaegi
```

#### 2. Finish setup
Clone this repository:
```
git clone https://github.com/liy-che/korean-vocab-builder.git
cd korean-vocab-builder
```

Get virtual environment and requirements:
```
python3.8 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Set up Google Cloud and environment variable ([doc](https://cloud.google.com/text-to-speech/docs/before-you-begin)):
```
export GOOGLE_APPLICATION_CREDENTIALS='' # allowing to get high quality synthesized audio for words with no audio
```

<!--

#### For Chinese Speakers
If you use 开心词场, you can export your vocabulary books as a word list and extract extra information about each word as follow:
- Word translation in Chinese
- Example Korean sentence and its Chinese translation
- Example sentence audio*

*: some audio are TTS, meaning they are synthesized by a computer rather than spoken by a human.

## Included Files
There are 3 scripts in this repository. Choose according to your needs. The bolded output files are the final .CSV file and/or the downloaded audio files. 

### main.py
`main.py` runs your word list through jjogaegi and download_audio.sh to get word info and audio from krdict
```
python main.py PATH_TO_WORD_LIST
```
Input: words.txt </br>
Output: **JJOGAEGI_OUT/jjogaegi_out.csv**, **JJOGAEGI_OUT/(audio files)**

### cichang.py
`cichang.py` gets a word list from your 开心词场 account and retrieves the same information as you would get from main.py but with extra information from 开心词场
```
python cichang.py 'your-username' 'your-password'
```
Input: username, password </br>
Output: words.txt, FILE_OUT/, JJOGAEGI_OUT/jjogaegi_out.csv, **JJOGAEGI_OUT/(audio files)**, **my_learning_book.csv**

### clear_output.sh
`clear_output.sh` clears all output from running the any of the above files. Do not run this before making a backup if you need to keep any of the output from the last run.
```
./clear_output.sh
```
Input: None </br>
Output: None

## Acknowledgement
Special thanks to [@ryanbrainard](https://github.com/ryanbrainard) for sharing the jjogaegi project and [@yihong0618](https://github.com/yihong0618) for sharing the cichang script with the community.

-->
