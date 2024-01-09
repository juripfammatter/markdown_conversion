import re

file_name = "markdown conversion test"


# Specify the file path
file_path = "src/md/" + file_name + ".md"

""" Open the file in read mode ('r') """
with open(file_path, 'r', encoding="utf-8") as file:
    # Read the entire contents of the file into a string
    markdown_file = file.read()



""" Replacements """
section_pattern = r'#\s*(.*)'
subsection_pattern = r'##\s*(.*)'
subsubsection_pattern = r'###\s*(.*)'

# indent_pattern = r'\>\s*(.*)'
eq_pattern = r'\$\$(.*?)\$\$'

bf_pattern = r'\*\*(.*?)\*\*'
it_pattern = r'\*(.*?)\*'

itemize_pattern = r'^\s*\*\s*(.*)$'
enumerate_pattern = r'^\d+\.\s*(.*)$'
enumerate_indent_pattern = r'^\t\d+\.\s*(.*)$'
enumerate_indent2_pattern = r'^\t\t\d+\.\s*(.*)$'

codeblock_pattern = r'```(.*?)```'
codeline_pattern = r'\`(.*?)\`'

image_pattern = r'!\[\[(.*?)\s*\|\s*(.*?)\]\]'

itemize_cleanup_pattern = r'\\begin{itemize}\[leftmargin=8pt, label = ·\]\n\s*(.*?)\\end{itemize}\n\n\\begin{itemize}\[leftmargin=8pt, label = ·\]\n'
enumerate_cleanup_pattern = r'\\begin{enumerate}\[leftmargin=12pt, label = ·\]\n\s*(.*?)\\end{enumerate}\n\n\\begin{enumerate}\[leftmargin=12pt, label = ·\]\n'
enumerate_indent_cleanup_pattern = r'\\begin{enumerate}\[leftmargin=24pt, label = ·\]\n\s*(.*?)\\end{enumerate}\n\n\\begin{enumerate}\[leftmargin=24pt, label = ·\]\n'
enumerate_indent2_cleanup_pattern = r'\\begin{enumerate}\[leftmargin=36pt, label = ·\]\n\s*(.*?)\\end{enumerate}\n\n\\begin{enumerate}\[leftmargin=36pt, label = ·\]\n'

# Define a function to perform the replacement

def section_replace_match(match):
    text = match.group(1)
    return f'\n\\subsection{{{text}}}'

def subsection_replace_match(match):
    text = match.group(1)
    return f'\n\\subsubsection{{{text}}}'

def subsubsection_replace_match(match):
    text = match.group(1)
    return f'\n\\paragraph{{{text}}}'

# def indent_replace_match(match):
#     text = match.group(1)
#     return r'>' + text

def eq_replace_match(match):
    text = match.group(1)
    return f'\n\\begin{{equation*}}{text}\\end{{equation*}}'

def bf_replace_match(match):
    text = match.group(1)
    return r'\textbf{' + text + '}'

def it_replace_match(match):
    text = match.group(1)
    return r'\textit{' + text + '}'

def itemize_replace_match(match):
    text = match.group(1)
    return f'\n\\begin{{itemize}}[leftmargin=8pt, label = ·]\n \\item[·] {text}\n\\end{{itemize}}'

def enumerate_replace_match(match):
    text = match.group(1)
    return f'\n\\begin{{enumerate}}[leftmargin=12pt, label = ·]\n \\item {text}\n\\end{{enumerate}}'

def enumerate_indent_replace_match(match):
    text = match.group(1)
    return f'\n\\begin{{enumerate}}[leftmargin=24pt, label = ·]\n \\item {text}\n\\end{{enumerate}}'

def enumerate_indent2_replace_match(match):
    text = match.group(1)
    return f'\n\\begin{{enumerate}}[leftmargin=36pt, label = ·]\n \\item {text}\n\\end{{enumerate}}'

def codeblock_replace_match(match):
    text = match.group(1)
    return f'\n\lstset{{style=bright}}\\begin{{lstlisting}}[basicstyle=\\footnotesize, language=C++]\n' + text + f'\\end{{lstlisting}}'

def codeline_replace_match(match):
    text = match.group(1)
    return r'\texttt{' + text + '}'

