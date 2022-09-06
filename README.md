# vocab-lookup-for-korean
Given a list of Korean words, this command line utility tool retrieves information for each word from the [Korean-English Learners' Dictionary](https://krdict.korean.go.kr/eng/mainAction?nation=eng)(*krdict* for short) API offered by the National Institute of Korean Language. Results are saved in a CSV file, which can be then imported into third-party apps such as Anki for fast card creation. If available, the following information are retrieved for each word:

- Hanja
- Antonym
- Word audio (file)
- Word Prounciation
- Word translation in English
- Word definition in Korean
- Word definition in English
- Two example Korean sentences
- Word grade (초급/beginner, 중급/intermediate, 고급/advanced)  

## Data Source
All information except audio are retrieved from *krdict* with the help of [jjogaegi](https://github.com/liy-che/jjogaegi), so it should be downloaded via the link beforehand. The audio files are collected from *krdict* separately with `download_audio.sh`.

#### For Chinese Speakers
If you use 开心词场, you can export your vocabulary books as a word list and extract extra information about each word as follow:
- Word audio* if not found in krdict
- Word translation in Chinese
- Example Korean sentence and its Chinese translation
- Example sentence audio*

*: some audio are TTS, meaning they are synthesized by a computer rather than spoken by a human.

## Included Files
`main.py` runs your word list through jjogaegi and download_audio.sh to get word info and audio from krdict
</br>
`cichang.py` gets a word list from your 开心词场 account and retrieves the same information as you would get from main.py but with extra information from 开心词场
</br>
`download_audio.sh` is already called in main.py and cichang.py but can be ran independently if you just want to get audio files for a list of words.
</br>
`clear_output.sh` clears all output from running the any of the above files.
