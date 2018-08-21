#!/usr/bin/env python
import os, base64, time, sys
from subprocess import call
reciver_key_filename=''
sender_cert_filename=''

#base_dir = os.path.abspath('/root/tmp/scripts')
base_dir = r'/root/tmp/scripts/'
file_crypted = sys.argv[1:]
file_crypted_str = " ".join(file_crypted)
#file_signed = [x for x in file_crypted if x.endswith('.enc')]
file_signed = os.path.splitext(file_crypted_str)[0]
#file_signed = filter(lambda x: x.endswith('.enc'), file_crypted)
file_dec = os.path.splitext(file_signed)[0]
reciver_key = os.path.join(base_dir, 'reciver_key_filename')
sender_cert = os.path.join(base_dir, 'sender_cert_filename')

call(['openssl', 'cms', '-decrypt', '-gost89', '-noattr', '-inform', 'DER', '-in', file_crypted_str, '-out', file_signed, '-inkey', reciver_key])

call(['openssl', 'smime', '-ignore_critical', '-CAfile', sender_cert, '-verify', '-noverify', '-inform', 'DER', '-in', file_signed, '-out', file_dec])
