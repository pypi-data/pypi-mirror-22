# -*- coding: utf-8 -*-

from __future__ import print_function

import gzip
import time
import sys

if sys.version_info.major == 3:
    from io import StringIO
elif sys.version_info.major == 2:
    try:
        import cStringIO as StringIO
    except ImportError:
        import StringIO
else:
    raise ValueError('Python %s not supported' % (sys.version_info.major, ))

from threading import Lock
from dummy_spark.rdd import RDD

try:
    import tinys3
    has_tinys3 = True
except ImportError as e:
    has_tinys3 = False


__all__ = ['SparkContext']
__author__ = 'willmcginnis'


class hadoopConfiguration(object):
    def __init__(self):
        pass

    def set(self, a, b):
        setattr(self, a, b)
        return True

    def get(self, a):
        return getattr(self, a, None)


class jvm(object):
    def __init__(self):
        self.hc = hadoopConfiguration()

    def hadoopConfiguration(self):
        return self.hc

    def textFile(self, file_name):
        if file_name.startswith('s3'):
            if has_tinys3:
                file_name = file_name.split('://')[1]
                bucket_name = file_name.split('/')[0]
                key_name = file_name.replace(bucket_name, '')[1:]
                access_key = self.hc.get('fs.s3n.awsAccessKeyId')
                secret_key = self.hc.get('fs.s3n.awsSecretAccessKey')
                region = self.hc.get('fs.s3n.endpoint')
                if region is None:
                    region = 's3.amazonaws.com'
                conn = tinys3.Connection(access_key, secret_key, endpoint=region)
                file = conn.get(key_name, bucket_name)
                if file_name.endswith('.gz'):
                    compressed = StringIO.StringIO(file.content)
                    gzipper = gzip.GzipFile(fileobj=compressed) 
                    return gzipper.readlines()
                return file.content.decode('utf-8').split('\n')
            else:
                raise Exception('Need TinyS3 to use s3 files')
        else:
            if file_name.endswith('.gz'):
                opener = gzip.open
            else:
                opener = open
            with opener(file_name, 'r') as f:
                return f.readlines()


