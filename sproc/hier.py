# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/30_hierarchical.ipynb.

# %% auto 0
__all__ = ['flat_series_to_multiindexed_series', 'flat_df_to_multiindexed_df', 'pad_col_levels', 'columns_containing',
           'flatten_columns_names']

# %% ../nbs/30_hierarchical.ipynb 2
import pathlib
import itertools

import pandas as pd
import numpy as np
from lxml import etree
import yaml

import sproc.xml
import sproc.structure

# %% ../nbs/30_hierarchical.ipynb 24
def flat_series_to_multiindexed_series(s: pd.Series) -> pd.Series:
    
    index_paths = []
    values = []
    
    for i, v in s.iteritems():
        index_paths.append(tuple(i.split(sproc.structure.nested_tags_separator)))
        values.append(v)
        
    return pd.Series(values, index=pd.MultiIndex.from_tuples(index_paths))

# %% ../nbs/30_hierarchical.ipynb 34
def flat_df_to_multiindexed_df(input_df: pd.DataFrame) -> pd.DataFrame:
    """
    Reads and parses an XML file into a `pd.DataFrame`.
    
    **Parameters**
    
    - input_df: `pd.DataFrame`
    
        Input dataframe.
        
    **Returns**
    
    - out: pd.DataFrame
    
        A column-hierarchical version of the input dataframe.
    
    """
    
    # every field becomes a `tuple`
    fields = [tuple(c.split(sproc.structure.nested_tags_separator)) for c in input_df.columns]
    
    # the number of levels in the multindex for the columns
    n_levels = len(max(fields, key=len))
    
    # every tuple is padded with empty string until it has `n_levels`
    fields = [e + ('',)*(n_levels-len(e)) for e in fields]

    index_hierarchical = pd.MultiIndex.from_tuples(fields)

    # an empty `pd.DataFrame`
    res = pd.DataFrame(None, columns=index_hierarchical)

    # every column in the *output* `pd.DataFrame`...
    for c in res.columns:

        # ...is filled in looking up the data in the input `pd.DataFrame` by means of the appropriate "merged" column name
        res[c] = input_df[sproc.structure.assemble_name(c)]
    
    return res

# %% ../nbs/30_hierarchical.ipynb 47
def pad_col_levels(df: pd.DataFrame, levels: tuple | list, denan: bool = False) -> tuple:
    
    # if "de-NaN" was requested...
    if denan:
        levels = [e for e in levels if pd.notna(e)]
    
    # if any([np.nan in c for c in df.columns]):
    #     nan_marker = np.nan
    # elif any(['nan' in c for c in df.columns]):
    #     nan_marker = 'nan'
    # else:
    #     raise Exception('marker of empty levels could not be guessed')
    
    return tuple(list(levels) + [''] * (df.columns.nlevels - len(levels)))
    # return tuple(list(levels) + [np.nan] * (df.columns.nlevels - len(levels)))
    # return tuple(list(levels) + ['nan'] * (df.columns.nlevels - len(levels)))
    # return tuple(list(levels) + [nan_marker] * (df.columns.nlevels - len(levels)))

# %% ../nbs/30_hierarchical.ipynb 55
def columns_containing(df: pd.DataFrame, substring: str):
    
    is_contained = [list(filter(lambda e: (type(e) != float) and (substring in e), c)) != [] for c in df.columns]
    
    return df.columns[is_contained]

# %% ../nbs/30_hierarchical.ipynb 74
def _data_scheme_ok(data_scheme: dict) -> bool:
    
    lengths = []
    
    for l in data_scheme.values():
        
        lengths.append(len(l))
        
        if not np.all([(type(e) == str) or np.isnan(e) for e in data_scheme['id']]):
            
            return False
        
    return np.unique(lengths).shape[0] == 1

# %% ../nbs/30_hierarchical.ipynb 83
def flatten_columns_names(df: pd.DataFrame, data_scheme: dict, inplace: bool = False) -> None | pd.DataFrame:
    
    assert _data_scheme_ok(data_scheme), f'data scheme is not OK'
    
    # the inverse of the above mapping (turning nan's into empty strings, and concatenating all the levels together)
    inv_data_scheme = {''.join([e if pd.notna(e) else '' for e in v]): k for k, v in data_scheme.items()}
    
    new_names = []
    # unmapped_names = []
    
    for c in df.columns:
        
        # print(c)
        
        stitched_c = ''.join(c)
        
        # if the columns is found in the inverse mapping...
        if stitched_c in inv_data_scheme:
            
            # ...the given name is used
            new_names.append(inv_data_scheme[stitched_c])
            
        # if the columns is NOT found in the inverse mapping...
        else:
            
            # ...the new name is obtained by contatenating the individual components
            new_names.append(sproc.structure.nested_tags_separator.join([e for e in c if e != '']))

            # # it is also recorded in its own list
            # unmapped_names.append(new_names[-1])
    
    if inplace:
        
       res = df
    
    else:
        
        res = df.copy()
    
    res.columns = new_names
    
    # print(f'Unmapped columns:\n{unmapped_names}')
    
    return res
