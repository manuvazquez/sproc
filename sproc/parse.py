# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/50_parse.ipynb.

# %% auto 0
__all__ = ['domain_discriminative_columns_paths', 'domain', 'year_and_maybe_month']

# %% ../nbs/50_parse.ipynb 2
import pathlib
import urllib.parse
import datetime

import pandas as pd

import sproc.xml
import sproc.hier

# %% ../nbs/50_parse.ipynb 11
domain_discriminative_columns_paths = [
    ['ContractFolderStatus', 'LocatedContractingParty', 'BuyerProfileURIID'],
    ['ContractFolderStatus', 'LegalDocumentReference', 'Attachment', 'ExternalReference', 'URI']
]

# %% ../nbs/50_parse.ipynb 25
def domain(df: pd.DataFrame) -> pd.Series:
    
    # columns names from "path"s
    columns = [sproc.hier.pad_col_levels(df, p) for p in domain_discriminative_columns_paths]
    
    domains = df[columns].applymap(lambda x: urllib.parse.urlparse(x).netloc if pd.notna(x) else pd.NA)
    
    # the result is initialized with the first column of domains...
    res = domains[columns[0]]
    
    # ...and  the remaining...
    for c in columns[1:]:

        # ...are used to update it
        res = res.combine_first(domains[c])
    
    return res

# %% ../nbs/50_parse.ipynb 30
def year_and_maybe_month(
    s: str # Raw date
    ) -> datetime.datetime: # Parsed date

    try:

        # year and month
        d = datetime.datetime.strptime(s, '%Y%d')
    
    except ValueError:

        # only year
        d = datetime.datetime.strptime(s, '%Y').replace(month=12)

    return d

