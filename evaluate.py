import nltk
from nltk.translate import AlignedSent, Alignment, metrics
from subprocess import call
from bs4 import BeautifulSoup


def naacl_to_ph(naacl_path):
    """ Take a file of naacl formatted alignments,
     and return an array of pharao formatted alignments (1-1 2-2 3-3)"""
    naacl = open(naacl_path, 'r')
    lines = naacl.readlines()
    curr_sent_align = ''
    sent_aligns = []
    sent_num = '1'

    for line in lines:
        naacl_align = line.split()
        prev_sent_num = sent_num
        sent_num = naacl_align[0]

        if sent_num != prev_sent_num:
            sent_aligns.append(curr_sent_align[:-1])
            curr_sent_align = ''

        # word_align = '-'.join([naacl_align[1], naacl_align[2]])
        # curr_sent_align.append(word_align)
        if naacl_align[1] != '0' and naacl_align[2] != '0' and len(naacl_align) < 4:
            curr_sent_align += '%d-%d ' % (
                int(naacl_align[2]) - 1, int(naacl_align[1]) - 1)
    # print(sent_aligns)
    return sent_aligns


def evaluate_alignment(ref, test):
    # ref_align = Alignment.fromstring(
    #     '0-0 1-1 2-2 3-4 4-4 5-4 6-5 7-6 10-7 11-7 12-8 12-9 13-7 14-10 16-13 17-12 19-12 20-12 22-12 27-14 28-16 29-18 30-20 30-17 31-17 31-20 33-19 34-19 35-21')
    # test_align = Alignment.fromstring(
    #     '0-0 0-1 2-2 1-3 2-4 3-5 2-6 6-7 4-8 8-9 7-10 7-12 7-13 10-14 10-15 9-16 16-17 0-18 11-19 12-21 13-22 14-23 15-25 16-26 14-27 16-28 18-29 18-30 19-31 19-32 20-34 21-35')
    # print(ref)
    # print(test)
    ref_align = Alignment.fromstring(ref)
    test_align = Alignment.fromstring(test)
    return metrics.alignment_error_rate(ref_align, test_align)


def evaluate(test_align_file):
    naacl_align_file = 'alignments-sv-en/test/test.ensv.naacl'
    ref_aligns = naacl_to_ph(naacl_align_file)
    test_aligns = open(test_align_file, 'r').read().splitlines()
    error_rates_total = 0.0

    for ref, test in zip(ref_aligns, test_aligns):
        error_rate = evaluate_alignment(ref, test)
        error_rates_total += error_rate

    print(error_rates_total / len(ref_aligns))
