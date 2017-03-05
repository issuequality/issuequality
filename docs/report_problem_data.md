# Problem Report Data

As part of our analysis of the language, content, and structure of problem
report summaries, we gathered a corpus of data from various open source
projects on or around January 18th, 2006. You can download these for your own
analyses: the problem report corpus and analysis tool

We've also provided a simple querying tool with the data, written in Java, that
we used to analyze various parts of the data. It's not very well documented,
but most of its features should be self-explanatory.

These are the projects we studied:

   *Linux Kernel (5,916 summaries, 1.1 MB)
   *Apache (1,234 summaries, 3.5 MB)
   *Firefox (37,952 summaries, 10.6 MB)
   *OpenOffice (38,325 summaries 6.9 MB)
   *Eclipse (90,424 summaries 20.3 MB)

The data is structured as comma-separated values, where each value is wrapped
with "'s. The first line is a comma separated list of names for each column.

For example, here's the first two lines of the Linux kernel file:

project,id,type,opendate,changeddate,priority,platform,assigntodemail,assignedtoname,reporteremail,reportername,status,resolution,version,component,description
"linux","1","","2002-11-06","2003-02-20","","","","","tmolina@linuxmail.org","","clos","patc","","ide","oops/NNS when/WRB using/VBG ide-cd/JJ with/IN 2.5.45/CD and/CC cdrecord/NN"

The columns are:

   -project - one of the five projects listed above
   -id - the id assigned to the report in the project's report database
   -type - some projects listed the type of report as "feature", "bug", etc.
   -opendate - the date the report was filed
   -changedate - the date the report was last changed
   -priority - each project assigned different priority ratings, so they aren't
			   necessarily on the same scales.
   -platform - the software and hardware platform the report is relevant to.
   -assignedtoemail, assignedtoname - the person or group in charge of the report
   -reporteremail, reportername - the person who submitted the report
   -status, resolution - one of various states such as 'opened', 'closed',
						 'fixed'. The legal values depend on the project,
						   since each defined their own.
   -version, component - the version of the software the report regards, and
						 the component of the software that its related to.
   -description - the one-line summary of the problem. These are what we studied in-depth. 

To run the analysis tool, run the jar file included in the download as follows:
```shell
java -jar Analyze file1.csv file2.csv ...
```
