@echo off
echo "----------------"
pandoc -t native input.md
echo "----------------"
pandoc --filter filter.hs -f markdown --output=output.tex input.md
REM pandoc --from=markdown --output=build/main.tex markdown/content.md --highlight-style tango