def image_replace_match(match):
    file_name = (match.group(1)).replace('\\', '' )
    size = match.group(2)
    # differentiate between sizes
    if(size == "small"): 
        return f'\n\\begin{{center}}\n \includegraphics[width=0.7\linewidth]{{{file_name}}}\n\\end{{center}}'
    if(size == "medium"): 
        return f'\n\\begin{{center}}\n \includegraphics[width=0.9\linewidth]{{{file_name}}}\n\\end{{center}}'
    if(size == "large"): 
        return f'\n\\begin{{center}}\n \includegraphics[width=\linewidth]{{{file_name}}}\n\\end{{center}}'

def itemize_cleanup_replace_match(match):
    text = match.group(1)
    return f'\\begin{{itemize}}[leftmargin=8pt, label = ·]\n {text}'

def enumerate_cleanup_replace_match(match):
    text = match.group(1)
    return f'\\begin{{enumerate}}[leftmargin=12pt, label = ·]\n {text}'

def enumerate_indent_cleanup_replace_match(match):
    text = match.group(1)
    return f'\\begin{{enumerate}}[leftmargin=24pt, label = ·]\n {text}'

def enumerate_indent2_cleanup_replace_match(match):
    text = match.group(1)
    return f'\\begin{{enumerate}}[leftmargin=36pt, label = ·]\n {text}'


# brute force replacements
tex_file = markdown_file.replace("<br>", "\\newline")
tex_file = re.sub(r'\| -+\s*', '', tex_file)
tex_file = tex_file.replace("---", "\\par\\noindent\\textcolor{gray}{\\rule{\\linewidth}{0.4pt}}")
tex_file = tex_file.replace("$$\n\\begin{align}", "\\begin{align*}")
tex_file = tex_file.replace("\\end{align}\n$$", "\\end{align*}")
tex_file = tex_file.replace("u\u0308", "ü")
tex_file = tex_file.replace("a\u0308", "ä")
tex_file = tex_file.replace("o\u0308", "ö")
tex_file = tex_file.replace("<->", "$\leftrightarrow$")
tex_file = tex_file.replace("->", "$\rightarrow$")

# Use re.sub() to replace the pattern
tex_file = re.sub(subsubsection_pattern, subsubsection_replace_match, tex_file)
tex_file = re.sub(subsection_pattern, subsection_replace_match, tex_file)
tex_file = re.sub(section_pattern, section_replace_match, tex_file)

# tex_file = re.sub(indent_pattern, indent_replace_match, tex_file)

tex_file = re.sub(eq_pattern, eq_replace_match, tex_file, flags=re.DOTALL)

tex_file = re.sub(bf_pattern, bf_replace_match, tex_file)
tex_file = re.sub(it_pattern, it_replace_match, tex_file)

tex_file = re.sub(itemize_pattern, itemize_replace_match, tex_file, flags=re.MULTILINE)
tex_file = re.sub(enumerate_pattern, enumerate_replace_match, tex_file, flags=re.MULTILINE)
tex_file = re.sub(enumerate_indent_pattern, enumerate_indent_replace_match, tex_file, flags=re.MULTILINE)
tex_file = re.sub(enumerate_indent2_pattern, enumerate_indent2_replace_match, tex_file, flags=re.MULTILINE)

tex_file = re.sub(codeblock_pattern, codeblock_replace_match, tex_file, flags=re.DOTALL)
tex_file = re.sub(codeline_pattern, codeline_replace_match, tex_file)

tex_file = re.sub(image_pattern, image_replace_match, tex_file)

# post processing
tex_file = re.sub(itemize_cleanup_pattern, itemize_cleanup_replace_match, tex_file, flags=re.DOTALL)
tex_file = re.sub(enumerate_cleanup_pattern, enumerate_cleanup_replace_match, tex_file, flags=re.DOTALL)
tex_file = re.sub(enumerate_indent_cleanup_pattern, enumerate_indent_cleanup_replace_match, tex_file, flags=re.DOTALL)
tex_file = re.sub(enumerate_indent2_pattern, enumerate_indent2_cleanup_replace_match, tex_file, flags=re.DOTALL)

# add section name
tex_file = "\section{" + file_name + "}\n" +tex_file
""" write file """
output_file_path = "src/sections/" + file_name + ".tex"

with open(output_file_path, 'w') as output_file:
    output_file.write(tex_file)