class SparkContext(object):
    """
    Main entry point for Spark functionality. A SparkContext represents the
    connection to a Spark cluster, and can be used to create L{RDD} and
    broadcast variables on that cluster.
    """

    _gateway = None
    _jvm = None
    _next_accum_id = 0
    _active_spark_context = None
    _lock = Lock()
    _jsc = jvm()
    _python_includes = None  # zip and egg files that need to be added to PYTHONPATH

    PACKAGE_EXTENSIONS = ('.zip', '.egg', '.jar')

    DUMMY_VERSION = 'dummy version'

    def __init__(self, master=None, appName=None, sparkHome=None, pyFiles=None, environment=None, batchSize=0, serializer=None, conf=None, gateway=None, jsc=None, profiler_cls=None):
        """

        :param master:
        :param appName:
        :param sparkHome:
        :param pyFiles:
        :param environment:
        :param batchSize:
        :param serializer:
        :param conf:
        :param gateway:
        :param jsc:
        :param profiler_cls:
        :return:
        """
        self._callsite = None
        SparkContext._ensure_initialized(self, gateway=gateway)
        self.start_time = time.time()
        try:
            self._do_init(master, appName, sparkHome, pyFiles, environment, batchSize, serializer, conf, jsc, profiler_cls)
        except:
            # If an error occurs, clean up in order to allow future SparkContext creation:
            self.stop()
            raise

    def _do_init(self, master, appName, sparkHome, pyFiles, environment, batchSize, serializer, conf, jsc, profiler_cls):
        """

        :param master:
        :param appName:
        :param sparkHome:
        :param pyFiles:
        :param environment:
        :param batchSize:
        :param serializer:
        :param conf:
        :param jsc:
        :param profiler_cls:
        :return:
        """
        # TODO: add included files to python path
        return

    def _initialize_context(self, jconf):
        """

        :param jconf:
        :return:
        """
        return None

    @classmethod
    def _ensure_initialized(cls, instance=None, gateway=None):
        """

        :param instance:
        :param gateway:
        :return:
        """
        return True

    def __enter__(self):
        """

        :return:
        """
        return self

    def __exit__(self, type, value, trace):
        """

        :param type:
        :param value:
        :param trace:
        :return:
        """
        self.stop()

    def setLogLevel(self, logLevel):
        """

        :param logLevel:
        :return:
        """
        pass

    @classmethod
    def setSystemProperty(cls, key, value):
        """

        :param key:
        :param value:
        :return:
        """
        pass

    @property
    def version(self):
        """

        :return:
        """
        return self.DUMMY_VERSION

    @property
    def startTime(self):
        """

        :return:
        """
        return self.start_time

    @property
    def defaultParallelism(self):
        """

        :return:
        """
        return 1

    @property
    def defaultMinPartitions(self):
        """

        :return:
        """
        return 1

    def stop(self):
        """

        :return:
        """
        pass

    def emptyRDD(self):
        """

        :return:
        """
        return RDD([], self, None)

    def range(self, start, end=None, step=1, numSlices=None):
        """

        :param start:
        :param end:
        :param step:
        :param numSlices:
        :return:
        """
        return RDD(list(range(start, end, step)), self, None)

    def parallelize(self, c, numSlices=None):
        """

        :param c:
        :param numSlices:
        :return:
        """
        return RDD(c, self, None)

    def textFile(self, name, minPartitions=None, use_unicode=True):
        """

        :param name:
        :param minPartitions:
        :param use_unicode:
        :return:
        """
        data = self._jsc.textFile(name)
        rdd = RDD(data, self, None)
        return rdd

    def addPyFile(self, path):
        """

        :param path:
        :return:
        """
        sys.path.append(path)

    def pickleFile(self, name, minPartitions=None):
        """
        NotImplemented

        :param name:
        :param minPartitions:
        :return:
        """

        raise NotImplementedError

    def wholeTextFiles(self, path, minPartitions=None, use_unicode=True):
        """
        NotImplemented

        :param path:
        :param minPartitions:
        :param use_unicode:
        :return:
        """
        raise NotImplementedError

    def binaryFiles(self, path, minPartitions=None):
        """
        NotImplemented

        :param path:
        :param minPartitions:
        :return:
        """
        raise NotImplementedError

    def binaryRecords(self, path, recordLength):
        """
        NotImplemented

        :param path:
        :param recordLength:
        :return:
        """
        raise NotImplementedError

    def _dictToJavaMap(self, d):
        """
        NotImplemented

        :param d:
        :return:
        """
        raise NotImplementedError

    def sequenceFile(self, path, keyClass=None, valueClass=None, keyConverter=None, valueConverter=None, minSplits=None, batchSize=0):
        """
        NotImplemented

        :param path:
        :param keyClass:
        :param valueClass:
        :param keyConverter:
        :param valueConverter:
        :param minSplits:
        :param batchSize:
        :return:
        """
        raise NotImplementedError

    def newAPIHadoopFile(self, path, inputFormatClass, keyClass, valueClass, keyConverter=None, valueConverter=None, conf=None, batchSize=0):
        """
        NotImplemented

        :param path:
        :param inputFormatClass:
        :param keyClass:
        :param valueClass:
        :param keyConverter:
        :param valueConverter:
        :param conf:
        :param batchSize:
        :return:
        """
        raise NotImplementedError

    def newAPIHadoopRDD(self, inputFormatClass, keyClass, valueClass, keyConverter=None, valueConverter=None, conf=None, batchSize=0):
        """
        Read a 'new API' Hadoop InputFormat with arbitrary key and value class, from an arbitrary Hadoop configuration,
        which is passed in as a Python dict. This will be converted into a Configuration in Java. The mechanism is the
        same as for sc.sequenceFile.

        :param inputFormatClass: fully qualified classname of Hadoop InputFormat (e.g. "org.apache.hadoop.mapreduce.lib.input.TextInputFormat")
        :param keyClass: fully qualified classname of key Writable class (e.g. "org.apache.hadoop.io.Text")
        :param valueClass: fully qualified classname of value Writable class (e.g. "org.apache.hadoop.io.LongWritable")
        :param keyConverter: (None by default)
        :param valueConverter: (None by default)
        :param conf: Hadoop configuration, passed in as a dict (None by default)
        :param batchSize: The number of Python objects represented as a single Java object. (default 0, choose batchSize automatically)
        """

        if 'elasticsearch' in inputFormatClass and 'elasticsearch' in valueClass:
            try:
                from elasticsearch import Elasticsearch
            except ImportError:
                raise ImportError('Must have elasticsearch-py installed to use NewAPIHadoopRDD with the elasticsearch driver')

            host_name = conf.get('es.nodes')
            host_port = conf.get('es.port')
            index, mapping = conf.get('es.resource', '/').split('/')
            query = conf.get('es.query')

            client = Elasticsearch(hosts=['http://%s:%s' % (host_name, host_port, )])

            data = client.search(index=index, doc_type=mapping, body=query)
            data = data.get('hits', {}).get('hits', [])

            cleaned_data = []
            for dat in data:
                if '_source' in dat.keys():
                    cleaned_data.append((dat.get('_id'), dat.get('_source', {})))
                elif 'fields' in dat.keys():
                    cleaned_data.append((dat.get('_id'), dat.get('fields')))

            rdd = RDD(cleaned_data, self, None)

            return rdd
        else:
            raise NotImplementedError('Have not implimented %s for NewAPIHadoopRDD' % (inputFormatClass, ))

    def hadoopFile(self, path, inputFormatClass, keyClass, valueClass, keyConverter=None, valueConverter=None, conf=None, batchSize=0):
        """
        NotImplemented

        :param path:
        :param inputFormatClass:
        :param keyClass:
        :param valueClass:
        :param keyConverter:
        :param valueConverter:
        :param conf:
        :param batchSize:
        :return:
        """
        raise NotImplementedError

    def hadoopRDD(self, inputFormatClass, keyClass, valueClass, keyConverter=None, valueConverter=None, conf=None, batchSize=0):
        """
        NotImplemented

        :param inputFormatClass:
        :param keyClass:
        :param valueClass:
        :param keyConverter:
        :param valueConverter:
        :param conf:
        :param batchSize:
        :return:
        """
        raise NotImplementedError

    def _checkpointFile(self, name, input_deserializer):
        """
        NotImplemented

        :param name:
        :param input_deserializer:
        :return:
        """
        raise NotImplementedError

    def union(self, rdds):
        """
        NotImplemented

        :param rdds:
        :return:
        """
        raise NotImplementedError

    def broadcast(self, value):
        """
        NotImplemented

        :param value:
        :return:
        """
        raise NotImplementedError

    def accumulator(self, value, accum_param=None):
        """
        NotImplemented

        :param value:
        :param accum_param:
        :return:
        """
        raise NotImplementedError

    def addFile(self, path):
        """
        NotImplemented

        :param path:
        :return:
        """
        raise NotImplementedError

    def clearFiles(self):
        """
        NotImplemented

        :return:
        """
        raise NotImplementedError

    def setCheckpointDir(self, dirName):
        """
        NotImplemented

        :param dirName:
        :return:
        """
        raise NotImplementedError

    def _getJavaStorageLevel(self, storageLevel):
        """
        NotImplemented

        :param storageLevel:
        :return:
        """
        raise NotImplementedError

    def setJobGroup(self, groupId, description, interruptOnCancel=False):
        """
        NotImplemented

        :param groupId:
        :param description:
        :param interruptOnCancel:
        :return:
        """
        raise NotImplementedError

    def setLocalProperty(self, key, value):
        """
        NotImplemented

        :param key:
        :param value:
        :return:
        """
        raise NotImplementedError

    def getLocalProperty(self, key):
        """
        NotImplemented

        :param key:
        :return:
        """
        raise NotImplementedError

    def sparkUser(self):
        """
        NotImplemented

        :return:
        """
        raise NotImplementedError

    def cancelJobGroup(self, groupId):
        """
        NotImplemented

        :param groupId:
        :return:
        """
        raise NotImplementedError

    def cancelAllJobs(self):
        """
        NotImplemented

        :return:
        """
        raise NotImplementedError

    def statusTracker(self):
        """
        NotImplemented

        :return:
        """
        raise NotImplementedError

    def runJob(self, rdd, partitionFunc, partitions=None, allowLocal=False):
        """
        NotImplemented

        :param rdd:
        :param partitionFunc:
        :param partitions:
        :param allowLocal:
        :return:
        """
        raise NotImplementedError

    def show_profiles(self):
        """
        NotImplemented

        :return:
        """
        raise NotImplementedError

    def dump_profiles(self, path):
        """
        NotImplemented

        :param path:
        :return:
        """
        raise NotImplementedError
