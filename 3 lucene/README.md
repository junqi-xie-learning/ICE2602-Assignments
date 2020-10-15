# Lab 3: Lucene

## Part A

### Step 1

Download test data from [EE208-Assignments-Test-Data](https://github.com/junqi-xie/EE208-Assignments-Test-Data) and move the data to root folder.

Desired folder structure:
```
3 lucene/
-- html/ (test data)
-- index.txt (test data)
-- Ticker.py
-- ConvertFiles.py
-- IndexFiles.py
-- SearchFiles.py
```

### Step 2 (IndexFiles.py)

* Input: html directory, docs directory (temp), index directory
* Output: docs directory (temp), `titles.txt` (temp), index directory
* Example Command in Terminal:
```
python IndexFiles.py html docs index
```

### Step 3 (SearchFiles.py)

* Input: index directory
* Output: In Terminal (Interactive script)
* Example Command in Terminal:
```
python SearchFiles.py index
```

## Part B Exercise 1

### Step 1 (IndexUpdate.py)

* Input: docs directory (from Part A), index directory (from Part A), new index directory
* Output: new index directory
* Example Command in Terminal:
```
python IndexUpdate.py docs index index_new
```

### Step 2 (SearchFiles.py)

* Input: new index directory
* Output: In Terminal (Interactive script)
* Example Command in Terminal:
```
python SearchFiles.py index_new
```