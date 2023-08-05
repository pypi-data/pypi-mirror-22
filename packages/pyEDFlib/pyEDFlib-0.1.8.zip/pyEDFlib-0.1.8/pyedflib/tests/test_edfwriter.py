# -*- coding: utf-8 -*-
# Copyright (c) 2015 Holger Nahrstaedt
from __future__ import division, print_function, absolute_import

import os
import numpy as np
# from numpy.testing import (assert_raises, run_module_suite,
#                            assert_equal, assert_allclose, assert_almost_equal)
import unittest
import pyedflib


class TestEdfWriter(unittest.TestCase):
    def setUp(self):
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.bdfplus_data_file = os.path.join(data_dir, 'tmp_test_file_plus.bdf')
        self.edfplus_data_file = os.path.join(data_dir, 'tmp_test_file_plus.edf')
        self.bdf_data_file = os.path.join(data_dir, 'tmp_test_file.bdf')
        self.edf_data_file = os.path.join(data_dir, 'tmp_test_file.edf')

    def test_EdfWriter_BDFplus(self):
        channel_info = {'label': 'test_label', 'dimension': 'mV', 'sample_rate': 100,
                        'physical_max': 1.0, 'physical_min': -1.0,
                        'digital_max': 8388607, 'digital_min': -8388608,
                        'prefilter': 'pre1', 'transducer': 'trans1'}
        f = pyedflib.EdfWriter(self.bdfplus_data_file, 1,
                               file_type=pyedflib.FILETYPE_BDFPLUS)
        f.setSignalHeader(0,channel_info)
        f.setTechnician('tec1')
        data = np.ones(100) * 0.1
        f.writePhysicalSamples(data)
        f.writePhysicalSamples(data)
        f.close()
        del f

        f = pyedflib.EdfReader(self.bdfplus_data_file)
        np.testing.assert_equal(f.getTechnician(), 'tec1')

        np.testing.assert_equal(f.getLabel(0), 'test_label')
        np.testing.assert_equal(f.getPhysicalDimension(0), 'mV')
        np.testing.assert_equal(f.getPrefilter(0), 'pre1')
        np.testing.assert_equal(f.getTransducer(0), 'trans1')
        np.testing.assert_equal(f.getSampleFrequency(0), 100)
        f._close()
        del f

    def test_EdfWriter_BDF(self):
        channel_info1 = {'label': 'test_label', 'dimension': 'mV', 'sample_rate': 100,
                        'physical_max': 1.0, 'physical_min': -1.0,
                        'digital_max': 8388607, 'digital_min': -8388608,
                        'prefilter': 'pre1', 'transducer': 'trans1'}
        channel_info2 = {'label': 'test_label', 'dimension': 'mV', 'sample_rate': 100,
                            'physical_max': 1.0, 'physical_min': -1.0,
                            'digital_max': 8388607, 'digital_min': -8388608,
                            'prefilter': 'pre1', 'transducer': 'trans1'}
        f = pyedflib.EdfWriter(self.bdf_data_file, 2,
                               file_type=pyedflib.FILETYPE_BDF)
        f.setSignalHeader(0,channel_info1)
        f.setSignalHeader(1,channel_info2)

        data = np.ones(100) * 0.1
        f.writePhysicalSamples(data)
        f.writePhysicalSamples(data)
        f.writePhysicalSamples(data)
        f.writePhysicalSamples(data)
        f.close()
        del f

        f = pyedflib.EdfReader(self.bdf_data_file)

        np.testing.assert_equal(f.getLabel(0), 'test_label')
        np.testing.assert_equal(f.getPhysicalDimension(0), 'mV')
        np.testing.assert_equal(f.getPrefilter(0), 'pre1')
        np.testing.assert_equal(f.getTransducer(0), 'trans1')
        np.testing.assert_equal(f.getSampleFrequency(0), 100)
        f._close()
        del f

    def test_EdfWriter_EDFplus(self):
        channel_info = {'label': 'test_label', 'dimension': 'mV', 'sample_rate': 100,
                        'physical_max': 1.0, 'physical_min': -1.0,
                        'digital_max': 32767, 'digital_min': -32768,
                        'prefilter': 'pre1', 'transducer': 'trans1'}
        f = pyedflib.EdfWriter(self.edfplus_data_file, 1,
                               file_type=pyedflib.FILETYPE_EDFPLUS)
        f.setSignalHeader(0,channel_info)
        f.setTechnician('tec1')
        data = np.ones(100) * 0.1
        f.writePhysicalSamples(data)
        f.writePhysicalSamples(data)
        f.close()
        del f

        f = pyedflib.EdfReader(self.edfplus_data_file)
        np.testing.assert_equal(f.getTechnician(), 'tec1')

        np.testing.assert_equal(f.getLabel(0), 'test_label')
        np.testing.assert_equal(f.getPhysicalDimension(0), 'mV')
        np.testing.assert_equal(f.getPrefilter(0), 'pre1')
        np.testing.assert_equal(f.getTransducer(0), 'trans1')
        np.testing.assert_equal(f.getSampleFrequency(0), 100)
        f._close()
        del f

    def test_EdfWriter_EDF(self):
        channel_info1 = {'label': 'test_label', 'dimension': 'mV', 'sample_rate': 100,
                        'physical_max': 1.0, 'physical_min': -1.0,
                        'digital_max': 32767, 'digital_min': -32768,
                        'prefilter': 'pre1', 'transducer': 'trans1'}
        channel_info2 = {'label': 'test_label', 'dimension': 'mV', 'sample_rate': 100,
                             'physical_max': 1.0, 'physical_min': -1.0,
                            'digital_max': 32767, 'digital_min': -32768,
                            'prefilter': 'pre1', 'transducer': 'trans1'}
        f = pyedflib.EdfWriter(self.edf_data_file, 2,
                               file_type=pyedflib.FILETYPE_EDF)
        f.setSignalHeader(0,channel_info1)
        f.setSignalHeader(1,channel_info2)
        data = np.ones(100) * 0.1
        f.writePhysicalSamples(data)
        f.writePhysicalSamples(data)
        f.close()
        del f

        f = pyedflib.EdfReader(self.edf_data_file)

        np.testing.assert_equal(f.getLabel(0), 'test_label')
        np.testing.assert_equal(f.getPhysicalDimension(0), 'mV')
        np.testing.assert_equal(f.getPrefilter(0), 'pre1')
        np.testing.assert_equal(f.getTransducer(0), 'trans1')
        np.testing.assert_equal(f.getSampleFrequency(0), 100)
        f._close()
        del f

    def test_SampleWriting(self):
        channel_info1 = {'label':'test_label1', 'dimension':'mV', 'sample_rate':100,
                         'physical_max':1.0,'physical_min':-1.0,
                         'digital_max':8388607,'digital_min':-8388608,
                         'prefilter':'pre1','transducer':'trans1'}
        channel_info2 = {'label':'test_label2', 'dimension':'mV', 'sample_rate':100,
                         'physical_max':1.0,'physical_min':-1.0,
                         'digital_max':8388607,'digital_min':-8388608,
                         'prefilter':'pre2','transducer':'trans2'}
        f = pyedflib.EdfWriter(self.bdfplus_data_file, 2,
                              file_type=pyedflib.FILETYPE_BDFPLUS)
        f.setSignalHeader(0,channel_info1)
        f.setSignalHeader(1,channel_info2)

        data1 = np.ones(500) * 0.1
        data2 = np.ones(500) * 0.2
        data_list = []
        data_list.append(data1)
        data_list.append(data2)
        f.writeSamples(data_list)

        f.close()
        del f

        f = pyedflib.EdfReader(self.bdfplus_data_file)
        data1_read = f.readSignal(0)
        data2_read = f.readSignal(1)
        f._close()
        del f
        np.testing.assert_equal(len(data1), len(data1_read))
        np.testing.assert_equal(len(data2), len(data2_read))
        np.testing.assert_almost_equal(data1, data1_read)
        np.testing.assert_almost_equal(data2, data2_read)

    def test_AnnotationWriting(self):
        channel_info = {'label': 'test_label', 'dimension': 'mV', 'sample_rate': 100,
                        'physical_max': 1.0, 'physical_min': -1.0,
                        'digital_max': 8388607, 'digital_min': -8388608,
                        'prefilter': 'pre1', 'transducer': 'trans1'}
        f = pyedflib.EdfWriter(self.bdf_data_file, 1,
                               file_type=pyedflib.FILETYPE_BDFPLUS)
        f.setSignalHeader(0,channel_info)
        data = np.ones(100) * 0.1
        f.writePhysicalSamples(data)
        f.writePhysicalSamples(data)
        f.writePhysicalSamples(data)
        f.writePhysicalSamples(data)
        f.writeAnnotation(1.23, 0.2, u"annotation1_ä")
        f.writeAnnotation(0.25, -1, u"annotation2_ü")
        f.writeAnnotation(1.25, 0, u"annotation3_ö")
        f.writeAnnotation(1.30, -1, u"annotation4_ß")
        f.close()
        del f

        f = pyedflib.EdfReader(self.bdf_data_file)
        ann_time, ann_duration, ann_text = f.readAnnotations()
        f._close()
        del f
        np.testing.assert_almost_equal(ann_time[0], 1.23)
        np.testing.assert_almost_equal(ann_duration[0], 0.2)
        np.testing.assert_equal(ann_text[0], "annotation1_..")
        np.testing.assert_almost_equal(ann_time[1], 0.25)
        np.testing.assert_almost_equal(ann_duration[1], -1)
        np.testing.assert_equal(ann_text[1], "annotation2_..")
        np.testing.assert_almost_equal(ann_time[2], 1.25)
        np.testing.assert_almost_equal(ann_duration[2], 0)
        np.testing.assert_equal(ann_text[2], "annotation3_..")
        np.testing.assert_almost_equal(ann_time[3], 1.30)
        np.testing.assert_almost_equal(ann_duration[3], -1)
        np.testing.assert_equal(ann_text[3], "annotation4_..")

    def test_AnnotationWritingUTF8(self):
        channel_info = {'label': 'test_label', 'dimension': 'mV', 'sample_rate': 100,
                        'physical_max': 1.0, 'physical_min': -1.0,
                        'digital_max': 8388607, 'digital_min': -8388608,
                        'prefilter': u'test', 'transducer': 'trans1'}
        f = pyedflib.EdfWriter(self.bdf_data_file, 1,
                               file_type=pyedflib.FILETYPE_BDFPLUS)
        f.setSignalHeader(0,channel_info)
        data = np.ones(100) * 0.1
        f.writePhysicalSamples(data)
        f.writePhysicalSamples(data)
        f.writePhysicalSamples(data)
        f.writePhysicalSamples(data)
        f.writeAnnotation(1.23, 0.2, u"Zähne")
        f.writeAnnotation(0.25, -1, u"Fuß")
        f.writeAnnotation(1.25, 0, u"abc")
        f.close()
        del f

        f = pyedflib.EdfReader(self.bdf_data_file)
        ann_time, ann_duration, ann_text = f.readAnnotations()
        f._close()
        del f
        np.testing.assert_almost_equal(ann_time[0], 1.23)
        np.testing.assert_almost_equal(ann_duration[0], 0.2)
        np.testing.assert_equal(ann_text[0], "Z..hne")
        np.testing.assert_almost_equal(ann_time[1], 0.25)
        np.testing.assert_almost_equal(ann_duration[1], -1)
        np.testing.assert_equal(ann_text[1], "Fu..")
        np.testing.assert_almost_equal(ann_time[2], 1.25)
        np.testing.assert_almost_equal(ann_duration[2], 0)
        np.testing.assert_equal(ann_text[2], "abc")

    def test_BytesChars(self):
        channel_info = {'label': b'test_label', 'dimension': b'mV', 'sample_rate': 100,
                        'physical_max': 1.0, 'physical_min': -1.0,
                        'digital_max': 8388607, 'digital_min': -8388608,
                        'prefilter': b'      ', 'transducer': b'trans1'}
        f = pyedflib.EdfWriter(self.bdf_data_file, 1,
                               file_type=pyedflib.FILETYPE_BDFPLUS)
        f.setSignalHeader(0,channel_info)
        data = np.ones(100) * 0.1
        f.writePhysicalSamples(data)
        f.writePhysicalSamples(data)
        f.writePhysicalSamples(data)
        f.writePhysicalSamples(data)
        f.writeAnnotation(1.23, 0.2, b'Zaehne')
        f.writeAnnotation(0.25, -1, b'Fuss')
        f.writeAnnotation(1.25, 0, b'abc')
        f.close()
        del f

        f = pyedflib.EdfReader(self.bdf_data_file)
        ann_time, ann_duration, ann_text = f.readAnnotations()
        f._close()
        del f
        np.testing.assert_almost_equal(ann_time[0], 1.23)
        np.testing.assert_almost_equal(ann_duration[0], 0.2)
        np.testing.assert_equal(ann_text[0], "Zaehne")
        np.testing.assert_almost_equal(ann_time[1], 0.25)
        np.testing.assert_almost_equal(ann_duration[1], -1)
        np.testing.assert_equal(ann_text[1], "Fuss")
        np.testing.assert_almost_equal(ann_time[2], 1.25)
        np.testing.assert_almost_equal(ann_duration[2], 0)
        np.testing.assert_equal(ann_text[2], "abc")


if __name__ == '__main__':
    # run_module_suite(argv=sys.argv)
    unittest.main()
