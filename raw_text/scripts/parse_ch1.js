// To English: "\chapter{([\w\s]+)}" into "# $1".
/// To Latex: "# ([\w\s]+)$" into "\chapter{$1}".

// To English: "\\section{([\w\s]+)}" into "## $1".
/// To Latex: "## ([\w\s]+)$" into "\section{$1}".

// To English: "\\subsection\{([\w\s\-,]+)\}" into "### $1".
/// To Latex: "### ([\w\s\-,]+)$" into "\subsection{$1}".

// To English: "\item" into "-".
/// To Latex: "\t- (.+)$" into "\t\item $1". Wrap all within "\begin{itemize}" "\end".

// To English: "\\cite\{([\w\s\-,]+)\}" into "[$1]".
/// To Latex: "\[([\w\s\-,]+)\]" into "\cite{$1}".

// To English: "\\%" into "%."
/// To Latex: "%" into "\%".

// To English: "\\textit\{([\w\s\-,*]+)\}" into "$1".
/// Nothing to do.

// To English: "\\gls\{([\w\s\-,]+)\}" into "<$1>".
/// To Latex: "\<([\w\s\-,]+)\>" into "\gls{$1}".

// To English: "\\acrshort\{([\w\s\-,]+)\}" into "$1".
/// To Latex: "(NLoS)" into "\acrshort{$1}".
/// To Latex: "(ITS)" into "\acrshort{$1}".
/// To Latex: "(DSRC)" into "\acrshort{$1}".
/// To Latex: "(LoS)" into "\acrshort{$1}".
/// To Latex: "(ER)" into "\acrshort{$1}".
/// To Latex: "(V2I)" into "\acrshort{$1}".
/// To Latex: "(RSU)" into "\acrshort{$1}".
/// To Latex: "(VANET)" into "\acrshort{$1}".
/// To Latex: "(GUI)" into "\acrshort{$1}".

// To English: "\\acrlong\{ITS\}" into "Intelligent Transport System".
/// To Latex: "Intelligent Transport System" into "\acrlong{ITS}".

// To English: "\\acrlong\{LoS\}" into "Line-of-Sight".
/// To Latex: "Line-of-Sight" into "\acrlong{LoS}".

// To English: "\\acrlong\{DSRC\}" into "Dedicated Short-Range Communication".
/// To Latex: "(Dedicated Short-Range Communication)" into "\acrlong{DSRC}".

// To English: "\\acrlong\{NLoS\}" to "Non-Line-of-Sight".
// To Latex: "Non-Line-of-Sight" to "\acrlong{NLoS}".
