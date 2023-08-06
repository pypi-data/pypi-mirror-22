from __future__ import division, print_function

import myvariant
import os
import sys
from pymongo import MongoClient
import VAPr.definitions as definitions
from VAPr.models import TxtParser, HgvsParser
import tqdm
from multiprocessing import Pool
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
try:
    logger.handlers[0].stream = sys.stdout
except:
    pass

__author__ = 'Carlo Mazzaferro<cmazzafe@ucsd.edu>'


class VariantParsing:

    def __init__(self,
                 input_dir,
                 output_csv_path,
                 annovar_path,
                 project_data,
                 mapping,
                 design_file=None,
                 build_ver=None):

        """ Project data """
        self.input_dir = input_dir
        self.output_csv_path = output_csv_path
        self.annovar = annovar_path
        self.project_data = project_data
        self.design_file = design_file
        self.buildver = build_ver
        self.mapping = mapping
        self.chunksize = definitions.chunk_size
        self.step = 0
        self.collection = project_data['project_name']
        self.db = project_data['db_name']
        self._last_round = False
        # self.completed_jobs = dict.fromkeys(list(self.mapping.keys()), 0)
        self.verbose = 0
        self.mongo_client = self.mongo_client_setup()
        self.n_vars = 0

    """
            if not csv:

                while hgvs.num_lines > self.step * self.chunksize:

                    list_hgvs_ids = hgvs.get_variants_from_vcf(self.step)
                    myvariants_variants = self.get_dict_myvariant(list_hgvs_ids, sample_id)

                    if len(myvariants_variants) < self.chunksize:
                        self._last_round = True

                    if self._last_round:
                        return 'Done'
                    else:
                        self.export(myvariants_variants)
                        self.step += 1

                return 'Done'

            else:
    """

    def mongo_client_setup(self):
        """
        Setup MongoDB client
        :return: null
        """
        client = MongoClient(maxPoolSize=None, waitQueueTimeoutMS=200)
        db = getattr(client, self.db)
        collection = getattr(db, self.collection)

        return collection

    def get_sample_csv_vcf_tuple(self):
        """ Locate files associated with a specific sample """

        list_tupls = []

        for _map in self.mapping:

            matching_csv = [i for i in os.listdir(_map['csv_file_full_path']) if i.startswith(_map['csv_file_basename'])
                            and i.endswith('txt')]

            matching_vcf = [i for i in os.listdir(_map['csv_file_full_path']) if i.startswith(_map['csv_file_basename'])
                            and i.endswith('vcf')]

            print(matching_vcf, matching_csv)

            if len(matching_csv) > 1 or len(matching_vcf) > 1:
                raise ValueError('Too many matching csvs')
            elif len(matching_csv) == 0 or len(matching_vcf) == 0:
                raise ValueError('Csv not found')
            else:
                csv_path = os.path.join(_map['csv_file_full_path'], matching_csv[0])
                vcf_path = os.path.join(_map['csv_file_full_path'], matching_vcf[0])
                list_tupls.append((_map['sample_names'],
                                   vcf_path,
                                   csv_path,
                                   self.db,
                                   self.collection))

        return list_tupls

    def parallel_annotation(self, n_processes, verbose=1):

        """
        Set up variant parsing scheme. Since a functional programming style is required for parallel
        processing, the input to the Pool.map function from the multiprocessing library must be
        immutable. We use tuples of the type:

            (samples, vcf_path, csv_path, db_name, collection_name, step)

        The parallel annotation will split the vcf, csv file in N steps where N equals the number of lines
        (variants) to be annotated divided a pre-defined 'chunk size'. For instance, a vcf, csv pair containing
        250 000 variants and a chunksize of 5 000 will yield 50 steps. Given 8 parallel procrsses, the annotation
        will happen over those 50 steps with 8 cores working cuncurrently until the 50 jobs are fully annotated.

        :param n_processes: number of cores to be used
        :param verbose: verbosity level [0,1,2,3]
        :return: None
        """

        self.verbose = verbose
        list_tupls = self.get_sample_csv_vcf_tuple()
        print(list_tupls)
        for tpl in list_tupls:

            hgvs = HgvsParser(tpl[1])
            csv_parsing = TxtParser(tpl[2], samples=hgvs.samples)
            num_lines = csv_parsing.num_lines
            print(num_lines, self.chunksize)
            n_steps = int(num_lines/self.chunksize) + 1
            print(n_steps)
            map_job = self.assign_step_to_tuple(tpl, n_steps)
            pool = Pool(n_processes)
            for _ in tqdm.tqdm(pool.imap_unordered(parse_by_step, map_job), total=len(map_job)):
                pass

            logger.info('Completed annotation and parsing for variants in sample %s' % tpl[0])

    @staticmethod
    def assign_step_to_tuple(_tuple, n_steps):
        """ Assign step number to each tuple to be consumed by parsing function """
        new_tuple_list = []
        for i in range(n_steps):
            sample = _tuple[0]
            vcf_file = _tuple[1]
            csv_file = _tuple[2]
            db_name = _tuple[3]
            collection_name = _tuple[4]
            step = i
            new_tuple_list.append((sample,
                                   vcf_file,
                                   csv_file,
                                   db_name,
                                   collection_name,
                                   step))
        return new_tuple_list


def parse_by_step(maps):
    """ The function that implements the parsing """

    db_name = maps[3]
    collection_name = maps[4]

    client = MongoClient(maxPoolSize=None, waitQueueTimeoutMS=200)
    db = getattr(client, db_name)
    collection = getattr(db, collection_name)
    hgvs = HgvsParser(maps[1])
    csv_parsing = TxtParser(maps[2], samples=hgvs.samples)

    list_hgvs_ids = hgvs.get_variants_from_vcf(maps[3])
    myvariants_variants = get_dict_myvariant(list_hgvs_ids, 2, maps[0])

    csv_variants = csv_parsing.open_and_parse_chunks(maps[3], build_ver='hg19')

    merged_list = []
    for i, _ in enumerate(myvariants_variants):
        for dict_from_sample in csv_variants[i]:
            merged_list.append(merge_dict_lists(myvariants_variants[i], dict_from_sample))

    logging.info('Parsing Buffer...')
    collection.insert_many(merged_list, ordered=False)


def merge_dict_lists(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def get_dict_myvariant(variant_list, verbose, sample_id):
    """ Retrieve variants from MyVariant.info"""

    if verbose >= 2:
        verbose = True
    else:
        verbose = False

    mv = myvariant.MyVariantInfo()
    # This will retrieve a list of dictionaries
    variant_data = mv.getvariants(variant_list, verbose=verbose, as_dataframe=False)
    variant_data = remove_id_key(variant_data, sample_id)

    return variant_data


def remove_id_key(variant_data, sample_id):
    """ Let mongo create an _id key to prevent insert attempts of documents with same key """

    for dic in variant_data:
        dic['hgvs_id'] = dic.pop("_id", None)
        dic['hgvs_id'] = dic.pop("query", None)
        dic['sample_id'] = sample_id

    return variant_data
