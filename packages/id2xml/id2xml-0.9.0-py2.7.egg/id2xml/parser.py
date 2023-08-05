#!/bin/env python
# -*- coding: utf-8 -*-
# Copyright The IETF Trust 2017, All Rights Reserved

"""
NAME
  id2xml - Convert text format RFCs and Internet-Drafts to .xml format

DESCRIPTION
  id2xml reads text-format RFCs and IETF drafts which are reasonably
  well formatted (i.e., conforms to the text format produced by xml2rfc)
  and tries to generate a reasonably appropriate .xml file following the
  format accepted by xml2rfc, defined in RFC 7749 and its predecessors/
  successors
...

AUTHOR
  Written by Henrik Levkowetz, <henrik@levkowetz.com>

COPYRIGHT
  Copyright (c) 2017, The IETF Trust.
  All rights reserved.

  Licenced under the 3-clause BSD license; see the file LICENSE
  for details.
"""


from __future__ import print_function, unicode_literals

import os
import re
import six
import sys
import copy
import lxml
import zlib
import shlex
import datetime
import textwrap
from pyterminalsize import get_terminal_size
from xml2rfc.writers.base import BaseRfcWriter
from collections import namedtuple, deque
from lxml.etree import Element, SubElement, ElementTree, ProcessingInstruction, CDATA
from lxml.builder import E
from StringIO import StringIO
from __init__ import __version__

try:
    import debug
    debug.debug = True
except ImportError:
    pass



# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
#
# This is the entrypoint which is invoked from command-line scripts:

