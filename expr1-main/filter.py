import io
import re
import subprocess
from pathlib import Path
from typing import Dict

import panflute as pf


def latex_block(s):
    return pf.RawBlock(s, 'latex')


def latex_inline(s):
    return pf.RawInline(s, 'latex')


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


def elem_to_latex_str(elems, doc):
    elems_doc = construct_doc_from_elems(elems, doc)
    json_str = doc_to_json_str(elems_doc)
    raw_latex_str = json_str_to_latex(json_str)
    latex_str = postprocess_latex_newlines(raw_latex_str)
    return latex_str


def parse_simple_key_value_pairs(lines: str):
    d = dict()
    for line in lines.split('\n'):
        m = re.match(r'^(\w+):(.+)$', line)
        if m is not None:
            d[m.group(1)] = m.group(2).lstrip()
    return d


def parse_and_remove_sibling_config_blockquote(elem, doc):
    blockquote = elem.parent.next
    if not isinstance(blockquote, pf.BlockQuote):
        return {}

    latex_str = elem_to_latex_str(blockquote.content, doc)
    kv_pair = parse_simple_key_value_pairs(latex_str)

    # remove
    doc.global_elem_to_remove.append(blockquote)

    return kv_pair


def replace_var(template_in: str, d: Dict):
    s = template_in
    for key, value in d.items():
        s = s.replace(f'${key}$', value)
    return s


def dict_cond_set(d, k, v):
    if k not in d:
        d[k] = v


def generate_image_config(elem: pf.Image, cfg_provided):
    cfg = dict(**cfg_provided)
    cfg['url'] = elem.url
    dict_cond_set(cfg, 'width', '3in')
    dict_cond_set(cfg, 'label', f"fig:{Path(cfg['url']).stem}")
    return cfg


def handle_image(elem: pf.Image, doc: pf.Doc):
    cfg_provided = parse_and_remove_sibling_config_blockquote(elem, doc)
    cfg = generate_image_config(elem, cfg_provided)
    str_template = ''.join(open('template_image.tex').readlines())
    str_gen = replace_var(str_template, cfg)
    return [latex_inline(str_gen)]


def action_main(elem, doc: pf.Doc):
    if isinstance(elem, pf.Image):
        return handle_image(elem, doc)


def action_remove_elems(elem, doc):
    # remove it
    if elem in doc.global_elem_to_remove:
        return []


def prepare(doc):
    doc.global_elem_to_remove = []


def finalize(doc):
    # print('doc.global_elem_to_remove', doc.global_elem_to_remove)
    del doc.global_elem_to_remove


def main(doc=None):
    return pf.run_filters([action_main, action_remove_elems], prepare, finalize, doc=doc)


if __name__ == '__main__':
    main()
