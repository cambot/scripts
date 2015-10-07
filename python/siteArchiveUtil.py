import zipfile
import sys
import os
import shutil
import csv

'''
Utility intended to aid in archiving snapshots of a list of websites.
'''

# Load a *.tsv file and return a list of dictionaries of the values
#    tsv = Tab separated values
def loadTSVFile(file_name):
	with open(file_name) as file_handle:
		return [row for row in csv.DictReader(file_handle, delimiter="\t")]


def archive_site(target_url):
	wget_wrapper(target_url)
	x = target_url.split("//")[1]
	oldDirName = x.split('/')[0]
	newDirName = x.replace('/', '_')
	print "Renaming " + oldDirName + " to " + newDirName
	os.rename(oldDirName, newDirName)
	zip_folder(newDirName, newDirName + '.zip')
	print "Archived to " + newDirName + '.zip'
	shutil.rmtree(newDirName)


# grabs the supplied website url from the web and copies it to the current directory
# Dependency: wget is not natively available on Mac or Windows
def wget_wrapper(site):
	os.system( 'wget --mirror -np -p --html-extension -e robots=off --base=./ -k -P ./ ' + site )
	return


# Source: https://www.calazan.com/how-to-zip-an-entire-directory-with-python/
def zip_folder(folder_path, output_path):
    """
	Zip the contents of an entire folder (with that folder included
    in the archive). Empty subfolders will be included in the archive
    as well.
    """
    parent_folder = os.path.dirname(folder_path)
    # Retrieve the paths of the folder contents.
    contents = os.walk(folder_path)
    try:
        zip_file = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)
        for root, folders, files in contents:
            # Include all subfolders, including empty ones.
            for folder_name in folders:
                absolute_path = os.path.join(root, folder_name)
                relative_path = absolute_path.replace(parent_folder + '\\', '')
                print "Adding '%s' to archive." % absolute_path
                zip_file.write(absolute_path, relative_path)
            for file_name in files:
                absolute_path = os.path.join(root, file_name)
                relative_path = absolute_path.replace(parent_folder + '\\', '')
                print "Adding '%s' to archive." % absolute_path
                zip_file.write(absolute_path, relative_path)
        print "'%s' created successfully." % output_path
    except IOError, message:
        print message
        sys.exit(1)
    except OSError, message:
        print message
        sys.exit(1)
    except zipfile.BadZipfile, message:
        print message
        sys.exit(1)
    finally:
        zip_file.close()
