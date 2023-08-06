"""
This module defines the XFrame class which provides the
ability to create, access and manipulate a remote scalable dataframe object.

XFrame acts similarly to pandas.DataFrame, but the data is immutable
and is stored as Spark RDDs.
"""

import array
from textwrap import wrap
import inspect
import time
import itertools
# noinspection PyPackageRequirements
from dateutil import parser as date_parser
import datetime
import copy
import ast
import logging
import types
from sys import stderr

import pyspark

from xframes.deps import pandas, HAS_PANDAS
from xframes.prettytable import PrettyTable
from xframes.xframe_impl import XFrameImpl
from xframes.xarray_impl import infer_type_of_list
from xframes.utils import make_internal_url
from xframes.type_utils import classify_type, classify_auto, is_sortable_type, is_xframe_type
from xframes.object_utils import check_input_uri, check_output_uri
from xframes import object_utils
from xframes.xarray import XArray
import xframes

"""
Copyright (c) 2014, Dato, Inc.
All rights reserved.

Copyright (c) 2017, Charles Hayden
All rights reserved.
"""

__all__ = ['XFrame']


# noinspection PyUnresolvedReferences,PyShadowingNames
class XFrame(object):
    """
    A tabular, column-mutable dataframe object that can scale to big data. 
    XFrame is able to hold data that are much larger than the machine's main
    memory. The data in XFrame is stored row-wise in a Spark RDD.
    Each row of the RDD is a list, whose elements correspond
    to the values in each column.  The column names and types are stored in the XFrame
    instance, and give the mapping to the row list.
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, data=None, format='auto', impl=None, verbose=False):
        """
        Construct a new XFrame from a url, a pandas.DataFrame or a Spark RDD or DataFrame.

        An XFrame can be constructed from the following data formats:
        * csv file (comma separated value)
        * xframe directory archive (A directory where an XFrame was saved previously)
        * a spark RDD plus the column names and types
        * a spark.DataFrame
        * general text file (with csv parsing options, See :py:meth:`read_csv()`)
        * parquet file
        * a Python dictionary
        * pandas.DataFrame
        * JSON
        * Apache Avro

        and from the following sources:

        * your local file system
        * the XFrame Server's file system
        * HDFS
        * Hive
        * Amazon S3
        * HTTP(S)

        Only basic examples of construction are covered here. For more information
        and examples, please see the `User Guide`.

        XFrames are immutable except for assignments to a column.

        Parameters
        ----------
        data : array | pandas.DataFrame | spark.rdd | spark.DataFrame | string | dict, optional
            The actual interpretation of this field is dependent on the `format`
            parameter. If `data` is an array, Pandas DataFrame or Spark RDD, the contents are
            stored in the XFrame. If `data` is an object supporting iteritems, then is is handled
            like a dictionary.  If `data` is an object supporting iteration, then the values
            are iterated to form the XFrame.  If `data` is a string, it is interpreted as a
            file. Files can be read from local file system or urls (hdfs://, s3://, or other
            Hadoop-supported file systems).  To read files from s3, you must set the
            AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables, even if the
            file is publicly accessible.

        format : string, optional
            Format of the data. The default, "auto" will automatically infer the
            input data format. The inference rules are simple: If the data is an
            array or a dataframe, it is associated with 'array' and 'dataframe'
            respectively. If the data is a string, it is interpreted as a file, and
            the file extension is used to infer the file format. The explicit
            options are:

            - "auto"
            - "array"
            - "dict"
            - "xarray"
            - "pandas.dataframe"
            - "csv"
            - "tsv"
            - "psv"
            - "parquet"
            - "rdd"
            - "spark.dataframe"
            - "hive"
            - "xframe"

        verbose : bool, optional
            If True, print the progress while reading a file.

        Notes
        -----
        The following functionality is currently not implemented.
            - pack_columns data types except list, array, and dict
            - groupby quantile

        See Also
        --------
        xframes.XFrame.read_csv():
            Create a new XFrame from a csv file. Preferred for text and CSV formats,
            because it has a lot more options for controlling the parser.

        xframes.XFrame.read_parquet
            Read an XFrame from a parquet file.

        xframes.XFrame.from_rdd
            Create a new XFrame from a Spark RDD or Spark DataFrame.
            Column names and types can be specified if a spark RDD is given; otherwise
            they are taken from the DataFrame.

        xframes.XFrame.save
            Save an XFrame in a file for later use within XFrames or Spark.

        xframes.XFrame.load
            Load an XFrame from a file.  The filename extension is used to determine the
            file format.

        xframes.XFrame.set_trace
            Controls entry and exit tracing.

        xframes.XFrame.spark_context
            Returns the spark context.

        xframes.XFrame.spark_sql_context
            Returns the spark sql context.

        Examples
        --------
        Create an XFrame from a Python dictionary.

        >>> from xframes import XFrame
        >>> sf = XFrame({'id':[1,2,3], 'val':['A','B','C']})
        >>> sf
        Columns:
            id  int
            val str
        Rows: 3
        Data:
              id  val
           0  1   A
           1  2   B
           2  3   C

        Create an XFrame from a remote CSV file.

        >>> url = 'http://testdatasets.s3-website-us-west-2.amazonaws.com/users.csv.gz'
        >>> xf = XFrame.read_csv(url,
        ...     delimiter=',', header=True, comment_char="#",
        ...     column_type_hints={'user_id': int})

        .. document private functions
        .. automethod:: xframes.XFrame.__getitem__
        """
        if impl:
            self._impl = impl
            return

        _format = self._classify_auto(data) if format == 'auto' else format
        # print >>stderr, 'format', _format

        def construct_array(data):
            if len(data) > 0:
                unique_types = set([type(x) for x in data if x is not None])
                if len(unique_types) == 1 and XArray in unique_types:
                    xf = XFrameImpl()
                    for arr in data:
                        xf = xf.add_column(arr.impl(), '')
                    return xf
                if XArray in unique_types:
                    raise ValueError('Cannot create XFrame from mix of regular values and XArrays.')
                return XFrameImpl.from_xarray(XArray(data).impl())
            return XFrameImpl()

        def construct_dict(data):
            if not isinstance(data, dict):
                raise ValueError('Data is not dictionary')

            # special case if all are regular lists
            all_list = True
            list_len = None
            for val in data.itervalues():
                if not isinstance(val, list):
                    all_list = False
                    break
                if list_len is None:
                    list_len = len(val)
                if len(val) != list_len:
                    raise ValueError('Cannot create XFrame from dict of lists of different lengths.')
            if all_list:
                column_names = []
                cols = []
                for key, val in iter(sorted(data.iteritems())):
                    column_names.append(key)
                    cols.append(val)
                rows = [row for row in zip(*cols)]
                column_types = [classify_auto(col) for col in cols]
                return XFrameImpl.load_from_tuple_list(rows, column_names, column_types)
            # General case
            xf = XFrameImpl()
            for key, val in iter(sorted(data.iteritems())):
                if isinstance(val, XArray):
                    xf = xf.add_column(val.impl(), key)
                else:
                    xf = xf.add_column(XArray(val).impl(), key)
            return xf

        def construct_iteritems(data):
            if data is None:
                raise ValueError('Empty iterable')
            xf = XFrameImpl()
            for key, val in iter(sorted(data.iteritems())):
                if not hasattr(val, '__iter__'):
                    raise TypeError('Iterator values must be iterable.')
                xf = xf.add_column(XArray(val).impl(), key)
            return xf

        def construct_csv(path, delimiter):
            if not isinstance(path, basestring):
                raise ValueError('Path is not a string: {}'.format(type(path).__name__))
            url = make_internal_url(path)
            tmpxf = XFrame.read_csv(url, delimiter=delimiter, header=True, verbose=verbose)
            return tmpxf.impl()

        if _format == 'pandas.dataframe':
            if not isinstance(data, pandas.DataFrame):
                raise ValueError('Data is not pandas.DataFrame')
            self._impl = XFrameImpl.load_from_pandas_dataframe(data)
        elif _format == 'xframe_obj':
            if not isinstance(data, XFrame):
                raise ValueError('Data is not XFrame')
            self._impl = XFrameImpl(data.to_rdd(), data.column_names(), data.column_types())
        elif _format == 'xarray':
            if not isinstance(data, XArray):
                raise ValueError('Data is not XArray')
            self._impl = XFrameImpl.from_xarray(data.impl())
        elif _format == 'array':
            self._impl = construct_array(data)
        elif _format == 'iter':
            self._impl = XFrameImpl.from_xarray(XArray(data).impl())
        elif _format == 'dict':
            self._impl = construct_dict(data)
        elif _format == 'iteritems':
            self._impl = construct_iteritems(data)
        elif _format == 'csv':
            self._impl = construct_csv(data, ',')
        elif _format == 'tsv':
            self._impl = construct_csv(data, '\t')
        elif _format == 'psv':
            self._impl = construct_csv(data, '|')
        elif _format == 'parquet':
            if not isinstance(data, basestring):
                raise ValueError('Parquet path is not a string: {}'.format(type(data).__name__))
            url = make_internal_url(data)
            tmpxf = XFrame.read_parquet(url)
            self._impl = tmpxf.impl()
        elif _format == 'xframe':
            if data is None:
                raise ValueError('Empty XFrame')
            url = make_internal_url(data)
            check_input_uri(url)
            self._impl = XFrameImpl.load_from_xframe_index(url)
        elif _format == 'spark.dataframe':
            if data is None:
                raise ValueError('Empty Spark Dataframe')
            self._impl = XFrameImpl.load_from_spark_dataframe(data)
        elif _format == 'hive':
            if not isinstance(data, basestring):
                raise ValueError('Hive path is not a string: {}'.format(type(data).__name__))
            self._impl = XFrameImpl.load_from_hive(data)
        elif _format == 'rdd':
            if data is None:
                raise ValueError('Empty RDD')
            self._impl = XFrameImpl.load_from_rdd(data)
        elif _format == 'empty':
            self._impl = XFrameImpl()
        else:
            raise ValueError("Unknown input type: '{}'.".format(format))
        if self._impl is None:
            raise ValueError('Constructor failed')

    @staticmethod
    def _classify_auto(data):
        if HAS_PANDAS and isinstance(data, pandas.DataFrame):
            return 'pandas.dataframe'
        if isinstance(data, XArray):
            return 'xarray'
        if isinstance(data, XFrame):
            return 'xframe_obj'
        if isinstance(data, dict):
            return 'dict'
        if isinstance(data, array.array):
            return 'array'
        if hasattr(data, 'iteritems'):
            return 'iteritems'
        if hasattr(data, '__iter__'):
            return 'iter'
        if data is None:
            return 'empty'
        if isinstance(data, pyspark.sql.DataFrame):
            return 'spark.dataframe'
        if isinstance(data, pyspark.RDD):
            return 'rdd'
        if isinstance(data, basestring):
            if data.endswith(('.csv', '.csv.gz')):
                return 'csv'
            if data.endswith(('.tsv', '.tsv.gz')):
                return 'tsv'
            if data.endswith(('.psv', '.psv.gz')):
                return 'psv'
            if data.endswith('.parquet'):
                return 'parquet'
            if data.endswith(('.txt', '.txt.gz')):
                logging.info('Assuming file is csv. For other delimiters, use `XFrame.read_csv`.')
                return 'csv'
            else:
                return 'xframe'
        raise ValueError('Cannot infer input type for data {}.'.format(data))

    @classmethod
    def empty(cls, column_names, column_types):
        """
        Create an empty XFrame.

        Creates an empty XFrame, with column names and column types.

        Parameters
        ----------
        column_names : list[str]
            The column names.

        column_types : list[type]
            The column types.

        Returns
        -------
        :class:`.XFrame`
            An empty XFrame with the given column names and types.
        """
        if not isinstance(column_names, list):
            raise TypeError('Column_names must be a list.')
        for name in column_names:
            if not isinstance(name, basestring):
                raise TypeError('Column_names must be strings.')
        for typ in column_types:
            if not isinstance(typ, type):
                raise TypeError('Column_types must be types.')
            if not is_xframe_type(typ):
                raise TypeError('Type "{}" is not a valid column type.'.format(typ.__name__))

        if not isinstance(column_types, list):
            raise TypeError('Column_types must be a list')
        if len(column_names) != len(column_types):
            raise ValueError('Column_names and column_types must be of the same length.')
        return XFrame(impl=XFrameImpl.empty(column_names, column_types))

    @classmethod
    def set_max_row_width(cls, width):
        """
        Set the maximum display width for printing.

        Parameters
        ----------
        width : int
            The maximum width of the table when printing.
        """
        object_utils.MAX_ROW_WIDTH = width

    @classmethod
    def set_html_max_row_width(cls, width):
        """
        Set the maximum display width for displaying in HTML.

        Parameters
        ----------
        width : int
            The maximum width of the table when printing in html.
        """
        object_utils.HTML_MAX_ROW_WIDTH = width

    @classmethod
    def set_footer_strs(cls, footer_strs):
        """
        Set the footer printed beneath tables.

        Parameters
        ----------
        footer_strs : list
            A list of strings.  Each string is a separate line, printed beneath
            a table.  This footer is used when the length of the table
            is known.  To disable printing the footer, pass an empty list.
        """
        if not isinstance(footer_strs, list):
            raise TypeError('Footer strs must be a list')
        object_utils.FOOTER_STRS = footer_strs

    @classmethod
    def set_lazy_footer_strs(cls, footer_strs):
        """
        Set the footer printed beneath tables when the length is unknown.

        Parameters
        ----------
        footer_strs : list
            A list of strings.  Each string is a separate line, printed beneath
            a table.  This footer is used when the length of the table
            is not known because the XFrame has not been evaluated.
            To disable printing the footer, pass an empty list.
        """
        if not isinstance(footer_strs, list):
            raise TypeError('Footer strs must be a list')
        object_utils.LAZY_FOOTER_STRS = footer_strs

    @staticmethod
    def _infer_column_types_from_lines(first_rows, na_values):
        if len(first_rows.column_names()) < 1:
            logging.warn('Insufficient number of columns to perform type inference.')
            raise RuntimeError('Insufficient columns.')
        if len(first_rows) < 1:
            logging.warn('Insufficient number of rows to perform type inference.')
            raise RuntimeError('Insufficient rows.')

        column_names = first_rows.column_names()

        # TODO get this in a way that does not require an iterator
        def row_as_array(row):
            return [row[col] for col in column_names]

        head = [row_as_array(row) for row in first_rows]

        def infer_type(col, na_values):
            col = [val for val in col if val not in na_values]
            types = [classify_type(val) for val in col if val is not None]
            unique_types = set(types)
            if len(unique_types) == 1:
                dtype = types[0]
            elif unique_types == {int, float}:
                dtype = float
            else:
                dtype = str
            return dtype

        n_cols = len(head[0])
        cols = [[row[i] for row in head] for i in range(n_cols)]
        types = [infer_type(col, na_values) for col in cols]

        # special handling for '\n'
        #        if delimiter == '\n' and len(column_type_hints) != 1:
        #          column_type_hints = [str]

        column_type_hints = types
        return column_type_hints

    @classmethod
    def load(cls, filename):
        """
        Load an XFrame. The filename extension is used to determine the format
        automatically. This function is particularly useful for XFrames previously
        saved in binary format. For CSV imports the :py:meth:`~xframes.XFrame.read_csv` function
        provides greater control. If the XFrame is in binary format, `filename` is
        actually a directory, created when the XFrame is saved.

        Parameters
        ----------
        filename : string
            Location of the file to load. Can be a local path or a remote URL.

        Returns
        -------
        :class:`.XFrame`

        See Also
        --------
        xframes.XFrame.save
            Saves the XFrame to a file.

        xframes.XFrame.read_csv
            Allows more control over csv parsing.

        Examples
        --------
        >>> sf = xframes.XFrame({'id':[1,2,3], 'val':['A','B','C']})
        >>> sf.save('my_xframe')        # 'my_xframe' is a directory
        >>> sf_loaded = xframes.XFrame.load('my_xframe')
        """
        sf = cls(data=filename)
        return sf

    @classmethod
    def _read_csv_impl(cls,
                       url,
                       delimiter=',',
                       header=True,
                       error_bad_lines=False,
                       comment_char='',
                       escape_char='\\',
                       double_quote=True,
                       quote_char='\"',
                       skip_initial_space=True,
                       column_type_hints=None,
                       na_values=None,
                       nrows=None,
                       verbose=False,
                       store_errors=True):
        """
        Constructs an XFrame from a CSV file or a path to multiple CSVs, and
        returns a pair containing the XFrame and optionally
        (if store_errors=True) a dict of filenames to XArray
        indicating for each file, what are the incorrectly parsed lines
        encountered.

        Parameters
        ----------
        store_errors : bool
            If true, the output errors dict will be filled.

        See `read_csv` for the rest of the parameters.

        Returns
        -------
        :class:`.XFrame`
            A new XFrame with the contents that were read.
        """
        na_values = na_values or ['']
        parsing_config = dict()
        parsing_config['delimiter'] = delimiter
        parsing_config['use_header'] = header
        parsing_config['continue_on_failure'] = not error_bad_lines
        parsing_config['comment_char'] = comment_char
        parsing_config['escape_char'] = escape_char
        parsing_config['double_quote'] = double_quote
        parsing_config['quote_char'] = quote_char
        parsing_config['skip_initial_space'] = skip_initial_space
        parsing_config['store_errors'] = store_errors
        if isinstance(na_values, basestring):
            na_values = [na_values]
        if na_values is not None and len(na_values) > 0:
            parsing_config['na_values'] = na_values

        if nrows is not None:
            parsing_config['row_limit'] = nrows

        internal_url = make_internal_url(url)
        check_input_uri(internal_url)

        # Attempt to automatically detect the column types. Either produce a
        # list of types; otherwise default to all str types.
        column_type_inference_was_used = False
        if column_type_hints is None:
            try:
                # Get the first 100 rows (using all the desired arguments).
                # first row may be excluded (based on heder setting)
                first_rows = xframes.XFrame.read_csv(url,
                                                     nrows=100,
                                                     column_type_hints=str,
                                                     header=header,
                                                     delimiter=delimiter,
                                                     comment_char=comment_char,
                                                     escape_char=escape_char,
                                                     double_quote=double_quote,
                                                     quote_char=quote_char,
                                                     skip_initial_space=skip_initial_space)
                column_type_hints = XFrame._infer_column_types_from_lines(first_rows, na_values)
                typelist = '[' + ','.join(t.__name__ for t in column_type_hints) + ']'
                if verbose:
                    print >> stderr, '------------------------------------------------------'
                    print >> stderr, 'Inferred types from first line of file as '
                    print >> stderr, 'column_type_hints=' + typelist
                    print >> stderr, 'If parsing fails due to incorrect types, you can correct'
                    print >> stderr, 'the inferred type list above and pass it to read_csv in'
                    print >> stderr, 'the column_type_hints argument'
                    print >> stderr, '------------------------------------------------------'
                column_type_inference_was_used = True
            except Exception as e:
                # If the above fails, default back to str for all columns.
                if verbose:
                    logging.info('Error {} {}'.format(type(e).__name__, e))
                    logging.warn('Could not detect types. Using str for each column.')
                column_type_hints = str

        if isinstance(column_type_hints, type):
            type_hints = {'__all_columns__': column_type_hints}
        elif isinstance(column_type_hints, list):
            type_hints = dict(zip(['__X%d__' % i for i in range(len(column_type_hints))], column_type_hints))
        elif isinstance(column_type_hints, dict):
            type_hints = column_type_hints
        else:
            raise TypeError("Invalid type for column_type_hints. Must be a 'dict, 'list' or a single type.")

        try:
            errors, impl = XFrameImpl.load_from_csv(internal_url, parsing_config, type_hints)
        except IOError:
            if column_type_inference_was_used:
                # try again
                logging.warn('Unable to parse the file with automatic type inference.')
                logging.warn('Defaulting to column_type_hints=str')
                type_hints = {'__all_columns__': str}
                try:
                    errors, impl = XFrameImpl.load_from_csv(internal_url, parsing_config, type_hints)
                except:
                    raise
            else:
                raise

        return cls(impl=impl), {f: XArray(impl=es) for f, es in errors.iteritems() if es.size() != 0}

    @classmethod
    def read_csv_with_errors(cls,
                             url,
                             delimiter=',',
                             header=True,
                             comment_char='',
                             escape_char='\\',
                             double_quote=True,
                             quote_char='\"',
                             skip_initial_space=True,
                             column_type_hints=None,
                             na_values=None,
                             nrows=None,
                             verbose=False):
        """
        Constructs an XFrame from a CSV file or a path to multiple CSVs, and
        returns a pair containing the XFrame and a dict of error type to XArray
        indicating for each type, what are the incorrectly parsed lines
        encountered.

        The kinds of errors that are detected are:
            * width -- The row has the wrong number of columns.
            * header -- The first row in the file did not parse correctly.  This row is used to
                        determine the table width, so the rest of the file is not processed.
                        The result is an empty XFrame.
            * csv -- The csv parser raised a csv.Error or a SystemError exception.
                     This can be caused by having an
                     unacceptable character, such as a null byte, in the input,
                     or by serious system errors.
                     This presence of this error indicates that processing has been
                     interrupted, so all remaining data in
                     the input file is not processed.

        Parameters
        ----------
        url : string
            Location of the CSV file or directory to load. If URL is a directory
            or a "glob" pattern, all matching files will be loaded.

        delimiter : string, optional
            This describes the delimiter used for parsing csv files. Must be a
            single character.  Files with double delimiters such as "||" should specify
            delimiter='|' and should drop columns with empty heading and data.

        header : bool, optional
            If true, uses the first row as the column names. Otherwise use the
            default column names: 'X.1, X.2, ...'.

        comment_char : string, optional
            The character which denotes that the
            remainder of the line is a comment.  The line must contain valid data
            preceding the commant.

        escape_char : string, optional
            Character which begins a C escape sequence

        double_quote : bool, optional
            If True, two consecutive quotes in a string are parsed to a single
            quote.

        quote_char : string, optional
            Character sequence that indicates a quote.

        skip_initial_space : bool, optional
            Ignore extra spaces at the start of a field

        column_type_hints : None, type, list[type], dict{string: type}, optional
            This provides type hints for each column. By default, this method
            attempts to detect the type of each column automatically.

            Supported types are int, float, str, list, dict, and array.array.

            * If a single type is provided, the type will be
              applied to all columns. For instance, column_type_hints=float
              will force all columns to be parsed as float.
            * If a list of types is provided, the types applies
              to each column in order, e.g.[int, float, str]
              will parse the first column as int, second as float and third as
              string.
            * If a dictionary of column name to type is provided,
              each type value in the dictionary is applied to the key it
              belongs to.
              For instance {'user':int} will hint that the column called "user"
              should be parsed as an integer, and the rest will default to
              string.

        na_values : str | list of str, optional
            A string or list of strings to be interpreted as missing values.

        nrows : int, optional
            If set, only this many rows will be read from the file.

        verbose : bool, optional
            If True, print the progress while reading files.

        Returns
        -------
        tuple
            The first element is the XFrame with good data. The second element
            is a dictionary of filenames to XArrays indicating for each file,
            what are the incorrectly parsed lines encountered.

        See Also
        --------
        xframes.XFrame.read_csv
            Reads csv without error controls.
        xframes.XFrame
            The constructor can read csv files, but is not configurable.

        Examples
        --------
        >>> bad_url = 'https://s3.amazonaws.com/gl-testdata/bad_csv_example.csv'
        >>> (xf, bad_lines) = xframes.XFrame.read_csv_with_errors(bad_url)
        >>> xf
        +---------+----------+--------+
        | user_id | movie_id | rating |
        +---------+----------+--------+
        |  25904  |   1663   |   3    |
        |  25907  |   1663   |   3    |
        |  25923  |   1663   |   3    |
        |  25924  |   1663   |   3    |
        |  25928  |   1663   |   2    |
        |   ...   |   ...    |  ...   |
        +---------+----------+--------+
        [98 rows x 3 columns]

        >>> bad_lines
        {'https://s3.amazonaws.com/gl-testdata/bad_csv_example.csv': dtype: str
         Rows: 1
         ['x,y,z,a,b,c']}
        """
        na_values = na_values or '[NA]'
        return cls._read_csv_impl(url,
                                  delimiter=delimiter,
                                  header=header,
                                  error_bad_lines=False,  # we are storing errors,
                                  # thus we must not fail
                                  # on bad lines
                                  comment_char=comment_char,
                                  escape_char=escape_char,
                                  double_quote=double_quote,
                                  quote_char=quote_char,
                                  skip_initial_space=skip_initial_space,
                                  column_type_hints=column_type_hints,
                                  na_values=na_values,
                                  nrows=nrows,
                                  verbose=verbose,
                                  store_errors=True)

    @classmethod
    def read_csv(cls,
                 url,
                 delimiter=',',
                 header=True,
                 error_bad_lines=False,
                 comment_char='',
                 escape_char='\\',
                 double_quote=True,
                 quote_char='\"',
                 skip_initial_space=True,
                 column_type_hints=None,
                 na_values=None,
                 nrows=None,
                 verbose=False):
        """
        Constructs an XFrame from a CSV file or a path to multiple CSVs.

        Parameters
        ----------
        url : string
            Location of the CSV file or directory to load. If URL is a directory
            or a "glob" pattern, all matching files will be loaded.

        delimiter : string, optional
            This describes the delimiter used for parsing csv files. Must be a
            single character.

        header : bool, optional
            If true, uses the first row as the column names. Otherwise use the
            default column names : 'X1, X2, ...'.

        error_bad_lines : bool
            If true, will fail upon encountering a bad line. If false, will
            continue parsing skipping lines which fail to parse correctly.
            A sample of the first 10 encountered bad lines will be printed.

        comment_char : string, optional
            The character which denotes that the remainder of the line is a
            comment.

        escape_char : string, optional
            Character which begins a C escape sequence

        double_quote : bool, optional
            If True, two consecutive quotes in a string are parsed to a single
            quote.

        quote_char : string, optional
            Character sequence that indicates a quote.

        skip_initial_space : bool, optional
            Ignore extra spaces at the start of a field

        column_type_hints : None, type, list[type], dict[string, type], optional
            This provides type hints for each column. By default, this method
            attempts to detect the type of each column automatically.

            Supported types are int, float, str, list, dict, and array.array.

            * If a single type is provided, the type will be
              applied to all columns. For instance, column_type_hints=float
              will force all columns to be parsed as float.
            * If a list of types is provided, the types applies
              to each column in order, e.g.[int, float, str]
              will parse the first column as int, second as float and third as
              string.
            * If a dictionary of column name to type is provided,
              each type value in the dictionary is applied to the key it
              belongs to.
              For instance {'user':int} will hint that the column called "user"
              should be parsed as an integer, and the rest will default to
              string.

        na_values : str | list of str, optional
            A string or list of strings to be interpreted as missing values.

        nrows : int, optional
            If set, only this many rows will be read from the file.

        verbose : bool, optional
            If True, print the progress while reading files.

        Returns
        -------
        :class:`.XFrame`

        See Also
        --------
        xframes.XFrame.read_csv_with_errors
            Allows more control over errors.

        xframes.XFrame
            The constructor can read csv files, but is not configurable.

        Examples
        --------

        Read a regular csv file, with all default options, automatically
        determine types:

        >>> url = 'http://s3.amazonaws.com/gl-testdata/rating_data_example.csv'
        >>> xf = xframes.XFrame.read_csv(url)
        >>> xf
        Columns:
          user_id int
          movie_id  int
          rating  int
        Rows: 10000
        +---------+----------+--------+
        | user_id | movie_id | rating |
        +---------+----------+--------+
        |  25904  |   1663   |   3    |
        |  25907  |   1663   |   3    |
        |  25923  |   1663   |   3    |
        |  25924  |   1663   |   3    |
        |  25928  |   1663   |   2    |
        |   ...   |   ...    |  ...   |
        +---------+----------+--------+
        [10000 rows x 3 columns]

        Read only the first 100 lines of the csv file:

        >>> xf = xframes.XFrame.read_csv(url, nrows=100)
        >>> xf
        Columns:
          user_id int
          movie_id  int
          rating  int
        Rows: 100
        +---------+----------+--------+
        | user_id | movie_id | rating |
        +---------+----------+--------+
        |  25904  |   1663   |   3    |
        |  25907  |   1663   |   3    |
        |  25923  |   1663   |   3    |
        |  25924  |   1663   |   3    |
        |  25928  |   1663   |   2    |
        |   ...   |   ...    |  ...   |
        +---------+----------+--------+
        [100 rows x 3 columns]

        Read all columns as str type

        >>> xf = xframes.XFrame.read_csv(url, column_type_hints=str)
        >>> xf
        Columns:
          user_id  str
          movie_id  str
          rating  str
        Rows: 10000
        +---------+----------+--------+
        | user_id | movie_id | rating |
        +---------+----------+--------+
        |  25904  |   1663   |   3    |
        |  25907  |   1663   |   3    |
        |  25923  |   1663   |   3    |
        |  25924  |   1663   |   3    |
        |  25928  |   1663   |   2    |
        |   ...   |   ...    |  ...   |
        +---------+----------+--------+
        [10000 rows x 3 columns]

        Specify types for a subset of columns and leave the rest to be str.

        >>> xf = xframes.XFrame.read_csv(url,
        ...                               column_type_hints={
        ...                               'user_id':int, 'rating':float
        ...                               })
        >>> xf
        Columns:
          user_id str
          movie_id  str
          rating  float
        Rows: 10000
        +---------+----------+--------+
        | user_id | movie_id | rating |
        +---------+----------+--------+
        |  25904  |   1663   |  3.0   |
        |  25907  |   1663   |  3.0   |
        |  25923  |   1663   |  3.0   |
        |  25924  |   1663   |  3.0   |
        |  25928  |   1663   |  2.0   |
        |   ...   |   ...    |  ...   |
        +---------+----------+--------+
        [10000 rows x 3 columns]

        Not treat first line as header:

        >>> xf = xframes.XFrame.read_csv(url, header=False)
        >>> xf
        Columns:
          X1  str
          X2  str
          X3  str
        Rows: 10001
        +---------+----------+--------+
        |    X1   |    X2    |   X3   |
        +---------+----------+--------+
        | user_id | movie_id | rating |
        |  25904  |   1663   |   3    |
        |  25907  |   1663   |   3    |
        |  25923  |   1663   |   3    |
        |  25924  |   1663   |   3    |
        |  25928  |   1663   |   2    |
        |   ...   |   ...    |  ...   |
        +---------+----------+--------+
        [10001 rows x 3 columns]

        Treat '3' as missing value:

        >>> xf = xframes.XFrame.read_csv(url, na_values=['3'], column_type_hints=str)
        >>> xf
        Columns:
          user_id str
          movie_id  str
          rating  str
        Rows: 10000
        +---------+----------+--------+
        | user_id | movie_id | rating |
        +---------+----------+--------+
        |  25904  |   1663   |  None  |
        |  25907  |   1663   |  None  |
        |  25923  |   1663   |  None  |
        |  25924  |   1663   |  None  |
        |  25928  |   1663   |   2    |
        |   ...   |   ...    |  ...   |
        +---------+----------+--------+
        [10000 rows x 3 columns]

        Throw error on parse failure:

        >>> bad_url = 'https://s3.amazonaws.com/gl-testdata/bad_csv_example.csv'
        >>> xf = xframes.XFrame.read_csv(bad_url, error_bad_lines=True)
        RuntimeError: Runtime Exception. Unable to parse line "x,y,z,a,b,c"
        Set error_bad_lines=False to skip bad lines
        """

        na_values = na_values or ['']
        ret = cls._read_csv_impl(url,
                                 delimiter=delimiter,
                                 header=header,
                                 error_bad_lines=error_bad_lines,
                                 comment_char=comment_char,
                                 escape_char=escape_char,
                                 double_quote=double_quote,
                                 quote_char=quote_char,
                                 skip_initial_space=skip_initial_space,
                                 column_type_hints=column_type_hints,
                                 na_values=na_values,
                                 nrows=nrows,
                                 verbose=verbose,
                                 store_errors=False)
        return ret[0]

    @classmethod
    def from_xarray(cls, arry, name):
        """
        Constructs a one column XFrame from an XArray and a column name.

        Parameters
        ----------
        arry : :class:`.XArray`
            The XArray that will become an XFrame of one column.

        name: str
            The column name.

        Returns
        -------
        out: :class:`.XFrame`
            Returns an XFrame with one column, containing the values in arry and with the given name.

        Examples
        Create an XFrame from an XArray.
        >>>  print  XFrame.from_xarray(XArray([1, 2, 3]), 'name')
        +------+
        | name |
        +------+
        |  1   |
        |  2   |
        |  3   |
        +------+
        """
        return XFrame(impl=XFrameImpl.from_xarray(arry.impl(), name))

    @classmethod
    def read_text(cls, path, delimiter=None, nrows=None, verbose=False):
        """
        Constructs an XFrame from a text file or a path to multiple text files.

        Parameters
        ----------
        path : string
            Location of the text file or directory to load. If 'path' is a directory
            or a "glob" pattern, all matching files will be loaded.

        delimiter : string, optional
            This describes the delimiter used for separating records. Must be a
            single character.  Defaults to newline.

        nrows : int, optional
            If set, only this many rows will be read from the file.

        verbose : bool, optional
            If True, print the progress while reading files.

        Returns
        -------
        :class:`.XFrame`

        Examples
        --------

        Read a regular text file, with default options.

        >>> path = 'http://s3.amazonaws.com/gl-testdata/rating_data_example.csv'
        >>> xf = xframes.XFrame.read_text(path)
        >>> xf
        +-------
        | text |
        +---------+
        |  25904  |
        |  25907  |
        |  25923  |
        |  25924  |
        |  25928  |
        |   ...   |
        +---------+
        [10000 rows x 1 column]

        Read only the first 100 lines of the text file:

        >>> xf = xframes.XFrame.read_text(path, nrows=100)
        >>> xf
        Rows: 100
        +---------+
        |  25904  |
        |  25907  |
        |  25923  |
        |  25924  |
        |  25928  |
        |   ...   |
        +---------+
        [100 rows x 1 columns]

        Read using a given delimiter.

        >>> xf = xframes.XFrame.read_text(path, delimiter='.')
        >>> xf
        Rows: 250
        +---------+
        |  25904  |
        |  25907  |
        |  25923  |
        |  25924  |
        |  25928  |
        |   ...   |
        +---------+
        [250 rows x 1 columns]


        """
        check_input_uri(path)
        url = make_internal_url(path)
        return cls(impl=XFrameImpl.read_from_text(url, delimiter=delimiter, nrows=nrows, verbose=verbose))

    @classmethod
    def read_parquet(cls, url):
        """
        Constructs an XFrame from a parquet file.

        Parameters
        ----------
        url : string
            Location of the parquet file to load. 

        Returns
        -------
        :class:`.XFrame`

        See Also
        --------
        xframes.XFrame
            The constructor can read parquet files.

        """
        check_input_uri(url)
        return cls(impl=XFrameImpl.load_from_parquet(url))

    def impl(self):
        return self._impl

    def dump_debug_info(self):
        """
        Print information about the Spark RDD associated with this XFrame.
        """
        return self._impl.dump_debug_info()

    def _get_pretty_tables(self, wrap_text=False, max_wrap_rows=2, max_row_width=None,
                           max_column_width=30, max_columns=20,
                           max_rows_to_display=60):
        """
        Returns a list of pretty print tables representing the current XFrame.
        If the number of columns is larger than max_columns, the last pretty
        table will contain an extra column of "...".

        Parameters
        ----------
        wrap_text : bool, optional

        max_wrap_rows : int, optional
            Max number of rows after wrapping, Default 2

        max_row_width : int, optional
            Max number of characters per table.

        max_column_width : int, optional
            Max number of characters per column.

        max_columns : int, optional
            Max number of columns per table.

        max_rows_to_display : int, optional
            Max number of rows to display.

        Returns
        -------
        list[PrettyTable]
        """
        # We are going to need a column of values at a time
        # Take should return a list of tuples
        max_row_width = max_row_width or object_utils.MAX_ROW_WIDTH
        if self._impl.rdd() is None:
            return [PrettyTable()]
        head_rows = self._impl.rdd().take(max_rows_to_display + 1)
        if len(head_rows) == 0:
            return [PrettyTable()]
        if len(head_rows) > max_rows_to_display:
            extra_rows = True
            head_rows = head_rows[:max_rows_to_display]
        else:
            extra_rows = False
        n_rows = len(head_rows)

        # organize the results as columns
        cols = {}
        for index, col_name in enumerate(self.column_names()[:max_columns]):
            cols[col_name] = [row[index] for row in head_rows]

        def truncate_str(s, wrap_str, max_wrap_rows):
            # Truncate and optionally wrap the input string as unicode, replace
            # unconvertible character with a diamond ?.
            s = repr(s)
            # repr adds the escape characters. but also adds quotes around
            # the string
            if len(s) >= 2:
                if s[0] == 'u':
                    s = s[2:-1]
                else:
                    s = s[1:-1]
            if len(s) <= max_column_width:
                return unicode(s, errors='replace')
            else:
                # if wrap_str is true, wrap the text and take at most max_wrap_rows
                if wrap_str:
                    wrapped_lines = wrap(s, max_column_width)
                    ret = '\n'.join(wrapped_lines[:max_wrap_rows])
                    last_line = wrapped_lines[:max_wrap_rows][-1]
                    if len(last_line) >= max_column_width or len(wrapped_lines) > max_wrap_rows:
                        space_left = max_column_width - len(last_line)
                        space_truncate = max(0, 4 - space_left)
                        if space_truncate > 0:
                            ret = ret[:-space_truncate] + ' ...'
                        else:
                            ret += ' ...'
                else:
                    ret = s[:max_column_width]
                    ret = ret[:-4] + ' ...'
                return unicode(ret, errors='replace')
                # end of truncate_str

        columns = self.column_names()[:max_columns]
        columns.reverse()  # reverse the order of columns and we will pop from the end

        num_column_of_last_table = 0
        row_of_tables = []
        # let's build a list of tables with max_columns
        # each table should satisfy, max_row_width, and max_column_width
        while len(columns) > 0:
            tbl = PrettyTable()
            table_width = 0
            num_column_of_last_table = 0
            while len(columns) > 0:
                col = columns.pop()
                # check the max length of element in the column
                header = truncate_str(col, wrap_text, max_wrap_rows)
                if n_rows > 0:
                    col_width = min(max_column_width, max(max(len(str(x)) for x in cols[col]), len(header) + 3))
                else:
                    col_width = max_column_width
                if table_width + col_width < max_row_width:
                    # truncate the header if necessary
                    # tbl.add_column(header, [truncate_str(str(x, max_wrap_rows), wrap_text) for x in headxf[col]])
                    tbl.add_column(str(header), [truncate_str(str(x), wrap_text, max_wrap_rows) for x in cols[col]])
                    table_width = str(tbl).find('\n')
                    num_column_of_last_table += 1
                else:
                    # the column does not fit in the current table, push it back to columns
                    columns.append(col)
                    break
            tbl.align = 'c'
            row_of_tables.append(tbl)

        # add a column of all "..." if there are more columns than displayed
        if self.num_columns() > max_columns:
            row_of_tables[-1].add_column('...', ['...'] * n_rows)
            num_column_of_last_table += 1

        # add a row of all "..." if there are more rows than displayed
        if extra_rows:
            row_of_tables[-1].add_row(['...'] * num_column_of_last_table)
        return row_of_tables

    def _create_footer(self, html_flag, max_rows_to_display):
        sep = '<br>' if html_flag else '\n'
        if self._is_materialized():
            footer = '[{} rows x {} columns]{}'.format(self.num_rows(), self.num_columns(), sep)
            if self.num_rows() > max_rows_to_display:
                footer += sep.join(object_utils.FOOTER_STRS)
        else:
            footer = '[? rows x {} columns]\n'.format(self.num_columns(), sep)
            footer += '\n'.join(object_utils.LAZY_FOOTER_STRS)
        return footer

    def print_rows(self, num_rows=10, num_columns=40,
                   max_column_width=30, max_row_width=None,
                   wrap_text=False, max_wrap_rows=2, footer=True):
        """
        Print the first rows and columns of the XFrame in human readable format.

        Parameters
        ----------
        num_rows : int, optional
            Number of rows to print.

        num_columns : int, optional
            Number of columns to print.

        max_column_width : int, optional
            Maximum width of a column. Columns use fewer characters if possible.

        max_row_width : int, optional
            Maximum width of a printed row. Columns beyond this width wrap to a
            new line. `max_row_width` is automatically reset to be the
            larger of itself and `max_column_width`.

        wrap_text : boolean, optional
            Wrap the text within a cell.  Defaults to False.

        max_wrap_rows : int, optional
            When wrapping is in effect, the maximum number of resulting rows for each cell
            before truncation takes place.

        footer : bool, optional
            True to pinrt a footer.

        See Also
        --------
        xframes.XFrame.head
            Returns the first part of a XFrame.

        xframes.XFrame.tail
            Returns the last part of an XFrame.
        """

        max_rows_to_display = num_rows
        max_row_width = max_row_width or object_utils.MAX_ROW_WIDTH
        max_row_width = max(max_row_width, max_column_width + 1)

        row_of_tables = self._get_pretty_tables(wrap_text=wrap_text,
                                                max_wrap_rows=max_wrap_rows,
                                                max_rows_to_display=num_rows,
                                                max_columns=num_columns,
                                                max_column_width=max_column_width,
                                                max_row_width=max_row_width)
        if footer:
            footer = self._create_footer(False, max_rows_to_display)
        else:
            footer = ''
        print '\n'.join([str(tb) for tb in row_of_tables]) + '\n' + footer

    def __str__(self, num_rows=10, footer=True):
        """
        Returns a string containing the first 10 elements of the frame, along
        with a description of the frame.
        """
        max_rows_to_display = num_rows

        row_of_tables = self._get_pretty_tables(wrap_text=False,
                                                max_rows_to_display=max_rows_to_display,
                                                max_row_width=object_utils.MAX_ROW_WIDTH)
        if not footer:
            return '\n'.join([str(tb) for tb in row_of_tables])

        footer = self._create_footer(False, max_rows_to_display)
        return '\n'.join([str(tb) for tb in row_of_tables]) + '\n' + footer

    def _repr_html_(self):
        max_rows_to_display = 10

        row_of_tables = self._get_pretty_tables(wrap_text=True,
                                                max_row_width=object_utils.HTML_MAX_ROW_WIDTH,
                                                max_columns=40,
                                                max_column_width=25,
                                                max_rows_to_display=max_rows_to_display)
        footer = self._create_footer(True, max_rows_to_display)
        begin = '<div style="max-height:1000px;max-width:1500px;overflow:auto;">'
        end = '\n</div>'
        return begin + '\n'.join([tb.get_html_string(format=True) for tb in row_of_tables]) + '\n' + footer + end

    def __nonzero__(self):
        """
        Returns true if the frame is not empty.
        """
        return self.num_rows() != 0

    def __len__(self):
        """
        Returns the number of rows of the XFrame.
        """
        return self.num_rows()

    def __copy__(self):
        """
        Returns a shallow copy of the XFrame.
        """
        return XFrame(impl=self._impl.copy())

    def width(self):
        """
        Diagnostic: the number of elements in each tuple of the RDD.
        """
        return XArray(impl=self._impl.width())

    def num_rows(self):
        """
        The number of rows in this XFrame.

        Returns
        -------
        int
            Number of rows in the XFrame.

        See Also
        --------
        xframes.XFrame.num_columns
            Returns the number of columns.
        """
        return self._impl.num_rows()

    def num_columns(self):
        """
        The number of columns in this XFrame.

        Returns
        -------
        int
            Number of columns in the XFrame.

        See Also
        --------
        xframes.XFrame.num_rows
            Returns the number of rows.
        """
        return self._impl.num_columns()

    def column_names(self):
        """
        The name of each column in the XFrame.

        Returns
        -------
        list[string]
            Column names of the XFrame.

        See Also
        --------
        xframes.XFrame.rename
            Renames the columns.
        """
        return copy.copy(self._impl.column_names())

    def column_types(self):
        """
        The type of each column in the XFrame.

        Returns
        -------
        list[type]
            Column types of the XFrame.

        See Also
        --------
        xframes.XFrame.dtype
            This is a synonym for column_types.
        """
        return copy.copy(self._impl.dtype())

    def dtype(self):
        """
        The type of each column in the XFrame.

        Returns
        -------
        list[type]
            Column types of the XFrame.

        See Also
        --------
        xframes.XFrame.column_types
            This is a synonym for dtype.

        """
        return copy.copy(self._impl.dtype())

    def lineage(self):
        """
        The table lineage: the files that went into building this table.

        Returns
        -------
        dict
            * key 'table': set[filename]
                The files that were used to build the XArray
            * key 'column': dict{column_name: set[filename]}
                The set of files that were used to build each column
        """
        return self._impl.lineage_as_dict()

    def head(self, n=10):
        """
        The first n rows of the XFrame.

        Parameters
        ----------
        n : int, optional
            The number of rows to fetch.

        Returns
        -------
        :class:`.XFrame`
            A new XFrame which contains the first n rows of the current XFrame

        See Also
        --------
        xframes.XFrame.tail
            Returns the last part of the XFrame.

        xframes.XFrame.print_rows
            Prints the XFrame.
        """
        return XFrame(impl=self._impl.head(n))

    def tail(self, n=10):
        """
        The last n rows of the XFrame.

        Parameters
        ----------
        n : int, optional
            The number of rows to fetch.

        Returns
        -------
        :class:`.XFrame`
            A new XFrame which contains the last n rows of the current XFrame.

        See Also
        --------
        xframes.XFrame.head
            Returns the first part of the XFrame.

        xframes.XFrame.print_rows
            Prints the XFrame.
        """
        return XFrame(impl=self._impl.tail(n))

    def to_pandas_dataframe(self):
        """
        Convert this XFrame to pandas.DataFrame.

        This operation will construct a pandas.DataFrame in memory. Care must
        be taken when size of the returned object is big.

        Returns
        -------
        pandas.DataFrame
            The dataframe which contains all rows of XFrame.
        """
        if not HAS_PANDAS:
            raise TypeError('Pandas not found in PYTHONPATH.')
        df = pandas.DataFrame()
        for i in range(self.num_columns()):
            column_name = self.column_names()[i]
            df[column_name] = list(self[column_name])
            if len(df[column_name]) == 0:
                df[column_name] = df[column_name].astype(self.column_types()[i])
        return df

    def to_rdd(self):
        """
        Convert the current XFrame to a Spark RDD.  The RDD consists of tuples
        containing the column data.  No conversion is necessary: the internal RDD is
        returned.

        Returns
        -------
        spark.RDD
            The spark RDD that is used to represent the XFrame.

        See Also
        --------
        from_rdd
            Converts from a Spark RDD.
        """
        return self._impl.to_rdd()

    def to_spark_dataframe(self,
                           table_name=None,
                           column_names=None,
                           column_type_hints=None,
                           number_of_partitions=None):
        """
        Convert the current XFrame to a Spark DataFrame.

        Parameters
        ----------
        table_name : str, optional
            If given, give this name to the temporary table.

        column_names : list, optional
            A list of the column names to assign.
            Defaults to the names in the table, edited to fit the Dataframe restrictions.

        column_type_hints : dict, optional
            Column types must be supplied when creating a DataFrame.  These hints specify these
            types,  If hints are not given,
            the column types are derived from the XFrame column types.
            The column types in DataFrames are more restricted in XFrames.

            XFrames attempts to supply the correct column types, but
            cannot always determine the correct settings.  The caller can supply hints to 
            ensure the desired settings, but
            the caller is still responsible for making sure the values in the XFrame are
            consistent with these settings.
            * Integers: In DataFrames integers must fit in 64 bits.  In python, large
            integers can be larger.
            If an XFrame contains such integers, it will fail to store as a DataFrame.
            The column can be
            converted to strings in this case.

            * Lists must be of a uniform type in a DataFrame.  The caller must convert 
            lists to meet this requirement, and
            must provide a hint specifying the element type.

            * Dictionaries must have a uniform key and value type.  
            The caller must convert dictionaries to meet this
            requirement and must provide a hint specifying the key and value types.

            Hints are given as a dictionary of column_name: column_hint.  Any column without a hint
            is handled using the XFrame column type.
            For simple types, hints are just type names (as strings): int, long float, 
            bool, datetime, or str.
            For lists, hints are "list[<type>]" where <type> is one of the simple types.
            For dictionaries, hints are "dict{<key_type>:<value_type>}" where key_type and 
            value_type is one of the simple types.

        number_of_partitions : int, optional
            The number of partitions to create.

        Returns
        -------
        spark.DataFrame
            The converted spark dataframe.
        """
        return self._impl.to_spark_dataframe(table_name, column_names, column_type_hints, number_of_partitions)

    @classmethod
    def from_rdd(cls, rdd, column_names=None, column_types=None):
        """
        Create a XFrame from a spark RDD or spark DataFrame.  The data should be:
        * an RDD of tuples
        * Each tuple should be of the same length.
        * Each "column" should be of a uniform type.

        Parameters
        ----------
        rdd: spark.RDD or spark.DataFrame
            Data used to populate the XFrame

        column_names : list of string, optional
            The column names to use.  Ignored for Spark DataFrames.

        column_types : list of type, optional
            The column types to use.  Ignored for Spark DataFrames.

        Returns
        -------
        :class:`.XFrame`

        See Also
        --------
        to_rdd
            Converts to a Spark RDD.
        """
        check_res = rdd.take(1)

        if len(check_res) > 0 \
                and check_res[0].__class__.__name__ == 'Row' \
                and rdd.__class__.__name__ != 'DataFrame':
            raise Exception('Conversion from RDD(pyspark.sql.Row) to XFrame not supported. ' +
                            'Please call inferSchema(RDD) first.')
        xf = cls()
        if XFrameImpl.is_dataframe(rdd):
            xf._impl = XFrameImpl.load_from_spark_dataframe(rdd)
        elif XFrameImpl.is_rdd(rdd):
            xf._impl = XFrameImpl.load_from_rdd(rdd, column_names, column_types)
        else:
            raise ValueError('Argument is not an RDD.')
        return xf

    def select_rows(self, xa):
        """
        Selects rows of the XFrame where the XArray evaluates to True.

        Parameters
        ----------
        xa : :class:`.XArray`
            Must be the same length as the XFrame. The filter values.

        Returns
        -------
        :class:`.XFrame`
            A new XFrame which contains the rows of the XFrame where the
            XArray is True.  The truth
            test is the same as in python, so non-zero values are considered true.

        """
        if not isinstance(xa, XArray):
            raise ValueError('Argument must be an XArray')
        return XFrame(impl=self._impl.logical_filter(xa.impl()))

    def foreach(self, row_fn, init_fn=None, final_fn=None, use_columns=None, seed=None):
        """
        Apply the given function to each row of a XFrame.  This is intended to be used
        for functions with side effects.

        Rows are processed in groups.  Each group is processed sequentially in one execution context.
        An initial funciton, if given, is executed forst for each group.
        Its results are passed to each row function.
        The row function receives the row data as a dictionary of column name: column value.

        Parameters
        ----------
        row_fn : function
            The function to be applied to each row of the XFrame.
            Any value that is returned is ignored.
            The row_fn takes two parameters: row and init.
            The row is a dictionary of column-name: column_value.
            The init value is returned by init_fn.

        init_fn : function, optional
            The function to be applied before row_fn is called.
            The rows are processed in groups: init_fn is called once for each group.
            If no init_fn is supplied, the row_fn is passed None as its second parameter.
            Init_fn takes no parameters.

        final_fn : function, optional
            The function to be applied after all row_fn calls are made.
            Final_fn takes one parameter, the value returned by the init_fn.

        use_columns : str | list[str], optional
            The column or list of columns to be supplied in the row passed to the function.
            If not given, all columns wll be used to build the row.

        seed : int, optional
            Used as the seed if a random number generator is included in `fn`.

        Examples
        --------
        Send rows to an external sink.

        >>> xf = xframes.XFrame({'user_id': [1, 2, 3], 'movie_id': [3, 3, 6],
                                  'rating': [4, 5, 1]})
        >>> xf.foreach(lambda row, ini: send(row['user_id'], row['movie_id'], row['rating']))

        Send rows to an external sink with modification.

        >>> xf = xframes.XFrame({'user_id': [1, 2, 3], 'movie_id': [3, 3, 6],
                                  'rating': [4, 5, 1]})
        >>> xf.foreach(lambda row, bias: send(row['user_id'], row['movie_id'], row['rating'] + bias),
                    lambda: 10)
        """

        if not inspect.isfunction(row_fn):
            raise TypeError('Row_fn must be a function.')
        if init_fn is not None and not inspect.isfunction(init_fn):
            raise TypeError('Init_fn must be a function.')
        if final_fn is not None and not inspect.isfunction(final_fn):
            raise TypeError('Final_fn must be a function.')
        if isinstance(use_columns, basestring):
            use_columns = [use_columns]
        if not seed:
            seed = int(time.time())

        if not use_columns:
            use_columns = self.column_names()

        self._impl.foreach(row_fn, init_fn, final_fn, use_columns, seed)

    def apply(self, fn, dtype=None, use_columns=None, seed=None):
        """
        Transform each row to an XArray according to a
        specified function. Returns a new XArray of `dtype` where each element
        in this XArray is transformed by `fn(x)` where `x` is a single row in
        the XFrame represented as a dictionary.  The `fn` should return
        exactly one value which can be cast into type `dtype`. If `dtype` is
        not specified, the first 100 rows of the XFrame are used to make a guess
        of the target data type.

        Parameters
        ----------
        fn : function
            The function to transform each row of the XFrame. The return
            type should be convertible to `dtype` if `dtype` is not None.

        dtype : data type, optional
            The `dtype` of the new XArray. If None, the first 100
            elements of the array are used to guess the target
            data type.

        use_columns : str | list[str], optional
            The column or list of columns to be supplied in the row passed to the function.
            If not given, all columns wll be used to build the row.

        seed : int, optional
            Used as the seed if a random number generator is included in `fn`.

        Returns
        -------
        :class:`.XArray`
            The XArray transformed by fn.  Each element of the XArray is of
            type `dtype`

        Examples
        --------
        Concatenate strings from several columns:

        >>> xf = xframes.XFrame({'user_id': [1, 2, 3], 'movie_id': [3, 3, 6],
                                  'rating': [4, 5, 1]})
        >>> xf.apply(lambda x: str(x['user_id']) + str(x['movie_id']) + str(x['rating']))
        dtype: str
        Rows: 3
        ['134', '235', '361']
        """
        if not inspect.isfunction(fn):
            raise TypeError('Fn must be a function.')
        if isinstance(use_columns, basestring):
            use_columns = [use_columns]
        rows = self._impl.head_as_list(10)
        names = self._impl.column_names()
        if use_columns:
            col_indexes = [self.column_names().index(col) for col in use_columns]
            rows = [[row[i] for i in col_indexes] for row in rows]
            names = [name for name in names if name in use_columns]
        if dtype is None:
            dryrun = [fn(dict(zip(names, row))) for row in rows]
            dtype = infer_type_of_list(dryrun)

        if not seed:
            seed = int(time.time())

        if not use_columns:
            use_columns = self.column_names()

        return XArray(impl=self._impl.apply(fn, dtype, use_columns, seed))

    def transform_col(self, col, fn=None, dtype=None, use_columns=None, seed=None):
        """
        Transform a single column according to a specified function.
        The remaining columns are not modified.
        The type of the transformed column types becomes `dtype`, with
        the new value being the result of `fn(x)`, where `x` is a single row in
        the XFrame represented as a dictionary.  The `fn` should return
        exactly one value which can be cast into type `dtype`. If `dtype` is
        not specified, the first 100 rows of the XFrame are used to make a guess
        of the target data type.

        Parameters
        ----------
        col : string
            The name of the column to transform.

        fn : function, optional
            The function to transform each row of the XFrame. The return
            type should be convertible to `dtype` if `dtype` is not None.
            If the function is not given, an identity function is used.

        dtype : dtype, optional
            The column data type of the new XArray. If None, the first 100
            elements of the array are used to guess the target
            data type.

        use_columns : str | list[str], optional
            The column or list of columns to be supplied in the row passed to the function.
            If not given, all columns wll be used to build the row.

        seed : int, optional
            Used as the seed if a random number generator is included in `fn`.

        Returns
        -------
        :class:`.XFrame`
            An XFrame with the given column transformed by the function and cast to the given type.

        Examples
        --------
        Translate values in a column:

        >>> xf = xframes.XFrame({'user_id': [1, 2, 3], 'movie_id': [3, 3, 6],
                                  'rating': [4, 5, 1]})
        >>> xf.transform_col('rating', lambda row: row['rating'] * 2)


        Cast values in a column to a different type

        >>> xf = xframes.XFrame({'user_id': [1, 2, 3], 'movie_id': [3, 3, 6],
                                  'rating': [4, 5, 1]})
        >>> xf.transform_col('user_id', dtype=str)

        """
        names = self._impl.column_names()
        if col not in names:
            raise ValueError('Column name must be in XFrame')
        if fn is None:
            def fn(row):
                return row[col]
        elif not inspect.isfunction(fn):
            raise TypeError('Input must be a function.')
        if isinstance(use_columns, basestring):
            use_columns = [use_columns]
        rows = self._impl.head_as_list(10)
        if use_columns:
            col_indexes = [self.column_names().index(col_name) for col_name in use_columns]
            rows = [[row[i] for i in col_indexes] for row in rows]
            names = [name for name in names if name in use_columns]
        if dtype is None:
            dryrun = [fn(dict(zip(names, row))) for row in rows]
            dtype = infer_type_of_list(dryrun)
        if not seed:
            seed = int(time.time())

        if not use_columns:
            use_columns = self.column_names()

        return XFrame(impl=self._impl.transform_col(col, fn, dtype, use_columns, seed))

    # noinspection PyTypeChecker
    def transform_cols(self, cols, fn=None, dtypes=None, use_columns=None, seed=None):
        """
        Transform multiple columns according to a specified function.
        The remaining columns are not modified.
        The type of the transformed column types are given by  `dtypes`, with
        the new values being the result of `fn(x)` where `x` is a single row in
        the XFrame represented as a dictionary.  The `fn` should return
        a value for each element of cols, which can be cast into the corresponding `dtype`.
        If `dtypes` is not specified, the first 100 rows of the XFrame are
        used to make a guess of the target data types.

        Parameters
        ----------
        cols : list [str]
            The names of the column to transform.

        fn : function, optional
            The function to transform each row of the XFrame. The return
            value should be a list of values, one for each column of cols.
            each type should be convertible to the corresponding `dtype` if `dtype` is not None.
            If the function is not given, an identity function is used.

        dtypes : list[type], optional
            The data types of the new columns. There must be one data type
            for each column in cols.  If not supplied, the first 100
            elements of the array are used to guess the target
            data types.

        use_columns : str | list[str], optional
            The column or list of columns to be supplied in the row passed to the function.
            If not given, all columns wll be used to build the row.

        seed : int, optional
            Used as the seed if a random number generator is included in `fn`.

        Returns
        -------
        :class:`.XFrame`
            An XFrame with the given columns transformed by the function and cast to the given types.

        Examples
        --------
        Translate values in a column:

        >>> xf = xframes.XFrame({'user_id': [1, 2, 3], 'movie_id': [3, 3, 6],
                                  'rating': [4, 5, 1]})
        >>> xf.transform_col(['movie_id', 'rating'], lambda row: [row['movie_id'] + 1, row['rating'] * 2])


        Cast types in several columns:

        >>> xf = xframes.XFrame({'user_id': [1, 2, 3], 'movie_id': [3, 3, 6],
                                  'rating': [4, 5, 1]})
        >>> xf.transform_col(['movie_id', 'rating'], dtype=[str, str])

        """
        if fn is None:
            def fn(row):
                return [row[col] for col in cols]
        elif not inspect.isfunction(fn):
            raise TypeError('Input must be a function: {}: {}.'.format(fn, type(fn).__name__))
        if dtypes is None:
            rows = self._impl.head_as_list(10)
            names = self._impl.column_names()
            if use_columns:
                col_indexes = [self.column_names().index(col_name) for col_name in use_columns]
                rows = [[row[i] for i in col_indexes] for row in rows]
                names = [name for name in names if name in use_columns]
            # do the dryrun so we can get column types
            dryrun = [fn(dict(zip(names, row))) for row in rows]

            if len(dryrun[0]) != len(cols):
                raise ValueError('Function return length must match number of cols.')
            dtypes = []
            for index in range(0, len(cols)):
                dryrun_col = [row[index] for row in dryrun]
                dtypes.append(infer_type_of_list(dryrun_col))
        else:
            if len(cols) != len(dtypes):
                raise ValueError('Length of cols and dtypes must match.')
        if not seed:
            seed = int(time.time())

        if not use_columns:
            use_columns = self.column_names()

        return XFrame(impl=self._impl.transform_cols(cols, fn, dtypes, use_columns, seed))

    def detect_type(self, column_name):
        """
        If the column is of string type, and the values can safely be cast to int or float, then
        return the type to be cast to.  Uses the entire column to detect the type.

        Parameters
        ----------
        column_name : str
            The name of the column to cast.

        Returns
        -------
        type
            int or float: The column can be cast to this type.

            str: The column cannot be cast to one of the types above.

        Examples
        --------

        >>> xf = xpatterns.XFrame({'value': ['1', '2', '3']})
        >>> xf.detect_type('value')

        """
        column = self.__getitem__(column_name)
        if not issubclass(column.dtype(), str):
            return str

        def classify_type(s):
            if not isinstance(s, basestring):
                return 'Expected str, got {}: {}'.format(type(s).__name__, s)
            if len(s) == 0:
                return ''
            if s.startswith('-'):
                s = s[1:]
            try:
                dt = date_parser.parse(s, default=datetime.datetime(1, 1, 1, 0, 0, 0))
                if not s.isdigit() and dt.year != 1:
                    return 'datetime'
            except ValueError:
                pass
            except OverflowError:
                pass
            if s.isdigit():
                return 'int'
            if s.replace('.', '', 1).isdigit():
                return 'float'
            if s.startswith('[') or s.startswith('{'):
                val = ast.literal_eval(s)
                if isinstance(val, list) or isinstance(val, dict):
                    return type(val).__name__
            return 'str'

        types = list(column.apply(classify_type).unique())
        if 'str' in types:
            return str

        if '' in types:
            types.remove('')

        if len(types) == 1 and types[0] == 'datetime':
            return datetime.datetime

        if len(types) == 1 and types[0] == 'list':
            return list

        if len(types) == 1 and types[0] == 'dict':
            return dict

        if 'datetime' in types:
            types.remove('datetime')

        if len(types) == 2 and 'float' in types and 'int' in types:
            return float
        if len(types) == 1 and types[0] == 'int':
            return int
        if len(types) == 1 and types[0] == 'float':
            return float

        return str

    def detect_type_and_cast(self, column_name):
        """
        If the column is of string type, and the values can all be interpreted as
        integer or float values, then cast the column to the numerical type.
        Otherwise, returns a copy of the XFrame.

        Parameters
        ----------
        column_name : str
            The name of the column to cast.

        Examples
        --------

        >>> xf = xpatterns.XFrame({'value': ['1', '2', '3']})
        >>> xf.detect_type_and_cast('value')

        """
        new_type = self.detect_type(column_name)
        if new_type is None:
            return self

        def cast_int(row):
            val = row[column_name]
            if val is None:
                return [None]
            if len(val) == 0:
                return [None]
            try:
                return [int(val)]
            except ValueError:
                raise ValueError('Cast failed: (int) {}'.format(val))

        def cast_float(row):
            val = row[column_name]
            if val is None:
                return [None]
            if len(val) == 0:
                return [None]
            try:
                return [float(val)]
            except ValueError:
                raise ValueError('Cast failed: (float) {}'.format(val))

        def cast_datetime(row):
            val = row[column_name]
            if val is None:
                return [None]
            if len(val) == 0:
                return [None]
            try:
                dt = date_parser.parse(val)
                return [dt]
            except ValueError:
                raise ValueError('Cast failed: (datetime) {}'.format(val))

        def cast_list(row):
            val = row[column_name]
            if val is None:
                return [None]
            if len(val) == 0:
                return [None]
            try:
                lst = ast.literal_eval(val)
                return [lst]
            except ValueError:
                raise ValueError('Cast failed: (list) {}'.format(val))

        def cast_dict(row):
            val = row[column_name]
            if val is None:
                return [None]
            if len(val) == 0:
                return [None]
            try:
                dct = ast.literal_eval(val)
                return [dct]
            except ValueError:
                raise ValueError('Cast failed: (dict) {}'.format(val))

        if new_type is int:
            return XFrame(impl=self._impl.transform_cols([column_name], cast_int, [int], None, 0))
        if new_type is float:
            return XFrame(impl=self._impl.transform_cols([column_name], cast_float, [float], None, 0))
        if new_type is list:
            return XFrame(impl=self._impl.transform_cols([column_name], cast_list, [list], None, 0))
        if new_type is dict:
            return XFrame(impl=self._impl.transform_cols([column_name], cast_dict, [dict], None, 0))
        if new_type is datetime.datetime:
            return XFrame(impl=self._impl.transform_cols([column_name], cast_datetime, [datetime.datetime], None, 0))

        return self

    def flat_map(self, column_names, fn, column_types='auto', use_columns=None, seed=None):
        """
        Map each row of the XFrame to multiple rows in a new XFrame via a
        function.

        The output of `fn` must have type ``list[list[...]]``.  Each inner list
        will be a single row in the new output, and the collection of these
        rows within the outer list make up the data for the output XFrame.
        All rows must have the same length and the same order of types to
        make sure the result columns are homogeneously typed.  For example, if
        the first element emitted into the outer list by `fn` is
        ``[43, 2.3, 'string']``, then all other elements emitted into the outer
        list must be a list with three elements, where the first is an `int`,
        second is a `float`, and third is a `string`.  If `column_types` is not
        specified, the first 10 rows of the XFrame are used to determine the
        column types of the returned XFrame.

        Parameters
        ----------
        column_names : list[str]
            The column names for the returned XFrame.

        fn : function
            The function that maps each of the XFrame rows into multiple rows,
            returning ``list[list[...]]``.  All output rows must have the same
            length and order of types.  The function is passed a dictionary
            of column name: value for each row.

        column_types : list[type], optional
            The column types of the output XFrame. Default value
            will be automatically inferred by running `fn` on the first
            10 rows of the output.

        use_columns : str | list[str], optional
            The column or list of columns to be supplied in the row passed to the function.
            If not given, all columns wll be used to build the row.

        seed : int, optional
            Used as the seed if a random number generator is included in `fn`.

        Returns
        -------
        :class:`.XFrame`
            A new XFrame containing the results of the ``flat_map`` of the
            original XFrame.

        Examples
        ---------
        Repeat each row according to the value in the 'number' column.

        >>> xf = xframes.XFrame({'letter': ['a', 'b', 'c'],
        ...                       'number': [1, 2, 3]})
        >>> xf.flat_map(['number', 'letter'],
        ...             lambda x: [list(x.itervalues()) for _ in range(0, x['number'])])
        +--------+--------+
        | number | letter |
        +--------+--------+
        |   1    |   a    |
        |   2    |   b    |
        |   2    |   b    |
        |   3    |   c    |
        |   3    |   c    |
        |   3    |   c    |
        +--------+--------+
        [6 rows x 2 columns]
        """
        if not inspect.isfunction(fn):
            raise TypeError('Input must be a function')
        if not seed:
            seed = int(time.time())
        if isinstance(use_columns, basestring):
            use_columns = [use_columns]

        # determine the column_types
        if column_types == 'auto':
            types = set()
            rows = self._impl.head_as_list(10)
            names = self._impl.column_names()
            if use_columns:
                rows = [{k: v for k, v in row.iteritems() if k in use_columns} for row in rows]
                names = [name for name in names if name in use_columns]
            results = [fn(dict(zip(names, row))) for row in rows]
            if not (results is None or isinstance(results, list)):
                raise TypeError('Output type of the lambda function must be a list of lists.')
            else:
                for rows in results:
                    if not isinstance(rows, list):
                        raise TypeError('Output type of the lambda function must be a list of lists.')
                    for row in rows:
                        if not isinstance(row, list):
                            raise TypeError('Output type of the lambda function must be a list of lists.')
                        types.add(tuple([type(v) for v in row]))
            if len(types) != 1:
                raise TypeError('Mapped rows must have the same length and types.')

            column_types = list(types.pop())

        if not use_columns:
            use_columns = self.column_names()

        if not isinstance(column_types, list):
            raise TypeError('Column_types must be a list: {} {}.'.format(type(column_types).__name__, column_types))
        if not len(column_types) == len(column_names):
            raise ValueError('Number of output columns must match the size of column names.')
        return XFrame(impl=self._impl.flat_map(fn, column_names, column_types, use_columns, seed))

    def sample(self, fraction, max_partitions=None, seed=None):
        """
        Sample the current XFrame's rows.

        Parameters
        ----------
        fraction : float
            Approximate fraction of the rows to fetch. Must be between 0 and 1.
            The number of rows returned is approximately the fraction times the
            number of rows.

        max_partitions : int, optional
            After sampling, coalesce to this number of partition.  If not given,
            do not perform this step.

        seed : int, optional
            Seed for the random number generator used to sample.

        Returns
        -------
        :class:`.XFrame`
            A new XFrame containing sampled rows of the current XFrame.

        Examples
        --------
        Suppose we have an XFrame with 6,145 rows.

        >>> import random
        >>> xf = XFrame({'id': range(0, 6145)})

        Retrieve about 30% of the XFrame rows with repeatable results by
        setting the random seed.

        >>> len(xf.sample(.3, seed=5))
        1783
        """
        if not seed:
            seed = int(time.time())

        if fraction > 1 or fraction < 0:
            raise ValueError('Invalid sampling rate: {}.'.format(fraction))

        if self.num_rows() == 0 or self.num_columns() == 0:
            return XFrame(impl=self._impl.copy())
        else:
            return XFrame(impl=self._impl.sample(fraction, max_partitions, seed))

    def random_split(self, fraction, seed=None):
        """
        Randomly split the rows of an XFrame into two XFrames.
        The first XFrame
        contains *M* rows, sampled uniformly (without replacement) from the
        original XFrame. *M* is approximately the fraction times the original
        number of rows. The second XFrame contains the remaining rows of the
        original XFrame.

        Parameters
        ----------
        fraction : float
            Approximate fraction of the rows to fetch for the first returned
            XFrame. Must be between 0 and 1.

        seed : int, optional
            Seed for the random number generator used to split.

        Returns
        -------
        tuple [:class:`.XFrame`]
            Two new XFrame.

        Examples
        --------
        Suppose we have an XFrame with 6,145 rows and we want to randomly split
        it into training and testing datasets with about a 70%/30% split.

        >>> xf = xframes.XFrame({'id': range(1024)})
        >>> xf_train, xf_test = xf.random_split(.9, seed=5)
        >>> print len(xf_test), len(xf_train)
        102 922
        """
        if fraction > 1 or fraction < 0:
            raise ValueError('Invalid sampling rate: {}.'.format(fraction))
        if self.num_rows() == 0 or self.num_columns() == 0:
            return XFrame(), XFrame()

        if not seed:
            seed = int(time.time())

        # The server side requires this to be an int, so cast if we can
        try:
            seed = int(seed)
        except ValueError:
            raise ValueError("The 'seed' parameter must be of type int.")

        impl_pair = self._impl.random_split(fraction, seed)
        return XFrame(data=[], impl=impl_pair[0]), XFrame(data=[], impl=impl_pair[1])

    def topk(self, column_name, k=10, reverse=False):
        """
        Get k rows according to the largest values in the given column. Result is
        sorted by `column_name` in the given order (default is descending).
        When `k` is small, `topk` is more efficient than `sort`.

        Parameters
        ----------
        column_name : string
            The column to sort on

        k : int, optional
            The number of rows to return

        reverse : bool, optional
            If True, return the top k rows in ascending order, otherwise, in
            descending order.

        Returns
        -------
        :class:`.XFrame`
            An XFrame containing the top k rows sorted by column_name.

        See Also
        --------
        xframes.XFrame.sort

        Examples
        --------
        >>> xf = xframes.XFrame({'id': range(1000)})
        >>> xf['value'] = -xf['id']
        >>> xf.topk('id', k=3)
        +--------+--------+
        |   id   |  value |
        +--------+--------+
        |   999  |  -999  |
        |   998  |  -998  |
        |   997  |  -997  |
        +--------+--------+
        [3 rows x 2 columns]

        >>> xf.topk('value', k=3)
        +--------+--------+
        |   id   |  value |
        +--------+--------+
        |   1    |  -1    |
        |   2    |  -2    |
        |   3    |  -3    |
        +--------+--------+
        [3 rows x 2 columns]
        """
        if not isinstance(column_name, str):
            raise TypeError('Column_name must be a string.')

        xf = self[self[column_name].topk_index(topk=k, reverse=reverse)]
        return xf.sort(column_name, ascending=reverse)

    # noinspection PyShadowingBuiltins
    def save(self, filename, format=None):
        """
        Save the XFrame to a file system for later use.

        Parameters
        ----------
        filename : string
            The location to save the XFrame. Either a local directory or a
            remote URL. If the format is 'binary', a directory will be created
            at the location which will contain the XFrame.

        format : {'binary', 'csv', 'tsv', 'parquet', json}, optional
            Format in which to save the XFrame. Binary saved XFrames can be
            loaded much faster and without any format conversion losses. If not
            given, will try to infer the format from filename given. If file
            name ends with 'csv' or '.csv.gz', then save as 'csv' format.
            If the file ends with 'json', then save as json file.
            If the file ends with 'parquet', then save as parquet file.
            Otherwise save as 'binary' format.

        See Also
        --------
        xframes.XFrame.load
        xframes.XFrame.XFrame

        Examples
        --------
        >>> # Save the xframe into binary format
        >>> xf.save('data/training_data_xframe')

        >>> # Save the xframe into csv format
        >>> xf.save('data/training_data.csv', format='csv')
        """

        if format is None:
            if filename.endswith(('.csv', '.csv.gz')):
                format = 'csv'
            elif filename.endswith(('.tsv', '.tsv.gz')):
                format = 'tsv'
            elif filename.endswith('.parquet'):
                format = 'parquet'
            elif filename.endswith('.json'):
                format = 'json'
            else:
                format = 'binary'
        else:
            if format == 'csv':
                if not filename.endswith(('.csv', '.csv.gz')):
                    filename += '.csv'
            elif format == 'tsv':
                if not filename.endswith(('.tsv', '.tsv.gz')):
                    filename += '.tsv'
            elif format == 'json':
                if not filename.endswith('.json'):
                    filename += '.json'
            elif format == 'parquet':
                if not filename.endswith('.parquet'):
                    filename += '.parquet'
            elif format != 'binary':
                raise ValueError("Invalid format: {}. Supported formats are " +
                                 "'csv', 'tsv', 'parquet', 'json', and 'binary'."
                                 .format(format))

        # Save the XFrame
        url = make_internal_url(filename)
        check_output_uri(url)

        if format == 'binary':
            self._impl.save(url)

        elif format == 'csv':
            if not filename.endswith(('.csv', '.csv.gz')):
                raise ValueError('File name must end with .csv or .csv.gz.')
            self._impl.save_as_csv(url)
        elif format == 'tsv':
            if not filename.endswith(('.tsv', '.tsv.gz')):
                raise ValueError('File name must end with .tsv or .tsv.gz.')
            self._impl.save_as_csv(url, delimiter='\t')
        elif format == 'json':
            if not filename.endswith('.json'):
                raise ValueError('File name must end with .json.')
            self._impl.save_as_json(url, number_of_partitions=8)
        elif format == 'parquet':
            if not filename.endswith('.parquet'):
                raise ValueError('File name must end with .parquet.')
            self._impl.save_as_parquet(url, number_of_partitions=8)
        else:
            raise ValueError('Unsupported format: {}.'.format(format))

    def save_as_parquet(self, filename, column_names=None, column_type_hints=None):
        url = make_internal_url(filename)
        check_output_uri(url)
        self._impl.save_as_parquet(url,
                                   column_names=column_names,
                                   column_type_hints=column_type_hints,
                                   number_of_partitions=8)

    def select_column(self, column_name):
        """
        Return an  XArray that corresponds with
        the given column name. Throws an exception if the column name is something other than a
        string or if the column name is not found.

        Subscripting an XFrame by a column name is equivalent to this function.

        Parameters
        ----------
        column_name : str
            The column name.

        Returns
        -------
        :class:`.XArray`
            The XArray that is referred by `column_name`.

        See Also
        --------
        xframes.XFrame.select_columns
            Returns multiple columns.

        Examples
        --------
        >>> xf = xframes.XFrame({'user_id': [1,2,3],
        ...                       'user_name': ['alice', 'bob', 'charlie']})
        >>> # This line is equivalent to `sa = xf['user_name']`
        >>> sa = xf.select_column('user_name')
        >>> sa
        dtype: str
        Rows: 3
        ['alice', 'bob', 'charlie']
        """
        if not isinstance(column_name, str):
            raise TypeError('Invalid column_name type must be str.')
        return XArray(data=[], impl=self._impl.select_column(column_name))

    def select_columns(self, keylist):
        """
        Get XFrame composed only of the columns referred to in the given list of
        keys. Throws an exception if ANY of the keys are not in this XFrame or
        if `keylist` is anything other than a list of strings.

        Parameters
        ----------
        keylist : list[str]
            The list of column names.

        Returns
        -------
        :class:`.XFrame`
            A new XFrame that is made up of the columns referred to in
            `keylist` from the current XFrame.  The order of the columns
            is preserved.

        See Also
        --------
        xframes.XFrame.select_column
            Returns a single column.

        Examples
        --------
        >>> xf = xframes.XFrame({'user_id': [1,2,3],
        ...                       'user_name': ['alice', 'bob', 'charlie'],
        ...                       'zipcode': [98101, 98102, 98103]
        ...                      })
        >>> # This line is equivalent to `xf2 = xf[['user_id', 'zipcode']]`
        >>> xf2 = xf.select_columns(['user_id', 'zipcode'])
        >>> xf2
        +---------+---------+
        | user_id | zipcode |
        +---------+---------+
        |    1    |  98101  |
        |    2    |  98102  |
        |    3    |  98103  |
        +---------+---------+
        [3 rows x 2 columns]
        """
        if not hasattr(keylist, '__iter__'):
            raise TypeError('Keylist must be an iterable.')
        if not all([isinstance(x, str) for x in keylist]):
            raise TypeError('Invalid key type: must be str.')

        key_set = set(keylist)
        if len(key_set) != len(keylist):
            for key in key_set:
                if keylist.count(key) > 1:
                    raise ValueError("There are duplicate keys in key list: '{}'.".format(key))

        return XFrame(data=[], impl=self._impl.select_columns(keylist))

    def add_column(self, col, name=''):
        """
        Add a column to this XFrame. The length of the new column
        must match the length of the existing XFrame. This
        operation returns a new XFrame with the additional columns.
        If no `name` is given, a default name is chosen.

        Parameters
        ----------
        col : :class:`.XArray`
            The 'column' of data to add.

        name : string, optional
            The name of the column. If no name is given, a default name is
            chosen.

        Returns
        -------
        :class:`.XFrame`
            A new XFrame with the new column.

        See Also
        --------
        xframes.XFrame.add_columns
            Adds multiple columns.

        Examples
        --------
        >>> xf = xframes.XFrame({'id': [1, 2, 3], 'val': ['A', 'B', 'C']})
        >>> xa = xframes.XArray(['cat', 'dog', 'fossa'])
        >>> # This line is equivalant to `xf['species'] = xa`
        >>> xf2 = xf.add_column(xa, name='species')
        >>> xf2
        +----+-----+---------+
        | id | val | species |
        +----+-----+---------+
        | 1  |  A  |   cat   |
        | 2  |  B  |   dog   |
        | 3  |  C  |  fossa  |
        +----+-----+---------+
        [3 rows x 3 columns]
        """
        # Check type for pandas dataframe or XArray?
        if not isinstance(col, XArray):
            raise TypeError('Must give column as XArray.')
        if not isinstance(name, str):
            raise TypeError('Invalid column name: must be str.')
        return XFrame(impl=self._impl.add_column(col.impl(), name))

    def add_columns(self, cols, names=None):
        """
        Adds multiple columns to this XFrame. The length of the new columns
        must match the length of the existing XFrame. This
        operation returns a new XFrame with the additional columns.

        Parameters
        ----------
        cols : :class:`.XArray` or list of :class:`.XArray` or :class:`XFrame`
            The columns to add.  If `cols` is an XFrame, all columns in it are added.

        names : string or list of string, optional
            If cols is an XArray, then the name of the column. If no name is given, a default name is
            chosen.
            If cols is a list of :class:`.XArray`, then a list of column names. 
            All names must be specified. 
            `Namelist` is ignored if `cols` is an XFrame.  
            If there are columns with duplicate names, they
            will be made unambiguous by adding .1 to the second copy.

        Returns
        -------
        :class:`.XFrame`
            The XFrame with additional columns.

        See Also
        --------
        xframes.XFrame.add_column
            Adds one column

        Examples
        --------
        >>> xf = xframes.XFrame({'id': [1, 2, 3], 'val': ['A', 'B', 'C']})
        >>> xa = xframes.XArray(['cat', 'dog', 'fossa'])
        >>> # This line is equivalant to `xf['species'] = xa`
        >>> xf2 = xf.add_columns(xa, names='species')
        >>> xf2
        +----+-----+---------+
        | id | val | species |
        +----+-----+---------+
        | 1  |  A  |   cat   |
        | 2  |  B  |   dog   |
        | 3  |  C  |  fossa  |
        +----+-----+---------+
        [3 rows x 3 columns]

        >>> xf = xframes.XFrame({'id': [1, 2, 3], 'val': ['A', 'B', 'C']})
        >>> xf2 = xframes.XFrame({'species': ['cat', 'dog', 'horse'],
        ...                        'age': [3, 5, 9]})
        >>> xf3 = xf.add_columns(xf2)
        >>> xf3
        +----+-----+-----+---------+
        | id | val | age | species |
        +----+-----+-----+---------+
        | 1  |  A  |  3  |   cat   |
        | 2  |  B  |  5  |   dog   |
        | 3  |  C  |  9  |  horse  |
        +----+-----+-----+---------+
        [3 rows x 4 columns]
        """
        if isinstance(cols, XFrame):
            return XFrame(impl=self._impl.add_columns_frame(cols._impl))
        if isinstance(cols, XArray):
            if not isinstance(names, str):
                raise TypeError('Invalid column name: must be str.')
            return XFrame(impl=self._impl.add_column(cols.impl(), names))
        else:
            if not hasattr(cols, '__iter__'):
                raise TypeError('Column list must be an iterable.')
            if not hasattr(names, '__iter__'):
                raise TypeError('Namelist must be an iterable.')

        if not all([isinstance(x, XArray) for x in cols]):
            raise TypeError('Must give column as XArray.')
        if not all([isinstance(x, str) for x in names]):
            raise TypeError("Invalid column name in list : must all be str.")
        if len(names) != len(cols):
            raise ValueError('Namelist length mismatch.')

        cols_impl = [col.impl() for col in cols]
        return XFrame(impl=self._impl.add_columns_array(cols_impl, names))

    def replace_column(self, name, col):
        """
        Replace a column in this XFrame. The length of the new column
        must match the length of the existing XFrame. This
        operation returns a new XFrame with the replacement column.

        Parameters
        ----------
        name : string
            The name of the column.

        col : :class:`.XArray`
            The 'column' to add.

        Returns
        -------
        :class:`.XFrame`
            A new XFrame with specified column replaced.


        Examples
        --------
        >>> xf = xframes.XFrame({'id': [1, 2, 3], 'val': ['A', 'B', 'C']})
        >>> xa = xframes.XArray(['cat', 'dog', 'horse'])
        >>> xf2 = xf.replace_column('val', xa)
        >>> xf2
        +----+---------+
        | id | species |
        +----+---------+
        | 1  |   cat   |
        | 2  |   dog   |
        | 3  |  horse  |
        +----+---------+
        [3 rows x 2 columns]
        """
        # Check type for pandas dataframe or XArray?
        if not isinstance(col, XArray):
            raise TypeError('Must give column as XArray.')
        if not isinstance(name, str):
            raise TypeError('Invalid column name: must be str.')
        if name not in self.column_names():
            raise ValueError('Column name must be in XFrame.')
        return XFrame(impl=self._impl.replace_selected_column(name, col.impl()))

    def remove_column(self, name):
        """
        Remove a column or more columns from this XFrame. This
        operation returns a new XFrame with the given column removed.

        Parameters
        ----------
        name : string or list or iterable
            The name of the column to remove.
            If a list or iterable is given, all the named columns are removed.

        Returns
        -------
        :class:`.XFrame`
            A new XFrame with given column or columns removed.

        Examples
        --------
        >>> xf = xframes.XFrame({'id': [1, 2, 3], 'val': ['A', 'B', 'C']})
        >>> xf2 = xf.remove_column('val')
        >>> xf2
        +----+
        | id |
        +----+
        | 1  |
        | 2  |
        | 3  |
        +----+
        [3 rows x 1 columns]
        
        >>> xf = xframes.XFrame({'id': [1, 2, 3], 'val1': ['A', 'B', 'C'], 'val2': [10, 11, 12]})
        >>> xf2 = xf.remove_column(['val1', 'val2'])
        >>> xf2
        +----+
        | id |
        +----+
        | 1  |
        | 2  |
        | 3  |
        +----+
        [3 rows x 1 columns]
        """
        if isinstance(name, basestring):
            column_names = [name]
        else:
            column_names = name
        for name in column_names:
            if name not in self.column_names():
                raise KeyError("Cannot find column '{}'.".format(name))
        return XFrame(impl=self._impl.remove_columns(column_names))

    def remove_columns(self, column_names):
        """
        Removes one or more columns from this XFrame. This
        operation returns a new XFrame with the given columns removed.

        Parameters
        ----------
        column_names : list or iterable
            A list or iterable of the column names.

        Returns
        -------
        :class:`.XFrame`
            A new XFrame with given columns removed.

        Examples
        --------
        >>> xf = xframes.XFrame({'id': [1, 2, 3], 'val1': ['A', 'B', 'C'], 'val2': [10, 11, 12]})
        >>> xf2 = xf.remove_columns(['val1', 'val2'])
        >>> xf2
        +----+
        | id |
        +----+
        | 1  |
        | 2  |
        | 3  |
        +----+
        [3 rows x 1 columns]
        """
        if not hasattr(column_names, '__iter__'):
            raise TypeError('Column_names must be an iterable.')
        for name in column_names:
            if name not in self.column_names():
                raise KeyError("Cannot find column '{}'.".format(name))
        return XFrame(impl=self._impl.remove_columns(column_names))

    def swap_columns(self, column_1, column_2):
        """
        Swap the columns with the given names. This
        operation returns a new XFrame with the given columns swapped.

        Parameters
        ----------
        column_1 : string
            Name of column to swap

        column_2 : string
            Name of other column to swap

        Returns
        -------
        :class:`.XFrame`
            A new XFrame with specified columns swapped.

        Examples
        --------
        >>> xf = xframes.XFrame({'id': [1, 2, 3], 'val': ['A', 'B', 'C']})
        >>> xf2 = xf.swap_columns('id', 'val')
        >>> xf2
        +-----+-----+
        | val | id  |
        +-----+-----+
        |  A  |  1  |
        |  B  |  2  |
        |  C  |  3  |
        +----+-----+
        [3 rows x 2 columns]
        """
        if column_1 not in self.column_names():
            raise KeyError("Cannot find column '{}'.".format(column_1))
        if column_2 not in self.column_names():
            raise KeyError("Cannot find column '{}'.".format(column_2))

        return XFrame(impl=self._impl.swap_columns(column_1, column_2))

    def reorder_columns(self, column_names):
        """
        Reorder the columns in the table.  This
        operation returns a new XFrame with the given columns reordered.

        Parameters
        ----------
        column_names : list of string
            Names of the columns in desired order.

        Returns
        -------
        :class:`.XFrame`
            A new XFrame with reordered columns.

        See Also
        --------
        xframes.XFrame.select_columns
            Returns a subset of the columns but does not change the column order.

        Examples
        --------
        >>> xf = xframes.XFrame({'id': [1, 2, 3], 'val': ['A', 'B', 'C']})
        >>> xf2 = xf.reorder_columns(['val', 'id'])
        >>> xf2
        +-----+-----+
        | val | id  |
        +-----+-----+
        |  A  |  1  |
        |  B  |  2  |
        |  C  |  3  |
        +----+------+
        [3 rows x 2 columns]
        """
        if not hasattr(column_names, '__iter__'):
            raise TypeError('Keylist must be an iterable.')
        for col in column_names:
            if col not in self.column_names():
                raise KeyError("Cannot find column '{}'.".format(col))
        for col in self.column_names():
            if col not in column_names:
                raise KeyError("Column '{}' not assigned'.".format(col))

        return XFrame(impl=self._impl.reorder_columns(column_names))

    def rename(self, names):
        """
        Rename the given columns. `Names` can be a dict specifying
        the old and new names. This changes the names of the columns given as
        the keys and replaces them with the names given as the values.  Alternatively,
        `names` can be a list of the new column names.  In this case it must be
        the same length as the number of columns.  This
        operation returns a new XFrame with the given columns renamed.

        Parameters
        ----------
        names : dict [string, string] | list [ string ]
            Dictionary of [old_name, new_name] or list of new names

        Returns
        -------
        :class:`.XFrame`
            A new XFrame with columns renamed.

        See Also
        --------
        xframes.XFrame.column_names

        Examples
        --------
        >>> xf = XFrame({'X.1': ['Alice','Bob'],
        ...              'X.2': ['123 Fake Street','456 Fake Street']})
        >>> xf2 = xf.rename({'X.1': 'name', 'X.2':'address'})
        >>> xf2
        +-------+-----------------+
        |  name |     address     |
        +-------+-----------------+
        | Alice | 123 Fake Street |
        |  Bob  | 456 Fake Street |
        +-------+-----------------+
        [2 rows x 2 columns]
        """
        if not isinstance(names, (list, dict)):
            raise TypeError('Names must be a dictionary: oldname -> newname or a list of newname ({}).'
                            .format(type(names).__name__))
        if isinstance(names, dict):
            new_names = copy.copy(self.column_names())
            for k in names:
                if k not in self.column_names():
                    raise ValueError("Cannot find column '{}' in the XFrame.".format(k))
                index = self.column_names().index(k)
                new_names[index] = names[k]
        else:
            new_names = names
            if len(new_names) != len(self.column_names()):
                raise ValueError('Names must be the same length as the number of columns (names: {} columns: {}).'
                                 .format(len(new_names), len(self.column_names())))
        return XFrame(impl=self._impl.replace_column_names(new_names))

    def __getitem__(self, key):
        """
        This provides XFrame "indexing", for examle xf['column_name'].
        The type of the index determine what the construct does: electing a column,
        doing a logical filter, or returning one or more rows from the XFrame.

        This method does things based on the type of `key`.

        If `key` is:
            * str
              Calls `select_column` on `key` to return a single column as an XArray.
            * XArray
              Performs a logical filter.  Expects given XArray to be the same
              length as all columns in current XFrame.  Every row
              corresponding with an entry in the given XArray that is
              equivalent to False is filtered from the result.
            * int
              Returns a single row of the XFrame (the `key`th one) as a dictionary.
            * slice
              Returns an XFrame including only the sliced rows.

        Examples
        --------
        >>> xf = xframes.XFrame({'id': [4, 6, 8], 'val': ['D', 'F', 'H']})
        >>> xf
        """
        if isinstance(key, XArray):
            return self.select_rows(key)
        if isinstance(key, list):
            return self.select_columns(key)
        if isinstance(key, str):
            return self.select_column(key)
        if isinstance(key, unicode):
            return self.select_column(str(key))
        if isinstance(key, int):
            if key < 0:
                key += len(self)
            if key >= len(self):
                raise IndexError('XFrame index out of range (too high).')
            res = list(XFrame(impl=self._impl.copy_range(key, 1, key + 1)))
            if len(res) == 0:
                raise IndexError('XFrame index out of range (too low).')
            return res[0]
        if isinstance(key, slice):
            start = key.start
            stop = key.stop
            step = key.step
            if start is None:
                start = 0
            if stop is None:
                stop = len(self)
            if step is None:
                step = 1
            # handle negative indices
            if start < 0:
                start += len(self)
            if stop < 0:
                stop += len(self)
            return XFrame(impl=self._impl.copy_range(start, step, stop))

        raise TypeError('Invalid index type: must be XArray, ' +
                        "'int', 'list', slice, or 'str': ({}).".format(type(key).__name__))

    def __setitem__(self, key, value):
        """
        Adds columns and returns the modified XFrame.

        Key can be either a list or a str.  If
        value is an XArray, it is added to the XFrame as a column.  If it is a
        constant value (int, str, or float), then a column is created where
        every entry is equal to the constant value.  Existing columns can also
        be replaced using this wrapper.

        """
        if isinstance(key, list):
            column_list = value
            if isinstance(value, XFrame):
                for name in value.column_names():
                    if name in self.column_names():
                        raise ValueError("Column '{}' already exists in current XFrame.".format(name))
                self._impl.add_columns_frame_in_place(value._impl)
            else:
                if not hasattr(column_list, '__iter__'):
                    raise TypeError('Column list must be an iterable.')
                if not hasattr(key, '__iter__'):
                    raise TypeError('Namelist must be an iterable.')
                if not all([isinstance(x, XArray) for x in column_list]):
                    raise TypeError('Must give column as XArray.')
                if not all([isinstance(x, str) for x in key]):
                    raise TypeError("Invalid column name in list : must all be 'str'.")
                if len(key) != len(column_list):
                    raise ValueError('Namelist length mismatch.')
                cols_impl = [col.impl() for col in column_list]
                self._impl.add_columns_array_in_place(cols_impl, key)
        elif isinstance(key, str):
            if isinstance(value, XArray):
                sa_value = value
            elif hasattr(value, '__iter__'):  # wrap list, array... to xarray
                sa_value = XArray(value)
            else:
                # Special case of adding a const column.
                # It is very inefficient to create a column and then zip it in
                # a) num_rows() is inefficient
                # b) parallelize is inefficient
                # c) partitions differ, so zip --> zipWithIndex, sortByKey, etc
                # Map it in instead
                if not isinstance(value, (int, float, str, array.array, list, dict)):
                    raise TypeError("Cannot create xarray of value type '{}'.".format(type(value).__name__))
                if key not in self.column_names():
                    self._impl.add_column_const_in_place(key, value)
                else:
                    self._impl.replace_column_const_in_place(key, value)
                return

            # set new column
            if key not in self.column_names():
                self._impl.add_column_in_place(sa_value.impl(), key)
            else:
                # special case if replacing the only column.
                # server would fail the replacement if the new column has different
                # length than current one, which doesn't make sense if we are replacing
                # the only column. To support this, we call a different function in the 
                # implementation.
                single_column = (self.num_columns() == 1)
                if single_column:
                    self._impl.replace_single_column_in_place(key, sa_value.impl())
                else:
                    self._impl.replace_selected_column_in_place(key, sa_value.impl())

        else:
            raise TypeError('Cannot set column with key type {}.'.format(type(key).__name__))

    def __delitem__(self, name):
        """
        Removes a column and returns the modified XFrame.
        """
        if name not in self.column_names():
            raise KeyError("Cannot find column '{}'.".format(name))
        self._impl.remove_column_in_place(name)
        return self

    def persist(self, persist_flag):
        """
        Persist or unpersist the underlying data storage object.

        Persisting makes a copy of the object on the disk, so that it does not have to be recomputed in times of
        low memory.  Unpersisting frees up this space.

        Parameters
        ----------
        persist_flag : boolean
            If True, peersist the object.  If False, unpersist it.
        """
        self._impl.persist(persist_flag)

    def _materialize(self):
        """
        For an XFrame that is lazily evaluated, force the persistence of the
        XFrame to disk, committing all lazy evaluated operations.
        """
        self._impl.materialize()

    def _is_materialized(self):
        """
        Returns whether or not the XFrame has been materialized.
        """
        return self._impl.is_materialized()

    def __iter__(self):
        """
        Provides an iterator to the rows of the XFrame.
        """

        def generator():
            # The more we get at a time, the more buffer space it takes.
            # But getting a lot of items takes a lot of time, if we only need a few.
            # Getting more is expensive, because we have to number everything and then
            #  filter out the ones we don't want.  This is a compromise.
            # TODO: start with getting fwer, and if that is not enough, get
            # TODO: a bigger chunk.
            elems_at_a_time = 200000
            self._impl.begin_iterator()
            ret = self._impl.iterator_get_next(elems_at_a_time)
            column_names = self.column_names()
            while True:
                for j in ret:
                    # Iterator returns dictionaries
                    yield dict(zip(column_names, j))

                if len(ret) == elems_at_a_time:
                    ret = self._impl.iterator_get_next(elems_at_a_time)
                else:
                    break

        return generator()

    def range(self, key):
        """
        Extracts and returns rows of the XFrame.

        Parameters
        ----------

        key: int or slice
            If `key` is:
                * int
                  Returns a single row of the XFrame (the `key`th one) as a dictionary.
                * slice
                  Returns an XFrame including only the sliced rows.

        Returns
        -------
        dict or :class:`.XFrame`
            The specified row of the XFrame or
            an XFrame containing the specified rows.

        """
        if isinstance(key, int):
            if key < 0:
                key += len(self)
            if key >= len(self):
                raise IndexError('XFrame index out of range (too high).')
            res = list(XFrame(impl=self._impl.copy_range(key, 1, key + 1)))
            if len(res) == 0:
                raise IndexError('XFrame index out of range (too low).')
            return res[0]
#            return list(XFrame(impl=self._impl.copy_range(key, 1, key + 1)))[0]
        elif isinstance(key, slice):
            start = key.start
            stop = key.stop
            step = key.step
            if start is None:
                start = 0
            if stop is None:
                stop = len(self)
            if step is None:
                step = 1
            # handle negative indices
            if start < 0:
                start += len(self)
            if stop < 0:
                stop += len(self)
            return XFrame(impl=self._impl.copy_range(start, step, stop))
        else:
            raise TypeError("Invalid argument type: must be int or slice ({}).".format(type(key).__name__))

    def append(self, other):
        """
        Add the rows of an XFrame to the end of this XFrame.

        Both XFrame must have the same set of columns with the same column
        names and column types.

        Parameters
        ----------
        other : :class:`.XFrame`
            Another XFrame whose rows are appended to the current XFrame.

        Returns
        -------
        :class:`.XFrame`
            The result XFrame from the append operation.

        Examples
        --------
        >>> xf = xframes.XFrame({'id': [4, 6, 8], 'val': ['D', 'F', 'H']})
        >>> xf2 = xframes.XFrame({'id': [1, 2, 3], 'val': ['A', 'B', 'C']})
        >>> xf = xf.append(xf2)
        +----+-----+
        | 4  |  D  |
        | 6  |  F  |
        | 8  |  H  |
        | 1  |  A  |
        | 2  |  B  |
        | 3  |  C  |
        +----+-----+
        [6 rows x 2 columns]
        """
        if not isinstance(other, XFrame):
            raise RuntimeError('XFrame append can only work with XFrame.')

        left_empty = len(self.column_names()) == 0
        right_empty = len(other.column_names()) == 0

        if left_empty and right_empty:
            return XFrame()

        if left_empty or right_empty:
            non_empty_xframe = self if right_empty else other
            return non_empty_xframe

        # check length of names 
        my_column_names = self.column_names()
        my_column_types = self.column_types()
        other_column_names = other.column_names()
        other_column_types = other.column_types()
        if len(my_column_names) != len(other_column_names):
            raise RuntimeError('Two XFrames must have the same number of columns.')

        # check if the order of column name is the same
        for i in range(len(my_column_names)):
            if other_column_names[i] != my_column_names[i]:
                raise RuntimeError('Column {} name is not the same in two XFrames, one is {} the other is {}.'
                                   .format(my_column_names[i], my_column_names[i], other_column_names[i]))
            # check column type
            if my_column_types[i] != other_column_types[i]:
                raise RuntimeError('Column {} type is not the same in two XFrames, one is {} the other is {}.'
                                   .format(my_column_names[i], my_column_types[i], other_column_types))

        return XFrame(impl=self._impl.append(other.impl()))

    def _groupby(self, key_columns, operations, *args):

        # TODO: groupby CONCAT produces unicode output from utf8 input
        # TODO: Preserve character encoding.

        operations = operations or {}
        # some basic checking first
        # make sure key_columns is a list
        if isinstance(key_columns, str):
            key_columns = [key_columns]
        # check that every column is a string, and is a valid column name
        my_column_names = self.column_names()
        my_column_types = self.column_types()
        key_columns_array = []
        for column in key_columns:
            if not isinstance(column, str):
                raise TypeError('Column name must be a string.')
            if column not in my_column_names:
                raise KeyError("Column '{}' does not exist in XFrame.".format(column))
            column_type = my_column_types[my_column_names.index(column)]
            if column_type is dict:
                raise TypeError('Cannot group on a dictionary column.')
            key_columns_array.append(column)

        group_output_columns = []
        group_columns = []
        group_properties = []

        all_ops = [operations] + list(args)
        for op_entry in all_ops:
            # if it is not a dict, nor a list, it is just a single aggregator
            # element (probably COUNT). wrap it in a list so we can reuse the
            # list processing code
            operation = op_entry
            if not (isinstance(operation, list) or isinstance(operation, dict)):
                operation = [operation]
            if isinstance(operation, dict):
                # now sweep the dict and add to group_columns and group_properties
                for key, val in operation.iteritems():
                    if not isinstance(val, tuple) and not callable(val):
                        raise TypeError("Unexpected type in aggregator definition of output column: '{}'"
                                        .format(key))
                    if callable(val):
                        prop, column = val()
                    else:
                        prop, column = val
                    num_args = prop.num_args
                    if num_args == 2 and (isinstance(column[0], tuple)) != (isinstance(key, tuple)):
                        raise TypeError('Output column(s) and aggregate column(s) for ' +
                                        'aggregate operation should be either all tuple or all string.')

                    if num_args == 2 and isinstance(column[0], tuple):
                        for (col, output) in zip(column[0], key):
                            group_columns += [[col, column[1]]]
                            group_properties += [prop]
                            group_output_columns += [output]
                    else:
                        group_columns += [column]
                        group_properties += [prop]
                        group_output_columns += [key]

            elif isinstance(operation, list):
                # we will be using automatically defined column names
                for val in operation:
                    if not isinstance(val, tuple) and not callable(val):
                        raise TypeError('Unexpected type in aggregator definition.')
                    if callable(val):
                        prop, column = val()
                    else:
                        prop, column = val
                    num_args = prop.num_args
                    if num_args == 2 and isinstance(column[0], tuple):
                        for col in column[0]:
                            group_columns += [[col, column[1]]]
                            group_properties += [prop]
                            group_output_columns += ['']
                    else:
                        group_columns += [column]
                        group_properties += [prop]
                        group_output_columns += ['']

        # let's validate group_columns
        for cols in group_columns:
            for col in cols:
                if not isinstance(col, str):
                    raise TypeError('Column name must be a string.')

                # TODO:  test for num_args != 0 or don't store empty column name
                if col != '' and col not in my_column_names:
                    raise KeyError("Column '{}' does not exist in XFrame.".format(col))

        return XFrame(impl=self._impl.groupby_aggregate(key_columns_array,
                                                        group_columns,
                                                        group_output_columns,
                                                        group_properties))

    def groupby(self, key_columns, operations=None, *args):
        """
        Perform a group on the `key_columns` followed by aggregations on the
        columns listed in `operations`.

        The `operations` parameter is a dictionary that indicates which
        aggregation operators to use and which columns to use them on. The
        available operators are SUM, MAX, MIN, COUNT, MEAN, VARIANCE, STD, CONCAT,
        SELECT_ONE, ARGMIN, ARGMAX, and QUANTILE.
        See :mod:`~xframes.aggregate` for more detail on the aggregators.

        Parameters
        ----------
        key_columns : string | list[string]
            Column(s) to group by. Key columns can be of any type other than
            dictionary.

        operations : dict, list, optional
            Dictionary of columns and aggregation operations. Each key is a
            output column name and each value is an aggregator. This can also
            be a list of aggregators, in which case column names will be
            automatically assigned.

        \*args
            All other remaining arguments will be interpreted in the same
            way as the operations argument.

        Returns
        -------
        out_xf : :class:`.XFrame`
            A new XFrame, with a column for each groupby column and each
            aggregation operation.

        See Also
        --------
        :mod:`xframes.aggregate`

        Examples
        --------
        Suppose we have an XFrame with movie ratings by many users.

        >>> import xframes.aggregate as agg
        >>> url = 'http://atg-testdata/rating.csv'
        >>> xf = xframes.XFrame.read_csv(url)
        >>> xf
        +---------+----------+--------+
        | user_id | movie_id | rating |
        +---------+----------+--------+
        |  25904  |   1663   |   3    |
        |  25907  |   1663   |   3    |
        |  25923  |   1663   |   3    |
        |  25924  |   1663   |   3    |
        |  25928  |   1663   |   2    |
        |  25933  |   1663   |   4    |
        |  25934  |   1663   |   4    |
        |  25935  |   1663   |   4    |
        |  25936  |   1663   |   5    |
        |  25937  |   1663   |   2    |
        |   ...   |   ...    |  ...   |
        +---------+----------+--------+
        [10000 rows x 3 columns]

        Compute the number of occurrences of each user.

        >>> user_count = xf.groupby('user_id',
        ...                         {'count': agg.COUNT()})
        >>> user_count
        +---------+-------+
        | user_id | count |
        +---------+-------+
        |  62361  |   1   |
        |  30727  |   1   |
        |  40111  |   1   |
        |  50513  |   1   |
        |  35140  |   1   |
        |  42352  |   1   |
        |  29667  |   1   |
        |  46242  |   1   |
        |  58310  |   1   |
        |  64614  |   1   |
        |   ...   |  ...  |
        +---------+-------+
        [9852 rows x 2 columns]

        Compute the mean and standard deviation of ratings per user.

        >>> user_rating_stats = xf.groupby('user_id',
        ...                                {
        ...                                    'mean_rating': agg.MEAN('rating'),
        ...                                    'std_rating': agg.STD('rating')
        ...                                })
        >>> user_rating_stats
        +---------+-------------+------------+
        | user_id | mean_rating | std_rating |
        +---------+-------------+------------+
        |  62361  |     5.0     |    0.0     |
        |  30727  |     4.0     |    0.0     |
        |  40111  |     2.0     |    0.0     |
        |  50513  |     4.0     |    0.0     |
        |  35140  |     4.0     |    0.0     |
        |  42352  |     5.0     |    0.0     |
        |  29667  |     4.0     |    0.0     |
        |  46242  |     5.0     |    0.0     |
        |  58310  |     2.0     |    0.0     |
        |  64614  |     2.0     |    0.0     |
        |   ...   |     ...     |    ...     |
        +---------+-------------+------------+
        [9852 rows x 3 columns]

        Compute the movie with the minimum rating per user.

        >>> chosen_movies = xf.groupby('user_id',
        ...                            {
        ...                                'worst_movies': agg.ARGMIN('rating','movie_id')
        ...                            })
        >>> chosen_movies
        +---------+-------------+
        | user_id | worst_movies |
        +---------+-------------+
        |  62361  |     1663    |
        |  30727  |     1663    |
        |  40111  |     1663    |
        |  50513  |     1663    |
        |  35140  |     1663    |
        |  42352  |     1663    |
        |  29667  |     1663    |
        |  46242  |     1663    |
        |  58310  |     1663    |
        |  64614  |     1663    |
        |   ...   |     ...     |
        +---------+-------------+
        [9852 rows x 2 columns]

        Compute the movie with the max rating per user and also the movie with
        the maximum imdb-ranking per user.

        >>> xf['imdb-ranking'] = xf['rating'] * 10
        >>> chosen_movies = xf.groupby('user_id',
        ...         {('max_rating_movie','max_imdb_ranking_movie'):
        ...            agg.ARGMAX(('rating','imdb-ranking'),'movie_id')})
        >>> chosen_movies
        +---------+------------------+------------------------+
        | user_id | max_rating_movie | max_imdb_ranking_movie |
        +---------+------------------+------------------------+
        |  62361  |       1663       |          16630         |
        |  30727  |       1663       |          16630         |
        |  40111  |       1663       |          16630         |
        |  50513  |       1663       |          16630         |
        |  35140  |       1663       |          16630         |
        |  42352  |       1663       |          16630         |
        |  29667  |       1663       |          16630         |
        |  46242  |       1663       |          16630         |
        |  58310  |       1663       |          16630         |
        |  64614  |       1663       |          16630         |
        |   ...   |       ...        |          ...           |
        +---------+------------------+------------------------+
        [9852 rows x 3 columns]

        Compute the movie with the max rating per user.

        >>> chosen_movies = xf.groupby('user_id',
        ...         {'best_movies': agg.ARGMAX('rating','movie')})

        Compute the movie with the max rating per user and also the movie with the maximum imdb-ranking per user.

        >>> chosen_movies = xf.groupby('user_id',
        ...        {('max_rating_movie','max_imdb_ranking_movie'):
        ...                              agg.ARGMAX(('rating','imdb-ranking'),'movie')})

        Compute the count, mean, and standard deviation of ratings per (user,
        time), automatically assigning output column names.

        >>> xf['time'] = xf.apply(lambda x: (x['user_id'] + x['movie_id']) % 11 + 2000)
        >>> user_rating_stats = xf.groupby(['user_id', 'time'],
        ...                                [agg.COUNT(),
        ...                                 agg.MEAN('rating'),
        ...                                 agg.STDV('rating')])
        >>> user_rating_stats
        +------+---------+-------+---------------+----------------+
        | time | user_id | Count | Avg of rating | Stdv of rating |
        +------+---------+-------+---------------+----------------+
        | 2006 |  61285  |   1   |      4.0      |      0.0       |
        | 2000 |  36078  |   1   |      4.0      |      0.0       |
        | 2003 |  47158  |   1   |      3.0      |      0.0       |
        | 2007 |  34446  |   1   |      3.0      |      0.0       |
        | 2010 |  47990  |   1   |      3.0      |      0.0       |
        | 2003 |  42120  |   1   |      5.0      |      0.0       |
        | 2007 |  44940  |   1   |      4.0      |      0.0       |
        | 2008 |  58240  |   1   |      4.0      |      0.0       |
        | 2002 |   102   |   1   |      1.0      |      0.0       |
        | 2009 |  52708  |   1   |      3.0      |      0.0       |
        | ...  |   ...   |  ...  |      ...      |      ...       |
        +------+---------+-------+---------------+----------------+
        [10000 rows x 5 columns]


        The groupby function can take a variable length list of aggregation
        specifiers so if we want the count and the 0.25 and 0.75 quantiles of
        ratings:

        >>> user_rating_stats = xf.groupby(['user_id', 'time'], agg.COUNT(),
        ...                                {'rating_quantiles': agg.QUANTILE('rating',[0.25, 0.75])})
        >>> user_rating_stats
        +------+---------+-------+------------------------+
        | time | user_id | Count |    rating_quantiles    |
        +------+---------+-------+------------------------+
        | 2006 |  61285  |   1   | array('d', [4.0, 4.0]) |
        | 2000 |  36078  |   1   | array('d', [4.0, 4.0]) |
        | 2003 |  47158  |   1   | array('d', [3.0, 3.0]) |
        | 2007 |  34446  |   1   | array('d', [3.0, 3.0]) |
        | 2010 |  47990  |   1   | array('d', [3.0, 3.0]) |
        | 2003 |  42120  |   1   | array('d', [5.0, 5.0]) |
        | 2007 |  44940  |   1   | array('d', [4.0, 4.0]) |
        | 2008 |  58240  |   1   | array('d', [4.0, 4.0]) |
        | 2002 |   102   |   1   | array('d', [1.0, 1.0]) |
        | 2009 |  52708  |   1   | array('d', [3.0, 3.0]) |
        | ...  |   ...   |  ...  |          ...           |
        +------+---------+-------+------------------------+
        [10000 rows x 4 columns]

        To put all items a user rated into one list value by their star rating:

        >>> user_rating_stats = xf.groupby(["user_id", "rating"],
        ...                                {"rated_movie_ids": agg.CONCAT("movie_id")})
        >>> user_rating_stats
        +--------+---------+----------------------+
        | rating | user_id |     rated_movie_ids  |
        +--------+---------+----------------------+
        |   3    |  31434  | array('d', [1663.0]) |
        |   5    |  25944  | array('d', [1663.0]) |
        |   4    |  38827  | array('d', [1663.0]) |
        |   4    |  51437  | array('d', [1663.0]) |
        |   4    |  42549  | array('d', [1663.0]) |
        |   4    |  49532  | array('d', [1663.0]) |
        |   3    |  26124  | array('d', [1663.0]) |
        |   4    |  46336  | array('d', [1663.0]) |
        |   4    |  52133  | array('d', [1663.0]) |
        |   5    |  62361  | array('d', [1663.0]) |
        |  ...   |   ...   |         ...          |
        +--------+---------+----------------------+
        [9952 rows x 3 columns]

        To put all items and rating of a given user together into a dictionary
        value:

        >>> user_rating_stats = xf.groupby("user_id",
        ...                                {"movie_rating": agg.CONCAT("movie_id", "rating")})
        >>> user_rating_stats
        +---------+--------------+
        | user_id | movie_rating |
        +---------+--------------+
        |  62361  |  {1663: 5}   |
        |  30727  |  {1663: 4}   |
        |  40111  |  {1663: 2}   |
        |  50513  |  {1663: 4}   |
        |  35140  |  {1663: 4}   |
        |  42352  |  {1663: 5}   |
        |  29667  |  {1663: 4}   |
        |  46242  |  {1663: 5}   |
        |  58310  |  {1663: 2}   |
        |  64614  |  {1663: 2}   |
        |   ...   |     ...      |
        +---------+--------------+
        [9852 rows x 2 columns]
        """
        return self._groupby(key_columns, operations, *args)

    def join(self, right, on=None, how='inner'):
        """
        Merge two XFrames. Merges the current (left) XFrame with the given
        (right) XFrame using a SQL-style equi-join operation by columns.

        Parameters
        ----------
        right : :class:`.XFrame`
            The XFrame to join.

        on : str | list | dict, optional
            The column name(s) representing the set of join keys.  Each row that
            has the same value in this set of columns will be merged together.

            * If `on` is not given, the join keyd are all columns in the left and right
              XFrames that have the same name

            * If a string is given, this is interpreted as a join using one column,
              where both XFrames have the same column name.

            * If a list is given, this is interpreted as a join using one or
              more column names, where each column name given exists in both
              XFrames.

            * If a dict is given, each dict key is taken as a column name in the
              left XFrame, and each dict value is taken as the column name in
              right XFrame that will be joined together. e.g.
              {'left_column_name':'right_column_name'}.

        how : {'inner', 'left', 'right', 'outer', 'full'}, optional
            The type of join to perform.  'inner' is default.

            * inner: Equivalent to a SQL inner join.  Result consists of the
              rows from the two frames whose join key values match exactly,
              merged together into one XFrame.

            * left: Equivalent to a SQL left outer join. Result is the union
              between the result of an inner join and the rest of the rows from
              the left XFrame, merged with missing values.

            * right: Equivalent to a SQL right outer join.  Result is the union
              between the result of an inner join and the rest of the rows from
              the right XFrame, merged with missing values.

            * full: Equivalent to a SQL full outer join. Result is
              the union between the result of a left outer join and a right
              outer join.

            * cartesian: Cartesian product of left and right tables, with columns from each.
              There is no common column matching: the resulting number of rows is the product
              of the row counts of the left and right XFrames.

        Returns
        -------
        :class:`.XFrame`
            The joined XFrames.

        Examples
        --------
        >>> animals = xframes.XFrame({'id': [1, 2, 3, 4],
        ...                           'name': ['dog', 'cat', 'sheep', 'cow']})
        >>> sounds = xframes.XFrame({'id': [1, 3, 4, 5],
        ...                          'sound': ['woof', 'baa', 'moo', 'oink']})
        >>> animals.join(sounds, how='inner')
        +----+-------+-------+
        | id |  name | sound |
        +----+-------+-------+
        | 1  |  dog  |  woof |
        | 3  | sheep |  baa  |
        | 4  |  cow  |  moo  |
        +----+-------+-------+
        [3 rows x 3 columns]

        >>> animals.join(sounds, on='id', how='left')
        +----+-------+-------+
        | id |  name | sound |
        +----+-------+-------+
        | 1  |  dog  |  woof |
        | 3  | sheep |  baa  |
        | 4  |  cow  |  moo  |
        | 2  |  cat  |  None |
        +----+-------+-------+
        [4 rows x 3 columns]

        >>> animals.join(sounds, on=['id'], how='right')
        +----+-------+-------+
        | id |  name | sound |
        +----+-------+-------+
        | 1  |  dog  |  woof |
        | 3  | sheep |  baa  |
        | 4  |  cow  |  moo  |
        | 5  |  None |  oink |
        +----+-------+-------+
        [4 rows x 3 columns]

        >>> animals.join(sounds, on={'id':'id'}, how='full')
        +----+-------+-------+
        | id |  name | sound |
        +----+-------+-------+
        | 1  |  dog  |  woof |
        | 3  | sheep |  baa  |
        | 4  |  cow  |  moo  |
        | 5  |  None |  oink |
        | 2  |  cat  |  None |
        +----+-------+-------+
        [5 rows x 3 columns]
        """
        available_join_types = ['inner', 'left', 'right', 'full', 'cartesian']

        if not isinstance(right, XFrame):
            raise TypeError('Can only join two XFrames.')

        if how not in available_join_types:
            raise ValueError('Invalid join type.')

        join_keys = dict()
        if on is None:
            left_names = self.column_names()
            right_names = right.column_names()
            common_columns = [name for name in left_names if name in right_names]
            for name in common_columns:
                join_keys[name] = name
        elif isinstance(on, str):
            join_keys[on] = on
        elif isinstance(on, list):
            for name in on:
                if not isinstance(name, str):
                    raise TypeError('Join keys must each be a str.')
                join_keys[name] = name
        elif isinstance(on, dict):
            join_keys = on
        else:
            raise TypeError("Must pass a 'str', 'list', or 'dict' of join keys.")

        return XFrame(impl=self._impl.join(right._impl, how, join_keys))

    def split_datetime(self, expand_column, column_name_prefix=None, limit=None):
        """
        Splits a datetime column of XFrame to multiple columns, with each value in a
        separate column. Returns a new XFrame with the expanded column replaced with
        a list of new columns. The expanded column must be of datetime.datetime type.

        For more details regarding name generation and
        other, refer to :py:func:`xframes.XArray.expand()`

        Parameters
        ----------
        expand_column : str
            Name of the unpacked column.

        column_name_prefix : str, optional
            If provided, expanded column names would start with the given prefix.
            If not provided, the default value is the name of the expanded column.

        limit : list[str], optional
            Limits the set of datetime elements to expand.
            Elements are 'year','month','day','hour','minute',
            and 'second'.

        Returns
        -------
        :class:`.XFrame`
            A new XFrame that contains rest of columns from original XFrame with
            the given column replaced with a collection of expanded columns.

        Examples
        --------

        >>> xf
        Columns:
            id   int
            submission  datetime.datetime
        Rows: 2
        Data:
            +----+----------------------------------------------------------+
            | id |               submission                                 |
            +----+----------------------------------------------------------+
            | 1  | datetime.datetime(2011, 1, 21, 7, 17, 21)                |
            | 2  | datetime.datetime(2011, 1, 21, 5, 43, 21)                |
            +----+----------------------------------------------------------+

        >>> xf.split_datetime('submission',limit=['hour','minute'])
        Columns:
            id  int
            submission.hour int
            submission.minute int
        Rows: 2
        Data:
        +----+-----------------+-------------------+
        | id | submission.hour | submission.minute |
        +----+-----------------+-------------------+
        | 1  |        7        |        17         |
        | 2  |        5        |        43         |
        +----+-----------------+-------------------+

        """
        # TODO: example above output is not correct -- prints differently
        if expand_column not in self.column_names():
            raise KeyError("Column '{}' does not exist in current XFrame.".format(expand_column))

        if column_name_prefix is None:
            column_name_prefix = expand_column

        # let xarray.split_datetime check limit parameter

        new_xf = self[expand_column].split_datetime(column_name_prefix, limit)

        # construct return XFrame, check if there is conflict
        rest_columns = [name for name in self.column_names() if name != expand_column]
        new_names = new_xf.column_names()
        while set(new_names).intersection(rest_columns):
            new_names = [name + '.1' for name in new_names]
        new_xf.rename(dict(zip(new_xf.column_names(), new_names)))

        ret_xf = self.select_columns(rest_columns)
        return ret_xf.add_columns(new_xf)

    # noinspection PyComparisonWithNone
    def filterby(self, values, column_name, exclude=False):
        """
        Filter an XFrame by values inside an iterable object. Result is an
        XFrame that only includes (or excludes) the rows that have a column
        with the given `column_name` which holds one of the values in the
        given `values` XArray. If `values` is not an
        XArray, we attempt to convert it to one before filtering.

        Parameters
        ----------
        values : :class:`.XArray` | list |tuple | set | iterable | numpy.ndarray | pandas.Series | str | function
            The values to use to filter the XFrame.  The resulting XFrame will
            only include rows that have one of these values in the given
            column.
            If this is f function, it is called on each row and is passed the value in the
            column given by 'column_name'.  The result includes
            rows where the function returns True.

        column_name : str | None
            The column of the XFrame to match with the given `values`.  This can only be None if the values
            argument is a function.  In this case, the function is passed the whole row.

        exclude : bool
            If True, the result XFrame will contain all rows EXCEPT those that
            have one of `values` in `column_name`.

        Returns
        -------
        :class:`.XFrame`
            The filtered XFrame.

        Examples
        --------
        >>> xf = xframes.XFrame({'id': [1, 2, 3, 4],
        ...                      'animal_type': ['dog', 'cat', 'cow', 'horse'],
        ...                      'name': ['bob', 'jim', 'jimbob', 'bobjim']})
        >>> household_pets = ['cat', 'hamster', 'dog', 'fish', 'bird', 'snake']
        >>> xf.filterby(household_pets, 'animal_type')
        +-------------+----+------+
        | animal_type | id | name |
        +-------------+----+------+
        |     dog     | 1  | bob  |
        |     cat     | 2  | jim  |
        +-------------+----+------+
        [2 rows x 3 columns]
        >>> xf.filterby(household_pets, 'animal_type', exclude=True)
        +-------------+----+--------+
        | animal_type | id |  name  |
        +-------------+----+--------+
        |    horse    | 4  | bobjim |
        |     cow     | 3  | jimbob |
        +-------------+----+--------+
        [2 rows x 3 columns]
        """
        if isinstance(values, types.FunctionType) and column_name is None:
            return XFrame(impl=self._impl.filter_by_function_row(values, exclude))

        if not isinstance(column_name, str):
            raise TypeError('Column_name must be a string.')

        existing_columns = self.column_names()
        if column_name not in existing_columns:
            raise KeyError("Column '{}' not in XFrame.".format(column_name))

        if isinstance(values, types.FunctionType):
            return XFrame(impl=self._impl.filter_by_function(values, column_name, exclude))

        existing_type = self.column_types()[existing_columns.index(column_name)]

        # If we are given the values directly, use filter.
        if not isinstance(values, XArray):
            # If we were given a single element, put into a set.
            # If iterable, then convert to a set.

            if isinstance(values, basestring):
                # Strings are iterable, but we don't want a set of characters.
                values = {values}
            elif not hasattr(values, '__iter__'):
                values = {values}
            else:
                # Make a new set from the iterable.
                values = set(values)

            if len(values) == 0:
                raise ValueError('Value list is empty.')

            value_type = type(next(iter(values)))
            if value_type != existing_type:
                raise TypeError("Value type ({}) does not match column type ({}).".format(
                    value_type.__name__, existing_type.__name__))
            return XFrame(impl=self._impl.filter(values, column_name, exclude))

        # If we have xArray, then use a different strategy based on join.
        value_xf = XFrame().add_column(values, column_name)

        # Make sure the values list has unique values, or else join will not filter.
        value_xf = value_xf.groupby(column_name, {})

        existing_type = self.column_types()[existing_columns.index(column_name)]
        given_type = value_xf.column_types()[0]
        if given_type is not existing_type:
            raise TypeError("Type of given values ('{}') does not match type of column '{}' ('{}') in XFrame."
                            .format(given_type, column_name, existing_type))

        if exclude:
            id_name = "id"
            # Make sure this name is unique so we know what to remove in
            # the result
            while id_name in existing_columns:
                id_name += '1'
            value_xf = value_xf.add_row_number(id_name)

            tmp = XFrame(impl=self._impl.join(value_xf.impl(),
                                              'left',
                                              {column_name: column_name}))
            # DO NOT CHANGE the next line -- it is XArray operator ==
            ret_xf = tmp[tmp[id_name] == None]
            del ret_xf[id_name]
            return ret_xf
        else:
            return XFrame(impl=self._impl.join(value_xf.impl(),
                                               'inner',
                                               {column_name: column_name}))

    # noinspection PyTypeChecker
    def pack_columns(self, columns=None, column_prefix=None, dtype=list,
                     fill_na=None, remove_prefix=True, new_column_name=None):
        """
        Pack two or more columns of the current XFrame into one single
        column.  The result is a new XFrame with the unaffected columns from the
        original XFrame plus the newly created column.

        The list of columns that are packed is chosen through either the
        `columns` or `column_prefix` parameter. Only one of the parameters
        is allowed to be provided: `columns` explicitly specifies the list of
        columns to pack, while `column_prefix` specifies that all columns that
        have the given prefix are to be packed.

        The type of the resulting column is decided by the `dtype` parameter.
        Allowed values for `dtype` are dict, array.array list, and tuple:

         - dict: pack to a dictionary XArray where column name becomes
           dictionary key and column value becomes dictionary value

         - array.array: pack all values from the packing columns into an array

         - list: pack all values from the packing columns into a list.

         - tuple: pack all values from the packing columns into a tuple.

        Parameters
        ----------
        columns : list[str], optional
            A list of column names to be packed.  There needs to have at least
            two columns to pack.  If omitted and `column_prefix` is not
            specified, all columns from current XFrame are packed.  This
            parameter is mutually exclusive with the `column_prefix` parameter.

        column_prefix : str, optional
            Pack all columns with the given `column_prefix`.
            This parameter is mutually exclusive with the `columns` parameter.

        dtype : dict | array.array | list | tuple, optional
            The resulting packed column type. If not provided, dtype is list.

        fill_na : value, optional
            Value to fill into packed column if missing value is encountered.
            If packing to dictionary, `fill_na` is only applicable to dictionary
            values; missing keys are not replaced.

        remove_prefix : bool, optional
            If True and `column_prefix` is specified, the dictionary key will
            be constructed by removing the prefix from the column name.
            This option is only applicable when packing to dict type.

        new_column_name : str, optional
            Packed column name.  If not given and `column_prefix` is given,
            then the prefix will be used as the new column name, otherwise name
            is generated automatically.

        Returns
        -------
        :class:`.XFrame`
            An XFrame that contains columns that are not packed, plus the newly
            packed column.

        See Also
        --------
        xframes.XFrame.unpack

        Notes
        -----
        - There must be at least two columns to pack.

        - If packing to dictionary, a missing key is always dropped. Missing
          values are dropped if `fill_na` is not provided, otherwise, missing
          value is replaced by `fill_na`. If packing to list or array, missing
          values will be kept. If `fill_na` is provided, the missing value is
          replaced with `fill_na` value.

        Examples
        --------
        Suppose 'xf' is an an XFrame that maintains business category
        information.

        >>> xf = xframes.XFrame({'business': range(1, 5),
        ...                       'category.retail': [1, None, 1, None],
        ...                       'category.food': [1, 1, None, None],
        ...                       'category.service': [None, 1, 1, None],
        ...                       'category.shop': [1, 1, None, 1]})

        >>> xf
        +----------+-----------------+---------------+------------------+---------------+
        | business | category.retail | category.food | category.service | category.shop |
        +----------+-----------------+---------------+------------------+---------------+
        |    1     |        1        |       1       |       None       |       1       |
        |    2     |       None      |       1       |        1         |       1       |
        |    3     |        1        |      None     |        1         |      None     |
        |    4     |       None      |       1       |       None       |       1       |
        +----------+-----------------+---------------+------------------+---------------+
        [4 rows x 5 columns]

        To pack all category columns into a list:

        >>> xf.pack_columns(column_prefix='category')
        +----------+--------------------+
        | business |         X2         |
        +----------+--------------------+
        |    1     |  [1, 1, None, 1]   |
        |    2     |  [None, 1, 1, 1]   |
        |    3     | [1, None, 1, None] |
        |    4     | [None, 1, None, 1] |
        +----------+--------------------+
        [4 rows x 2 columns]

        To pack all category columns into a dictionary, with new column name:

        >>> xf.pack_columns(column_prefix='category', dtype=dict,
        ...                 new_column_name='category')
        +----------+--------------------------------+
        | business |            category            |
        +----------+--------------------------------+
        |    1     | {'food': 1, 'shop': 1, 're ... |
        |    2     | {'food': 1, 'shop': 1, 'se ... |
        |    3     |  {'retail': 1, 'service': 1}   |
        |    4     |     {'food': 1, 'shop': 1}     |
        +----------+--------------------------------+
        [4 rows x 2 columns]

        To keep column prefix in the resulting dict key:

        >>> xf.pack_columns(column_prefix='category', dtype=dict,
        ...                 remove_prefix=False)
        +----------+--------------------------------+
        | business |               X2               |
        +----------+--------------------------------+
        |    1     | {'category.retail': 1, 'ca ... |
        |    2     | {'category.food': 1, 'cate ... |
        |    3     | {'category.retail': 1, 'ca ... |
        |    4     | {'category.food': 1, 'cate ... |
        +----------+--------------------------------+
        [4 rows x 2 columns]

        To explicitly pack a set of columns:

        >>> xf.pack_columns(columns = ['business', 'category.retail',
        ...                            'category.food', 'category.service',
        ...                            'category.shop'])
        +-----------------------+
        |           X1          |
        +-----------------------+
        |   [1, 1, 1, None, 1]  |
        |   [2, None, 1, 1, 1]  |
        | [3, 1, None, 1, None] |
        | [4, None, 1, None, 1] |
        +-----------------------+
        [4 rows x 1 columns]

        To pack all columns with name starting with 'category' into an array
        type, and with missing value replaced with 0:

        >>> xf.pack_columns(column_prefix="category", dtype=array.array,
        ...                 fill_na=0)
        +----------+--------------------------------+
        | business |               X2               |
        +----------+--------------------------------+
        |    1     | array('d', [1.0, 1.0, 0.0, ... |
        |    2     | array('d', [0.0, 1.0, 1.0, ... |
        |    3     | array('d', [1.0, 0.0, 1.0, ... |
        |    4     | array('d', [0.0, 1.0, 0.0, ... |
        +----------+--------------------------------+
        [4 rows x 2 columns]

        """
        if columns is not None and column_prefix is not None:
            raise ValueError("'Columns' and 'column_prefix' parameter cannot be given at the same time.")

        if new_column_name is None and column_prefix is not None:
            new_column_name = column_prefix

        if column_prefix is not None:
            if not isinstance(column_prefix, str):
                raise TypeError("'Column_prefix' must be a string. Found '{}': {}.".format(
                    type(column_prefix).__name__, column_prefix))
            columns = [name for name in self.column_names() if name.startswith(column_prefix)]
            if len(columns) == 0:
                raise ValueError("There are no column starts with prefix '{}'.".format(column_prefix))
        elif columns is None:
            columns = self.column_names()
        else:
            if not hasattr(columns, '__iter__'):
                raise TypeError("Columns must be an iterable type.")

            column_names = set(self.column_names())
            for column in columns:
                if column not in column_names:
                    raise ValueError("Current XFrame has no column called '{}'.".format(column))

            # check duplicate names
            if len(set(columns)) != len(columns):
                raise ValueError('There are duplicate column names in columns parameter.')

        if len(columns) <= 1:
            raise ValueError('Please provide at least two columns to pack.')

        if dtype not in (dict, list, tuple, array.array):
            raise ValueError("Resulting dtype has to be one of 'dict', 'array.array', 'list', or 'tuple' type.")

        # fill_na value for array needs to be numeric
        if dtype is array.array:
            if fill_na is not None and not isinstance(fill_na, (int, float)):
                raise ValueError('Fill_na value for array needs to be numeric type.')
            # all columns have to be numeric type
            for column in columns:
                if not issubclass(self[column].dtype(), (int, float)):
                    raise TypeError("Column '{}' type is not numeric, cannot pack into array type.".format(column))

        # generate dict key names if pack to dictionary
        # we try to be smart here
        # if all column names are like: a.b, a.c, a.d,...
        # we then use "b", "c", "d", etc as the dictionary key during packing
        if dtype is dict and column_prefix is not None and remove_prefix:
            size_prefix = len(column_prefix)
            first_char = set([c[size_prefix:size_prefix + 1] for c in columns])
            if len(first_char) == 1 and first_char.pop() in ['.', '-', '_']:
                dict_keys = [name[size_prefix + 1:] for name in columns]
            else:
                dict_keys = [name[size_prefix:] for name in columns]

        else:
            dict_keys = columns

        rest_columns = [name for name in self.column_names() if name not in columns]
        if new_column_name is not None:
            if not isinstance(new_column_name, str):
                raise TypeError("'New_column_name' must be a string. Found '{}': {}.".format(
                    type(new_column_name).__name__, new_column_name))
            if new_column_name in rest_columns:
                raise KeyError("Current XFrame already contains a column name '{}'.".format(new_column_name))
        else:
            new_column_name = ''

        ret_sa = XArray(impl=self._impl.pack_columns(columns, dict_keys, dtype, fill_na))

        new_xf = self.select_columns(rest_columns)
        return new_xf.add_column(ret_sa, new_column_name)

    def unpack(self, unpack_column, column_name_prefix=None, column_types=None,
               na_value=None, limit=None):
        """
        Expand one column of this XFrame to multiple columns with each value in
        a separate column. Returns a new XFrame with the unpacked column
        replaced with a list of new columns.  The column must be of
        list, tuple, array, or dict type.

        For more details regarding name generation, missing value handling and
        other, refer to the XArray version of
        :py:func:`~xframes.XArray.unpack()`.

        Parameters
        ----------
        unpack_column : str
            Name of the unpacked column

        column_name_prefix : str, optional
            If provided, unpacked column names would start with the given
            prefix. If not provided, default value is the name of the unpacked
            column.

        column_types : [type], optional
            Column types for the unpacked columns.
            If not provided, column types are automatically inferred from first
            100 rows. For array type, default column types are float.  If
            provided, column_types also restricts how many columns to unpack.

        na_value : flexible_type, optional
            If provided, convert all values that are equal to "na_value" to
            missing value (None).

        limit : list[str] | list[int], optional
            Control unpacking only a subset of list/array/dict value. For
            dictionary XArray, `limit` is a list of dictionary keys to restrict.
            For list/array XArray, `limit` is a list of integers that are
            indexes into the list/array value.

        Returns
        -------
        :class:`.XFrame`
            A new XFrame that contains rest of columns from original XFrame with
            the given column replaced with a collection of unpacked columns.

        See Also
        --------
        xframes.XFrame.pack_columns
            The opposite of unpack.

        Examples
        ---------
        >>> xf = xframes.XFrame({'id': [1,2,3],
        ...                      'wc': [{'a': 1}, {'b': 2}, {'a': 1, 'b': 2}]})
        +----+------------------+
        | id |        wc        |
        +----+------------------+
        | 1  |     {'a': 1}     |
        | 2  |     {'b': 2}     |
        | 3  | {'a': 1, 'b': 2} |
        +----+------------------+
        [3 rows x 2 columns]

        >>> xf.unpack('wc')
        +----+------+------+
        | id | wc.a | wc.b |
        +----+------+------+
        | 1  |  1   | None |
        | 2  | None |  2   |
        | 3  |  1   |  2   |
        +----+------+------+
        [3 rows x 3 columns]

        To not have prefix in the generated column name:

        >>> xf.unpack('wc', column_name_prefix="")
        +----+------+------+
        | id |  a   |  b   |
        +----+------+------+
        | 1  |  1   | None |
        | 2  | None |  2   |
        | 3  |  1   |  2   |
        +----+------+------+
        [3 rows x 3 columns]

        To limit subset of keys to unpack:

        >>> xf.unpack('wc', limit=['b'])
        +----+------+
        | id | wc.b |
        +----+------+
        | 1  | None |
        | 2  |  2   |
        | 3  |  2   |
        +----+------+
        [3 rows x 3 columns]

        To unpack an array column:

        >>> xf = xframes.XFrame({'id': [1,2,3],
        ...                       'friends': [array.array('d', [1.0, 2.0, 3.0]),
        ...                                   array.array('d', [2.0, 3.0, 4.0]),
        ...                                   array.array('d', [3.0, 4.0, 5.0])]})
        >>> xf
        +----+-----------------------------+
        | id |            friends          |
        +----+-----------------------------+
        | 1  | array('d', [1.0, 2.0, 3.0]) |
        | 2  | array('d', [2.0, 3.0, 4.0]) |
        | 3  | array('d', [3.0, 4.0, 5.0]) |
        +----+-----------------------------+
        [3 rows x 2 columns]

        >>> xf.unpack('friends')
        +----+-----------+-----------+-----------+
        | id | friends.0 | friends.1 | friends.2 |
        +----+-----------+-----------+-----------+
        | 1  |    1.0    |    2.0    |    3.0    |
        | 2  |    2.0    |    3.0    |    4.0    |
        | 3  |    3.0    |    4.0    |    5.0    |
        +----+-----------+-----------+-----------+
        [3 rows x 4 columns]
        """
        if unpack_column not in self.column_names():
            raise KeyError("Column '{}' does not exist in current XFrame.".format(unpack_column))

        if column_name_prefix is None:
            column_name_prefix = unpack_column

        new_xf = self[unpack_column].unpack(column_name_prefix, column_types, na_value, limit)

        # construct return XFrame, check if there is conflict
        rest_columns = [name for name in self.column_names() if name != unpack_column]
        new_names = new_xf.column_names()
        while set(new_names).intersection(rest_columns):
            new_names = [name + '.1' for name in new_names]
        new_xf.rename(dict(zip(new_xf.column_names(), new_names)))

        ret_xf = self.select_columns(rest_columns)
        return ret_xf.add_columns(new_xf)

    def stack(self, column_name, new_column_name=None, drop_na=False):
        """
        Convert a "wide" column of an XFrame to one or two "tall" columns by
        stacking all values.

        The stack works only for columns of dict, list, or array type.  If the
        column is dict type, two new columns are created as a result of
        stacking: one column holds the key and another column holds the value.
        The rest of the columns are repeated for each key/value pair.

        If the column is array or list type, one new column is created as a
        result of stacking. With each row holds one element of the array or list
        value, and the rest columns from the same original row repeated.

        The new XFrame includes the newly created column and all columns other
        than the one that is stacked.

        Parameters
        --------------
        column_name : str
            The column to stack. This column must be of dict/list/array type

        new_column_name : str | list of str, optional
            The new column name(s). If original column is list/array type,
            new_column_name must a string. If original column is dict type,
            new_column_name must be a list of two strings. If not given, column
            names are generated automatically.

        drop_na : boolean, optional
            If True, missing values and empty list/array/dict are all dropped
            from the resulting column(s). If False, missing values are
            maintained in stacked column(s).

        Returns
        -------
        :class:`.XFrame`
            A new XFrame that contains newly stacked column(s) plus columns in
            original XFrame other than the stacked column.

        See Also
        --------
        xframes.XFrame.unstack
            Undo the effect of stack.

        Examples
        ---------
        Suppose 'xf' is an XFrame that contains a column of dict type:

        >>> xf = xframes.XFrame({'topic':[1,2,3,4],
        ...                       'words': [{'a':3, 'cat':2},
        ...                                 {'a':1, 'the':2},
        ...                                 {'the':1, 'dog':3},
        ...                                 {}]
        ...                      })
        +-------+----------------------+
        | topic |        words         |
        +-------+----------------------+
        |   1   |  {'a': 3, 'cat': 2}  |
        |   2   |  {'a': 1, 'the': 2}  |
        |   3   | {'the': 1, 'dog': 3} |
        |   4   |          {}          |
        +-------+----------------------+
        [4 rows x 2 columns]

        Stack would stack all keys in one column and all values in another
        column:

        >>> xf.stack('words', new_column_name=['word', 'count'])
        +-------+------+-------+
        | topic | word | count |
        +-------+------+-------+
        |   1   |  a   |   3   |
        |   1   | cat  |   2   |
        |   2   |  a   |   1   |
        |   2   | the  |   2   |
        |   3   | the  |   1   |
        |   3   | dog  |   3   |
        |   4   | None |  None |
        +-------+------+-------+
        [7 rows x 3 columns]

        Observe that since topic 4 had no words, an empty row is inserted.
        To drop that row, set ``dropna=True`` in the parameters to stack.

        Suppose 'xf' is an XFrame that contains a user and his/her friends,
        where 'friends' columns is an array type. Stack on 'friends' column
        would create a user/friend list for each user/friend pair:

        >>> xf = xframes.XFrame({'topic':[1,2,3],
        ...                       'friends':[[2,3,4], [5,6],
        ...                                  [4,5,10,None]]
        ...                      })
        >>> xf
        +------+------------------+
        | user |     friends      |
        +------+------------------+
        |  1   |     [2, 3, 4]    |
        |  2   |      [5, 6]      |
        |  3   | [4, 5, 10, None] |
        +------+------------------+
        [3 rows x 2 columns]

        >>> xf.stack('friends', new_column_name='friend')
        +------+--------+
        | user | friend |
        +------+--------+
        |  1   |  2     |
        |  1   |  3     |
        |  1   |  4     |
        |  2   |  5     |
        |  2   |  6     |
        |  3   |  4     |
        |  3   |  5     |
        |  3   |  10    |
        |  3   |  None  |
        +------+--------+
        [9 rows x 2 columns]
        """
        # validate column_name
        column_name = str(column_name)
        if column_name not in self.column_names():
            raise ValueError("Cannot find column '{}' in the XFrame.".format(column_name))

        stack_column_type = self[column_name].dtype()
        if stack_column_type not in (dict, array.array, list):
            raise TypeError("Stack is only supported for column of 'dict', 'list', or 'array' type.")

        if new_column_name is not None:
            if stack_column_type == dict:
                if not isinstance(new_column_name, list):
                    raise TypeError("'New_column_name' has to be a 'list' to stack 'dict' type. Found '{}': {}".format(
                        type(new_column_name).__name__, new_column_name))
                elif len(new_column_name) != 2:
                    raise TypeError("'New_column_name' must have length of two.")
            else:
                if not isinstance(new_column_name, str):
                    raise TypeError("'New_column_name' has to be a 'str'. Found '{}': {}".format(
                        type(new_column_name).__name__, new_column_name))
                new_column_name = [new_column_name]

            # check if the new column name conflicts with existing ones
            for name in new_column_name:
                if name in self.column_names() and name != column_name:
                    raise ValueError("Column with name '{}' already exists, pick a new column name.".format(name))
        else:
            if stack_column_type is dict:
                new_column_name = ['', '']
            else:
                new_column_name = ['']

        # infer column types
        # TODO do this with head_as_list
        head_row = XArray(self[column_name].head(100)).dropna()
        if len(head_row) == 0:
            raise ValueError('Cannot infer column type because there are not enough rows.')
        if stack_column_type is dict:
            # infer key/value type
            keys = []
            values = []
            for row in head_row:
                for val in row:
                    keys.append(val)
                    if val is not None:
                        values.append(row[val])

            new_column_type = [
                infer_type_of_list(keys),
                infer_type_of_list(values)
            ]
        else:
            values = [v for v in itertools.chain.from_iterable(head_row)]
            new_column_type = [infer_type_of_list(values)]

        if stack_column_type is dict:
            return XFrame(impl=self._impl.stack_dict(column_name, new_column_name, new_column_type, drop_na))
        else:
            return XFrame(impl=self._impl.stack_list(column_name, new_column_name, new_column_type, drop_na))

    def unstack(self, column, new_column_name=None):
        """
        Concatenate values from one or two columns into one column, grouping by
        all other columns. The resulting column could be of type list, array or
        dictionary.  If `column` is a numeric column, the result will be of
        array.array type.  If `column` is a non-numeric column, the new column
        will be of list type. If `column` is a list of two columns, the new
        column will be of dict type where the keys are taken from the first
        column in the list.

        Parameters
        ----------
        column : str | [str, str]
            The column(s) that is(are) to be concatenated.
            If str, then collapsed column type is either array or list.
            If [str, str], then collapsed column type is dict

        new_column_name : str, optional
            New column name. If not given, a name is generated automatically.

        Returns
        -------
        :class:`.XFrame`
            A new XFrame containing the grouped columns as well as the new
            column.

        See Also
        --------
        xframes.XFrame.stack
            The inverse of unstack.

        xframes.XFrame.groupby : ``Unstack`` is a special version of ``groupby`` that uses the
          :mod:`~xframes.aggregate.CONCAT` aggregator

        Notes
        -----
        - There is no guarantee the resulting XFrame maintains the same order as
          the original XFrame.

        - Missing values are maintained during unstack.

        - When unstacking into a dictionary, if there is more than one instance
          of a given key for a particular group, an arbitrary value is selected.

        Examples
        --------
        >>> xf = xframes.XFrame({'count':[4, 2, 1, 1, 2, None],
        ...                       'topic':['cat', 'cat', 'dog', 'elephant', 'elephant', 'fish'],
        ...                       'word':['a', 'c', 'c', 'a', 'b', None]})
        >>> xf.unstack(column=['word', 'count'], new_column_name='words')
        +----------+------------------+
        |  topic   |      words       |
        +----------+------------------+
        | elephant | {'a': 1, 'b': 2} |
        |   dog    |     {'c': 1}     |
        |   cat    | {'a': 4, 'c': 2} |
        |   fish   |       None       |
        +----------+------------------+
        [4 rows x 2 columns]

        >>> xf = xframes.XFrame({'friend': [2, 3, 4, 5, 6, 4, 5, 2, 3],
        ...                      'user': [1, 1, 1, 2, 2, 2, 3, 4, 4]})
        >>> xf.unstack('friend', new_column_name='friends')
        +------+-----------------------------+
        | user |           friends           |
        +------+-----------------------------+
        |  3   |      array('d', [5.0])      |
        |  1   | array('d', [2.0, 4.0, 3.0]) |
        |  2   | array('d', [5.0, 6.0, 4.0]) |
        |  4   |    array('d', [2.0, 3.0])   |
        +------+-----------------------------+
        [4 rows x 2 columns]
        """
        if not isinstance(column, basestring) and len(column) != 2:
            raise TypeError("'Column' parameter has to be either a string or a list of two strings.")

        if new_column_name is None:
            new_column_name = 'unstack'
        if isinstance(column, str):
            key_columns = [i for i in self.column_names() if i != column]
            if new_column_name is not None:
                return self.groupby(key_columns, {new_column_name: xframes.aggregate.CONCAT(column)})
            else:
                return self.groupby(key_columns, xframes.aggregate.CONCAT(column))
        elif len(column) == 2:
            key_columns = [i for i in self.column_names() if i not in column]
            if new_column_name is not None:
                return self.groupby(key_columns, {new_column_name: xframes.aggregate.CONCAT(column[0], column[1])})
            else:
                return self.groupby(key_columns, xframes.aggregate.CONCAT(column[0], column[1]))

    def unique(self):
        """
        Remove duplicate rows of the XFrame. Will not necessarily preserve the
        order of the given XFrame in the new XFrame.

        Returns
        -------
        :class:`.XFrame`
            A new XFrame that contains the unique rows of the current XFrame.

        Raises
        ------
        TypeError
          If any column in the XFrame is a dictionary type.

        See Also
        --------
        xframes.XFrame.unique

        Examples
        --------
        >>> xf = xframes.XFrame({'id':[1,2,3,3,4], 'value':[1,2,3,3,4]})
        >>> xf
        +----+-------+
        | id | value |
        +----+-------+
        | 1  |   1   |
        | 2  |   2   |
        | 3  |   3   |        | 3  |   3   |
        | 4  |   4   |
        +----+-------+
        [5 rows x 2 columns]

        >>> xf.unique()
        +----+-------+
        | id | value |
        +----+-------+
        | 2  |   2   |
        | 4  |   4   |
        | 3  |   3   |
        | 1  |   1   |
        +----+-------+
        [4 rows x 2 columns]
        """
        return XFrame(impl=self._impl.unique())

    def sort(self, sort_columns, ascending=True):
        """
        Sort current XFrame by the given columns, using the given sort order.
        Only columns that are type of str, int and float can be sorted.

        Parameters
        ----------
        sort_columns : str | list of str | list of (str, bool) pairs
            Names of columns to be sorted.  The result will be sorted first by
            first column, followed by second column, and so on. All columns will
            be sorted in the same order as governed by the `ascending`
            parameter. To control the sort ordering for each column
            individually, `sort_columns` must be a list of (str, bool) pairs.
            Given this case, the first value is the column name and the second
            value is a boolean indicating whether the sort order is ascending.

        ascending : bool, optional
            Sort all columns in the given order.

        Returns
        -------
        :class:`.XFrame`
            A new XFrame that is sorted according to given sort criteria

        See Also
        --------
        xframes.XFrame.topk

        Examples
        --------
        Suppose 'xf' is an xframe that has three columns 'a', 'b', 'c'.
        To sort by column 'a', ascending:

        >>> xf = xframes.XFrame({'a':[1,3,2,1],
        ...                       'b':['a','c','b','b'],
        ...                       'c':['x','y','z','y']})
        >>> xf
        +---+---+---+
        | a | b | c |
        +---+---+---+
        | 1 | a | x |
        | 3 | c | y |
        | 2 | b | z |
        | 1 | b | y |
        +---+---+---+
        [4 rows x 3 columns]

        >>> xf.sort('a')
        +---+---+---+
        | a | b | c |
        +---+---+---+
        | 1 | a | x |
        | 1 | b | y |
        | 2 | b | z |
        | 3 | c | y |
        +---+---+---+
        [4 rows x 3 columns]

        To sort by column 'a', descending:

        >>> xf.sort('a', ascending = False)
        +---+---+---+
        | a | b | c |
        +---+---+---+
        | 3 | c | y |
        | 2 | b | z |
        | 1 | a | x |
        | 1 | b | y |
        +---+---+---+
        [4 rows x 3 columns]

        To sort by column 'a' and 'b', all ascending:

        >>> xf.sort(['a', 'b'])
        +---+---+---+
        | a | b | c |
        +---+---+---+
        | 1 | a | x |
        | 1 | b | y |
        | 2 | b | z |
        | 3 | c | y |
        +---+---+---+
        [4 rows x 3 columns]

        To sort by column 'a' ascending, and then by column 'c' descending:

        >>> xf.sort([('a', True), ('c', False)])
        +---+---+---+
        | a | b | c |
        +---+---+---+
        | 1 | b | y |
        | 1 | a | x |
        | 2 | b | z |
        | 3 | c | y |
        +---+---+---+
        [4 rows x 3 columns]
        """
        sort_column_orders = []

        # validate sort_columns
        if isinstance(sort_columns, str):
            sort_column_names = [sort_columns]
        elif isinstance(sort_columns, list):
            if len(sort_columns) == 0:
                raise ValueError('Please provide at least one column to sort.')

            first_param_types = set([type(i) for i in sort_columns])
            if len(first_param_types) != 1:
                raise ValueError('Sort_columns element are not of the same type.')

            first_param_type = first_param_types.pop()
            if first_param_type is tuple:
                sort_column_names = [i[0] for i in sort_columns]
                sort_column_orders = [i[1] for i in sort_columns]
            elif first_param_type is str:
                sort_column_names = sort_columns
            else:
                raise TypeError('Sort_columns type is not supported.')
        else:
            raise TypeError('Sort_columns type is not correct. Supported types are ' +
                            "'str', 'list of str' or 'list of (str,bool)' pair.")

        # use the second parameter if the sort order is not given
        if len(sort_column_orders) == 0:
            sort_column_orders = [ascending for _ in sort_column_names]

        # make sure all column exists
        my_column_names = set(self.column_names())
        for column in sort_column_names:
            if not isinstance(column, str):
                raise TypeError('Only string parameter can be passed in as column names.')
            if column not in my_column_names:
                raise ValueError("XFrame has no column named: '{}'.".format(column))
            if not is_sortable_type(self[column].dtype()):
                raise TypeError("Only columns of type ('str', 'int', 'float', " +
                                "'numpy.int32, 'numpy.float64'') can be sorted: {}."
                                .format(self[column].dtype()))

        return XFrame(impl=self._impl.sort(sort_column_names, sort_column_orders))

    def dropna(self, columns=None, how='any'):
        """
        Remove missing values from an XFrame. A missing value is either None
        or NaN.  If `how` is 'any', a row will be removed if any of the
        columns in the `columns` parameter contains at least one missing
        value.  If `how` is 'all', a row will be removed if all of the columns
        in the `columns` parameter are missing values.

        If the `columns` parameter is not specified, the default is to
        consider all columns when searching for missing values.

        Parameters
        ----------
        columns : list or str, optional
            The columns to use when looking for missing values. By default, all
            columns are used.

        how : {'any', 'all'}, optional
            Specifies whether a row should be dropped if at least one column
            has missing values, or if all columns have missing values.  'any' is
            default.

        Returns
        -------
        :class:`.XFrame`
            XFrame with missing values removed (according to the given rules).

        See Also
        --------
        xframes.XFrame.dropna_split:  Drops missing rows from the XFrame and returns them.

        Examples
        --------
        Drop all missing values.

        >>> xf = xframes.XFrame({'a': [1, None, None], 'b': ['a', 'b', None]})
        >>> xf.dropna()
        +---+---+
        | a | b |
        +---+---+
        | 1 | a |
        +---+---+
        [1 rows x 2 columns]

        Drop rows where every value is missing.

        >>> xf.dropna(any="all")
        +------+---+
        |  a   | b |
        +------+---+
        |  1   | a |
        | None | b |
        +------+---+
        [2 rows x 2 columns]

        Drop rows where column 'a' has a missing value.

        >>> xf.dropna('a', any="all")
        +---+---+
        | a | b |
        +---+---+
        | 1 | a |
        +---+---+
        [1 rows x 2 columns]
        """

        # If the user gives an empty list (the indicator to use all columns)
        # NA values being dropped would not be the expected behavior. This
        # is a NOOP, so let's not bother the server
        if isinstance(columns, list) and len(columns) == 0:
            return XFrame(impl=self._impl)

        (columns, all_behavior) = self._dropna_errchk(columns, how)

        return XFrame(impl=self._impl.drop_missing_values(columns, all_behavior, False))

    def dropna_split(self, columns=None, how='any'):
        """
        Split rows with missing values from this XFrame. This function has the
        same functionality as :py:func:`~xframes.XFrame.dropna`, but returns a
        tuple of two XFrames.  The first item is the expected output from
        :py:func:`~xframes.XFrame.dropna`, and the second item contains all the
        rows filtered out by the `dropna` algorithm.

        Parameters
        ----------
        columns : list or str, optional
            The columns to use when looking for missing values. By default, all
            columns are used.

        how : {'any', 'all'}, optional
            Specifies whether a row should be dropped if at least one column
            has missing values, or if all columns have missing values.  'any' is
            default.

        Returns
        -------
        (:class:`.XFrame`, :class:`.XFrame`)
            (XFrame with missing values removed,
             XFrame with the removed missing values)

        See Also
        --------
        xframes.XFrame.dropna

        Examples
        --------
        >>> xf = xframes.XFrame({'a': [1, None, None], 'b': ['a', 'b', None]})
        >>> good, bad = xf.dropna_split()
        >>> good
        +---+---+
        | a | b |
        +---+---+
        | 1 | a |
        +---+---+
        [1 rows x 2 columns]

        >>> bad
        +------+------+
        |  a   |  b   |
        +------+------+
        | None |  b   |
        | None | None |
        +------+------+
        [2 rows x 2 columns]
        """

        # If the user gives me an empty list (the indicator to use all columns)
        # NA values being dropped would not be the expected behavior. This
        # is a NOOP, so let's not bother the server
        if isinstance(columns, list) and len(columns) == 0:
            return XFrame(impl=self._impl), XFrame()

        (columns, all_behavior) = self._dropna_errchk(columns, how)

        xframe_tuple = self._impl.drop_missing_values(columns, all_behavior, True)

        if len(xframe_tuple) != 2:
            raise RuntimeError('Did not return two XFrames.')

        return XFrame(impl=xframe_tuple[0]), XFrame(impl=xframe_tuple[1])

    @staticmethod
    def _dropna_errchk(columns, how):
        if columns is None:
            # Default behavior is to consider every column, specified to
            # the server by an empty list (to avoid sending all the column
            # in this case, since it is the most common)
            columns = list()
        elif isinstance(columns, str):
            columns = [columns]
        elif not isinstance(columns, list):
            raise TypeError("Must give columns as a 'list', 'str', or 'None'.")
        else:
            # Verify that we are only passing strings in our list
            list_types = set([type(i) for i in columns])
            if str not in list_types or len(list_types) > 1:
                raise TypeError("All columns must be of 'str' type.")

        if how not in ['any', 'all']:
            raise ValueError("Must specify 'any' or 'all'.")

        if how == 'all':
            all_behavior = True
        else:
            all_behavior = False

        return columns, all_behavior

    def fillna(self, column, value):
        """
        Fill all missing values with a given value in a given column. If the
        `value` is not the same type as the values in `column`, this method
        attempts to convert the value to the original column's type. If this
        fails, an error is raised.

        Parameters
        ----------
        column : str
            The name of the column to modify.

        value : type convertible to XArray's type
            The value used to replace all missing values.

        Returns
        -------
        :class:`.XFrame`
            A new XFrame with the specified value in place of missing values.

        See Also
        --------
        xframes.XFrame.dropna

        Examples
        --------
        >>> xf = xframes.XFrame({'a':[1, None, None],
        ...                       'b':['13.1', '17.2', None]})
        >>> xf = xf.fillna('a', 0)
        >>> xf
        +---+------+
        | a |  b   |
        +---+------+
        | 1 | 13.1 |
        | 0 | 17.2 |
        | 0 | None |
        +---+------+
        [3 rows x 2 columns]
        """
        # Normal error checking
        if not isinstance(column, basestring):
            raise TypeError("Must give column name as a 'str'. Found '{}': {}.".format(type(column).__name__, column))
        ret = self.select_columns(self.column_names())
        ret[column] = ret[column].fillna(value)
        return ret

    def add_row_number(self, column_name='id', start=0):
        """
        Returns a new XFrame with a new column that numbers each row
        sequentially. By default the count starts at 0, but this can be changed
        to a positive or negative number.  The new column will be named with
        the given column name.  An error will be raised if the given column
        name already exists in the XFrame.

        Parameters
        ----------
        column_name : str, optional
            The name of the new column that will hold the row numbers.

        start : int, optional
            The number used to start the row number count.

        Returns
        -------
        :class:`.XFrame`
            The new XFrame with a column name

        Notes
        -----
        The range of numbers is constrained by a signed 64-bit integer, so
        beware of overflow if you think the results in the row number column
        will be greater than 9 quintillion.

        Examples
        --------
        >>> xf = xframes.XFrame({'a': [1, None, None], 'b': ['a', 'b', None]})
        >>> xf.add_row_number()
        +----+------+------+
        | id |  a   |  b   |
        +----+------+------+
        | 0  |  1   |  a   |
        | 1  | None |  b   |
        | 2  | None | None |
        +----+------+------+
        [3 rows x 3 columns]
        """

        if not isinstance(column_name, str):
            raise TypeError("Must give column_name as 'str's. {} {}".format(type(column_name).__name__, column_name))

        if not isinstance(start, int):
            raise TypeError("Must give start as 'int'. {} {}".format(type(start).__name__, start))

        if column_name in self.column_names():
            raise RuntimeError("Column '{}' already exists in the current XFrame.".format(column_name))

        return XFrame(impl=self._impl.add_row_number(column_name, start))

    def sql(self, sql_statement, table_name='xframe'):
        """
        Executes the given sql statement over the data in the table.
        Returns a new XFrame with the results.

        Parameters
        ----------
        sql_statement : str
            The statement to execute.

            The statement is executed by the Spark Sql query processor.  
            See the SparkSql documentation for details.  
            XFrame column names and types are translated to Spark
            for query processing.

        table_name : str, optional
            The table name to create, referred to in the sql statement.
            Defaulst to 'xframe'.

        Returns
        -------
        XFrame
            The new XFrame with the results.


        Examples
        --------
        >>> xf = xframes.XFrame({'id': [1, 2, 3], 'val': ['a', 'b', 'c']})
        >>> xf.sql("SELECT * FROM xframe WHERE id > 1"
        +----+--------+
        | id |  val   |
        +----+--------+
        | 2  |   'b'  |
        | 3  |   'c'  |
        +----+-----  -+
        [3 rows x 2 columns]
        """
        return XFrame(impl=self._impl.sql(sql_statement, table_name=table_name))

    @property
    def shape(self):
        """
        The shape of the XFrame, in a tuple. The first entry is the number of
        rows, the second is the number of columns.

        Examples
        --------
        >>> xf = xframes.XFrame({'id':[1,2,3], 'val':['A','B','C']})
        >>> xf.shape
        (3, 2)
        """
        return self.num_rows(), self.num_columns()
