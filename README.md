# HoN-Installer [NOTE: This project is not funcitonal yet.]

A custom installer using backed-up files for HoN that will still work after the servers go offline.

![Image of the installer GUI](https://i.imgur.com/vsSaozP.png)

## How to install

1. Populate the following values: `GDRIVE_32_BIT_ID ` and `GDRIVE_64_BIT_ID` with IDs to google drive folders containing the backups.

TODO - Complete the instructions.

## How to uninstall

This script does not touch the registry or anything like that. To uninstall, simply delete the directory where the files were installed to.
(e.g. Delete the `.../Program Files/Heroes of Newerth 64/...`).

## Design

The install files should be stored on GoogleDrive. They can be backed up using the official CDNs (e.g. using https://github.com/mrhappyasthma/hon-client-scraper).

Install files should be kept as delta-packages. In other words, a given update only contains the new files since the last update stored in the repo.
For example, update `4.9.5.zip` only contains the new files since the `4.9.4.zip`.

The benefit is that this dramatically decreases the size of each update and allows applying each directory in-order up to the target installation version.

The installer is a simple python executable that performs the following actions:

1. Download the relevant files from the google drive backup.
2. Extract all of the archives (i.e. `.zip` files)
3. Iterate through each version from the first to the target installation version:
    - For each: copy all of the files to the target directory (e.g. `Program Files/...`), always overwriting any existing file
