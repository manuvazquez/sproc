# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/10_xml.ipynb.

# %% auto 0
__all__ = ['re_tag', 'get_namespaces', 'split_namespace_tag', 'get_entries', 'get_deleted_entries', 'deleted_to_series',
           'set_or_append', 'entry_to_dict', 'entry_to_series', 'to_df', 'to_curated_df', 'columns_depth']

# %% ../nbs/10_xml.ipynb 2
import pathlib
import re
import datetime
from collections.abc import Iterable

import numpy as np
import pandas as pd
from lxml import etree

import sproc.structure
import sproc.postprocess

# %% ../nbs/10_xml.ipynb 13
def get_namespaces(input_file: str | pathlib.Path, root_name: str = 'base') -> dict:
    
    tree = etree.parse(input_file)
    
    namespaces = tree.getroot().nsmap
    
    if None in namespaces:
        
        namespaces[root_name] = namespaces.pop(None)
        
    return namespaces

# %% ../nbs/10_xml.ipynb 16
re_tag = re.compile('\{(.*)\}(.*)')

# %% ../nbs/10_xml.ipynb 20
def split_namespace_tag(namespace_tag: str) -> str:
    
    return re_tag.match(namespace_tag).groups()

# %% ../nbs/10_xml.ipynb 26
def get_entries(root: etree.Element) -> list[etree.Element]:
    
    return [e for e in root if split_namespace_tag(e.tag)[1] == 'entry']

# %% ../nbs/10_xml.ipynb 37
def get_deleted_entries(root: etree.Element) -> list[etree.Element]:
    
    return [e for e in root if split_namespace_tag(e.tag)[1] == 'deleted-entry']

# %% ../nbs/10_xml.ipynb 43
def deleted_to_series(input_file: str | pathlib.Path) -> pd.Series:
    """
    Reads and parses "deleted" entries in an XML file.
    
    **Parameters**
    
    - input_file: str or Path
    
        Input file.
    
    **Returns**
    
    - out: pd.Series
    
        A Pandas Series with XML data.
    
    """
    
    tree = etree.parse(input_file)
    root = tree.getroot()
    
    ids = []
    dates = []

    for e in get_deleted_entries(root):
        ids.append(e.attrib['ref'])
        # dates.append(pd.to_datetime(e.attrib['when']))
        dates.append(pd.to_datetime(e.attrib['when'], utc=True))
        
    name = 'deleted_on'
        
    if not ids:
        
        return pd.Series([], dtype='datetime64[ns]', name=name)
    
    else:

        return pd.Series(data=dates, index=ids, name=name)

# %% ../nbs/10_xml.ipynb 51
def set_or_append(d: dict, key: str, value: str | dict) -> str | dict:
    if key in d:
        if type(d[key]) == list:
            d[key].append(value)
        else:
            d[key] = [d[key], value]
    else:
        d[key] = value

# %% ../nbs/10_xml.ipynb 61
def entry_to_dict(entry: etree.Element, recursive: bool = True) -> dict:

    res = {}
    
    # for every "child" of `entry` ...
    for e in entry:
        
        # ...the *namespace* and *tag* are extracted
        namespace, tag = split_namespace_tag(e.tag)
        
        # for the sake of readability
        value = e.text
            
        # if `value` is "something" and not an empty string after striping it of blank characteres...
        if value and (value.strip() != ''):
            
            # if the text contains a number...
            if value.isnumeric():
                
                # ...it is turned into a `float`
                value = float(value)
                
                # if the latter is actually an integer...
                if value.is_integer():
                    
                    # ...conversion is performed
                    value = int(value)
            
            # assert tag not in res, f'multiple values for {tag}'
            
            # the value of this element (whether the original text or the obtained number) is stored
            # res[tag] = value
            set_or_append(res, tag, value)
        
        # if in "recursive mode" and this element has children (`len(e)` is different from 0)...
        if recursive and len(e):
            
            # recursion
            sub_res = entry_to_dict(e)
            
            for k, v in sub_res.items():
                
                # the name of the new "key" is assembled from those of the parent and the child
                key_name = f'{tag}{sproc.structure.nested_tags_separator}{k}'
                
                # assert key_name not in res, f'multiple values for {key_name}'                
                # key_name = unique_name(key_name, res.keys()) # <-------------  a unique name
                
                # res[key_name] = v
                set_or_append(res, key_name, v)
    
    return res

# %% ../nbs/10_xml.ipynb 68
def entry_to_series(entry: etree.Element) -> pd.Series:

    return pd.Series(entry_to_dict(entry))

# %% ../nbs/10_xml.ipynb 77
def to_df(input_file: str | pathlib.Path) -> pd.DataFrame:
    """
    Reads and parses an XML file into a `pd.DataFrame`.
    
    **Parameters**
    
    - input_file: str or Path
    
        Input file.
    
    **Returns**
    
    - out: pd.DataFrame
    
        A Pandas DataFrame with XML data.
    
    """
    
    tree = etree.parse(input_file)
    root = tree.getroot()
    entries = get_entries(root)
    
    return pd.concat([entry_to_series(e) for e in entries], axis=1).T

# %% ../nbs/10_xml.ipynb 80
def to_curated_df(input_file: str | pathlib.Path) -> pd.DataFrame:
    """
    Reads, parses and tidies up an XML file into a `pd.DataFrame`.
    
    **Parameters**
    
    - input_file: str or Path
    
        Input file.
    
    **Returns**
    
    - out: pd.DataFrame
    
        A Pandas DataFrame with XML data.
    
    """
    
    return sproc.postprocess.typecast_columns(to_df(input_file))

# %% ../nbs/10_xml.ipynb 86
def columns_depth(df: pd.DataFrame) -> pd.Series:

    n_nestings = df.columns.str.extractall(f'(\\S{sproc.structure.nested_tags_separator}\\S)')
    n_nestings.index.names = ['column', 'match']
    
    return n_nestings[0].groupby('column').size()
