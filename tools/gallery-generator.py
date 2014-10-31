#!/usr/bin/env python

import sys,os
import shutil

if __name__ == '__main__':
    # Initial
    root_dir = os.path.abspath(os.path.dirname(sys.argv[0]) + '/..')

    # TODO preprocessing photos in /raw for fixing size
    print 'Preprocessing for raw photo in /raw ...'
    [ shutil.copy(root_dir+'/raw/'+f, root_dir+'/photo/'+f) for f in os.listdir(root_dir+'/raw') if os.path.isfile(os.path.join(root_dir+'/raw', f)) ]
    print 'Preprocessing for raw photo in /raw ... done'

    # generate file list to main/js/config.js
    print 'Generating file list from /photo ...'
    root_dir = os.path.abspath(os.path.dirname(sys.argv[0]) + '/..')
    custom_photo_files = [ f for f in os.listdir(root_dir+'/photo') if os.path.isfile(os.path.join(root_dir+'/photo', f)) ]
    outfile = open(root_dir+'/main/js/config.js', 'wb+');
    outfile.write('var filelist = ['+"\n");
    outfile.writelines( list( "'%s',\n" % item for item in custom_photo_files[:-1] ) )
    outfile.writelines( "'%s'\n" % custom_photo_files[-1] )
    outfile.write('];\n');
    outfile.close()
    print 'Generating file list from /photo ... done'
