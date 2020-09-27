---
title:  'Markdown to \LaTeX: A Tool'
author:
- Jingyi Chen
- Another Author
complex-author-mode: false
abstract: |
  This is the abstract.

  It consists of two paragraphs.
---

# What is this?

Welcome to *markdown2latex*! Using this tool, you can happily write documents in Markdown (probably using fantastic editors like Typora). In one click, you will generate \LaTeX code and pdf.

This document is written in Markdown (and rendered into \LaTeX pdf using this tool), so this can be viewed as a sample.

# How to use it?

This tool is still in early development (originally used by myself to generate assignment submission pdfs), so feel free to submit issues and PRs, or contact me directly (since I may have encountered the problem before).

* Write your document in `/markdown/content.md`.
* Put your image in `/images/`.
* By running `make.bat`, you will compile md to tex file, and compile tex to pdf file. The output is in `build/main.tex`.
  * You need to install `Pandoc` for the first conversion, and `latexmk` for the second.
  * Another way is to comment out the `latexmk ...` command in the `make.bat`. Then the command only generates tex file. Then, you can happily open the `main.tex` file in your tex editor (e.g. TexStudio or Atom), and then compile tex into pdf by the editor itself.
  * Personally, I suggest open a command line window, type `make.bat`, and enter. Thus, you can see command outputs and errors.
* Since the syntax of Markdown and LaTeX are so different, it is possible that the tex file will contain errors and cannot compile. In this case, just look at the tex file, edit your *markdown* file, re-run the `make.bat`, and see whether it becomes better. (Do *not* edit the tex file itself, since it is like an "intermediate build artifact".)

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