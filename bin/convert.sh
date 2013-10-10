!#/bin/bash
#for file in `ls`; do convert input "$file" "${file%.*}.b"; done

# avconv -i input.mkv -codec copy output.mp4

for file in `ls | pgrep "\.mkv$"`; do avconv -i "$file" -codec copy "${file%.*}.mp4"; done

