# hinata-blog-to-pdf
Simple Python script to archive Hinatazaka46 member's blog into pdf format. 
Watanabe Miho graduation hits me so hard so I created this script to archive all of member's blog as we know that their blogs will be deleted after they graduated😢
The script will download all articles located on the first page from each member's personal blog.
## How-to
### Preresquisite
This script is using weasyprint library which needed some initial setups. Follow the instruction at https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation in order to run this script properly.
If you're going to run this script as executable, just follow until the library installation part. On Windows, you only need to follow the instructions on how to install the GTK libraries.
### Running as python file
To run the script as normal python script, run
```
python hinata-blog-to-pdf.py
```
The script will save the blogs in the same folder where the script is running. To specify where to save the files, supply the script with `-d` or `--dir` and type your destination folder.
Type `-h` or `--help` to see other possible commands.
### Portable executable file
This script is available in portable executable format (Windows only). To run the executable, open command prompt and run `hinata-blog-to-pdf.exe`
## Requirements
This script can only run on Python 3.5 or higher. You must have the installed library used by the script to run.
To get the required libraries, please run
```
pip install -r requirements.txt
```
### Incorporating Windows Task Scheduler
You can use Windows Task Scheduler to automate the script to run at specific time. If you want to schedule the script to run automatically, it is recommended to use the portable executable format.
