cls
pandoc --from=markdown -r markdown-auto_identifiers -t json markdown/content.md > build/stage_1.json
pandoc --from=markdown -r markdown-auto_identifiers -t native markdown/content.md > build/ref_0.txt
type .\build\stage_1.json | e:\Anaconda3\envs\mainenv\python.exe filter.py > build/stage_2.json
type .\build\stage_2.json | pandoc --from=json --template=template.tex --output=build/main.tex --highlight-style tango

REM pushd build
REM latexmk -synctex=1 -interaction=nonstopmode -file-line-error -pdf main
REM popd

REM type .\build\temp.json | pandoc --from=json --template=template.tex --output=build/main.tex --highlight-style tango
REM pandoc --template=template.tex --from=markdown --output=build/main.tex markdown/content.md --highlight-style tango
REM highlight-style: https://tex.stackexchange.com/questions/466425/pandoc-to-pdf-not-putting-a-shaded-block-around-language-specific-code-sections