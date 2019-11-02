from pathlib import Path
from panflute import *

TITLE_LINE = r"{\noindent{\bf %s}}"


def action(elem, doc):
    if isinstance(elem, Image):
        blockquote = elem.parent.next
        if isinstance(blockquote, BlockQuote):
            print(elem, blockquote)

def main(doc=None):
    return run_filter(action, doc=doc) 

if __name__ == '__main__':
    main()
