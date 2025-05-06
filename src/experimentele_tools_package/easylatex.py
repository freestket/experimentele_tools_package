"""_
A package containing useful tools to make the transition from data/software to LaTeX easier

TODO:
    Check/finish documentation
    Add table customization options
"""


def generate_latex_table(data, table_header, caption_text, label_text) -> str:
    """
    This function generates a LaTeX table as a string when provided with a data list of columns a header, caption and label.
    The string can then be copied and pasted into a LaTeX editor.

    Args:
        data (list[list]): A list contain all data. Each element of data is a column of the generated table.
        table_header (list[str]): A list contain the header of each column.
        caption_text (str): The caption that will be used underneath the table.
        label_text (str): The text that will be used to reference the table. The program will add "tab:" in front of this.
    
    Returns:
        str: A string that contains the generated LaTeX table. It can be copied and pasted into a LaTeX editor.
    """
    #Generate caption and label strings:
    caption = "{" + caption_text + "}"
    label_string = "{tab:" + label_text + "}"

    #Generate columns command:
    columns_cmd = "{"
    for i in range(len(data)):
        columns_cmd += "|c"
    columns_cmd += "|}"
    tabular_cmd = "{tabular}"

    #Generate table beginning:
    latex_table = ""
    latex_table += "\\begin{table}[h!]\n"
    latex_table += "\t\\centering\n"
    latex_table += f"\t\\caption{caption}\n"
    latex_table += f"\t\\begin{tabular_cmd}{columns_cmd}\n"
    latex_table += "\t\t\\hline\n"

    #Generate headerline:
    headerline = "\t\t"
    for i in range(len(table_header)):
        headerline += table_header[i]
        if i < len(table_header) - 1:
            headerline += " & "
        else:
            headerline += " \\\\\n"
    headerline += "\t\t\\hline\\hline\n"

    latex_table += headerline

    #Generate lines of data values:
    for i in range(len(data[0])):
        new_line = "\t\t"
        for col in data:
            new_line += str(col[i])
            if data.index(col) < data.index(data[len(data)-1]):
                new_line += " & "
            else:
                new_line += " \\\\\n"
                new_line += "\t\t\\hline\n"
        latex_table += new_line

    latex_table += "\t\\end{tabular}\n"
    latex_table += f"\t\\label{label_string}\n"
    latex_table += "\\end{table}"

    return latex_table