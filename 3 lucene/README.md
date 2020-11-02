# Lab 3: Lucene

## Part A

### Step 1 (A/IndexFiles.py)

* Input: html directory, docs directory (temp), index directory
* Output: docs directory (temp), `titles.txt` (temp), index directory
* Example Command in Terminal:
```
python IndexFiles.py html docs index
```

### Step 2 (A/SearchFiles.py)

* Input: index directory
* Output: In Terminal (Interactive script)
* Example Command in Terminal:
```
python SearchFiles.py index
```

## Part B Exercise 1

### Step 1 (A/IndexUpdate.py)

* Input: docs directory (from Part A), index directory (from Part A), new index directory
* Output: new index directory
* Example Command in Terminal:
```
python IndexUpdate.py docs index
```

### Step 2 (A/SearchFiles.py)

* Input: new index directory
* Output: In Terminal (Interactive script)
* Example Command in Terminal:
```
python SearchFiles.py index
```

## Part B Exercise 2

### Step 1 (B/IndexImgs.py)

* Input: html directory, index directory
* Output: `images.txt` (temp), index directory
* Example Command in Terminal:
```
python IndexImgs.py html_img index_img
```

### Step 2 (B/SearchImgs.py)

* Input: index directory
* Output: In Terminal (Interactive script)
* Example Command in Terminal:
```
python SearchImgs.py index_img
```