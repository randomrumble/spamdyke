#!/usr/bin/env python

"""
Spamdyke has the ability to log individual email transactions which
include qmail's reception handshake, headers, email body, and connection
resolution. This can be quite useful when debugging various issues. This
scripts acts as a simple parser to these individual logs.

Logging can be enabled in /etc/spamdyke.conf with
  full-log-dir=<path-to-dir>
  
Additional logging can be enabled with:
  log-level=debug
  
"""

import os
import re
import sys
import optparse # lets support older python versions

class SpamdykeEmail(object):

  def __init__(self, log_file):
    self.log_file = log_file
    self._email_lines = []
    self._log_lines = []
    self._parse_start = False
    self._potential_end = False

  def read_log_file(self):
    if os.path.exists(self.log_file):
      f = open(self.log_file)
      return f.readlines()
    return []

  def parse_email(self):
    e = self.read_log_file()
    for l in e:
      if re.search('^(0[1-9]|1[0-2])/[0123][0-9]/\d+ \d+:\d+:\d+', l):
        self._log_lines.append(l.rstrip('\n'))
        if re.search('TO CHILD: 3 bytes', l, re.I):
          self._potential_end = True
      else:
        if self._potential_end == True:
          if l[0] == '.':
            self._parse_start = False
          else:
            self._potential_end = False
        if not self._parse_start:
          self._log_lines.append(l.rstrip('\n'))
        else:
          stripped = l.rstrip('\n')
          if stripped:
            self._email_lines.append(stripped)
      if re.search('354 go ahead', l, re.I):
        self._parse_start = True

  def dump_email(self):
    for l in self._email_lines:
      print r'%s' % l

  def dump_log(self):
    for l in self._log_lines:
      print r'%s' % l

  def write_email(self, file_name):
    self._write_file(file_name, self._email_lines)

  def write_log(self, file_name):
    self._write_file(file_name, self._log_lines)

  def _write_file(self, file_name, lines):
    if os.path.exists(file_name):
      print 'WARNING: File already exists: %s' % file_name
    with open(file_name, 'w') as f:
      for l in lines:
        f.write(l+'\n')
    print 'Wrote %s lines to "%s"' % (len(lines), file_name)


def main():
  parser = optparse.OptionParser(description='Parse spamdyke email debug logs to human readable format')
  parser.add_option("--email-log", metavar='FILE', help="Read spamdyke email debug/log (required)")
  parser.add_option("--write-email", metavar='FILE', help="Save email content to <file>")
  parser.add_option("--write-log", metavar='FILE', help="Save log content output to <file>")
  parser.add_option("--dump-email", default=None, action='store_true', help="Dump email to stdout")
  parser.add_option("--dump-log", default=None, action='store_true', help="Dump log to stdout")
  (vals, options) = parser.parse_args()
  if not vals.email_log:
    parser.print_help()
    print '\nExample: %s --email-log 20160125_205714_13064_1307764874 --dump-email\n' % sys.argv[0]
    sys.exit(1)
  spamdyke = SpamdykeEmail(vals.email_log)
  spamdyke.parse_email()
  if vals.write_email:
    spamdyke.write_email(vals.write_email)
  if vals.write_log:
    spamdyke.write_log(vals.write_log)
  if vals.dump_log:
    spamdyke.dump_log()
  if vals.dump_email or not any([vals.write_log,
                                 vals.write_email,
                                 vals.dump_log]):
    spamdyke.dump_email()

if __name__ == '__main__':
   main()
   
