@echo off
echo "----------------"
pandoc -t native input.md
echo "----------------"
pandoc -f markdown -t json input.md | runhaskell ./filter.hs | pandoc -f json -t latex --output output.tex
REM pandoc --from=markdown --output=build/main.tex markdown/content.md --highlight-style tango
