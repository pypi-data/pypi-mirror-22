import pyximport
pyximport.install()
import numpy as np

from inqbus.rainflow.data_formats.hdf5 import HDF5Table, RFCTable, \
    RFCCountedTable
from inqbus.rainflow.rainflow_algorithm.rainflow import rainflow
from inqbus.rainflow.rainflow_algorithm.classification import classification
from inqbus.rainflow.helpers import filter_data, get_extrema, count_pairs


def rainflow_for_numpy(data, maximum=None, minimum=None, classification=None):
    """
    :param data: input data
    :param maximum: maximum value to be recognized. Values bigger than max
    will be filtered
    :param minimum: minimum value to be recognized. Values smaller than min
    will be filtered
    :param classification: integer or None. If Integer the data will be
    classified before rainflow
    :return: result array with pairs, counted result array

    array with pairs is build like start, target
    array with counted is build like start, target, count
    """
    if minimum or maximum:
        data = filter_data(data, minimum=minimum, maximum=maximum)

    if classification:
        data = classification(classification, data)

    local_extrema = get_extrema(data)

    result_pairs, residuen_vector = rainflow(local_extrema)

    result_counted = count_pairs(result_pairs)

    return result_pairs, result_counted


def classification_for_numpy(array, number_of_classes=64):
    """
    Use this to add a classification after running the rainflow algorithm

    :param array: result array with pairs like returned from rainflow_for_numpy
    :param number_of_classes: number of classes
    :return: :return: result array with pairs, counted result array
    """
    res_pairs = classification(number_of_classes, array)
    res_counted = count_pairs(res_pairs)

    return res_pairs, res_counted


def rainflow_for_hdf5(source_table,
                      source_column,
                      target_group,
                      counted_table_name='RF_Counted',
                      pairs_table_name='RF_Pairs',
                      maximum=None,
                      minimum=None,
                      classification_number=None):
    """
    :param pairs_table_name: Table name for storing Pairs
    :param counted_table_name: Table name for storing Counted Pairs
    :param source_table: hdf5-url for table where data should be read
    :param source_column: name of column which should be used
    :param target_group: hdf5-url where to store data
    :param maximum: maximum value to be recognized. Values bigger than max
    will be filtered
    :param minimum: minimum value to be recognized. Values smaller than min
    will be filtered
    :param classification_number: integer or None. If Integer the data will be
    classified before rainflow
    :return:
    """
    source_table_obj = HDF5Table(source_table)

    data = source_table_obj.read_from_file(source_column)

    source_table_obj.close()

    result_pairs, result_counted = rainflow_for_numpy(
        data,
        minimum=minimum,
        maximum=maximum,
        classification=classification_number
    )

    table_path_pairs = '/'.join([target_group, pairs_table_name])
    table_path_counted = '/'.join([target_group, counted_table_name])

    pairs_table = HDF5Table(
        table_path_pairs,
        table_class=RFCTable,
        create_empty_table=True)
    pairs_table.write_to_file(result_pairs)
    pairs_table.close()

    counted_table = HDF5Table(
        table_path_counted,
        table_class=RFCCountedTable,
        create_empty_table=True)
    counted_table.write_to_file(result_counted)
    counted_table.close()


def classification_for_hdf5(source_table,
                            target_group,
                            number_of_classifications=64,
                            counted_table_name='RF_Counted_64',
                            pairs_table_name='RF_Pairs_64'):
    """
    Use this to add a classification after running the rainflow algorithm

    :param source_table: Table which includes pairs. Should be table like
    created in rainflow_for_hdf5
    :param target_group: hdf5-url where to store data
    :param number_of_classifications: number of classes
    :param pairs_table_name: Table name for storing Pairs
    :param counted_table_name: Table name for storing Counted Pairs
    :return:
    """
    source_table_ob = HDF5Table(source_table)
    start = source_table_ob.read_from_file('start')
    target = source_table_ob.read_from_file('target')
    source_table_ob.close()

    data = np.stack((start, target), axis=-1)

    result_pairs, result_counted = classification_for_numpy(
        data,
        number_of_classes=number_of_classifications
    )

    table_path_pairs = '/'.join([target_group, pairs_table_name])
    table_path_counted = '/'.join([target_group, counted_table_name])

    pairs_table = HDF5Table(
        table_path_pairs,
        table_class=RFCTable,
        create_empty_table=True)
    pairs_table.write_to_file(result_pairs)
    pairs_table.close()

    counted_table = HDF5Table(
        table_path_counted,
        table_class=RFCCountedTable,
        create_empty_table=True)
    counted_table.write_to_file(result_counted)
    counted_table.close()
