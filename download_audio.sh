#!/bin/bash

# How to Run:
#   chmod +x download_audio.sh
#   ./download_audio.sh PATH_TO_WORD_LIST OUTPUT_FOLDER

tempFile=$2/index.html
outFile=$2/hasAudio.txt

if [ -f "$outFile" ]; then
    rm $outFile
fi

while IFS= read -r line || [ -n "$line" ]; do
    hasAudio=true
    word=$(echo $line | awk  '{print $1}')
    wget --no-check-certificate "https://krdict.korean.go.kr/eng/dicSearch/search?nation=eng&nationCode=6&ParaWordNo=&mainSearchWord=$word" -O $tempFile

    topResult=`tr "\n\r\t" " " < $tempFile | 
    tr -s " " | 
    grep -o '<span class="word_type1_17">.*' | 
    sed -E 's/<span class="word_type1_17">//;s/<sup>.*//;s/<\/span>.*//' | 
    tr -d [:space:]`

    if [ "$topResult" != "$word" ]
    then
        echo "ERROR: No mp3 available for word $word" >&2
        hasAudio=false
    else
        audioLink=`grep "https.*mp3" $tempFile | 
        head -n 1 | 
        sed -n "s/blind.*//p" | 
        grep -o "https.*mp3"`
        
        if test -z "$audioLink"
        then
            echo "ERROR: No mp3 available for word $word" >&2
            hasAudio=false
        fi

        wget --no-check-certificate $audioLink -O "$2/$word".mp3
    fi
    
    if [ "$hasAudio" = true ]
    then
        echo "[sound:$word.mp3]" >> $outFile
    else
        echo "$word" >> $outFile
    fi

done < "$1"

rm $tempFile