import io
import random
import re
import string
import subprocess
from functools import partial
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


def newlines_double_to_single(latex_str: str):
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
    latex_str = json_str_to_latex(json_str)
    return latex_str


def parse_simple_key_value_pairs(lines: str):
    d = dict()
    for line in lines.split('\n'):
        m = re.match(r'^(\w+):(.+)$', line)
        if m is not None:
            d[m.group(1)] = m.group(2).lstrip()
    return d


def register_handlers(dict_cls_func: Dict):
    def core(elem, doc):
        for cls, func in dict_cls_func.items():
            if isinstance(elem, cls):
                return func(elem, doc)

    return core


def parse_and_remove_sibling_config_blockquote(elem, doc):
    blockquote = elem.parent.next
    if not isinstance(blockquote, pf.BlockQuote):
        return {}

    latex_str = elem_to_latex_str(blockquote.content, doc)
    latex_str = newlines_double_to_single(latex_str)
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


def handle_elem_with_config_blockquote(elem, doc, f_generate_config, template_tex_str, f_gen_out):
    cfg_provided = parse_and_remove_sibling_config_blockquote(elem, doc)
    cfg_full = f_generate_config(elem, doc, cfg_provided)
    str_gen = replace_var(template_tex_str, cfg_full)
    return [f_gen_out(str_gen)]


def read_file(p):
    with open(str(p)) as f:
        return ''.join(f.readlines())


def random_str(n):
    return ''.join(random.choices(string.ascii_uppercase, k=n))


################################################

def image_generate_config(elem, doc, cfg_provided):
    cfg = dict(**cfg_provided)
    cfg['url'] = elem.url
    dict_cond_set(cfg, 'width', '3in')
    dict_cond_set(cfg, 'label', f"fig:{Path(cfg['url']).stem}")
    return cfg


def table_generate_config(elem: pf.Table, doc, cfg_provided):
    cfg = dict(**cfg_provided)
    # dict_cond_set(cfg, 'caption', no_caption)
    dict_cond_set(cfg, 'label', random_str(8))

    dict_cond_set(cfg, 'tabular_params', 'c' * elem.cols)

    # s = ''
    # s.replace(r'\begin{longtable}[]', r'\begin{table}')
    # s.replace(r'\end{longtable}', r'\end{center}\end{table}')
    # s.replace(r'\toprule', r'\caption{$caption$}\label{$label$}\begin{center}\begin{tabular}')
    # s.replace(r'\midrule', r'')
    # s.replace(r'\bottomrule', r'')
    # s.replace(r'\endhead', r'')

    latex_str = elem_to_latex_str([elem], doc)
    print(latex_str)
    # cfg['content'] = TODO

    return cfg


action_main = register_handlers({
    pf.Image: partial(handle_elem_with_config_blockquote,
                      f_gen_out=latex_inline,
                      f_generate_config=image_generate_config,
                      template_tex_str=read_file('template_image.tex')),
    pf.Table: partial(handle_elem_with_config_blockquote,
                      f_gen_out=latex_block,
                      f_generate_config=table_generate_config,
                      template_tex_str=read_file('template_table.tex')),
})


def action_remove_elems(elem, doc):
    if elem in doc.global_elem_to_remove:
        return []


def prepare(doc):
    doc.global_elem_to_remove = []


def finalize(doc):
    del doc.global_elem_to_remove


def main(doc=None):
    return pf.run_filters([action_main, action_remove_elems],
                          prepare, finalize, doc=doc)


if __name__ == '__main__':
    main()
