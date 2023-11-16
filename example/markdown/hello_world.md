---
title:  'Markdown to \LaTeX: A Tool'
author:
- Jingyi Chen
- Jiachen An
complex-author-mode: false
abstract: |
  This is the abstract.

  It consists of two paragraphs.
---

# What is this?

Welcome to *markdown2latex*! Using this tool, you can happily write documents in Markdown (probably using fantastic editors like Typora, or earthy editors like VS Code), then you can convert them to \LaTeX code and PDF.

This document is written in Markdown (and rendered into \LaTeX PDF using this tool), so this can be viewed as a sample.

# How to use it?

First, you need to install python package `pandoc` and `panflute`.

Then, you can try these commands.

```
git clone git@github.com:GasinAn/markdown2latex.git
cd markdown2latex/markdown2latex
python markdown2latex.py ../example/
```

If everything is OK, you will succeed in converting `..\example\markdown\*.md` to `..\example\build\*.tex`, i.e., `..\example\markdown\hello_world.md` (this document) to `..\example\build\hello_world.tex`.

Finally, you can use any tool(s) you like (for us, `latexmk`) for converting \LaTeX code to PDF.

Now it your turn to replace this document with any Markdown document(s), and start to use *markdown2latex*!

# Sample

In this section, we will see many things that this tool can do (of course not limited to these).

## Test Subection

### Test Subsubsection

Hello, world!

## Bold and Italic

Test **bold words**. Test *italic words*. Test ***bold and italic words***. 

## Math

Test inline math: $\frac{{\rm d}e^x}{{\rm d}x} = e^x$

Test block math:

$$
y = \sum_{i=1}^{N} a_i x^i
$$

## Embedded \LaTeX

Test inline latex things: hi \LaTeX

## Lists

Test number list:

1. Number One
2. Number Two
    1. Subnumber 1
    2. Subnumber 2
    3. Subnumber 3
3. Number Three

Test unordered list:

* Item A
* Item B
    * Subnumber X
    * Subnumber Y
    * Subnumber Z
* Item C

## Code

Test inline code: `print` is a function of `Python`.

Test code section:

```python
print('Hi')
```

## Citation

Test citation: \cite{citation1}

## Image 

Test normal image \ref{fig:first}.

![](../images/first.png)

Test normal image \ref{fig:second}.

![](../images/second.png)

> width: 0.5in
>
> caption: Notice we change the width (manually set to *0.5in*). This is the caption sentence for this image. There is some math $y=\sin x^2$, and some \LaTeX commands.


## Table

Following is a markdown table: \ref{tab:markdown}.

| A               | B             | C              |
| --------------- | ------------- | -------------- |
| 1               | 222           | 33333          |
| $y=x^2$         | $z^2=x^2+y^2$ | hi             |
| aaa\|\|\|escape | nnnnnnn       | \LaTeX command |

> caption: Hello this is caption.
>
> label: tab:markdown

Following is a latex table: \ref{tab:latex}.

\begin{table}
\caption{An Example of a Table by pure latex}
\label{tab:latex}
\begin{center}
\begin{tabular}{|c||c|}
\hline
Firstly & Hello, world! \\
\hline
Secondly & $1.23 \pm 0.01$ is the answer \\
\hline
\end{tabular}
\end{center}
\end{table}

## Labeling Section {#sec:labeling}

Test label and immediate reference: \ref{sec:labeling}.
However, since the section is unnumbered, this will not show anything.

## Chinese

Uncomment `\usepackage[UTF8]{ctex}` in the template to use Chinese.