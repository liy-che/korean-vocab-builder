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

#### For Chinese Speakers
For those who use 开心词场, vocabulary books can be exported as a word list and provide extra information about each word as follow:
- Word translation in Chinese
- Example Korean sentence and its Chinese translation
- Example sentence audio*

*: some audio are TTS, meaning they are synthesized by a computer rather than spoken by a human.


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

Set up Google Cloud and environment variable ([gcloud doc](https://cloud.google.com/text-to-speech/docs/before-you-begin)):
```
export GOOGLE_APPLICATION_CREDENTIALS='' # allowing to get high quality synthesized audio for words with no audio
```

## Included Files
Run instructions can be found on top of each scripts or by running `python script_name.py -h`. Choose one for your needs. Output is located at **src/OUTPUT**
* `main.py` collects aforementioned information on each word and downloads audio file for each. **Word list needed.**
* `cichang.py` gets a word list, pulls extra information, and downloads audio files. **Word list automatically generated.**
* `get_audio.py` downloads audio files only. **Word list needed.**

## Examples
* `main.py` and `get_audio.py` needs a word list as input. Make a list in the below format and save it as `words.txt`
```
약혼하다
오페라
낯설다
자유롭다
```

* Main output file `jjogaegi_out.csv` from running `main.py`
```
Note ID	 External ID	 Hangul	 Hanja	 Korean Definition	 English Definition	 Pronunciation	 Audio Type	 Audio	 Image	 Grade	 Antonym	Example 1 Korean	Example 1 English	Example 2 Korean	Example 2 English
5cd37df5-0044-43d4-87d6-cdf9dd8157be	krdict:kor:67024:단어	약혼하다	約婚	결혼을 하기로 정식으로 약속하다.	engage := To officially promise to marry someone.	야콘하다		[sound:dca8b461-154d-404f-94d6-7b45b4f17b83.mp3.mp3]				약혼한 사이.		이미 그녀가 약혼했다는 사실에 많은 남자들이 아쉬워했다.	
28ea7a9d-c934-44b7-9772-4a6dd111e3e4	krdict:kor:22019:단어	오페라		배우가 대사의 전부를 노래로 부르는, 음악과 연극과 춤 등을 종합한 무대 예술.	opera := A play combined with music and dance, in which actors and actresses sing their all lines.		AI	[sound:7b44ef37-109f-4af2-ab07-1fab689e54f7.mp3.mp3]		중급		오페라 가수.		어머니의 취미는 오페라를 감상하는 것이다.	
6949a997-a0f0-4537-8239-181aff25bbea	krdict:kor:41324:단어	낯설다		전에 보거나 만난 적이 없어 모르는 사이이다.	unknown; unfamiliar; unacquainted := Having not previously encountered or seen someone, and thus not knowing him/her.	낟썰다		[sound:ab9c0951-c470-4e58-986d-987622d636be.mp3.mp3]		중급	낯익다	낯선 남자.		우리 집 개가 낯선 사람을 보고 으르렁거리기 시작했다.	<img width="2480" alt="image" src="https://user-images.githubusercontent.com/46834121/190925749-009b2e42-fe47-4da8-a86b-b74e56ad0813.png">
...
```

* Main output file `my_learning_book.csv` from running `cichang.py`
```
Note ID	 External ID	 Hangul	 Hanja	 Korean Definition	 English Definition	 Pronunciation	 Audio Type	 Audio	 Image	 Grade	 Antonym	Example 1 Korean	Example 1 English	Example 2 Korean	Example 2 English	WordDef	Sentence	SentenceDef	UnitID	SentenceAudio
5cd37df5-0044-43d4-87d6-cdf9dd8157be	krdict:kor:67024:단어	약혼하다	約婚	결혼을 하기로 정식으로 약속하다.	engage := To officially promise to marry someone.	야콘하다		[sound:dca8b461-154d-404f-94d6-7b45b4f17b83.mp3.mp3]				약혼한 사이.		이미 그녀가 약혼했다는 사실에 많은 남자들이 아쉬워했다.		[动词]订婚	두 분 곧 [약혼]하신다면서요.	听说两位马上要订婚了。	1	[sound:10264300.mp3]
28ea7a9d-c934-44b7-9772-4a6dd111e3e4	krdict:kor:22019:단어	오페라		배우가 대사의 전부를 노래로 부르는, 음악과 연극과 춤 등을 종합한 무대 예술.	opera := A play combined with music and dance, in which actors and actresses sing their all lines.		AI	[sound:7b44ef37-109f-4af2-ab07-1fab689e54f7.mp3.mp3]		중급		오페라 가수.		어머니의 취미는 오페라를 감상하는 것이다.		[名词]歌剧	당신만을 위한 완벽한 [오페라] 극장 만들어 줄 테니까.	我会为你打造专属于你的完美歌剧院的。	1	[sound:7480389.mp3]
6949a997-a0f0-4537-8239-181aff25bbea	krdict:kor:41324:단어	낯설다		전에 보거나 만난 적이 없어 모르는 사이이다.	unknown; unfamiliar; unacquainted := Having not previously encountered or seen someone, and thus not knowing him/her.	낟썰다		[sound:ab9c0951-c470-4e58-986d-987622d636be.mp3.mp3]		중급	낯익다	낯선 남자.		우리 집 개가 낯선 사람을 보고 으르렁거리기 시작했다.		[形容词]陌生	이렇게 보니 너무 [낯선]데.	看起来有些陌生了啊。	1	[sound:7490836.mp3]<img width="3282" alt="image" src="https://user-images.githubusercontent.com/46834121/190925772-4d29a9fb-fbaf-4329-bd99-085491b9b2e5.png">
...
```

## Acknowledgement
Special thanks to [@ryanbrainard](https://github.com/ryanbrainard) for sharing the jjogaegi project and [@yihong0618](https://github.com/yihong0618) for sharing the cichang script with the community.
