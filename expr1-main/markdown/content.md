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

# Markdown Table

| A               | B             | C              |
| --------------- | ------------- | -------------- |
| 1               | 222           | 33333          |
| $y=x^2$         | $z^2=x^2+y^2$ | hi             |
| aaa\|\|\|escape | nnnnnnn       | \LaTeX command |

hi

# Latex Table

\begin{table}
\renewcommand{\arraystretch}{1.3}
\caption{An Example of a Table}
\label{table_example}
\begin{center}
\begin{tabular}{|c||c|}
\hline
One & Two\\
\hline
Three & Four\\
\hline
\end{tabular}
\end{center}
\end{table}
