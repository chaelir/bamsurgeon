#!/usr/bin/env python

import pysam
import sys
from re import sub
from random import random

if len(sys.argv) == 2:
    assert sys.argv[1].endswith('.bam')
    inbamfn = sys.argv[1]
    outbam1fn = sub('.bam$', '.pick1.bam', inbamfn)
    outbam2fn = sub('.bam$', '.pick2.bam', inbamfn)

    inbam = pysam.Samfile(inbamfn, 'rb')
    outbam1 = pysam.Samfile(outbam1fn, 'wb', template=inbam)
    outbam2 = pysam.Samfile(outbam2fn, 'wb', template=inbam)

    lastname = None
    lastread = None
    paired = False
    for read in inbam.fetch(until_eof=True):
        if read.qname == lastname:
            paired=True

        if paired:
            rnd = random()
            if rnd > 0.5:
                outbam1.write(read)
                outbam1.write(lastread)
            else:
                outbam2.write(read)
                outbam2.write(lastread)
            lastname = None
            lastread = None
            paired = False

        else:
            lastname = read.qname
            lastread = read

    outbam1.close()
    outbam2.close()
    inbam.close()
else:
    print "usage:",sys.argv[0],"<bam sorted by readname>"
