import zipfile
import sys
import os
import shutil
import csv

'''
Utility intended to aid in archiving snapshots of a list of websites.

Provide a *.tsv file with the following columns:
	- URL: the full url to grab a snapshot of
	- Name: the name for the zip file
	- Redirect: URL to redirect to

archiveSites('sample.tsv')
	generates:
		*.zip files
		RewriteRules.txt that you can copy into an .htaccess file
'''

def archiveSites(file_name):
	sites = loadTSVFile(file_name)
	for website in sites:
		archive_site(website["URL"], website["Name"])
		rewriteRule = generateRewriteRule(website["URL"], website["Redirect"])
	return

def generateRewriteRules(file_name):
	sites = loadTSVFile(file_name)
	with open('RewriteRules.txt', 'a+') as file_handle:
		file_handle.write("\t#\n")
		for website in sites:
			rewriteRule = generateRewriteRule(website["URL"], website["Redirect"])
			file_handle.write("\t" + rewriteRule + "\n")
	file_handle.close()
	return



# Ex: RewriteRule ^erniepyle(.*)$ http://mediaschool.indiana.edu/erniepyle/$1 [R=301,NC,L]
def generateRewriteRule(old_url, new_url):
	subsite = extractSubsite(old_url)
	return "RewriteRule ^" + subsite + "(.*)$ " + new_url + " [R=301,NC,L]"

# Load a *.tsv file and return a list of dictionaries of the values
#    tsv = Tab separated values
def loadTSVFile(file_name):
	with open(file_name) as file_handle:
		return [row for row in csv.DictReader(file_handle, delimiter="\t")]


def archive_site(target_url, zipName=None):
	x = target_url.split("//")[1]   # journalism.indiana.edu/resources/webediting
	oldDirName = x.split('/')[0]    # journalism.indiana.edu
	if zipName is None:
		zipName = x.replace('/', '_')   # journalism.indiana.edu_resources_webediting
	wget_wrapper(target_url)
	print "Renaming " + oldDirName + " to " + zipName
	os.rename(oldDirName, zipName)
	zip_folder(zipName, zipName + '.zip')
	print "Archived to " + zipName + '.zip'
	shutil.rmtree(zipName)

def extractSubsite(url):
	x = url.rsplit("//")[1]
	return "/".join(x.rsplit('/')[1:])

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
        zip_file = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED, True)
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
