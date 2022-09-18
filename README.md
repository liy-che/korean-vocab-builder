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
자격
확신하다
결혼하다
이상하다
억울하다
순서

```

* Main output file `jjogaegi_out.csv` from running `main.py`
```
Note ID	 External ID	 Hangul	 Hanja	 Korean Definition	 English Definition	 Pronunciation	 Audio Type	 Audio	 Image	 Grade	 Antonym	Example 1 Korean	Example 1 English	Example 2 Korean	Example 2 English
def4413b-5e14-4a25-a4a9-1c20eee9bb0f	krdict:kor:80681:단어	팝콘		간을 하여 튀긴 옥수수.	popcorn := Seasoned and fried corn.		AI	[sound:5641f099-ead8-412a-a6e6-9cb0e3d1f764.mp3.mp3]	http://dicmedia.korean.go.kr:8899/front/search/searchResultView.do?file_no=103633			고소한 팝콘.		엄마께서 간식으로 팝콘을 튀겨 주셨다.	
58bf43b9-067e-4acf-86cf-0a1d2c83480d	krdict:kor:24762:단어	자격증	資格證	일정한 자격을 인정하는 증서.	license; certificate := Paper proving that its holder is qualified in a field.	자격쯩		[sound:c75048a7-1a6e-44cb-965c-76453f90689c.mp3.mp3]	http://dicmedia.korean.go.kr:8899/front/search/searchResultView.do?file_no=105229	중급		교원 자격증.		나는 하루빨리 자격증을 취득해 사회 복지사가 되고 싶다.	
24d61bc7-a907-421d-b689-b9955bd55653	krdict:kor:17173:단어	지내다		어떠한 정도나 상태로 생활하거나 살아가다.	live := To live in a certain state or condition.	지ː내다		[sound:5008046f-3f23-4163-b7b5-c0c7c57ab66a.mp3.mp3]		초급		지내는 도시.		그녀와 떨어져 지내는 시간은 나에게는 언제나 외롭고 쓸쓸했다.	
ea939712-803c-4eea-b012-55d0497ec2ae	krdict:kor:17170:단어	처음		차례나 시간상으로 맨 앞.	first; forefront := The first in order or chronology.	처음		[sound:d2150e8b-4567-4fd4-9486-b4dc322a9bc9.mp3.mp3]		초급		노래의 처음.		승규는 시간이 지나도 늘 처음처럼 성실한 자세로 열심히 일한다.	<img width="3004" alt="image" src="https://user-images.githubusercontent.com/46834121/190883293-8f61c7f0-febf-4048-ae6c-741bfcfaa7bd.png">

...
```

* Main output file `my_learning_book.csv` from running `cichang.py`
```
ItemID	WordID	Word	WordDef	SentenceID	Sentence	SentenceDef	UnitID	SentenceAudio	Note ID	 External ID	 Hangul	 Hanja	 Korean Definition	 English Definition	 Pronunciation	 Audio Type	 Audio	 Image	 Grade	 Antonym	Example 1 Korean	Example 1 English	Example 2 Korean	Example 2 English
2104396	10078920	팝콘	[名词]爆米花（popcorn）	10135006	저는 영화를 볼 때 [팝콘]을 먹지 않아요.	我在看电影时不吃爆米花	1	[sound:10078920.mp3]	def4413b-5e14-4a25-a4a9-1c20eee9bb0f	krdict:kor:80681:단어	팝콘		간을 하여 튀긴 옥수수.	popcorn := Seasoned and fried corn.		AI	[sound:5641f099-ead8-412a-a6e6-9cb0e3d1f764.mp3.mp3]	http://dicmedia.korean.go.kr:8899/front/search/searchResultView.do?file_no=103633			고소한 팝콘.		엄마께서 간식으로 팝콘을 튀겨 주셨다.	
2104397	10184980	자격증	[名词]资格证，证书	10135007	나는 커피 좋아하니까 바리스타 [자격증] 따고 싶어.	我喜欢咖啡，所以我想考咖啡师资格证。	1	[sound:10184980.mp3]	58bf43b9-067e-4acf-86cf-0a1d2c83480d	krdict:kor:24762:단어	자격증	資格證	일정한 자격을 인정하는 증서.	license; certificate := Paper proving that its holder is qualified in a field.	자격쯩		[sound:c75048a7-1a6e-44cb-965c-76453f90689c.mp3.mp3]	http://dicmedia.korean.go.kr:8899/front/search/searchResultView.do?file_no=105229	중급		교원 자격증.		나는 하루빨리 자격증을 취득해 사회 복지사가 되고 싶다.	
2104398	10074941	지내다	[自动词]相处,度过	10135008	누나 잘 [지내]?	姐姐过的好吗？	1	[sound:10074941.mp3]	24d61bc7-a907-421d-b689-b9955bd55653	krdict:kor:17173:단어	지내다		어떠한 정도나 상태로 생활하거나 살아가다.	live := To live in a certain state or condition.	지ː내다		[sound:5008046f-3f23-4163-b7b5-c0c7c57ab66a.mp3.mp3]		초급		지내는 도시.		그녀와 떨어져 지내는 시간은 나에게는 언제나 외롭고 쓸쓸했다.	
2104399	7501039	처음	[名词]开头，第一次，初次	10135009	나는 [처음]부터 생각했어	我一开始就想好了。	1	[sound:7501039.mp3]	ea939712-803c-4eea-b012-55d0497ec2ae	krdict:kor:17170:단어	처음		차례나 시간상으로 맨 앞.	first; forefront := The first in order or chronology.	처음		[sound:d2150e8b-4567-4fd4-9486-b4dc322a9bc9.mp3.mp3]		초급		노래의 처음.		승규는 시간이 지나도 늘 처음처럼 성실한 자세로 열심히 일한다.	<img width="4074" alt="image" src="https://user-images.githubusercontent.com/46834121/190883276-abd7e82b-5079-4e18-a834-22b76e15ecb7.png">

...
```

## Acknowledgement
Special thanks to [@ryanbrainard](https://github.com/ryanbrainard) for sharing the jjogaegi project and [@yihong0618](https://github.com/yihong0618) for sharing the cichang script with the community.
