#!/usr/bin/env python

"""
The file `swda/swda-metadata.csv` contains only some of the metadata included
with Switchboard. If you have a copy of the Switchboard and you want more
or different metadata, you can modify this file.
"""


__author__ = "Christopher Potts"
__version__ = "2.0"
__license__ = "GNU general public license, version 2"
__maintainer__ = "Christopher Potts"
__email__ = "See the author's website"


import csv
import os


def metadata2dict(filename, header, key_index=0):
    d = {}
    with open(filename, 'rt') as f:
        for row in csv.reader(f):
            row = [x.strip().strip('"') for x in row]
            c = row[key_index]
            d[c] = dict(zip(header, row))
    return d


# This should point to your copy of the Switchboard metadata tables:
PATH_TO_TABLES = "Switchboard/Switchboard-Transcripts/swb1/tables/tables/"


CALL_FILENAME = os.path.join(PATH_TO_TABLES, "call_con.tab")
CALL_HEADER = ['conversation_no', 'caller_no', 'phone_number', 'length', 'ivi_no', 'remarks', 'active']

CONV_FILENAME = os.path.join(PATH_TO_TABLES, "conv.tab")
CONV_HEADER = ['conversation_no', 'active', 'caller_from', 'caller_to', 'ivi_no', 'class', 'talk_day', 'time_start',
               'time_stop', 'trim_start', 'trim_stop', 'remarks']

CALLER_FILENAME = os.path.join(PATH_TO_TABLES, "caller.tab")
CALLER_HEADER = [ 'caller_no', 'pin', 'target', 'sex', 'birth_year', 'dialect_area', 'education', 'ti', 'payment_type',
                  'amt_pd', 'con', 'remarks', 'calls_deleted', 'speaker_partition']

TOPIC_FILENAME = os.path.join(PATH_TO_TABLES, "topic.tab")
TOPIC_HEADER = [ 'topic_description', 'ivi_no', 'prompt', 'flg', 'remarks', 'prompt_cont' ]

CALL = metadata2dict(CALL_FILENAME, CALL_HEADER)
CONV = metadata2dict(CONV_FILENAME, CONV_HEADER)
CALLER = metadata2dict(CALLER_FILENAME, CALLER_HEADER)
TOPIC = metadata2dict(TOPIC_FILENAME, TOPIC_HEADER, key_index=1)

######################################################################

def create_csv(output_filename):
    with open(output_filename, 'w') as f:
        csvwriter = csv.writer(f)
        header = [
            'conversation_no',        
            'talk_day',
            'length',
            'topic_description',
            'prompt',
            'from_caller',
            'from_caller_sex',
            'from_caller_education',
            'from_caller_birth_year',
            'from_caller_dialect_area',
            'to_caller',
            'to_caller_sex',
            'to_caller_education',
            'to_caller_birth_year',
            'to_caller_dialect_area']
        csvwriter.writerow(header)
        for conversation_no in sorted(CONV.keys()):
            from_no = CONV[conversation_no]['caller_from']
            to_no = CONV[conversation_no]['caller_to']
            ivi_no = CONV[conversation_no]['ivi_no']
            row = [
                conversation_no,
                CONV[conversation_no]['talk_day'],
                CALL[conversation_no]['length'],
                TOPIC[ivi_no]['topic_description'],
                TOPIC[ivi_no]['prompt'].strip() + TOPIC[ivi_no]['prompt_cont'].strip(),
                from_no,
                CALLER[from_no]['sex'],
                CALLER[from_no]['education'],
                CALLER[from_no]['birth_year'],
                CALLER[from_no]['dialect_area'],
                to_no,
                CALLER[to_no]['sex'],
                CALLER[to_no]['education'],
                CALLER[to_no]['birth_year'],
                CALLER[to_no]['dialect_area']]
            csvwriter.writerow(row)


create_csv('swda/swda-metadata.csv')

