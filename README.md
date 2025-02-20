This repository contains scripts to be used during the PRE-INGEST part of your institution's Archivematica workflow. 
These scripts allow Archivematica users to identify and reformat files which will NOT be automatically normalized during the system's ingest transfer process. Normalizing files refers to the process by which all files of a particular type (video files, audio files, images, text documents, etc.) are converted to a specific file format. Usually, this format is chosen for accessibility. At the same time, the original file format is still kept for preservation purposes.
For example, Word documents do not get normalized in Archivematica. Our policy states we must keep the Word document as part of the collection. But we would still like to have a copy accessible to patrons. In this case, we chose the PDF format as our proxy format to normalize to.
Aside from the scripts that have been shared, we have provided a comprehensive list of file formats that DO NOT get normalized during Archivematica's ingest processes. We've named this file "Formats-AM-Will-Not-Normalize_LIST."

The scripts and their corresponding READ ME text files (which include instructions for the use of the scripts) are numbered in the order in which they should be used.

The first script (formatcounter.py and README) requires the use of the DROID file identification tool first before running the script. DROID will identify all of the formats within a package and that data can be exported into a CSV. The formatcounter.py script will then be run on the CSV. The script will produce a report listing all of the formats in the package and will identify whether or not Archivematica will normalize the format. Once it's been determined there are formats Archivematica will not convert, you can refer back to the CSV to find the actual location of each individual file.
The next scripts are all used to convert formats. We have 3 conversion scripts so far, DOC (Word)-to-PDF, RTF-to-PDF and PPT-to-PDF. These scripts will require a dedicated folder within your institutions hard drive. The scripts will run on any and all packages within this dedicated folder. The scripts dive down into each package and recursively search through each sub-folder looking for specific file formats. The script then converts and properly names the new access copy.

Please be aware that you WILL be creating new files, thereby increasing the size of your package.

Please be aware that some file format conversions MAY NOT be necessary. For example, a collection may be comprised of many TIFF files. Your policy may be to make copies on demand. Therefore, you would not need to convert the TIFF files. 

Additionally, there have been instances where a package contains an excessive amount of folders nested within folders or will have files with extremely long file names. This causes errors as there is a 256-character file path threshold. For example, AIPs will not migrate from one location to another or will not ingest. In order to to determine whether or not an AIP contains a file path that exceeds the 256-character threshold, a script has been created to locate any instances where the threshold has been exceeded. This script, findlongpaths.py, has been added to any folder where an AIP may need to be checked prior to ingest. The script will look through all AIPs in a given folder and output a CSV. The CSV will list each file path that is too long and will also display how many characters are in the path. Following this path will help the Processing Archivist to rename or reorganize the AIP. Once the error has been fixed, the Digital Archivist may continue with their workflow.

KNOWN ERRORS:
"Word cannot open file because the file format does not match the file extension.”
This error occurs when the file extension (doc vs. docx, for example) does NOT match the file’s “magic number”, or the actual file format. Most commonly, this occurs between .doc and .docx Word files. The script will NOT create a PDF if the format and extension do not match.
The error will appear in the Powershell window. Additionally, the conversion scripts will output an error TXT file. The error should appear in this file, as well.
The error will give a location for the file. Navigate to the file’s location and change the extension to either .doc or .docx. Then re-run the script. A PDF should be created.

AIP won't copy and paste to a location or will get hung up during the ingest phase.
AIPs cannot be migrated or ingested when there is any file path longer than 256 characters. 
This script goes through an AIP to find any file path that exceeds 256 characters. 
Once the script finds an error, it will stop running. It will also list the file path in question in the PowerShell window.
Once the file path error is fixed, run the script again to find more file path issues, if they exist. 
The script only finds ONE file path issue at a time. So running the script multiple times ensures all errors are accounted for.
 

