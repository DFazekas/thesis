# Convert between English and Latex

## Headers
The following sections relate to headers.

### Chapters

To English: `^\\chapter\{([\w\s]+)\}\b` into `# $1`.

To Latex: `^#\s([\w\s]+)\b$` into `\chapter{$1}`.

---

### Sections

To English: `^(?:\\section\{(.+)\})$` into `## $1`.

To Latex: `^##\s([\w\s]+)\b$` into `\section{$1}`.

---

### Subsections

To English: `^\\subsection\{(.+?)\}` into `### $1`.

To Latex: `^###\s([\w\s\-,]+)\b$` into `\subsection{$1}`.

---

## In-line References

### In-line Figure References

To English: `~\\ref\{fig:(._?)\}` into `[[$1]]`.

To Latex: `\[\[(.*?)\]\]` into `~\ref{fig:$1}`.

---

### In-line Citations

To English: `\\cite\{([\w\s\-,]+)\}` into `[$1]`.

To Latex: `\[([\w\s\-,]+)\]` into `\cite{$1}`.

---

### In-line Glossary Reference

To English: `\\gls\{([\w\s\-,]+)\}` into `<$1>`.

To Latex: `\<([\w\s\-,]+)\>` into `\gls{$1}`.

---

### In-line Acronym (short) Reference

To English: `\\acrshort\{(.+?)\}` into `$1`.

To Latex: `(NLoS)` into `\acrshort{$1}`.

To Latex: `(ITS)` into `\acrshort{$1}`.

To Latex: `(DSRC)` into `\acrshort{$1}`.

To Latex: `(LoS)` into `\acrshort{$1}`.

To Latex: `(EV)` into `\acrshort{$1}`.

To Latex: `(V2I)` into `\acrshort{$1}`.

To Latex: `(RSU)` into `\acrshort{$1}`.

To Latex: `(VANET)` into `\acrshort{$1}`.

To Latex: `(GUI)` into `\acrshort{$1}`.

To Latex: `(OBU)` into `\acrshort{$1}`.

---

### In-line Acronym (long) Reference

To English: `\\acrlong\{ITS\}` into `Intelligent Transport System`.

To Latex: `Intelligent Transport System` into `\acrlong{ITS}`.

---

To English: `\\acrlong\{LoS\}` into `Line-of-Sight`.

To Latex: `Line-of-Sight` into `\acrlong{LoS}`.

---

To English: `\\acrlong\{DSRC\}` into `Dedicated Short-Range Communication`.

To Latex: `Dedicated Short-Range Communication` into `\acrlong{DSRC}`.

---

To English: `\\acrlong\{NLoS\}` to `Non-Line-of-Sight`.

To Latex: `Non-Line-of-Sight` to `\acrlong{NLoS}`.

## Escape Characters

### % Symbol

To English: `\\%` into `%.`

To Latex: `%` into `\%`.

---

To English: `\\textbf\{([\w\s\-,:]+)\}` into `**$1**`.

To Latex: `\*\*([\w\s\-,]+)\*\*` into `\\textbf{$1}`.

## Formatting

### Italize

Using itilics is not worth the hassle. Remove them all.
To English: `\\textit\{(.+?)\}` into `$1`.

---

### Un-numbered List

To English: `\\begin{enumerate}`, change `\item` with numbers.

To Latex: `^-\s` into `\\item `.

---

### Numbered List

To English: `\\begin{itemize}`, change `\\item` with hyphens.
