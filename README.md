eula-search
===========

Quick and dirty script to search documents for words and their containing sentences.
I got inspired to put this together quickly after viewing this wonderful [documentary](http://tacma.net/).

Requires python and [clint](https://github.com/kennethreitz/clint)
```
pip install clint
```

#### Usage

```
python eula.py file.txt word
```
will "context search" file.txt for every occurance of "word" and print the containing sentences.

For some fun, save the iTunes EULA to a text file and use "nuclear" as your search term.