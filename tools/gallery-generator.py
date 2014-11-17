#!/usr/bin/env python

import sys, os, getopt
import shutil
import subprocess
import re
import uuid

def remove_data(f):
    try:
        if os.path.isfile(f):
            os.unlink(f)
        else:
            shutil.rmtree(f)
    except:
        pass

def generate_thumbnail(src, dst):
    dim = subprocess.Popen(["identify","-format","\"%w,%h\"", src], stdout=subprocess.PIPE).communicate()[0]
    (width, height) = [ int(x) for x in re.sub('[\t\r\n"]', '', dim).split(',') ]
    thumb_width = thumb_height = 48
    if width > height:
        thumb_width = 48
        thumb_height = int( (48.0/width) * height )
    else:
        thumb_width = int( (48.0/height) * width )
        thumb_height = 48
    os.popen('convert -resize '+str(thumb_width)+'x'+str(thumb_height)+' '+src+' '+dst)

def get_max_width_and_height(dst_dir):
    max_width = max_height = 0
    for f in os.listdir(dst_dir):
        if os.path.isfile(os.path.join(dst_dir, f)):
            dim = subprocess.Popen(["identify","-format","\"%w,%h\"", os.path.join(dst_dir, f)], stdout=subprocess.PIPE).communicate()[0]
            (width, height) = [ int(x) for x in re.sub('[\t\r\n"]', '', dim).split(',') ]
            if width > max_width:
                max_width = width
            if height > max_height:
                max_height = height
    return max_width, max_height

def picture_postprocessing(src, dst, background_image, max_width, max_height):
    dim = subprocess.Popen(["identify","-format","\"%w,%h\"", src], stdout=subprocess.PIPE).communicate()[0]
    (width, height) = [ int(x) for x in re.sub('[\t\r\n"]', '', dim).split(',') ]
    if (width > max_width) or (height > max_height) :
        width = max_width
        height = max_height
    unique_filename = '/tmp/' + str(uuid.uuid4()) + os.path.splitext(src)[-1]
    os.popen('convert -resize '+str(width)+'x'+str(height)+' '+src+' '+unique_filename)
    os.popen('composite  -gravity center '+unique_filename+' '+background_image+' '+dst)
    remove_data(unique_filename);

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
        print "\tdelete /thumb ..."
        remove_data(root_dir+'/thumb');
        print "\tdelete /main/js/config.js ..."
        remove_data(root_dir+'/main/js/config.js');
        print "[clean done]"

    else:
        # TODO preprocessing photos in /raw for fixing size
        print 'Preprocessing for raw photo in /raw ...'
        (max_width, max_height) = get_max_width_and_height(root_dir + '/raw')
        max_width = int(max_width * 0.7)
        max_height = int(max_height * 0.7)
        os.popen('convert -resize '+str(max_width)+'x'+str(max_height)+'! '+'main/images/f5f5dc.png'+' '+'/tmp/background.png')
        remove_data(root_dir+'/photo');
        os.makedirs(root_dir+'/photo')
        [ picture_postprocessing(root_dir+'/raw/'+f, root_dir+'/photo/'+f, '/tmp/background.png', max_width, max_height) for f in os.listdir(root_dir+'/raw') if os.path.isfile(os.path.join(root_dir+'/raw', f)) ]
        print 'Preprocessing for raw photo in /raw ... done'

        # generate thumbnail
        print 'Generating thumbnail for raw photo in /thumb ...'
        remove_data(root_dir+'/thumb');
        os.makedirs(root_dir+'/thumb')
        [ generate_thumbnail(root_dir+'/raw/'+f, root_dir+'/thumb/'+f) for f in os.listdir(root_dir+'/raw') if os.path.isfile(os.path.join(root_dir+'/raw', f)) ]
        print 'Generating thumbnail for raw photo in /thumb ... done'


        # generate file list to main/js/config.js
        print 'Generating file list from /photo ...'
        custom_photo_files = [ f for f in os.listdir(root_dir+'/photo') if os.path.isfile(os.path.join(root_dir+'/photo', f)) ]
        custom_photo_files.sort();
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
