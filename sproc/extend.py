# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/70_extend.ipynb.

# %% auto 0
__all__ = ['parquet_with_zip']

# %% ../nbs/70_extend.ipynb 2
import pathlib

import pandas as pd
import yaml

import dlsproc.structure
import dlsproc.bundle
import dlsproc.hier
import dlsproc.io
import dlsproc.assemble
import dlsproc.postprocess

# %% ../nbs/70_extend.ipynb 64
def parquet_with_zip(history_file: str | pathlib.Path, zip_file: str | pathlib.Path, output_file: str | pathlib.Path | None = None) -> None | pd.DataFrame:
    
    # in case `str`s were passed
    history_file = pathlib.Path(history_file)
    zip_file = pathlib.Path(zip_file)
    
    assert history_file.exists(), f"can't find {history_file}"
    assert zip_file.exists(), f"can't find {zip_file}"
    
    # historical data
    history_df = pd.read_parquet(history_file)
    
    # new data is parsed into a `pd.DataFrame`...
    new_df = dlsproc.bundle.read_zip(zip_file, concatenate=True)
    
    # ...whose columns are a *multiindex*
    new_df = dlsproc.hier.flat_df_to_multiindexed_df(new_df)
    
    # we also need the information about which entries are flagged as deleted
    deleted_series = dlsproc.bundle.read_deleted_zip(zip_file)
    
    # the time zone for the above deleted series and the column "deleted_on" in the historical data
    history_deleted_timezone = history_df["deleted_on"].dt.tz
    deleted_series_timezone = deleted_series.dt.tz
    
    # if there is any actual value in the "deleted on" column...
    if history_deleted_timezone:
    
        # assert deleted_series.dt.tz == history_deleted_timezone, f'{deleted_series.dt.tz=}, {history_deleted_timezone=}'
        
        if history_deleted_timezone != deleted_series_timezone:

            print(f'converting time zone in zip file {deleted_series_timezone} to {history_deleted_timezone} (that in the historical file)...')
            deleted_series = deleted_series.dt.tz_convert(history_deleted_timezone)
    
    # the two dataframes are stacked together
    concatenated_df = dlsproc.assemble.stack(history_df, new_df)
    
    # the same contract might show up more than once due to updates...but only the last one is kept
    concatenated_df = dlsproc.postprocess.keep_updates_only(concatenated_df)
    
    # duplicates are dropped from the deleted series
    deduplicated_deleted_series = dlsproc.postprocess.deduplicate_deleted_series(deleted_series)
    
    # for the sake of flagging deleted entries, the new (concatenated) dataframe and the *deleted series* are indexed the same
    reindexed_concatenated_df = concatenated_df.reset_index().set_index(['id'])
    deduplicated_reindexed_deleted_series = deduplicated_deleted_series.droplevel(level='file name')
    
    # the `deleted_on` column in the dataframe is filled in whenever appropriate
    reindexed_concatenated_df['deleted_on'] = reindexed_concatenated_df['deleted_on'].fillna(deduplicated_reindexed_deleted_series)
    
    # the orginal index is set back in place
    res = reindexed_concatenated_df.reset_index().set_index(['file name', 'entry'])
    
    if output_file:
        
        # so that we can exploit pathlib's API...
        output_file = pathlib.Path(output_file)
        
        # ...for checking stuff
        assert output_file.suffix == '.parquet', f'output file should end in ".parquet"'
    
        parquet_df = dlsproc.assemble.parquet_amenable(res)
        
        parquet_df.to_parquet(output_file)
        
    else:
    
        return res
