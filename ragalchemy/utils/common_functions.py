from prettytable import PrettyTable
from pptx.oxml.xmlchemy import OxmlElement
from numpy import dot
from numpy.linalg import norm


def cosine_similarity(a,b):
    cos_sim = dot(a, b)/(norm(a)*norm(b))
    return cos_sim

def format_dataframe_to_prettytables(df):
    """
    Converts a pandas DataFrame to a prettytable.

    Args:
        df (pandas.DataFrame): The DataFrame to convert.

    Returns:
        str: The prettytable as a string.
    """
    table = PrettyTable([''] + list(df.columns))
    for row in df.itertuples():
        table.add_row(row)
    return str(table)

def convert_pptx_table_to_prettytable(table):
    """
    Converts a PowerPoint table to a prettytable.

    Args:
        table (pptx.table.Table): The PowerPoint table to convert.

    Returns:
        str: The prettytable as a string.
    """
    ptable = PrettyTable()
    for i, row in enumerate(table.rows):
        cell_list = [cell.text for cell in row.cells]
        ptable.add_row(cell_list)
    return str(ptable)

def SubElement(parent, tagname, **kwargs):
    """
    Creates a new XML element and appends it to the parent element.

    Args:
        parent (OxmlElement): The parent element.
        tagname (str): The tag name of the new element.
        **kwargs: Additional attributes for the new element.

    Returns:
        OxmlElement: The new element.
    """
    element = OxmlElement(tagname)
    element.attrib.update(kwargs)
    parent.append(element)
    return element



