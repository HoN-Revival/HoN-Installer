# HoN-Installer

A custom installer using backed-up files for HoN that will still work after the servers go offline.

![Image of the installer GUI](https://i.imgur.com/vsSaozP.png)

## How to install

TODO

## How to uninstall

This script does not touch the registry or anything like that. To uninstall, simply delete the directory where the files were installed to.
(e.g. Delete the `.../Program Files/Heroes of Newerth 64/...`).

## Design

The install files are stored in https://drive.google.com/drive/u/0/folders/1zZ0iSXaNF8tuGKxhpABZAKiXrLm2jIZN.
(They were backed up using https://github.com/mrhappyasthma/hon-client-scraper).

Install files are primarly kept as delta-packages. In other words, a given update only contains the new files since the last update stored in the repo.
For example, update `4.9.5.zip` only contains the new files since the `4.9.4.zip`.

The benefit is that this dramatically decreases the size of each update and allows applying each directory in-order up to the target installation version.

The installer is a simple python executable that performs the following actions:

1. Download the relevant files from the google drive backup.
2. Extract all of the archives (i.e. `.zip` files)
3. Iterate through each version from the first to the target installation version:
    - For each: copy all of the files to the target directory (e.g. `Program Files/...`), always overwriting any existing file
