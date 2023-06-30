#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
''' Initialize with default environment variables '''
__name__ = "ClassifierWorkLoads" # bag of words workloads
__module__ = "property"
__package__ = "markets"
__app__ = "mining"
__ini_fname__ = "app.ini"
__roomw__ = ""
__conf_fname__ = "app.cfg"

''' Load necessary and sufficient python librairies that are used throughout the class'''
try:
    ''' essential python packages for rezaware framewor '''
    import os
    import sys
    import configparser    
    import logging
    import traceback
    import functools
    
    ''' function specific python packages '''
    import pandas as pd
    import numpy as np
    from datetime import datetime, date, timedelta
    ''' pyspark packages '''
    from pyspark.sql import functions as F
    from pyspark.sql import DataFrame
    
    from pyspark.sql import SparkSession

    print("All functional %s-libraries in %s-package of %s-module imported successfully!"
          % (__name__.upper(),__package__.upper(),__module__.upper()))

except Exception as e:
    print("Some packages in {0} module {1} package for {2} function didn't load\n{3}"\
          .format(__module__.upper(),__package__.upper(),__name__.upper(),e))


'''
    CLASS runs pyspark corpus and bag of words functions
    
'''

class PropertySearches():

    ''' Function --- INIT ---

            author: <nuwan.waidyanatha@rezgateway.com>
    '''
    def __init__(self, desc : str="market cap data prep", **kwargs):
        """
        Decription:
            Initializes the ExtractFeatures: class property attributes, app configurations, 
                logger function, data store directory paths, and global classes 
        Attributes:
            desc (str) identify the specific instantiation and purpose
        Returns:
            None
        """

        self.__name__ = __name__
        self.__package__ = __package__
        self.__module__ = __module__
        self.__app__ = __app__
        self.__ini_fname__ = __ini_fname__
        self.__conf_fname__ = __conf_fname__
        if desc is None or "".join(desc.split())=="":
            self.__desc__ = " ".join([self.__app__,self.__module__,
                                      self.__package__,self.__name__])
        else:
            self.__desc__ = desc

        self._data = None
