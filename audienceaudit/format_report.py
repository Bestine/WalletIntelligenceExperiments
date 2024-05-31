from datetime import datetime  

"""
def format_markdown_report(output):
    # Format the output as markdown
    # ...

def format_txt_report(output):
    # Format the output as plain text
    # ...

def format_csv_report(output):
    # Format the output as CSV
    # ...
"""

def get_css():
    # CSS styling as a multi-line string for easy editing
    return """
    body {
        font-family: 'Arial', sans-serif;
        color: white;
        background-color: #000e55; /* Dark blue background */
    }
    h1 {
        font-size: 30px;
        color: white; /* White for main report heading */
    }
    h2 {
        font-size: 24px;
        color: #81FF9C; /* green for section headings */
    }   
    h3 {
        font-size: 18px;
        color: #9E7EFF; /* pink for subheadings */
        }
    table {
        font-family:monospace;
        /*width: 50%;*/
        border-collapse: collapse;
        margin: 20px 0;
    }
    th, td {
        border: 1px solid #45A29E; /* Lighter cyan border for table */
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #000e55; /* Dark blue header background */
    }
    p {
        font-size: 14px;
    }
    """

# HTML REPORT
def format_html_report(output):
    formatted_output = ""
    sections = output.split("\n===========================================================================")

    for section in sections:
        lines = section.strip().split("\n")
        if not lines:
            continue

        in_table = False  # Flag to track if we are inside a table block
        attribute_table_open = False  # Track if a table for attribute lines is open

        for line in lines:
            if line.startswith("> "):
                # Main title (H2)
                title = line.strip("> ").strip()
                if in_table:
                    # Close previous table if open
                    formatted_output += "</table>\n"
                    in_table = False
                formatted_output += f"<h2>{title}</h2>\n"
            elif line.startswith("---"):
                # Subsection title (H3)
                title = line.strip("-").strip()
                if in_table:
                    # Close previous table if open
                    formatted_output += "</table>\n"
                    in_table = False
                formatted_output += f"<h3>{title}</h3>\n"
            elif "|" in line:
                # Start or continue a data table
                if not in_table:
                    formatted_output += "<table>\n"
                    in_table = True
                cells = line.split("|")
                formatted_output += "<tr>" + "".join(f"<td>{cell.strip()}</td>" for cell in cells) + "</tr>\n"
            elif ": " in line:
                # Convert attribute lines into table rows
                if not attribute_table_open:
                    formatted_output += "<table>\n"
                    attribute_table_open = True
                attribute, value = line.split(": ", 1)
                formatted_output += f"<tr><td>{attribute.strip()}</td><td>{value.strip()}</td></tr>\n"
            else:
                # Normal text lines, handle outside of tables
                if in_table or attribute_table_open:
                    formatted_output += "</table>\n"
                    in_table = False
                    attribute_table_open = False
                formatted_output += f"<p>{line.strip()}</p>\n"

        # Close any open table
        if in_table or attribute_table_open:
            formatted_output += "</table>\n"
            in_table = False
            attribute_table_open = False

    return formatted_output

# TXT REPORT
def format_txt_report(output):
    return output

def format_markdown_report(output):
    formatted_output = ""
    lines = output.strip().split("\n")

    in_table = False  # Flag to track if we are inside a table block
    table_header = ""  # Variable to store the table header
    table_separator = ""  # Variable to store the table separator
    attribute_table_open = False  # Track if a table for attribute lines is open

    for line in lines:
        if line.startswith("> "):
            # Main title (H2)
            title = line.strip("> ").strip()
            if in_table:
                # Close previous table if open
                formatted_output += "\n"
                in_table = False
            formatted_output += f"## {title}\n\n"
        elif line.startswith("---"):
            # Subsection title (H3)
            title = line.strip("-").strip()
            if in_table:
                # Close previous table if open
                formatted_output += "\n"
                in_table = False
            formatted_output += f"### {title}\n\n"
        elif "|" in line:
            # Start or continue a data table
            if not in_table:
                table_header = f"|{line.strip()}|"
                table_separator = "|" + "|".join(["---"] * (line.count("|") + 1)) + "|"
                formatted_output += f"{table_header}\n{table_separator}\n"
                in_table = True
            else:
                formatted_output += f"|{line.strip()}|\n"
        elif ": " in line:
            # Convert attribute lines into table rows
            if not attribute_table_open:
                attribute_table_open = True
                formatted_output += "| Attribute | Value |\n|-----------|-------|\n"
            attribute, value = line.split(": ", 1)
            formatted_output += f"| {attribute.strip()} | {value.strip()} |\n"
        elif line.strip() == "" or all(c == "=" for c in line.strip()):
            # Ignore empty lines and lines with only equal signs
            continue
        else:
            # Normal text lines, handle outside of tables
            if in_table:
                # Close previous table if open
                formatted_output += "\n"
                in_table = False
            elif attribute_table_open:
                attribute_table_open = False
                formatted_output += "\n"
            formatted_output += f"{line.strip()}\n\n"

    # Close any open table or attribute table
    if in_table or attribute_table_open:
        formatted_output += "\n"

    return formatted_output.strip()

def generate_report(csv_file, output, output_format):
    if output_format == "html":
        file_extension = "html"
        formatted_output = format_html_report(output)
        css_style = get_css()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        html = f"<html><head><title>Thirdwave Wallet Intelligence Audit Report</title><style>{css_style}</style></head><body><h1>Thirdwave Wallet Intelligence Audit Report</h1>{formatted_output}<p>Report generated at {current_time}</p></body></html>"
        formatted_output = html

    elif output_format == "md":
        file_extension = "md"
        formatted_output = format_markdown_report(output)
    elif output_format == "txt":
        file_extension = "txt"
        formatted_output = format_txt_report(output)
        
    elif output_format == "csv":
        file_extension = "csv"
        formatted_output = format_csv_report(output)

    else:
        raise ValueError("Invalid output format specified.")

    # Generate the output file name
    output_file = f"Audit-{csv_file.split('/')[-1][:-4]}.{file_extension}"

    # Write the formatted output to the file
    with open(output_file, "w") as file:
        file.write(formatted_output)

    print(f"\nReport generated: {output_file}")