def run():
    import sys, os, getopt, re, argparse

    program = os.path.basename(sys.argv[0])
    progdir = os.path.dirname(sys.argv[0])

    # ----------------------------------------------------------------------
    # Parse options

    prolog, epilog = __doc__.split('...')
    parser = argparse.ArgumentParser(description=prolog, epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('DRAFT', nargs='*',                             help="text format draft(s) to be converted to xml")
    parser.add_argument('-2', '--v2', '--schema-v2', dest='schema', action='store_const', const='v2',
                                                                        help="output v2 (RFC 7749) schema")
    parser.add_argument('-3', '--v3', '--schema-v3', dest='schema', action='store_const', const='v3',
                                                                        help="output v3 (RFC 7991) schema")
    parser.add_argument('-o', '--output-file', metavar='FILE',          help="set the output file name")
    parser.add_argument('-p', '--output-path', metavar="DIR",           help="set the output directory name")
    parser.add_argument('-s', '--strip-only', action='store_true',      help="don't convert, only strip headers and footers")
    parser.add_argument('-v', '--version', action='store_true',         help="output version information, then exit")
    parser.add_argument('-V', '--verbose', action='store_true',         help="be (slightly) more verbose")
    parser.set_defaults(schema='v2')
    opts = parser.parse_args()

    # ----------------------------------------------------------------------
    def say(s):
        msg = "%s\n" % (s)
        sys.stderr.write(wrap(msg))

    # ----------------------------------------------------------------------
    def note(s):
        msg = "%s\n" % (s)
        if opts.verbose:
            sys.stderr.write(wrap(msg))

    # ----------------------------------------------------------------------
    def die(s, error=1):
        msg = "\n%s: Error:  %s\n\n" % (program, s)
        sys.stderr.write(wrap(msg))
        sys.exit(error)

    # ----------------------------------------------------------------------
    # The program itself    

    files = opts.DRAFT
    if opts.version:
        print(program, __version__)
        sys.exit(0)

    from pathlib import Path
    try:
        import debug
    except ImportError:
        pass

    if opts.output_path and opts.output_file:
        die("Mutually exclusive options -o / -p; use one or the other")

    if opts.strip_only:
        output_suffix = '.raw'
    else:
        output_suffix = '.xml'

    for file in files:
        try:
            inf = Path(file)
            name = re.sub('-[0-9][0-9]', '', inf.stem)
            if opts.output_file:
                # This is not what we want if opts.output_file=='-', but we fix
                # that in the 'with' clause below
                outf = Path(opts.output_file)
            elif opts.output_path:
                outf = Path(opts.output_path) / (inf.stem+output_suffix)
            else:
                outf = inf.with_suffix(output_suffix)
                # if we're using an implicit output file name (derived from the
                # input file name), and we're not just stripping headers, refuse
                # to overwrite an existing file.  It could be the original xml
                # file provided by the authors.
                if not opts.strip_only and outf.exists():
                    die("The implied output file (%s) already exists.  Provide an explicit "
                        "output filename (with -o) or a directory path (with -p) if you want "
                        "%s to overwrite an existing file." % (outf, program, ))
            with inf.open() as file:
                txt = file.read()
            if opts.strip_only:
                lines, __ = strip_pagebreaks(txt)
                with (sys.stdout if opts.output_file=='-' else outf.open('w')) as out:
                    out.write('\n'.join([l.txt for l in lines]))
                    out.write('\n')
                note('Wrote stripped file to %s' % out.name)
            else:
                parser = DraftParser(inf.name, txt, schema=opts.schema)
                xml = parser.parse_to_xml()
                with (sys.stdout if opts.output_file=='-' else outf.open('w')) as out:
                    out.write(xml)
                note('Wrote converted file to %s' % out.name)
        except Exception as e:
            sys.stderr.write("Failure converting %s: %s\n" % (inf.name, e))
            raise
    
# ----------------------------------------------------------------------

ns={
    'x':'http://relaxng.org/ns/structure/1.0',
    'a':'http://relaxng.org/ns/compatibility/annotations/1.0',
}

Line = namedtuple('Line', ['num', 'txt'])

boilerplate = BaseRfcWriter.boilerplate
approvers = BaseRfcWriter.approvers

status_of_memo = "Status of This Memo"
appendix_prefix = "Appendix "
#
code_re = r'(^\s*[A-Za-z][A-Za-z0-9_-]*\s*=\s*\S|{ *$|^ *})'
#
section_start_re = r"^((Appendix )?[A-Z0-9]+\.([0-9]+(\.[0-9]+)*\.?)? |Author's Address|Authors' Addresses|Acknowledgements|Contributors)"
#
one_ref_re = r"(([0-9A-Z-]|I-?D.)[0-9A-Za-z-]*( [0-9A-Z-]+)?|(IEEE|ieee)[A-Za-z0-9.-]+|(ITU ?|ITU-T ?|G\\.)[A-Za-z0-9.-]+)";
ref_ref_re =  r"\[{ref}(, *{ref})*\]".format(ref=one_ref_re)
#
# Elements of a reference item
ref_anchor_re = r'\[(?P<anchor>[^]]+)\]'
ref_name_re =   r'[-\' 0-9\w]+, (?:\w-?\w?\.)+(?:, Ed\.)?'
ref_last_re =   r'(?:\w-?\w?\.)+ [-\' 0-9\w]+(?:, Ed\.)?'
ref_org_re =   r'(?P<organization>[-/\w]+(?: [-/\w]+)*(, )?)'
ref_auth_re =   r'(?P<authors>({name})(, {name})*(,? and {last})?)'.format(name=ref_name_re, last=ref_last_re)
ref_title_re =  r'(?P<title>.+)'
ref_series_one =r'(?:(?:(?:RFC|STD|BCP|FYI|DOI|Internet-Draft) [^,]+|draft-[a-z0-9-]+)(?: \(work in progress\))?)'
ref_series_re = r'(?P<series>{item}(?:, {item})*)'.format(item=ref_series_one)
ref_docname_re= r'(?P<docname>[^,]+)'
month_re =      r'(?:January|February|March|April|May|June|July|August|September|October|November|December)'
date_re =       r'(?P<date>({month} )?[12]\d\d\d)'.format(month=month_re)
ref_url_re =    r'<(?P<target>(http|https|ftp)://[^>]+)>'
uri_re =        r'^<?\s*(?P<target>(http|https|ftp)://[^>\s]+)\s*>?$'
#
chunks = dict(
    anchor  = ref_anchor_re,
    authors = ref_auth_re,
    organiz = ref_org_re,
    title   = ref_title_re,
    series  = ref_series_re,
    docname = ref_docname_re,
    date    = date_re,
    url     = ref_url_re,
)

reference_patterns = [
    r'{anchor}  *{authors}, "{title}", {series}, {date}(, {url})?\.'.format(**chunks),
    r'{anchor}  *{authors}, "{title}", {date}(, {url})?\.'.format(**chunks),
    r'{anchor}  *{organiz}, "{title}"(, {docname})?, {date}(, {url})?\.'.format(**chunks),
    r'{anchor}  *"{title}", {url}\.'.format(**chunks),
## Lines commented out below are for debugging, when the full regex doesn't match (is buggy).
#    r'{anchor}  *{authors}, "{title}", {series}, {date}(, {url})?'.format(**chunks),
#    r'{anchor}  *{organiz}, "{title}", {docname}, {date}'.format(**chunks),
#    r'{anchor}  *{authors}, "{title}", {series}, {date}'.format(**chunks),
#    r'{anchor}  *{organiz}, "{title}", {docname}'.format(**chunks),
#    r'{anchor}  *{authors}, "{title}", {series}'.format(**chunks),
#    r'{anchor}  *{organiz}, "{title}"'.format(**chunks),
#    r'{anchor}  *{authors}, "{title}"'.format(**chunks),
#    r'{anchor}  *{organiz},'.format(**chunks),
#    r'{anchor}  *{authors}'.format(**chunks),
#    r'{anchor}  *'.format(**chunks),
#    r'{anchor}'.format(**chunks),
]

address_details = {
    'Phone:':   'phone',
    'Fax:':     'facsimile',
    'EMail:':   'email',
    'Email:':   'email',
    'URI:':     'uri',
}

# ----------------------------------------------------------------------

def wrap(s):
    cols = min(120, get_terminal_size()[0])

    lines = s.split('\n')
    wrapped = []
    # Preserve any indent (after the general indent)
    for line in lines:
        prev_indent = ''
        indent_match = re.search('^(\W+)', line)
        # Change the existing wrap indent to the original one
        if (indent_match):
            prev_indent = indent_match.group(0)
        wrapped.append(textwrap.fill(line, width=cols, subsequent_indent=prev_indent))
    return '\n'.join(wrapped)

def strip_pagebreaks(text):
    "Strip ID/RFC-style headers and footers from the given text"
    short_title = None
    stripped = []
    page = []
    line = ""
    newpage = False
    sentence = False
    blankcount = 0
    # We need to get rid of the \f, otherwise those will result in extra lines during line
    # splitting, and the line numbers reported in error messages will be off
    text = text.replace('\f','') 
    lines = text.splitlines()
    # two functions with side effects
    def endpage(page, newpage, line):
        if line:
            page += [ line ]
        return begpage(page, newpage)
    def begpage(page, newpage, line=None):
        if page and len(page) > 5:
            page = []
            newpage = True
        if line:
            page += [ line ]
        return page, newpage
    for lineno, line in enumerate(lines):
        line = line.rstrip()
        if re.search("\[?[Pp]age [0-9ivx]+\]?[ \t\f]*$", line, re.I):
            page, newpage = endpage(page, newpage, line)
            continue
        if re.search("\f", line, re.I):
            page, newpage = begpage(page, newpage)
            continue
        if lineno > 15:
            regex = "^(Internet.Draft|RFC \d+)( +)(\S.*\S)( +)(Jan|Feb|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|Sep|Oct|Nov|Dec)[a-z]+ (19[89][0-9]|20[0-9][0-9]) *$"
            match = re.search(regex, line, re.I)
            if not match is None:
                #debug.show('line')
                #debug.show('match')
                short_title = match.group(3)
                #debug.show('short_title')
                page, newpage = begpage(page, newpage, line)
                continue
        if lineno > 15 and re.search(".{58,}(Jan|Feb|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|Sep|Oct|Nov|Dec)[a-z]+ (19[89][0-9]|20[0-9][0-9]) *$", line, re.I):
            page, newpage = begpage(page, newpage, line)
            continue
        if re.search("^ *Internet.Draft.+[12][0-9][0-9][0-9] *$", line, re.I):
            page, newpage = begpage(page, newpage, line)
            continue
#        if re.search("^ *Internet.Draft  +", line, re.I):
#            newpage = True
#            continue
        if re.search("^ *Draft.+[12][0-9][0-9][0-9] *$", line, re.I):
            page, newpage = begpage(page, newpage, line)
            continue
        if re.search("^RFC[ -]?[0-9]+.*( +)[12][0-9][0-9][0-9]$", line, re.I):
            page, newpage = begpage(page, newpage, line)
            continue
        if re.search("^RFC[ -]?[0-9]+.*(  +)[12][0-9][0-9][0-9]$", line, re.I):
            page, newpage = begpage(page, newpage, line)
            continue
        if re.search("^draft-[-a-z0-9_.]+.*[0-9][0-9][0-9][0-9]$", line, re.I):
            page, newpage = endpage(page, newpage, line)
            continue
        if newpage and re.search("^ *draft-[-a-z0-9_.]+ *$", line, re.I):
            page, newpage = begpage(page, newpage, line)
            continue
        if re.search("^[^ \t]+", line):
            sentence = True
        if re.search("[^ \t]", line):
            if newpage:
                if sentence:
                    stripped += [ Line(lineno-1, "") ]
            else:
                if blankcount:
                    stripped += [ Line(lineno-1, "") ]
            blankcount = 0
            sentence = False
            newpage = False
        if re.search("[.:+]\)?$", line):    # line ends with a period; don't join with next page para
            sentence = True
        if re.search("^[0-9]+\.", line): # line starts with a section number; don't join with next page para
            sentence = True
        if re.search("^ +[o*+-]  ", line): # line starts with a list bullet; don't join with next page para
            sentence = True
        if re.search("^ +(E[Mm]ail): ", line): # line starts with an address component; don't join with next page para
            sentence = True
        if re.search("^[ \t]*$", line):
            blankcount += 1
            page += [ line ]
            continue
        page += [ line ]
        stripped += [ Line(lineno, line) ]
    page, newpage = begpage(page, newpage)
    return stripped, short_title

def split_on_large_whitespace(line):
    """
    Split on the largest contiguous whitespace.  If that is at the start
    or end of the line, then check if there is large whitespace at the
    opposite end of the line, too, and return the stripped line as centered.
    """
    left = center = right = ""
    pos = 0
    prev = 0
    count = 0
    bestp = 0
    bestc = 0
    for i, c in enumerate(line):
        if c == ' ':
            if prev+1 == i:
                count += 1
                prev = i
            else:

                pos = i
                prev = i
                count = 1
        if count > bestc:
            bestp = pos
            bestc = count
    # 
    if bestp == 0 or bestp == len(line.rstrip()):
        rwhite = len(line)-len(line.rstrip())
        lwhite = len(line)-len(line.lstrip())
        if abs(rwhite-lwhite) < min(rwhite, lwhite):
            center = line.strip()
    if not center:
        left, right = line[:bestp].strip(), line[bestp:].strip()
    return left, center, right

def ind(line):
    return len(line.txt) - len(line.txt.lstrip())

#@debug.trace
def is_section_start(line, numlist=None):
    text = line.txt
    if text.startswith(appendix_prefix):
        text = text[len(appendix_prefix):]
    return re.search('^%s([. ]|$)'%'.'.join(numlist), text) if numlist else re.search(section_start_re, text) != None

def parse_section_start(line, numlist, level, appendix):
    text = line.txt
    if appendix and text.startswith(appendix_prefix):
        text = text[len(appendix_prefix):]
    parts = text.strip().split(None, 1)
    if len(parts) == 2:
        number, title = parts
    elif len(parts) == 1:
        number, title = parts[0], ""
    else:
        return None, ""
    return number, title

def clean_name(txt):
    if txt.endswith('.txt'):
        txt = txt[:-4]
    if re.search('-[0-9][0-9]$', txt):
        txt = txt[:-3]
    return txt

def slugify(s):
    s = s.strip().lower()
    s = re.sub(r'[^\w\s/-]', '', s)
    s = re.sub(r'[-\s/]', '-', s)
    return s

def flatten(listoflists):
    return [ l for sublist in listoflists for l in sublist if not l is list ]

def strip(para):
    para = copy.copy(para)
    while para and para[0].txt.strip() == '':
        del para[0]
    while para and para[-1].txt.strip() == '':
        del para[-1]
    return para

def para2str(para):
    s = ''
    for ll in [ l.txt.strip() for l in para ]:
        s += ll if not s or not ll or re.search('\S[/-]$', s) else ' '+ll
    return s

def para2text(para):
    return '\n'.join([ l.txt for l in para ]).rstrip()

def colsplit(pos, txt):
    slices = [ (pos[i-1], pos[i]) for i in range(1,len(pos)) ]
    columns = [ txt[l:r].strip() for l,r in slices ]
    return columns

def parse_date(text):
    month_names = [ 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december' ]
    month_names_abbrev3 = [ n[:3] for n in month_names ]
    month_names_abbrev4 = [ n[:4] for n in month_names ]
    date_regexes = [
        r'^(?P<month>\w+)\s(?P<day>\d{1,2})(,|\s)+(?P<year>\d{4})',
        r'^(?P<day>\d{1,2})(,|\s)+(?P<month>\w+)\s(?P<year>\d{4})',
        r'^(?P<day>\d{1,2})-(?P<month>\w+)-(?P<year>\d{4})',
        r'^(?P<month>\w+)\s(?P<year>\d{4})',
        r'\s{3,}(?P<month>\w+)\s(?P<day>\d{1,2})(,|\s)+(?P<year>\d{4})',
        r'\s{3,}(?P<day>\d{1,2})(,|\s)+(?P<month>\w+)\s(?P<year>\d{4})',
        r'\s{3,}(?P<day>\d{1,2})-(?P<month>\w+)-(?P<year>\d{4})',
        # RFC 3339 date (also ISO date)
        r'\s{3,}(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})',
        # 'October 2008' - default day to today's.
        r'\s{3,}(?P<month>\w+)\s(?P<year>\d{4})',
    ]

    for regex in date_regexes:
        match = re.search(regex, text)
        if match:
            break
    else:
        raise RuntimeError("Unrecognized date format: '%s'" % text)

    md = match.groupdict()
    mon = md['month'].lower()
    day = int( md.get( 'day', 0 ) )
    year = int( md['year'] )
    if   mon in month_names:
        month = month_names.index( mon ) + 1
    elif mon in month_names_abbrev3:
        month = month_names_abbrev3.index( mon ) + 1
    elif mon in month_names_abbrev4:
        month = month_names_abbrev4.index( mon ) + 1
    elif mon.isdigit() and int(mon) in range(1,13):
        month = int(mon)
    else:
        raise RuntimeError("Cound not resolve the month name in '%s'" % text)

    date = {
        'year': str(year),
        'month': month_names[month-1].capitalize(),
    }
    if day:
        date['day'] = str(day)
    return date

def make_author_regex(name):
    aux = {
        "honor" : r"(?:[A-Z]\.|Dr\.?|Dr\.-Ing\.|Prof(?:\.?|essor)|Sir|Lady|Dame|Sri)",
        "prefix": r"([Dd]e|Hadi|van|van de|van der|Ver|von|[Ee]l)",
        "suffix": r"(jr.?|Jr.?|II|2nd|III|3rd|IV|4th)",
        #"first" : r"([A-Z][-A-Za-z]*)(( ?\([A-Z][-A-Za-z]*\))?(\.?[- ]{1,2}[A-Za-z]+)*)",
        #"last"  : r"([-A-Za-z']{2,})",
        }
    #
    def dotexp(s):
        s = re.sub(r"\. ",    r"\w* ", s)
        s = re.sub(r"\.$",    r"\w*", s)
        s = re.sub(r"\.(\w)", r"\w* \1", s)
        return s
    #
    # remove any suffix from the name before building the pattern
    suffix_match = re.search(" %(suffix)s$" % aux, name)
    if suffix_match:
        suffix = suffix_match.group(1)
        name = name[:-len(suffix)].strip()
    else:
        suffix = None
    #
    # Check if we have a comma, and reversed order first/last name
    if "," in name:
        last, first = name.split(",",1)
        name = "%s %s" % (first.strip(), last.strip())
    #
    # Check if the name consists of initials scrunched right up to surname,
    # or just a surname without any first name or initials
    if not " " in name:
        if "." in name:
            first, last = name.rsplit(".", 1)
            first += "."
        else:
            name = "[A-Z].+ " + name
            first, last = name.rsplit(" ", 1)
    else:
        first, last = name.rsplit(" ", 1)
        if "." in first and not ". " in first:
            first = first.replace(".", ". ").strip()
    first = first.strip()
    last = last.strip()
    #
    # did we manage to get a 'von ', 'van ', 'de ' etc. as part of the
    # first name instead of the surname?  If so, 
    prefix_match = re.search(" %(prefix)s$" % aux, first)
    if prefix_match:
        prefix = prefix_match.group(1)
        first = first[:-len(prefix)].strip()
        last = prefix+" "+last
    #
    # Replace abbreviation dots with regexp
    first = dotexp(first)
    last = dotexp(last)
    first = re.sub("[()]", " ", first)
    if " " in first:
        # if there's a middle part, let it be optional
        first, middle = first.split(" ", 1)
        first = "%s( +%s)?" % (first, middle)
    #
    # Double names (e.g., Jean-Michel) are abbreviated as two letter
    # connected by a dash -- let this expand appropriately
    first = re.sub(r"^([A-Z])-([A-Z])\\w\*", r"\1.*-\2.*", first) 
    #
    # Some chinese names are shown with double-letter(latin) abbreviated given names, rather than
    # a single-letter(latin) abbreviation:
    first = re.sub(r"^([A-Z])[A-Z]+\\w\*", r"\1[-\w]+", first) 
    #
    # permit insertion of middle names between first and last, and
    # add possible honorific and suffix information
    regex = r"(?:^| and )(?:%(hon)s ?)?(%(first)s\S*( +[^ ]+)* +%(last)s)( *\(.*|,( [A-Z][-A-Za-z0-9]*)?| %(suffix)s| [A-Z][a-z]+)?" % {"hon":aux['honor'], "first":first, "last":last, "suffix":suffix,}
    return regex

#@debug.trace
def match_name(name, authors):
    """
    Check the full name 'name' against the initials+surname in the list
    of dictionaries in 'authors', and return the matching author item.
    """
    #----------
    # If there's a comma, we have revered name order (last, first)
    for author in authors:
        if not 'regex' in author:
            briefname = author['initials']+' '+author['surname']
            author['regex'] = make_author_regex(briefname)
        regex = author['regex']
        if re.match(regex, name):
            return author

def symbol_ratio(text):
    wc = sum( c.isspace() for c in text )
    ac = sum( c.isalnum() for c in text )
    # symbol count is total minus whitespace and alphanumerics
    sc = len(text) - wc - ac
    sr = float(sc)/ac
    return sr

def indentation_levels(para):
    indent = []
    for line in strip(para):
        if len(line.txt):
            i = ind(line)
            if not i in indent:
                indent.append(i)
    indent.sort()
    return indent

def table_borders(para):
    symbols = ['-','=','|','+',]
    borders = []
    for line in para:
        if line.txt:
            l = ''.join([ ( c if c in symbols else ' ' ) for c in line.txt ]).strip()
            # get rid of solitary dashes which could occur in table cell text
            if re.search('[A-Za-z0-9]', line.txt):
                l = re.sub(' [-+]( |$)', r'  \1', l)
            if l:
                borders.append(l)
    borders.sort()
    return borders

def normalize_list_block(block):
    "Join and split items as needed, to produce one item per list item."
    assert type(block) is list and type(block[0]) is list
    items = []
    widow = []
    for b in block:
        b = strip(b)
        if widow:
            iw = ind(widow[0])
            sw, mw, __ = guess_list_style(widow[0])
            ib = ind(b[0])
            sb, mb, __ = guess_list_style(b[0])
            if ib > iw:
                if sb in [None, 'hanging']:
                    widow += b
                    items.append(widow)
                    widow = []
                else:
                    items.append(widow)
                    widow = []
                    items.append(b)
            elif ib == iw:
                items.append(widow)
                widow = b
            else:
                items.append(widow)
                widow = []
                items.append(b)
        else:
            if len(b) == 1:
                widow = b
            else:
                items += split_list_block(b)
    if widow:
        items.append(widow)
    items = normalize_sublists(items)
    return items

def split_list_block(block):
    "Split a block if it contains a transition to a lower indentation level"
    i = []
    items = []
    prev = 0
    for line in block:
        this = ind(line)
        if this < prev:
            items.append(i)
            i = [ line ]
        else:
            i.append(line)
        prev = this
    if i:
        items.append(i)
    return items

def normalize_sublists(block):
    """
    If a list block seems to contain a sublist, split that out and
    replace it with one sublist block.
    """
    sub = []
    items = []
    line = block[0][0]
    style, marker, __ = guess_list_style(line)
    indent = ind(line)
    for b in block:
        line = b[0]
        i = ind(line)
        s, m, __ = guess_list_style(line)
        if i == indent and s == style:
            if sub:
                items.append(sub)
                sub = []
            items.append(b)
        else:
            sub.append(b)
    if sub:
        items.append(sub)
        sub = []
    postlist = items
    return items

#@debug.trace
def guess_list_style(line, slice=None):
    list_styles = [
        ('numbers', r'^[1-9][0-9.]*\.$'),
        ('letters', r'^[a-z][a-z.]*\.$'),
        ('symbols', r'^[o*+-]$'),
        ('hanging', r'\S.+'),
        ('empty',   r'^$'),
    ]
    text = line.txt
    strp = text.strip()
    if (   re.search('^\S+  ', strp)        # doublespace after one nonspace chunk
        or re.search('^.+[^.]  ', strp)):   # doublespace after arbitrary characters, but no period before spaces
        if slice:
            b, e = slice
        else:
            b = ind(line)
            e = text.find('  ', b)+2
        marker = text[b:e].rstrip()
        text =   text[e:]
    else:
        marker = strp
        text = ''
    style = None
    for name, regex in list_styles:
        if re.search(regex, marker):
            style = name
            break
    return style, marker, text


def unindent(text, amount):
    prefix = ' '*amount
    fixed = []
    for line in text.splitlines():
        if line.strip() != '' and not line.startswith(prefix):
            return textwrap.dedent(text)
        fixed.append(line[amount:])
    return '\n'.join(fixed)

def match_boilerplate(bp, txt):
    if txt.startswith(bp):
        return True
    else:
        debug.pprint('bp')
        debug.pprint('txt')
        return False

class Stack(deque):
    def __init__(self, text):
        sep = r'(\s+|[][<>\'"])'
        tokens = re.split(sep, text)
        super(Stack, self).__init__(tokens)
    def pop(self):
        try:
            return super(Stack, self).popleft()
        except IndexError:
            return None
    def push(self, x):
        return super(Stack, self).appendleft(x)

class DraftParser():

    text = None
    root = None
    name = None
    schema = None
    entities = []

    rfc_pi_defaults = [
        'strict="yes"',
        'compact="yes"',
        'subcompact="no"',
        'symrefs="yes"',
    ]

    def __init__(self, name, text, schema="v2"):
        self.name = name
        self.is_draft = name.startswith('draft-')
        self.is_rfc = name.lower().startswith('rfc')
        if not (self.is_draft or self.is_rfc):
            self.err(0, "Expected the input document name to start with either 'draft-' or 'rfc'")
        assert type(text) is six.text_type # unicode in 2.x, str in 3.x.  
        self.raw = text
        schema_file = os.path.join(os.path.dirname(__file__), 'data', schema+'.rng')
        self.schema = ElementTree(file=schema_file)
        self.rfc_attr = self.schema.xpath("/x:grammar/x:define/x:element[@name='rfc']//x:attribute", namespaces=ns)
        self.rfc_attr_defaults = dict( (a.get('name'), a.get("{%s}defaultValue"%ns['a'], None)) for a in self.rfc_attr )

    def warn(self, lnum, text):
        # compose message.  report 1-based line numbers, rather than 0-based.
        msg = "\n%s(%s): %s" % (self.name, lnum+1, text)
        sys.stderr.write(wrap(msg))
        if not text.endswith('\n'):
            sys.stderr.write('\n')

    def err(self, lnum, text):
        msg = "\n%s(%s): %s" % (self.name, lnum+1, text)
        raise RuntimeError(wrap(msg))

    def parse_to_xml(self, **kwargs):
        self.lines, self.short_title = strip_pagebreaks(self.raw.expandtabs())
        self.l = 0
        self.p = None

        # Set up the <rfc/> element as root
        self.root = Element('rfc')
        for attr in self.rfc_attr_defaults:
            if not ':' in attr:
                val = self.rfc_attr_defaults[attr]
                if val:
                    self.root.set(attr, val)
        for attr in kwargs:
            if attr in self.rfc_attr_defaults:
                val = kwargs[attr]
                self.root.set(attr, val)

        # Default PI settings (at least some which differes from the xml2rfc
        # defaults)
        for item in self.rfc_pi_defaults:
            pi = ProcessingInstruction('rfc', item)
            self.root.append(pi)

        # Parse the document
        doc = self.document()

        # Return the xml document (if any)
        if len(doc):
            doctype = '<!DOCTYPE rfc SYSTEM "rfc2629.dtd"'
            if self.entities:
                doctype += '[\n'
                for entity in self.entities:
                    doctype += '<!ENTITY {name} SYSTEM "{url}">\n'.format(**entity)
                doctype += ']'
            doctype +='>'
            return lxml.etree.tostring(
                doc,
                xml_declaration=True,
                encoding='utf-8',
                doctype=doctype,
                pretty_print=True,
            ).decode('utf-8')
        else:
            return None

    def document(self):
        self.root.append(self.front())
        self.root.append(self.middle())
        self.root.append(self.back())
        self.postprocess()
        return self.root

    # ------------------------------------------------------------------------
    # front
    # ------------------------------------------------------------------------
    def front(self):
        # (title , author+ , date , area* , workgroup* , keyword* , abstract? , note*)
        lines_left, lines_right, lines_title, lines_name = self.get_first_page_top()
        #
        if self.is_draft and lines_name:
            self.root.set('docName', lines_name.txt)
        #

        workgroup, stream, series_number, rfc_number, obsoletes, updates, category, expires = self.parse_top_left(lines_left)

        if stream:
            self.root.set('submissionType', stream)
        if rfc_number:
            self.root.set('number', rfc_number)
        if category:
            self.root.set('category', category)
            if series_number:
                self.root.set('seriesNo', series_number)
        if obsoletes:
            self.root.set('obsoletes', ', '.join(obsoletes))
        if updates:
            self.root.set('updates', ', '.join(updates))

        authors, date = self.parse_top_right(lines_right)

        front = Element('front')
        title = E.title(para2str(lines_title))
        if self.short_title and self.short_title.strip() != title.text.strip():
            title.set('abbrev', self.short_title)
        front.append(title)
        #
        for item in authors:
            author = {}
            # pick out the elements which are valid as <author> attributes
            author_attrib_elem = self.schema.xpath("/x:grammar/x:define/x:element[@name='author']//x:attribute", namespaces=ns)
            author_attributes = [ a.get('name') for a in author_attrib_elem ]

            for key in author_attributes:
                if key in item:
                    author[key] = item[key]
            e = E.author(**author)
            if 'organization' in item:
                e.append(E.organization(item.get('organization')))
            front.append(e)
        #
        front.append(E.date(**date))
        #
        if workgroup:
            front.append(E.workgroup(workgroup))
        #
        abstract = self.section(numlist=["Abstract"], tag='abstract')
        if not abstract is None:
            front.append(abstract)
        #
        while True:
            note = self.note()
            if note is None:
                break
            front.append(note)
        #
        self.read_status_of_memo(workgroup, stream, rfc_number, category, date)
        self.read_copyright(date)

        line = self.skip_blank_lines()
        if line.txt == 'Table of Contents':
            toc = self.section(['Table'], tag='toc')
            self.root.append(ProcessingInstruction('rfc', text='toc="yes"'))

        return front

    def get_first_page_top(self):
        lines_left = []
        lines_right = []
        lines_title = []
        lines_name = []
        pad_len = 64                    # a bit less than 72, to accomodate some older documents
        found_centered = False
        found_blankline = False
        found_rightleft = False
        #
        self.skip_blank_lines()
        while True:
            line, p = self.get_line()
            if line.txt.strip() == "":
                found_blankline = True
                if lines_title and lines_name and found_rightleft:
                    break
                else:
                    continue
            # maybe pad line, to let us recognize centered text
            if len(line.txt) > pad_len:
                pad_len = min(len(line.txt), 72)
                padded = line.txt
            else:
                padded = (line.txt + ' '*pad_len)[:pad_len]
            left, center, right = split_on_large_whitespace(padded)
            if left.lower() in [ "abstract", "table of contents", status_of_memo.lower(), ]:
                self.push_line(line, p)
                break
            if center:
                found_centered = True
                if 'draft-' in center and not ' ' in center:
                    lines_name = Line(line.num, center.strip("[]<>"))
                    assert lines_name[1].startswith('draft-')
                else:
                    lines_title.append(Line(line.num, center))
            else:
                found_rightleft = True
                lines_left.append(Line(line.num, left))
                lines_right.append(Line(line.num, right))
        return lines_left, lines_right, lines_title, lines_name

    def skip_blank_lines(self):
        "Skip over blank lines, ending up before the first non-blank line, or at end of text"
        while True:
            line, p = self.get_line()
            if line is None:
                break
            if not line.txt.strip() == "":
                self.push_line(line, p)
                break
        return line

    #@debug.trace
    def get_line(self):
        "Get the next line, whether blank or not, or None if no more lines."
        if self.p == None:
            self.l += 1
        line = self.lines[self.l] if self.l < len(self.lines) else None
        p = self.p
        if self.p:
            line = Line(line.num, line.txt[self.p:])
            self.p = None
        #debug.show('line')
        #debug.show('line.txt')
        return line, p

    def get_text_line(self):
        "Skip blank lines if any, and return the first non-blank line or None if no more lines"
        while True:
            line, p = self.get_line()
            if not line or not line.txt.strip() == "":
                return line, p

    def prev_line(self):
        return self.lines[self.l-1]

    def get_para(self):
        para = []
        # skip blank lines
        while True:
            line, p = self.get_line()
            if line is None:
                return para
            if not line.txt.strip() == "":
                break
        # collect non-blank lines
        while True:
            para.append(line)
            line, p = self.get_line()
            if line is None:
                break
            if line.txt.strip() == "":
                para.append(line)
                break
        return para


    def next_para(self):
        saved_l = self.l
        saved_p = self.p
        para = self.get_para()
        self.l = saved_l
        self.p = saved_p
        return para

    def next_text(self):
        "Skip blank lines if any, then read lines until new blank line, and return text."
        return para2str(self.next_para())

    #@debug.trace
    def push_line(self, push, pos):
        if not self.lines[self.l].txt[pos:] == push.txt:
            if True:
                debug.show('pos')
                debug.show('self.lines[self.l]')
                debug.show('self.lines[self.l].txt[pos:]')
                debug.show('push')
            assert self.lines[self.l].txt[pos:] == push.txt
        if pos:
            self.p = pos
        else:
            self.l -= 1

    #@debug.trace
    def push_part(self, push, pos):
        if not self.lines[self.l] == push:
            if True:
                debug.show('self.lines[self.l]')
                debug.show('self.lines[self.l].txt[self.p:]')
                debug.show('push')
            assert self.lines[self.l] == push
        self.p = pos

    #@debug.trace
    def push_para(self, para):
        para.reverse()
        for line in para:
            self.push_line(line, 0)

    def parse_top_left(self, lines):
        """
        Parse the top left of a draft or RFC.

        Xml2Rfc renders top left elements in this order:
        - workgroup or 'Network Working Group' if draft else stream-name
        - 'Internet-Draft' or RFC number
        - maybe series_name: series_number
        - maybe obsoletes note
        - maybe updates note
        - intended status or category
        - expiration note if draft
        - maybe ISSN number if rfc
        """
        workgroup = stream = series_number = rfc_number = status = expires = None
        obsoletes = []
        updates = []
        # Get workgroup or stream
        submission_types = {
            'Network Working Group':                    None,
            'Internet Engineering Task Force (IETF)':   'IETF',
            'Internet Architecture Board (IAB)':        'IAB',
            'Internet Research Task Force (IRTF)':      'IRTF',
            'Independent Submission':                   'independent',
        }
        line = lines.pop(0) if lines else Line(None, "")
        if line.txt in submission_types.keys():
            stream = submission_types[line.txt]
            if self.is_draft and stream != None:
                self.warn(line.num, "The input document is named '%s' but has an RFC stream type:\n  '%'" % (self.name, line.txt))
        else:
            workgroup = line.txt
            stream = None
            if not self.is_draft:
                self.warn(line.num, "Unrecognized stream indicator in document top left: '%s'" % line.txt)
                
        # get internet-draft or RFC number
        line = lines.pop(0) if lines else Line(None, "")
        if self.is_draft and not line.txt == 'Internet-Draft':
            self.warn(line.num, "Expected to see 'Internet-Draft', found '%s'" % line.txt)
        if self.is_rfc:
            rfc_string = 'Request for Comments:'
            if not line.txt.startswith(rfc_string):
                self.warn(line.num, "Expected to see '%s ...', found '%s'" % (rfc_string, line.txt))
                rfc_number = "XXXX"
            else:
                rfc_number = line.txt.split()[3]
                if not rfc_number.isdigit():
                    self.warn(line.num, "Expected a numeric RFC number, found '%s'" % rfc_number)
            
        # maybe get series name and number
        line = lines.pop(0) if lines else Line(None, "")
        series_names = {
            'STD:': 'std',
            'BCP:': 'bcp',
            'FYI:': 'fyi',
        }
        if self.is_rfc:
            w = line.txt.split()[0]
            if w in series_names:
                series_name = series_names[w]
                series_number = line.txt.split(None, 1)[-1]
                line = lines.pop(0) if lines else Line(None, "")

        # maybe obsoletes and/or updates note
        while True:
            w = line.txt.lower().split()[0].rstrip(':')
            W = w.capitalize()
            if w in ['obsoletes', 'updates']:
                if not line.txt.startswith('%s:' % W):
                    warn(line, "Expected the %s notice to start with '%s:', found '%s'" % (w, W, line.txt))
                if self.is_draft and not '(if approved)' in line.txt:
                    self.warn(line.num, "Expected the %s notice to end with '(if approved)', found '%s'" % (w, line.txt))
                numbers = line.txt.split()[1:]
                while True:
                    num_list = [ n for n in numbers if n.isdigit() ]
                    if w == 'obsoletes':
                        obsoletes += num_list
                    if w == 'updates':
                        updates += num_list
                    line = lines.pop(0) if lines else Line(None, "")
                    # 3 spaces here is arbitraty; this should maybe be ' '*min([len('obsoletes'), len('updates')]) or just ' '
                    if line.txt.startswith('   '):
                        numbers = line.txt.split()
                    else:
                        break
            else:
                break

        # maybe intended status or category
        category_names = {
            'Standards Track':          'std',
            'Best Current Practice':    'bcp',
            'Experimental':             'exp',
            'Informational':            'info',
            'Historic':                 'historic',
        }
        if self.is_draft:
            if line.txt.startswith('Intended status: '):
                status_text = line.txt.split(None, 2)[-1].strip()
                if not status_text in category_names:
                    warn(line, "Expected a recognized status name, found '%s'" % (w, line.txt))
                else:
                    status = category_names[status_text]
                line = lines.pop(0) if lines else Line(None, "")
        else:
            if line.txt.startswith('Category: '):
                status_text = line.txt.split(None, 1)[-1].strip()
                if not status_text in category_names:
                    warn(line, "Expected a recognized category, found '%s'" % (w, line.txt))
                else:
                    status = category_names[status_text]
                line = lines.pop(0) if lines else Line(None, "")

        # maybe expiration date
        if self.is_draft:
            if line.txt.startswith('Expires: '):
                try:
                    expires = parse_date(line.txt.split(None, 1)[-1])
                except RuntimeError as e:
                    self.warn(line.num, e)
                line = lines.pop(0) if lines else Line(None, "")
            else:
                self.warn(line.num, "Expected an expiration date, found '%s'" % (line.txt,))

        if self.is_rfc and line.txt:
            if line.txt.strip() == 'ISSN: 2070-1721':
                pass
            else:
                self.warn(line.num, "Expected an ISSN number, found '%s'" % (line.txt, ))

        for line in lines:
            if line.txt.strip():
                self.warn(line.num, "Did not expect any more top left text, found '%s'" % (line.txt, ))

        return workgroup, stream, series_number, rfc_number, obsoletes, updates, status, expires

    def parse_top_right(self, lines):
        aux = {
            "honor" : r"(?:[A-Z]\.|Dr\.?|Dr\.-Ing\.|Prof(?:\.?|essor)|Sir|Lady|Dame|Sri)",
            "prefix": r"([Dd]e|Hadi|van|van de|van der|Ver|von|[Ee]l)",
            "suffix": r"(jr.?|Jr.?|II|2nd|III|3rd|IV|4th)",
            #"first" : r"([A-Z][-A-Za-z]*)(( ?\([A-Z][-A-Za-z]*\))?(\.?[- ]{1,2}[A-Za-z]+)*)",
            "first" : r"((?:[A-Z](?:-?[A-Z])?\. ?)+)",
            #"last"  : r"([-A-Za-z']{2,})",
            "last"  : r"((%(prefix)s )?[A-Z][a-z]+([- ]?[A-Z][a-z]+)?)",
            "months": r"(January|February|March|April|May|June|July|August|September|October|November|December)",
            "mabbr" : r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?",
            }
        authorformats = [
           r"^(%(first)s%(last)s)$" % aux,
            #r"^((%(first)s[ \.]{1,3})+((%(prefix)s )?%(last)s)( %(suffix)s)?)(, ([^.]+\.?|\([^.]+\.?|\)))?,?$" % aux,
            #r"^(((%(prefix)s )?%(last)s)( %(suffix)s)?, %(first)s)$" % aux,
            #r"^(%(last)s)$" % aux,
        ]
        editorformats = [
            r"(?:, | )([Ee]d\.?|\([Ee]d\.?\)|[Ee]ditor)$",
        ]

        dateformat = r"(((%(months)s|%(mabbr)s) |(%(months)s|%(mabbr)s) \d+, |\d+ (%(months)s|%(mabbr)s),? |\d+/\d+/)\d\d\d\d|\d\d\d\d-\d\d-\d\d)$" % aux
        #
        self.authors = []
        date = None
        #debug.pprint('lines')
        for line in lines:
            #debug.show('line')
            txt = line.txt
            is_editor = False
            if date and txt.strip() != '':
                self.warn(line.num, "Unexpected text; expected blank lines after document date, found '%s'" % (line, ))
                continue
            for regex in editorformats:
                if re.search(regex, txt):
                    txt = re.sub(regex, "", txt)
                    #debug.say('found editor')
                    #debug.show('txt')
                    is_editor = True
                    break
            for regex in authorformats:
                match = re.search(regex, txt)
                if match:
                    author = {
                        'fullname': match.group(1),
                        'initials': match.group(2),
                        'surname':  match.group(3),
                    }
                    if is_editor:
                        author['role'] = 'editor'
                    #debug.show('author')
                    #debug.show('regex')
                    self.authors.append(author)
                    break
            else:
                if re.search(dateformat, txt):
                    date = parse_date(txt)
                    continue
                else:
                    organization = txt
                    #debug.show('organization')
                    #debug.show('len(self.authors)')
                    for i in range(len(self.authors)-1, 0-1, -1):
                        #debug.show('i')
                        #debug.show('self.authors[i]')
                        a = self.authors[i]
                        if a.get('organization') != None:
                            break
                        self.authors[i]['organization'] = organization
        #debug.show('authors')
        #debug.show('date')
        return self.authors, date

    def note(self):
        "An element similar to section, but simpler; containing only t+"
        note = None
        line = self.skip_blank_lines()
        text = line.txt.strip()
        if text == status_of_memo:
            return None
        # Advance past the line we peeked at above
        line, p = self.get_line()
        note = Element('note')
        note.set('title', text)
        while True:
            paragraph = self.get_block()
            if paragraph is None:
                break
            elif paragraph.tag != 't':
                self.err(self.l, "Unexpected content: expected content mapping to <t>, found <%s>" % paragraph.tag)
            else:
                note.append(paragraph)
        return note

    #@debug.trace
    def read_status_of_memo(self, workgroup, stream, rfc_number, category, date):
        self.skip(status_of_memo)
        if self.is_rfc:
            assert stream
            assert rfc_number
            assert category
            consensus = None
            # Status of memo paragraph 1
            self.skip(boilerplate['status'][category].get('p1', None))
            # Status of memo paragraph 2, first sentence
            self.skip(boilerplate['status'][category].get('p2', None))
            # Status of memo paragraph 2, middle part
            text = self.next_text()
            for part in boilerplate['status'].keys():
                if part.startswith(stream):
                    bp = boilerplate['status'][part]
                    if '_workgroup' in part:
                        bp = bp % workgroup
                    if match_boilerplate(bp, text):
                        consensus = '_consensus' in part
                        self.skip(bp)
                        break
            if not consensus is None:
                self.root.set('consensus', 'yes' if consensus else 'no')

            # Status of memo paragraph 2, last sentence
            text = self.next_text()
            repl = 'RFC 5741' if 'RFC 5741' in text else 'RFC 7841'
            if stream == 'IETF' and category == 'std':
                self.skip(boilerplate['status']['p2end_ietf_std'].replace('RFC 7841', repl))
            elif stream == 'IETF' and category == 'bcp':
                self.skip(boilerplate['status']['p2end_ietf_bcp'].replace('RFC 7841', repl))
            elif stream == 'IETF':
                self.skip(boilerplate['status']['p2end_ietf_other'].replace('RFC 7841', repl))
            else:
                self.skip(boilerplate['status']['p2end_other'].replace('RFC 7841', repl) % approvers.get(stream, ''))

            self.skip(boilerplate['status']['p3'] % rfc_number)
        else:
            text = self.next_text()
            if text:
                ipr_date = None
                for part, d in [ ('ipr_200902_status', '200902'), ('ipr_200811_status', '200811'), ]:
                    bp = boilerplate[part]
                    if match_boilerplate(bp, text):
                        ipr_date = d
                        self.skip(bp)
                        break
            for text in boilerplate['status']['draft']:
                self.skip(text)
            text = self.next_text()
            bp = boilerplate['draft_expire'][:-3]
            if match_boilerplate(bp, text):
                expires = text[len(bp):-1]
                exp_date = parse_date(expires)
                self.skip(boilerplate['draft_expire'] % expires)

    def read_copyright(self, date):
        assert date
        self.skip('Copyright Notice')
        self.skip(boilerplate['base_copyright_header'] % date['year'])
        self.skip(boilerplate['base_copyright_body'])
        text = self.next_text()
        if text and text.startswith(boilerplate['ipr_200902_copyright_ietfbody'][:32]):
            self.skip(boilerplate['ipr_200902_copyright_ietfbody'])
        text = self.next_text()
        if text and text.startswith(boilerplate['ipr_pre5378Trust200902_copyright'][:32]):
            self.skip(boilerplate['ipr_pre5378Trust200902_copyright'])
            self.root.set('ipr', 'pre5378Trust200902')

    #@debug.trace
    def read_authors_addresses(self):
        line = self.skip_blank_lines()
        if line and (line.txt.startswith("Author's Address") or  line.txt.startswith("Authors' Addresses")):
            self.skip(line.txt)
        else:
            self.err(line.num, "Expected an Authors' Addresses section, but found '%s'" % (line.txt, ))
            return
        while True:
            # Fullname (Role)
            # [Organization]
            # [Address]
            #                       # (blank line)
            # [Phone: number]
            # [Fax: number]
            # [Email: address]      # or EMail
            # [URI: uri]
            #
            line = self.skip_blank_lines()
            if not line or is_section_start(line):
                break
            #
            item = self.read_author_name()
            self.maybe_author_org(item)
            self.maybe_author_address(item)
            line, p = self.get_line()
            assert line.txt.strip() == ''
            while True:
                found = self.maybe_address_detail(item)
                if not found:
                    break
        #
        for author in self.authors:
            auth = self.root.find(".//author[@surname='{surname}'][@initials='{initials}']".format(**author))
            auth.set('fullname', author['fullname'])
            addr = Element('address')
            auth.append(addr)
            for key in ['postal', 'phone', 'facsimile', 'email', 'uri', ]:
                if key in author['address']:
                    value = author['address'][key]
                    if key == 'postal':
                        e = Element(key)
                        for line in value:
                            street = Element('street')
                            street.text = line
                            e.append(street)
                        addr.append(e)
                    else:
                        e = Element(key)
                        e.text = value
                        addr.append(e)

    #@debug.trace
    def skip(self, expect):
        "Read, match, and skip over the given text."
        self.skip_blank_lines()
        line, p = self.get_line()
        text = line.txt
        l = len(text)
        text = text.lstrip()
        strip_count = l - len(text)
        expect = expect.lstrip()
        def fail(l, e, t):
            self.err(l.num, "Unexpected text: expected '%s', found '%s'" % (e, t))
        while True:
            el = len(expect)
            tl = len(text)
            #debug.show('el')
            #debug.show('expect')
            #debug.show('tl')
            #debug.show('text')
            if   el < tl:
                if expect == text[:el]:
                    self.push_part(line, el+strip_count)
                    break
                else:
                    fail(line, expect, text)
            elif tl < el:
                if expect[:tl] == text:
                    line, p = self.get_line()
                    text = line.txt
                    l = len(text)
                    text = text.strip()
                    strip_count = l - len(text)
                    expect = expect[tl:].lstrip()
                else:
                    fail(line, expect, text)
            else:                       # el == tl
                if expect[:tl] == text:
                    break
                else:
                    fail(line, expect, text)
        return True

    #@debug.trace
    def read_author_name(self):
        line, p = self.get_line()
        if line is None:
            err(self.lines[-1].num, "Expected an author's name, but found end of file")
        name = line.txt.strip()
        item = match_name(name, self.authors)
        if item:
            item['fullname'] = name.replace(' (editor)','')
        return item

    def maybe_author_org(self, item):
        line, p = self.get_line()
        if line is None:
            return None
        text = line.txt.strip()
        if text == '':
            self.push_line(line, p)
        
    #@debug.trace
    def maybe_author_address(self, item):
        address = []
        while True:
            line, p = self.get_line()
            if line is None:
                break
            text = line.txt.strip()
            if text == '' or text.split()[0] in address_details:
                self.push_line(line, p)
                break
            address.append(line.txt.strip())
        item['address'] = {}
        if address:
            item['address']['postal'] = address
        return item
        
    #@debug.trace
    def maybe_address_detail(self, item):
        line, p = self.get_line()
        if line is None:
            return None
        text = line.txt.strip()
        if text == '':
            self.push_line(line, p)
            return None
        try:
            label, value = text.split(None, 1)
        except ValueError:
            self.push_line(line, p)
            return None
        if label in address_details:
            key = address_details[label]
            item['address'][key] = value
        else:
            self.push_line(line, p)
            return None
        return item

    # ------------------------------------------------------------------------
    # middle
    # ------------------------------------------------------------------------
    #@debug.trace
    def middle(self):
        # section+
        middle = Element('middle')
        self.section_number = 1
        while True:
            section = self.section(numlist=[ str(self.section_number) ])
            if section is None:
                break
            middle.append(section)
            self.section_number += 1
        return middle

    #@debug.trace
    def section(self, numlist=["1"], level=0, tag='section', appendix=False):
        # (t | figure | texttable | iref)*, section*
        # figure out what a section number for this section is expected to
        # look like:
        #
        section = None
        line, p = self.get_text_line()
        if line is None:
            return None
        # Expect the start of a section: section number and title
        number, title = parse_section_start(line, numlist, level, appendix)

        if is_section_start(line, numlist):
            if len(numlist)==1 and title in ['References', 'Normative References', 'Informative References', 'Informational References', 'URIs', ]:
                self.push_line(line, p)
                return None
            # Get title continuation lines
            titleindent = line.txt.find(title)
            while True:
                next, p = self.get_line()
                if next.txt.strip() == '':
                    self.push_line(next, p)
                    break
                if ind(next) == titleindent:
                    title += ' ' + next.txt.strip()
                else:
                    self.err(next.num, "Unexpected indentation: Expected a title continuation line with indentation %s, but got '%s'" % (titleindent, next.txt))
            section = Element(tag)
            if tag == 'section':
                section.set('title', title)
                section.set('anchor', 'section-%s'%number)
        else:
            if number in ["Author's", "Authors'", "Acknowledgements", "Appendix", "Annex", "Contributors", "Index", ]:
                self.push_line(line, p)
                return None
            self.err(line.num, "Unexpected section number; expected '%s' or a subsection, found '%s'" % ('.'.join(numlist), number))
        #
        blank_line, p = self.get_line()
        if not blank_line.txt.strip() == '':
            self.warn(blank_line.num, "Unexpected text; expected a blank line after section title, found '%s'" % (blank_line, ))
            self.push_line(line, p)
        while True:
            paragraph = self.get_block()
            if paragraph is None:
                break
            else:
                section.append(paragraph)
        num = 0
        while True:
            # section*
            num += 1
            sublist = numlist + [ str(num) ]
            line, p = self.get_text_line()
            if is_section_start(line, sublist):
                self.push_line(line, p)
                subsection = self.section(sublist, level+1, appendix=appendix)
                if subsection is None:
                    break
                else:
                    section.append(subsection)
            else:
                self.push_line(line, p)
                break

        return section


    #@debug.trace
    def get_block(self):
        """
        This method does not parse and return one specific element type;
        it encapsulates the (t | figure | texttable | iref) alternatives
        which occur in <section>.
        """
        tag2label = {
            'figure': 'Figure',
            'texttable': 'Table',
        }
        #
        ##self.skip_blank_lines()
        block = []
        # Collect related sections with embedded blank lines, like lists
        tag = None
        element = None
        while True:
            # collect one block worth of text
            para = self.get_para()
            first = para[0].txt.strip()
            this_tag, text, linecount = self.identify_paragraph(para)
            #if not this_tag in ['t', 'figure', 'texttable', 'list', ]:
            if not this_tag in ['t', 'figure', 'texttable', 'list', ]:
                self.push_para(para)
                break
            if tag in ['figure', 'texttable']:
                expected = tag2label[tag]
                othertag = 'figure' if tag=='texttable' else 'texttable'
                unexpected = tag2label[othertag]
                if first.startswith(expected):
                    # label
                    block.append(para)
                    break
                elif first.startswith(unexpected):
                    self.warn(para[0].num, "Unexpected title: expected '%s ...', but found '%s'.  This looks like a %s that has been entered as a %s.  The generated XML will need adjustment." % (expected, first, tag, othertag))
                    self.push_para(para)
                    break
                elif linecount == 1 and len(block) == 1 and not '  ' in first:
                    # postamble, continue looking for a label
                    this_tag = tag
                else:
                    # somethig which is not part of the figure or table
                    self.push_para(para)
                    break
            elif tag and this_tag != tag:
                self.push_para(para)
                break
            block.append(para)
            tag = this_tag
            # break here unless this is a type with embedded blank lines:
            if not this_tag in ['figure', 'texttable', 'list', ]:
                break
            if tag in ['figure', 'texttable'] and len(block) >= 3:
                break
        if block and tag:
            flat = flatten(block)
            text = '\n'+para2text(flat)
            if tag == 'list':
                for b in block:
                    if re.search(code_re, b[0].txt):
                        # in vocabulary v3 this will be 'sourcecode'
                        tag = 'figure'
                        block = [ flat ]
                        #debug.pprint('block')
                        break
            if tag in ['figure', 'texttable']:
                label = para2str(block[-1])
                expected = tag2label[tag]
                if label.startswith(expected):
                    block.pop()
                else:
                    label = None
                assert len(block) in [1,2]
            if tag == 't':
                element = Element('t')
                element.text = text
            elif tag == 'list':
                element = Element('t')
                element.append(self.make_list(block))
            elif tag == 'section':
                self.push_para(para)
            elif tag == 'texttable':
                element = self.make_table(block, label)
            elif tag == 'figure':
                element = self.make_figure(block, label)

        return element

    #@debug.trace
    def parse_text(self, text):
        "A sequence of text, xref, and eref elements."
        quotes = {
            '"': '"',
            "'": "'",
        }
        angles = {
            '<': '>',
        }
        squares = {
            '[': ']'
        }
        endq = dict( (k,v) for (k,v) in quotes.items()+angles.items()+squares.items() )
        # ----
        def get_quoted(stack, tok):
            """
            Get quoted or bracketed string. Does not handle nested instances.
            """
            chunk = tok
            qbeg = tok
            qend = endq[tok]
            prev = ''
            while True:
                tok = stack.pop()
                if tok is None:
                    break
                elif tok and tok[0] == '\n':
                    tok = nl(stack, prev)
                elif tok == qbeg and not tok in quotes:
                    tok = get_quoted(stack, tok)
                chunk += tok
                if tok == qend:
                    break
                prev = tok
            return chunk
        def nl(stack, prev):
            "Found a newline.  Process following whitespace and return an appropriate token."
            lastchar = prev[-1] if prev else ''
            while True:
                tok = stack.pop()
                if tok is None:
                    break
                if tok.strip() != '':
                    stack.push(tok)
                    break
            tok = '' if lastchar in ['-', '/', ] else ' '
            return tok
        # ----
        stack = Stack(text)
        chunks = []
        prev = ""
        while True:
            tok = stack.pop()
            if tok is None:
                break
            if tok in quotes:
                tok = get_quoted(stack, tok)
            elif tok in squares:
                tok = get_quoted(stack, tok)
                target = tok[1:-1]
                if target in self.reference_list:
                    tok = Element('xref', target=target)
            elif tok in angles:
                tok = get_quoted(stack, tok)
                match = re.search(uri_re, tok)
                if match:
                    target= match.group('target')
                    tok = Element('eref', target=target)
            elif re.search(uri_re, tok):
                match = re.search(uri_re, tok)
                target= match.group('target')
                tok = Element('eref', target=target)
            elif tok == '\n':
                tok = nl(stack, prev)
            chunks.append(tok)
            prev = tok
        t = Element('t')
        if chunks:
            e = None
            text = []
            for chunk in chunks:
                if isinstance(chunk, six.string_types):
                        text.append(chunk)
                else:
                    if e is None:
                        t.text = ''.join(text)
                    else:
                        e.tail = ''.join(text)
                    text = []
                    e = chunk
                    t.append(e)
            if text:
                if e is None:
                    t.text = ''.join(text)
                else:
                    e.tail = ''.join(text)
        return t

    #@debug.trace
    def identify_paragraph(self, para):
        tag = None
        text = None
        sratio = None
        linecount = 0
        if para and para[0].txt:
            line = para[0]
            text = para2text(para)
            if is_section_start(line):
                tag = 'section'
            elif not line.txt.startswith('   '):
                tag = None
            else:
                # we want to distinguish between:
                # * figure
                # * list
                #   - numbers
                #   - letters
                #   - symbols
                #   - hanging
                #   - empty
                # * texttable
                #   - none      no borders
                #   - headers   border between headers and data, and beg/end
                #   - full      like headers + frame + vertical borders
                #   - all       like full + horizontal between data cells
                # * plain text, <t>
                indents = indentation_levels(para)
                border_set = set(table_borders(para))
                linecount = len(text.split('\n'))
                sratio = symbol_ratio(text)
                if False:
                    debug.say('------')
                    debug.show('indents')
                    debug.show('linecount')
                    debug.show('sratio')
                    debug.pprint('border_set')
                if not '----' in text and (sratio < 0.3 or (sratio < 0.8 and linecount==1)):
                    next = self.next_para()
                    if ( len(indents) > 1 or indents[0] != 3 
                        or (linecount == 1 and line.txt.strip()[:2] in ['o ', '* ', '+ ', '- ', ]) 
                        or (linecount == 1 and re.search('^[0-9a-z][ivx]*\. ', line.txt.strip()))
                        #or (linecount == 1 and not ' ' in line.txt.strip())
                        or (linecount == 1 and (  ind(next[0]) > ind(para[0]) ))
                        or ('  ' in line.txt.strip() and not '.  ' in line.txt.strip())
                        ):
                        tag = 'list'
                    else:
                        tag = 't'
                elif len(indents) > 1:
                    # uneven indentation; it's not a table (well, could
                    # be texttable with style none|headers and center or
                    # righ align on the first column, but we ignore that)
                    tag = 'figure'
                else:
                    if len(border_set) == 2 and not '+-+-+' in text and line.txt.strip() in border_set:
                        tag = 'texttable'
                    else:
                        tag = 'figure'
        return tag, text, linecount

    def make_figure(self, block, title):
        figure = Element('figure')
        if title and title.startswith('Figure'):
            __, num, title = title.split(None, 2)
            num = num.replace(':','')
            figure.set('title', title)
            figure.set('anchor', 'figure-%s'%num)
        text = para2text(block.pop(0))
        artwork = Element('artwork')
        artwork.text = CDATA('\n'+unindent(text, 3)+'\n')
        figure.append(artwork)
        if block:
            text = para2text(block.pop(0))
            postamble = Element('postamble')
            postamble.text = text
            figure.append(postamble)
        assert block == []
        return figure

    def make_table(self, block, title):
        paragraph = block.pop(0)
        first_line = paragraph[0]
        # figure out the table characteristics
        borders = table_borders(paragraph)
        # styles:
        #   none:
        #       Foo  Bar  Baz
        #       One  2    Three
        #       Two  2    Four
        #
        #   headers:
        #       ---- ---- -----
        #       Foo  Bar  Baz
        #       ---- ---- -----
        #       One  2    Three
        #       Two  2    Four
        #
        #   full:
        #       +-----+-----+------+
        #       | Foo | Bar | Baz  |
        #       +-----+-----+------+
        #       | One | 2   | Three|
        #       | Two | 2   | Four |
        #       +-----+-----+------+
        #
        #   all:
        #       +-----+-----+------+
        #       | Foo | Bar | Baz  |
        #       +-----+-----+------+
        #       | One | 2   | Three|
        #       +-----+-----+------+
        #       | Two | 2   | Four |
        #       +-----+-----+------+
        #
        if   borders[0][0] == '-':
            style = 'headers'
        else:
            style = 'full'
        ## Ignore 'none' and 'all' for now
        # find a horizontal border
        for border in borders:
            if '-' in border:
                break
        # find a line with that border, and the table column start positions
        columns = None
        for line in paragraph:
            if border in line.txt:
                indent = line.txt.find(border)
                sep = '+' if '+' in border else ' '
                if sep == '+':
                    columns = line.txt.split(sep)[1:-1]
                else:
                    columns = border.split(sep)
                break
        if not columns:
            self.err(first_line.num, "Malformed table, expected table to start with a border, but found '%s'"%(first_line.txt, ))
        colwidth = [ len(c)+1 for c in columns ]
        colpos = [ indent ]
        pos = indent
        for w in colwidth:
            pos += w
            colpos.append(pos)
        # --- Process the table, generate xml elements ---
        texttable = Element('texttable')
        if title:
            if title.startswith('Table'):
                __, num, title = title.split(None, 2)
                num = num.replace(':','')
                texttable.set('title', title)
                texttable.set('anchor', 'table-%s'%num)
        texttable.set('style', style)
        # skip top border
        line = paragraph.pop(0)
        assert border in line.txt
        # collect header text until next border
        headers = ['']*len(columns)
        while True:
            line = paragraph.pop(0)
            if border in line.txt:
                break
            txt = line.txt.replace('|', ' ')
            columns = colsplit(colpos, txt)
            headers = [ ' '.join(t) for t in zip(headers, columns) ]
        # generate <ttcol>
        for h in headers:
            ttcol = Element('ttcol')
            ttcol.text = h
            texttable.append(ttcol)
        # collect table cells and generate <c>
        while paragraph:
            line = paragraph.pop(0)
            if border in line.txt:
                continue
            txt = line.txt.replace('|', ' ')
            columns = colsplit(colpos, txt)
            for t in columns:
                c = Element('c')
                c.text = t
                texttable.append(c)
        if block:
            text = para2text(block.pop())
            postamble = Element('postamble')
            postamble.text = text
            texttable.append(postamble)
        assert block == []
        return texttable

    def make_list(self, block, base_indentation=3):
        #list[style, hangIndent, counter] : t+
        # style = (numbers|letters|symbols|hanging|empty|format:...)
        # t[hangText] 
        #
        if False:
            debug.say('------------------------------------------------------------------------')
            debug.pprint('block')
        #indents = indentation_levels(flatten(block))
        #debug.show('len(indents)')
        #if len(indents) > 2:
        items = normalize_list_block(block)
        #debug.pprint('items')
        indents = indentation_levels(flatten(block))
        list = Element('list')
        #
        if False:
            debug.pprint('items')
            debug.pprint('indents')
            debug.show('base_indentation')
        #
        item = items[0]
        if indents[0] > base_indentation and (len(item) == 1 or len(indentation_levels(item)) > 1):
            # handle extra indentation by adding an extra level of <t/><list/>
            list.set('hangIndent', str(indents[0]-base_indentation))
            list.text = ' '
            t = Element('t')
            t.tail = '\n'
            t.append(self.make_list(block, base_indentation=indents[0]))
            list.append(t)
        else:
            set_style = None
            t = None
            for i, item in enumerate(items):
                # check for sublist
                if type(item[0]) == type([]):
                    assert t is not None
                    line = item[0][0]
                    t.append(self.make_list(item, ind(line)))
                    t.tail = '\n'
                else:
                    line = item[0]
                    indent = indentation_levels(item)
                    first = line.txt
                    style, marker, rest = guess_list_style(line)
                    if style and i == 0:
                        list.set('style', style)
                        if style == 'hanging' and len(indent) > 1:
                            list.set('hangIndent', str(indent[1] - indent[0]))
                    t = Element('t')
                    t.tail = '\n'
                    if style == 'hanging':
                        if indent[0] == indents[0]:
                            t.set('hangText', marker)
                            # Handle hanging lists with no item text on the first line
                            if rest == '':
                                list.append(t)
                                t = Element('t')
                                t.tail = '\n'
                            text = '\n'.join( [ tt for tt in [ rest ]+[ l.txt for l in item[1:]] if tt] )
                        else:
                            text = '\n'.join( [ tt for tt in [marker, rest ]+[ l.txt for l in item[1:]] if tt] )
                    else:
                        text = '\n'.join( [ tt for tt in [ rest ]+[ l.txt for l in item[1:]] if tt] )                        
                    t.text = text
                    list.append(t)
        return list



    # ------------------------------------------------------------------------
    # back
    # ------------------------------------------------------------------------
    def back(self):
        back = Element('back')
        while True:
            references = self.references([ str(self.section_number) ])
            if references is None:
                break
            for refs in references:
                back.append(refs)
            self.section_number += 1
        # maybe read the eref section
        line = self.skip_blank_lines()
        parts = line.txt.split()
        if len(parts)>1 and parts[1] == 'URIs':
            section = self.section([str(self.section_number-1), str(len(refs)+1)])
        #
        num = ord('A')
        while True:
            line = self.skip_blank_lines()
            section = self.section(numlist=[ chr(num) ], appendix=True)
            if section is None:
                break
            back.append(section)
            num += 1
        #
        while True:
            # other sections
            line = self.skip_blank_lines()
            word = line.txt.split()[0]
            if word in ['Acknowledgements', 'Contributors', 'Index', ]:
                section = self.section([word])
                back.append(section)
            else:
                break
        #
        self.read_authors_addresses()

        return back

    def references(self, numlist, level=0):
        refs = []
        # peek at the first nonblank line
        line, p = self.get_text_line()
        if not is_section_start(line, numlist):
            self.push_line(line, p)
            return None
        #
        number, title = parse_section_start(line, numlist, level, appendix=False)
        if not title in ['References', 'Normative References', 'Informative References', 'Informational References', 'Normative', 'Informative',]:
            self.push_line(line, p)
            return None
        # peek at the next nonblank line
        line = self.skip_blank_lines()
        if is_section_start(line):
            num = 1
            while True:
                sublist = numlist + [ str(num) ]
                references = self.references(sublist, level+1)
                if references is None:
                    break
                refs += references
                num += 1
            return refs
        else:
            references = Element('references', title=title)
            refs.append(references)
            # a series of reference entries
            while True:
                ref = self.reference()
                if ref is None:
                    break
                references.append(ref)
            return refs
        return None

    def reference(self):
        line = self.skip_blank_lines()
        if is_section_start(line):
            return None
        reference = Element('reference')
        front = Element('front')
        reference.append(front)
        para = self.get_para()
        line = para[0]
        if not para:
            return None
        text = para2str(para)
        faild = None
        for regex in reference_patterns:
            match = re.search(regex, text)
            if match:
                if faild and False:
                    debug.show('text')
                    debug.show('faild')
                    debug.show('regex')
                    debug.pprint('match.groups()')
                    debug.pprint('match.groupdict()')
                #
                refinfo = match.groupdict()
                # Attributes
                for key in ['anchor', 'target', ]:
                    value = refinfo.get(key)
                    if value:
                        reference.set(key, value)
                # Front matter
                key = 'title'
                value = refinfo.get(key)
                e = Element(key)
                if value:
                    e.text = value
                front.append(e)
                # Author info
                if 'authors' in refinfo:
                    authors = refinfo.get('authors')
                    if authors:
                        ed = ', Ed.'
                        if ' and ' in authors:
                            first, last = authors.split(' and ', 1)
                        else:
                            first, last = authors, None
                        for author in re.findall(ref_name_re, first):
                            editor = author.endswith(ed)
                            if editor:
                                author = author[:-len(ed)]
                            surname, initials = author.split(', ', 1)
                            e = Element('author', initials=initials, surname=surname, fullname=' '.join([initials, surname]))
                            if editor:
                                e.set('role', 'editor')
                            front.append(e)
                        if last:
                            author = last
                            editor = author.endswith(ed)
                            if editor:
                                author = author[:-len(ed)]
                            initials, surname = author.split(None, 1)
                            e = Element('author', initials=initials, surname=surname, fullname=' '.join([initials, surname]))
                            if editor:
                                e.set('role', 'editor')
                            front.append(e)
                elif 'organization' in refinfo:
                    organization = refinfo.get('organization')
                    e = Element('author')
                    org = Element('organization')
                    org.text = organization
                    e.append(org)
                    front.append(e)
                else:
                    e = Element('author')
                    front.append(e)
                key = 'date'
                value = refinfo.get(key)
                if value:
                    if ' ' in value:
                        month, year = value.split(None, 1)
                        e = Element(key, month=month, year=year)
                    else:
                        e = Element(key, year=value)                        
                else:
                    e = Element(key)
                front.append(e)
                # Document / Series
                if 'series' in refinfo:
                    series  = refinfo.get('series')
                    if series:
                        for item in re.findall(ref_series_one, series):
                            name, value = item.split(None, 1)
                            e = Element('seriesInfo', name=name, value=value)
                            reference.append(e)
                            if name == 'RFC':
                                self.entities.append({'name': refinfo.get('anchor'),
                                    'url': 'https://xml.ietf.org/public/rfc/bibxml/reference.RFC.%s.xml'%value, })
                            if name == 'Internet-Draft':
                                self.entities.append({'name': refinfo.get('anchor'),
                                    'url': 'https://xml.ietf.org/public/rfc/bibxml3/reference.I-D.%s.xml'%value, })
                            reference.append(e)
                elif 'docname' in refinfo:
                    docname = refinfo.get('docname')
                    if docname:
                        name, value = docname.split(None, 1)
                        e = Element('seriesInfo', name=name, value=value)
                        reference.append(e)
                #
                break
            else:
                faild = regex
        else:
            if not line or is_section_start(line) or line.txt.startswith('Author'):
                self.push_para(para)
                return None
            else:
                self.warn(line.num, "Failed parsing a reference:\n%s" % para2text(para))
                return reference

        return reference

    # ------------------------------------------------------------------------
    # postprocess
    # ------------------------------------------------------------------------

    def postprocess(self):
        self.add_text_refs()

    def add_text_refs(self):
        """
        Iterate through all <t> elements, and if they have .text, process
        that to generate a new <t> element with <xref>s and <eref>s.
        """
        self.reference_list = [ r.get('anchor') for r  in self.root.findall('.//reference') ]
        for old in self.root.findall('.//t'):
            if old.text:
                new = self.parse_text(old.text)
                for key in old.keys():
                    value = old.get(key)
                    new.set(key, value)
                for child in old:
                    new.append(child)
                old.getparent().replace(old, new)

if __name__ == '__main__':
    run()
    