#         self._portfolio=None

        global pkgConf
        global appConf
        global logger
        global clsSDB
        global clsSCNR
        global clsNoSQL
        global clsSFile

        __s_fn_id__ = f"{self.__name__} function <__init__>"
        
        try:
            self.cwd=os.path.dirname(__file__)
            pkgConf = configparser.ConfigParser()
            pkgConf.read(os.path.join(self.cwd,__ini_fname__))

            self.rezHome = pkgConf.get("CWDS","REZAWARE")
            sys.path.insert(1,self.rezHome)

            ''' innitialize the logger '''
            from rezaware import Logger as logs
            logger = logs.get_logger(
                cwd=self.rezHome,
                app=self.__app__, 
                module=self.__module__,
                package=self.__package__,
                ini_file=self.__ini_fname__)

            ''' set a new logger section '''
            logger.info('########################################################')
            logger.info("%s Class",self.__name__)

            ''' import spark database work load utils to read and write data '''
            from utils.modules.etl.loader import sparkFILEwls as sFile
            clsSFile = sFile.FileWorkLoads(desc=self.__desc__)
            ''' import spark clean-n-rich work load utils to transform the data '''

            logger.debug("%s initialization for %s module package %s %s done.\nStart workloads: %s."
                         %(self.__app__,
                           self.__module__,
                           self.__package__,
                           self.__name__,
                           self.__desc__))

            print("%s Class initialization complete" % self.__name__)

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return None


    ''' Function --- CLASS PROPERTIES ---

            author: <nuwan.waidyanatha@rezgateway.com>
                    <ushan.jayasuriya@colombo.rezgateway.com>
    '''
    ''' --- DATA --- '''
    @property
    def data(self):
        """
        Description:
            data @property and @setter functions. make sure it is a valid spark dataframe
        Attributes:
            data in @setter will instantiate self._data    
        Returns (dataframe) self._data
        """

        __s_fn_id__ = f"{self.__name__} function <@property data>"

        try:
            if self._data is not None and not isinstance(self._data,DataFrame):
                self._data = clsSFile.session.createDataFrame(self._data)
                logger.debug("%s converted non pyspark data object to %s",
                             __s_fn_id__,type(self._data))

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return self._data

    @data.setter
    def data(self,data):

        __s_fn_id__ = f"{self.__name__} function <@setter data>"

        try:
            if data is None:
                raise AttributeError("Invalid data attribute, must be a valid pyspark dataframe")
            if not isinstance(data,DataFrame):
                self._data = clsSFile.session.createDataFrame(data)
                logger.debug("%s converted %s object to %s",
                             __s_fn_id__,type(data),type(self._data))
            else:
                self._data = data

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return self._data


    ''' --- BOW --- '''
    @property
    def bow(self):
        """
        Description:
            bow @property and @setter functions. make sure it is a valid dict
        Attributes:
            bow in @setter will instantiate self._bow  
        Returns (dict) self._bow
        """

        __s_fn_id__ = f"{self.__name__} function <@property bow>"

        try:
            if not isinstance(self._bow,dict):
                raise AttributeError("bow is not a valid dict, % unacceptable" % type(self._bow))

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return self._bow

    @bow.setter
    def bow(self,_bow):

        __s_fn_id__ = f"{self.__name__} function <@setter bow>"

        try:
            if bow is None or bot isinstance(bow,dict):
                raise AttributeError("Cannot set bow class property with %s" % type(bow))

            self._bow = bow

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return self._bow


    ''' --- CORPUS --- '''
    @property
    def corpus(self):
        """
        Description:
            corpus @property and @setter functions. make sure it is a valid list
        Attributes:
            corpus in @setter will instantiate self._corpus    
        Returns (dataframe) self._data
        """

        __s_fn_id__ = f"{self.__name__} function <@property corpus>"

        try:
            if self._corpus is not None and not isinstance(self._corpus,list):
                raise AttributeError("corpus is not a valid list, % unacceptable" % type(self._corpus))

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return self._corpus

    @corpus.setter
    def corpus(self,corpus):

        __s_fn_id__ = f"{self.__name__} function <@setter corpus>"

        try:
            if corpus is None and not isinstance(corpus,list):
                raise AttributeError("Cannot set bow class property with %s" % type(corpus))
            self._corpus = corpus

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return self._corpus


    ''' Function --- READ BOW FILE ---

            author: <ushan.jayasuriya@colombo.rezgateway.com>
    '''

    def get_sentences(
        self,
        file_name: str,
        file_path: str,
        **kwargs):
        """
        Description:

        Arguments:

        Returns: self._data (dataframe)
        """

        __s_fn_id__ = f"{self.__name__} function <read_bow_from_file>"

        ''' declare variables & default values '''

        try:
            ''' validate input attributes '''
            
            ''' read bow from file '''
            self._bow = {"hello" : "world"}
            
            ''' << ADD THE LOGIC HERE >> '''

            ''' check if function produced a valid return object '''
            if self._bow is None or len(self._bow) <= 0:
                raise RuntimeError("retuned an empty %s bow dict",
                                   type(self._bow))
            logger.debug("%s loaded corpus with %d rows",__s_fn_id__,len(self._bow))

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return self._bow

    ''' Function --- READ BOW FILE ---

            author: <ushan.jayasuriya@colombo.rezgateway.com>
    '''

    def write_bow_to_file(
        self,
        bow : dict,
        file_name: str,
        file_path: str,
        **kwargs):
        """
        Description:

        Arguments:

        Returns: self._bow (dataframe)
        """

        __s_fn_id__ = f"{self.__name__} function <write_bow_to_file>"

        ''' declare variables & default values '''

        try:
            ''' validate input attributes '''
            
            ''' << ADD THE LOGIC HERE >> '''

            ''' write bow from file '''
            self._bow = {"hello" : "world"}
            
            ''' check if function produced a valid return object '''
            if self._bow is None or len(self._bow) <= 0:
                raise RuntimeError("retuned an empty %s bow dict",
                                   type(self._bow))
            logger.debug("%s loaded corpus with %d rows",__s_fn_id__,len(self._bow))

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return self._bow


    ''' Function --- READ BOW FILE ---

            author: <ushan.jayasuriya@colombo.rezgateway.com>
    '''

    def update_bow(
        self,
        corpus: list,
        bow : dict,
        file_name: str,
        file_path: str,
        **kwargs):
        """
        Description:

        Arguments:

        Returns: self._bow (dataframe)
        """

        __s_fn_id__ = f"{self.__name__} function <update_bow>"

        ''' declare variables & default values '''

        try:
            ''' validate input attributes '''
            self.corpus = corpus
            
            ''' << ADD THE LOGIC HERE >> '''

            ''' update bow from file '''
            self._bow = {"hello" : "world"}
            
            ''' check if function produced a valid return object '''
            if self._bow is None or len(self._bow) <= 0:
                raise RuntimeError("retuned an empty %s bow dict",
                                   type(self._bow))
            logger.debug("%s loaded corpus with %d rows",__s_fn_id__,len(self._bow))

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return self._bow


    def read_rooms_data(self, 
        folder_path: str,   # mandetory relative folder path to parent directory 
        files_list : list=[],  # specific list of files to read the data
        **kwargs,
        ):
        """
        Description:
            Read and filter data from the historic database (archives); specifically the
            AWS-S3 cold storage. 
            * If the file names are specified then the data for the specific files are retrieved
            * If no file list is given then all 'csv' files in folder and child folders are read
        Attributes :
            folder_path (str)- madatory; relative folder path
            file_list (list) - optional; specific a list of files to read the data
            kwargs (dict) - optional; 
                'CASCADE' (Bool) - default is 'True', if set to false will only read files in the
                    parent folder path
        Return(s) :
            self._data (DataFrame) with data in 
        Exceptions:
            If file_path is None or empty, abort
        """

        __s_fn_id__ = f"{self.__name__} function <read_rooms_data>"

        ''' declare variables & default values '''
        __def_ftype_list__ = 'csv'
        #_prop_data = pd.DataFrame()

        spark = SparkSession.builder.getOrCreate()
        # Create an empty Spark DataFrame
        _prop_data = spark.createDataFrame([])


        options = {
            "inferSchema":True,
            "header":True,
            "delimiter":",",
            "pathGlobFilter":'*.csv',
            "recursiveFileLookup":True,}


        try:
            ''' validate input attributes '''
            if not isinstance(folder_path,str) or "".join(folder_path.split())=="":
                raise AttributeError("Invalid folder path")

            ''' set the options from kwargs '''
            if "inferSchema" in kwargs.keys():
                options['inferSchema']=kwargs['inferSchema']
            if "header" in kwargs.keys():
                options['header']=kwargs['header']
            if "delimiter" in kwargs.keys():
                options['delimiter']=kwargs['delimiter']
            if "pathGlobFilter" in kwargs.keys():
                options['pathGlobFilter']=kwargs['pathGlobFilter']
            if "recursiveFileLookup" in kwargs.keys():
                options['recursiveFileLookup']=kwargs['recursiveFileLookup']
            
            
            if isinstance(files_list,list) and len(files_list)>0:
                ''' loop through file list and append data to DataFrame '''
                self._data = spark.createDataFrame([])
                for _file in files_list:
                    try:
 
                        _prop_data = clsSFile.read_csv_to_sdf(
                            file_path = str(folder_path) +"/"+str(_file),
                            **kwargs,
                        )
                        
                        if not isinstance(_prop_data,DataFrame) or _prop_data.shape[0]<=0:
                            raise AttributeError("%s in %s had errors; read_data returned "+\
                                                 "%s empty dataframe" 
                                                 % (_file.upper(),folder_path.upper(),type(_prop_data)))

                        logger.debug("%s concatenating file %s returned %d data rows and %d columns",
                                      __s_fn_id__, _file.upper(), _prop_data.count() , len(_prop_data.columns))
                                        
                        self._data = self._data.union(_prop_data)    
                    except Exception as file_err:
                        logger.warning("%s %s",__s_fn_id__,file_err)

            elif "CASCADE" in kwargs.keys() and not kwargs['CASCADE']:
                ''' read all files from only the parent folder '''
                logger.warning("TBD")

            else:
                ''' read all csv files from parent and child folders '''
                _prop_data = clsSFile.read_csv_to_sdf(
                            file_path = folder_path
                            **kwargs,
                        )
                if not isinstance(_prop_data,DataFrame) or _prop_data.shape[0]<=0:
                    raise AttributeError("Files in %s had errors; read_data returned %s empty dataframe" 
                                         % (folder_path.upper(),type(_prop_data)))
                self._data = _prop_data
                
            if not isinstance(self._data,DataFrame) or self._data.shape[0]<=0:
                raise RuntimeError("No data retrieved from %s; process returned %s dataframe",
                                   folder_path.upper(),type(_prop_data))
            logger.debug("%s successfully got %d rows %d columns from data in %s",
                         __s_fn_id__,self._data.count() , len(self._data.columns),folder_path.upper())
                        

        except Exception as err:
            logger.error("%s %s \n",__s_fn_id__, err)
            logger.debug(traceback.format_exc())
            print("[Error]"+__s_fn_id__, err)

        return self._data
