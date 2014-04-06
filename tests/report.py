#coding=utf-8

import os

FILE_DIC = os.path.split(os.path.realpath(__file__))[0]
import time


def report_static_test(report_data, flag=''):
    report_file = open(os.path.join(FILE_DIC, 'test_report.log'),
                       mode='a')

    delimiter = '#' * 20
    timestamp = time.strftime('%m/%d %H:%M', time.localtime())
    title = 'Test - ' + flag + ' - ' + timestamp
    report_content = 'Prediction: {p_count}\t' \
                     'Reality: {r_count}\t' \
                     'Hit: {hit_count}\n' \
                     'Precision: {precision:.2%}\t' \
                     'Recall: {recall:.2%}\t' \
                     'F1-Score: {score:.2%}\n'.format(**report_data)

    report_file.write('\n'.join((delimiter,
                                 title,
                                 delimiter,
                                 report_content,
                                 delimiter)))

    report_file.close()
    return report_content


def report_dynamic_test(report_data, flag=''):
    report_file = open(os.path.join(FILE_DIC, 'dynamic_test_report.log'),
                       mode='a')

    delimiter = '#' * 20
    timestamp = time.strftime('%m/%d %H:%M', time.localtime())
    title = 'Test - ' + flag + ' - ' + timestamp
    report_content = 'Prediction: {p_count}\t' \
                     'Reality: {r_count}\t' \
                     'Hit: {hit_count}\n' \
                     'Precision: {precision:.2%}\t' \
                     'Recall: {recall:.2%}\t' \
                     'F1-Score: {score:.2%}\n'.format(**report_data)

    report_file.write('\n'.join((delimiter,
                                 title,
                                 delimiter,
                                 report_content,
                                 delimiter)))

    report_file.close()
    return report_content