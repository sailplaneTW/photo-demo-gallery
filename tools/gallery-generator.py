#!/usr/bin/env python

import sys,os

if __name__ == '__main__':
    # TODO preprocessing photos for fixing size

    # generate file list to main/js/config.js
    print 'Generating file list from /photo ...'
    root_dir = os.path.abspath(os.path.dirname(sys.argv[0]) + '/..')
    onlyfiles = [ f for f in os.listdir(root_dir+'/photo') if os.path.isfile(os.path.join(root_dir+'/photo', f)) ]
    outfile = open(root_dir+'/main/js/config.js', 'wb+');
    outfile.write('var filelist = ['+"\n");
    outfile.writelines( list( "'%s',\n" % item for item in onlyfiles[:-1] ) )
    outfile.writelines( "'%s'\n" % onlyfiles[-1] )
    outfile.write('];\n');
    outfile.close()
    print 'Generating file list from /photo ... done'
