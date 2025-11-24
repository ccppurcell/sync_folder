# Sync Folder

This is a program I wrote as part of a job application process. I
didn't get the job but I learned a lot. I intend to continue
developing and testing this program as a learning exercise. The
initial commit is an improvement upon the version I submitted, after
receiving feedback from the hiring committee.

The spec was to create a program that syncs two folders at regular
intervals a certain number of times. The program must log the changes.
The source and replica folders, the log file,
and the number of syncs and the length of the interval, are
supplied as command line arguments. The program had to be
single-threaded and in one file. We were encouraged to use standard
libraries to achieve the goals.

## Installation and usage

This project is for learning purposes only. But if you want, you can
clone it, cd into the folder and run 
```
python main.py <source> <replica> <interval> <runs> <log_file>
```
where <source>, <replica> and <log_file> are paths and <runs> and
<interval> are integers.

## Future improvements

- Support subdirectories (currently assumes flat source directory)
- Make fingerprinting more efficient (currently hashes whole file)
- Improve error logging
