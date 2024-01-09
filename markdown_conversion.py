import re

file_name = "markdown conversion test"

""" Open file  """
file_path = "src/md/" + file_name + ".md"
with open(file_path, 'r', encoding="utf-8") as file:
    # Read the entire contents of the file into a string
    markdown_file = file.read()


""" Replacement pattern """
section_pattern =                           r'#\s*(.*)'
subsection_pattern =                        r'##\s*(.*)'
subsubsection_pattern =                     r'###\s*(.*)'

eq_pattern =                                r'\$\$(.*?)\$\$'

bf_pattern =                                r'\*\*(.*?)\*\*'
it_pattern =                                r'\*(.*?)\*'

itemize_pattern =                           r'^\s*\*\s*(.*)$'
enumerate_pattern =                         r'^\d+\.\s*(.*)$'
enumerate_indent_pattern =                  r'^\t\d+\.\s*(.*)$'
enumerate_indent2_pattern =                 r'^\t\t\d+\.\s*(.*)$'

codeblock_pattern =                         r'```(.*?)```'
codeline_pattern =                          r'\`(.*?)\`'

image_pattern =                             r'!\[\[(.*?)\s*\|\s*(.*?)\]\]'

itemize_cleanup_pattern =                   r'\\begin{itemize}\[leftmargin=8pt, label = ·\]\n\s*(.*?)\\end{itemize}\n\n\\begin{itemize}\[leftmargin=8pt, label = ·\]\n'
enumerate_cleanup_pattern =                 r'\\begin{enumerate}\[leftmargin=12pt\]\n\s*(.*?)\\end{enumerate}\n\n\\begin{enumerate}\[leftmargin=12pt\]\n'
enumerate_indent_cleanup_pattern =          r'\\begin{enumerate}\[leftmargin=24pt\]\n\s*(.*?)\\end{enumerate}\n\n\\begin{enumerate}\[leftmargin=24pt\]\n'
enumerate_indent2_cleanup_pattern =         r'\\begin{enumerate}\[leftmargin=36pt\]\n\s*(.*?)\\end{enumerate}\n\n\\begin{enumerate}\[leftmargin=36pt\]\n'


""" Replace match """
# Sections
section_replace_match =                     lambda match: f'\n\\subsection{{{match.group(1)}}}'
subsection_replace_match =                  lambda match: f'\n\\subsubsection{{{match.group(1)}}}'
subsubsection_replace_match =               lambda match: f'\n\\paragraph{{{match.group(1)}}}'

# Typefacing 
bf_replace_match =                          lambda match: r'\textbf{' + match.group(1) + '}'
it_replace_match =                          lambda match: r'\textit{' + match.group(1) + '}'

# Environments
eq_replace_match =                          lambda match: f'\n\\begin{{equation*}}{match.group(1)}\\end{{equation*}}'
itemize_replace_match =                     lambda match: f'\n\\begin{{itemize}}[leftmargin=8pt, label = ·]\n\t\\item {match.group(1)}\n\\end{{itemize}}'
enumerate_replace_match =                   lambda match: f'\n\\begin{{enumerate}}[leftmargin=12pt]\n\t\\item {match.group(1)}\n\\end{{enumerate}}'
enumerate_indent_replace_match =            lambda match: f'\n\\begin{{enumerate}}[leftmargin=24pt]\n\t\\item {match.group(1)}\n\\end{{enumerate}}'
enumerate_indent2_replace_match =           lambda match: f'\n\\begin{{enumerate}}[leftmargin=36pt]\n\t\\item {match.group(1)}\n\\end{{enumerate}}'
codeblock_replace_match =                   lambda match: f'\n\lstset{{style=bright}}\\begin{{lstlisting}}[basicstyle=\\footnotesize, language=C++]\n' + match.group(1) + f'\\end{{lstlisting}}'
codeline_replace_match =                    lambda match: r'\texttt{' + match.group(1) + '}'

# cleanup 
itemize_cleanup_replace_match =             lambda match: f'\\begin{{itemize}}[leftmargin=8pt, label = ·]\n\t{match.group(1)}'
enumerate_cleanup_replace_match =           lambda match: f'\\begin{{enumerate}}[leftmargin=12pt]\n\t{match.group(1)}'
enumerate_indent_cleanup_replace_match =    lambda match: f'\\begin{{enumerate}}[leftmargin=24pt]\n\t{match.group(1)}'
enumerate_indent2_cleanup_replace_match =   lambda match: f'\\begin{{enumerate}}[leftmargin=36pt]\n\t{match.group(1)}'


# Images
def image_replace_match(match):
    file_name = (match.group(1)).replace('\\', '' )
    size = match.group(2)
    # differentiate between sizes
    if(size == "small"): 
        return f'\n\\begin{{center}}\n\t\includegraphics[width=0.7\linewidth]{{{file_name}}}\n\\end{{center}}'
    if(size == "medium"): 
        return f'\n\\begin{{center}}\n\t\includegraphics[width=0.9\linewidth]{{{file_name}}}\n\\end{{center}}'
    if(size == "large"): 
        return f'\n\\begin{{center}}\n\t\includegraphics[width=\linewidth]{{{file_name}}}\n\\end{{center}}'


""" brute force replacements """
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


""" Replace with regex (order matters!) """
tex_file = re.sub(subsubsection_pattern, subsubsection_replace_match, tex_file)
tex_file = re.sub(subsection_pattern, subsection_replace_match, tex_file)
tex_file = re.sub(section_pattern, section_replace_match, tex_file)

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

""" Post processing """
tex_file = re.sub(itemize_cleanup_pattern, itemize_cleanup_replace_match, tex_file, flags=re.DOTALL)
for i in range(10):
    tex_file = re.sub(enumerate_cleanup_pattern, enumerate_cleanup_replace_match, tex_file, flags=re.DOTALL)
    tex_file = re.sub(enumerate_indent_cleanup_pattern, enumerate_indent_cleanup_replace_match, tex_file, flags=re.DOTALL)
    tex_file = re.sub(enumerate_indent2_pattern, enumerate_indent2_cleanup_replace_match, tex_file, flags=re.DOTALL)

# add section name
tex_file = "\section{" + file_name + "}\n" +tex_file

""" Write file """
output_file_path = "src/sections/" + file_name + ".tex"
with open(output_file_path, 'w') as output_file:
    output_file.write(tex_file)