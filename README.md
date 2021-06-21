<h1>GrassHopper</h1>

<h2>Description</h2>
GrassHopper is a python script that checks the list of web pages for a specific link and generates results in the excel file.

<h2>Aim of the project</h2>
SEO specialists order articles with links from different websites to promote their brands. The website owners often remove these links overtime or add unwanted tags to them. Checking links manually is time-consuming and inconvenient. That is why I decided to create a script that automatically scans websites and generates a link-status report.
There is a similar project on the market (linkchecker.pro/ru), however, it is rather expensive.

<h2>How to use it?</h2>
Add excel_file.xlsx and GrassHopper.py files to the root folder. In the excel file, add a promoted domain to cell A1. In column B, add the list of pages that we want to check. Save and close the file. After that, run the script in the IDE and wait for the program to display the status "Success". Then, the result_list.xlsx file will appear in the root folder.

In the generated report, you will find:
<li>Status code (200, 301, 404, 500, etc.)
<li>Unwanted tags (Sponsored, NoFollow, UGC)
<li>Links Status (Found / Not Found)

In Example.rar you will find an example of the representative scan.<br>
<b>To reuse the script, remove the result_list.xlsx from the root folder.</b>
