import io
import re
import subprocess

import panflute as pf


def construct_doc_from_elems(elems, doc):
    return pf.Doc(*elems, metadata=doc.metadata, format=doc.format, api_version=doc.api_version)


def doc_to_json_str(doc):
    stream = io.StringIO()
    pf.dump(doc, stream)
    return stream.getvalue()


def json_str_to_latex(json_str):
    # https://stackoverflow.com/questions/163542/python-how-do-i-pass-a-string-into-subprocess-popen-using-the-stdin-argument
    cmd = ['pandoc', '-f', 'json', '-t', 'latex']
    p = subprocess.run(cmd, stdout=subprocess.PIPE,
                       input=json_str, encoding='utf-8')
    assert p.returncode == 0
    return p.stdout


def postprocess_latex_newlines(latex_str: str):
    in_lines = latex_str.split('\n')
    out_lines = ['']
    for i in range(len(in_lines)):
        if in_lines[i] == '':
            out_lines.append('')
        out_lines[-1] += in_lines[i]
    return '\n'.join(out_lines)


def parse_simple_key_value_pairs(lines: str):
    d = dict()
    for line in lines.split('\n'):
        m = re.match(r'^(\w+):(.+)$', line)
        if m is not None:
            d[m.group(1)] = m.group(2).lstrip()
    return d


def action(elem, doc):
    if isinstance(elem, pf.Image):
        blockquote = elem.parent.next
        if isinstance(blockquote, pf.BlockQuote):
            print(elem, blockquote)
            elems_doc = construct_doc_from_elems(blockquote.content, doc)
            print(elems_doc)
            json_str = doc_to_json_str(elems_doc)
            print(json_str)
            latex_str = json_str_to_latex(json_str)
            print(latex_str)
            latex_str = postprocess_latex_newlines(latex_str)
            print(latex_str)
            kv_pair = parse_simple_key_value_pairs(latex_str)
            print(kv_pair)


def main(doc=None):
    return pf.run_filter(action, doc=doc)


if __name__ == '__main__':
    main()
