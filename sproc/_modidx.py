# Autogenerated by nbdev

d = { 'settings': { 'branch': 'main',
                'doc_baseurl': '/sproc',
                'doc_host': 'https://manuvazquez.github.io',
                'git_url': 'https://github.com/manuvazquez/sproc',
                'lib_path': 'sproc'},
  'syms': { 'sproc.assemble': { 'sproc.assemble.distilled_data_from_zip': ('assemble.html#distilled_data_from_zip', 'sproc/assemble.py'),
                                'sproc.assemble.merge_deleted': ('assemble.html#merge_deleted', 'sproc/assemble.py'),
                                'sproc.assemble.parquet_amenable': ('assemble.html#parquet_amenable', 'sproc/assemble.py'),
                                'sproc.assemble.sparsity': ('assemble.html#sparsity', 'sproc/assemble.py'),
                                'sproc.assemble.stack': ('assemble.html#stack', 'sproc/assemble.py')},
            'sproc.bundle': { 'sproc.bundle.read_deleted_zip': ('bundle.html#read_deleted_zip', 'sproc/bundle.py'),
                              'sproc.bundle.read_zip': ('bundle.html#read_zip', 'sproc/bundle.py')},
            'sproc.core': { 'sproc.core.cli_extend_parquet_with_zip': ('core.html#cli_extend_parquet_with_zip', 'sproc/core.py'),
                            'sproc.core.cli_process_zip': ('core.html#cli_process_zip', 'sproc/core.py'),
                            'sproc.core.cli_read_zips': ('core.html#cli_read_zips', 'sproc/core.py'),
                            'sproc.core.cli_rename_columns': ('core.html#cli_rename_columns', 'sproc/core.py'),
                            'sproc.core.read_zips': ('core.html#read_zips', 'sproc/core.py')},
            'sproc.download': { 'sproc.download.file': ('download.html#file', 'sproc/download.py'),
                                'sproc.download.from_date': ('download.html#from_date', 'sproc/download.py'),
                                'sproc.download.make_urls': ('download.html#make_urls', 'sproc/download.py')},
            'sproc.extend': { 'sproc.extend.df_with_zip': ('extend.html#df_with_zip', 'sproc/extend.py'),
                              'sproc.extend.parquet_with_zip': ('extend.html#parquet_with_zip', 'sproc/extend.py')},
            'sproc.hier': { 'sproc.hier._data_scheme_ok': ('hierarchical.html#_data_scheme_ok', 'sproc/hier.py'),
                            'sproc.hier.columns_containing': ('hierarchical.html#columns_containing', 'sproc/hier.py'),
                            'sproc.hier.flat_df_to_multiindexed_df': ('hierarchical.html#flat_df_to_multiindexed_df', 'sproc/hier.py'),
                            'sproc.hier.flat_series_to_multiindexed_series': ( 'hierarchical.html#flat_series_to_multiindexed_series',
                                                                               'sproc/hier.py'),
                            'sproc.hier.flatten_columns_names': ('hierarchical.html#flatten_columns_names', 'sproc/hier.py'),
                            'sproc.hier.pad_col_levels': ('hierarchical.html#pad_col_levels', 'sproc/hier.py')},
            'sproc.io': { 'sproc.io.File': ('io.html#file', 'sproc/io.py'),
                          'sproc.io.File.__init__': ('io.html#file.__init__', 'sproc/io.py'),
                          'sproc.io.File.__repr__': ('io.html#file.__repr__', 'sproc/io.py'),
                          'sproc.io.File.__str__': ('io.html#file.__str__', 'sproc/io.py'),
                          'sproc.io.File.exists': ('io.html#file.exists', 'sproc/io.py'),
                          'sproc.io._cast_to_list_if_not_already': ('io.html#_cast_to_list_if_not_already', 'sproc/io.py'),
                          'sproc.io.cast_list_to_floats_or_strs': ('io.html#cast_list_to_floats_or_strs', 'sproc/io.py'),
                          'sproc.io.cast_multivalued_series_to_common_type': ( 'io.html#cast_multivalued_series_to_common_type',
                                                                               'sproc/io.py'),
                          'sproc.io.homogenize_multivalued': ('io.html#homogenize_multivalued', 'sproc/io.py'),
                          'sproc.io.read': ('io.html#read', 'sproc/io.py'),
                          'sproc.io.write': ('io.html#write', 'sproc/io.py')},
            'sproc.parse': { 'sproc.parse.domain': ('parse.html#domain', 'sproc/parse.py'),
                             'sproc.parse.year_and_maybe_month': ('parse.html#year_and_maybe_month', 'sproc/parse.py')},
            'sproc.postprocess': { 'sproc.postprocess.deduplicate_deleted_series': ( 'postprocess.html#deduplicate_deleted_series',
                                                                                     'sproc/postprocess.py'),
                                   'sproc.postprocess.keep_updates_only': ('postprocess.html#keep_updates_only', 'sproc/postprocess.py'),
                                   'sproc.postprocess.typecast_columns': ('postprocess.html#typecast_columns', 'sproc/postprocess.py')},
            'sproc.structure': { 'sproc.structure.assemble_name': ('structure.html#assemble_name', 'sproc/structure.py'),
                                 'sproc.structure.is_multivalued': ('structure.html#is_multivalued', 'sproc/structure.py'),
                                 'sproc.structure.multivalued_columns': ('structure.html#multivalued_columns', 'sproc/structure.py')},
            'sproc.xml': { 'sproc.xml.columns_depth': ('xml.html#columns_depth', 'sproc/xml.py'),
                           'sproc.xml.deleted_to_series': ('xml.html#deleted_to_series', 'sproc/xml.py'),
                           'sproc.xml.entry_to_dict': ('xml.html#entry_to_dict', 'sproc/xml.py'),
                           'sproc.xml.entry_to_series': ('xml.html#entry_to_series', 'sproc/xml.py'),
                           'sproc.xml.get_deleted_entries': ('xml.html#get_deleted_entries', 'sproc/xml.py'),
                           'sproc.xml.get_entries': ('xml.html#get_entries', 'sproc/xml.py'),
                           'sproc.xml.get_namespaces': ('xml.html#get_namespaces', 'sproc/xml.py'),
                           'sproc.xml.set_or_append': ('xml.html#set_or_append', 'sproc/xml.py'),
                           'sproc.xml.split_namespace_tag': ('xml.html#split_namespace_tag', 'sproc/xml.py'),
                           'sproc.xml.to_curated_df': ('xml.html#to_curated_df', 'sproc/xml.py'),
                           'sproc.xml.to_df': ('xml.html#to_df', 'sproc/xml.py')}}}
