#!/usr/bin/env python

import sys, os, getopt
import shutil

def remove_data(f):
    try:
        if os.path.isfile(f):
            os.unlink(f)
        else:
            shutil.rmtree(f)
    except:
        pass

def main(root_dir, argv):
    # Initial
    root_dir = os.path.abspath(os.path.dirname(sys.argv[0]) + '/..')

    # Parcing argument
    try:
        opts, args = getopt.getopt(argv, "ch")
    except getopt.GetoptError:
        pass

    if len(opts) > 0 and '-h' in opts[0]:
        print 'gallery-generator.py'
        print "\t-c : clean data"
    elif len(opts) and '-c' in opts[0]:
        # clean system
        print "[start clean]"
        print "\tdelete /photo ..."
        remove_data(root_dir+'/photo');
        print "\tdelete /main/js/config.js ..."
        remove_data(root_dir+'/main/js/config.js');
        print "[clean done]"

    else:
        # TODO preprocessing photos in /raw for fixing size
        print 'Preprocessing for raw photo in /raw ...'
        remove_data(root_dir+'/photo');
        os.makedirs(root_dir+'/photo')
        [ shutil.copy(root_dir+'/raw/'+f, root_dir+'/photo/'+f) for f in os.listdir(root_dir+'/raw') if os.path.isfile(os.path.join(root_dir+'/raw', f)) ]
        print 'Preprocessing for raw photo in /raw ... done'

        # generate file list to main/js/config.js
        print 'Generating file list from /photo ...'
        custom_photo_files = [ f for f in os.listdir(root_dir+'/photo') if os.path.isfile(os.path.join(root_dir+'/photo', f)) ]
        remove_data(root_dir+'/main/js/config.js');
        outfile = open(root_dir+'/main/js/config.js', 'wb+');
        outfile.write('var filelist = ['+"\n");
        outfile.writelines( list( "'%s',\n" % item for item in custom_photo_files[:-1] ) )
        outfile.writelines( "'%s'\n" % custom_photo_files[-1] )
        outfile.write('];\n');
        outfile.close()
        print 'Generating file list from /photo ... done'

if __name__ == '__main__':
    main(os.path.abspath(os.path.dirname(sys.argv[0]) + '/..'), sys.argv[1:])
