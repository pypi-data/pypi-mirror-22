#!/usr/bin/env python3

import json
import os
from scanner import scanner, dupecheck, chan_info, downloader

print("Testing scanner.py")

print("--------------------------------------------------------")
print("Testing: scanner.get_catalog_json                      -")
print("--------------------------------------------------------")
catalog_json = scanner.get_catalog_json("a", "4chan")
print('\x1b[6;30;42m' + 'OK' + '\x1b[0m')

print("--------------------------------------------------------")
print("Testing: scanner.scan_thread                           -")
print("--------------------------------------------------------")

list_of_threads = scanner.scan_thread("anime", catalog_json)
for i in list_of_threads:
     print(i)

print('\x1b[6;30;42m' + 'OK' + '\x1b[0m')

print("--------------------------------------------------------")
print("!!! scanner.download_thread not tested yet !!!         -")
print("--------------------------------------------------------")

print("--------------------------------------------------------")
print("Testing: scanner.add_to_downloaded                     -")
print("----------------------------------------------thread_id----------")

scanner.add_to_downloaded("139294614", "log", ".")

print('\x1b[6;30;42m' + 'OK' + '\x1b[0m')

print("--------------------------------------------------------")
print("Testing: scanner.folder_size_mb                        -")
print("--------------------------------------------------------")

#Creating a 15mb file in a subfolder of a folder
os.system("mkdir folder_size_test")
os.system("mkdir folder_size_test/subfolder")
os.system("dd if=/dev/zero of=folder_size_test/subfolder/15mbfile bs=15000000 count=1")

# Getting folder size
size = scanner.folder_size_mb("folder_size_test")
if int(size) != 15:
    print(size)
    exit(1)

print('\x1b[6;30;42m' + 'OK' + '\x1b[0m')

print("--------------------------------------------------------")
print("!!! scanner.check_quota not tested yet !!!             -")
print("--------------------------------------------------------")

print("--------------------------------------------------------")
print("Testing:                                               -")
print("scanner.get_check_duplicate                            -")
print("scanner.get_condition                                  -")
print("scanner.get_imageboard                                 -")
print("scanner.get_keyword                                    -")
print("--------------------------------------------------------")

json_file = json.load(open("test/test_config.json"))

# Get a list of every search entry in the json file
search_list = []
for search in json_file["searches"]:
    search_list.append(search)

# Test on the first search with all optionals parameters
duplicate1  = scanner.get_check_duplicate(search_list[0])
condition1  = scanner.get_condition(search_list[0])
imageboard1 = scanner.get_imageboard(search_list[0])
keyword1    = scanner.get_keyword(search_list[0])

if not duplicate1:
    print("duplicate1 should be True but is False")
    exit(1)

if condition1["filename"] != ['IMG_']:
    print("filename error in condition1")
    exit(1)

if condition1["width"] != '>100':
    print("width error in condition1")
    exit(1)

if condition1["height"] != '>200':
    print("height error in condition1")
    exit(1)

if condition1["ext"] != ['.jpg', '.png']:
    print("ext error in condition1")
    exit(1)

if imageboard1 != '4chan':
    print("imageboard1 should be 4chan")
    exit(1)

if keyword1 != ['keyword1', 'keyword2', 'keyword3']:
    print("keyword1 should be equal to ['keyword1', 'keyword2', 'keyword3']")
    exit(1)

duplicate2  = scanner.get_check_duplicate(search_list[1])
condition2  = scanner.get_condition(search_list[1])
imageboard2 = scanner.get_imageboard(search_list[1])
keyword2    = scanner.get_keyword(search_list[1])

if not duplicate2:
    print("duplicate2 should be True but is False")
    exit(1)

if condition2["filename"]:
    print("filename should be false")
    exit(1)

if condition2["width"]:
    print("width should be false")
    exit(1)

if condition2["height"]:
    print("height should be false")
    exit(1)

if condition2["ext"]:
    print("ext should be false")
    exit(1)

if imageboard2 != '4chan':
    print("imageboard2 should be 4chan")
    exit(1)

if keyword2 != ['keyword']:
    print("keyword2 should be equal to ['keyword']")
    exit(1)

print('\x1b[6;30;42m' + 'OK' + '\x1b[0m')

print("--------------------------------------------------------")
print("!!! scanner.scan not tested yet !!!                    -")
print("--------------------------------------------------------")

print('\x1b[6;30;42m' + 'All test OK for scanner.py' + '\x1b[0m')

print("Testing dupecheck.py")

print("--------------------------------------------------------")
print("Testing: dupecheck.hash_image                          -")
print("--------------------------------------------------------")

hash = dupecheck.hash_image("test/test_img.png")
if hash != "b3ce9cb3aefc5e240b4295b406ce8b9a":
    print("hash should be b3ce9cb3aefc5e240b4295b406ce8b9a")
    exit(1)

print('\x1b[6;30;42m' + 'OK' + '\x1b[0m')

print("--------------------------------------------------------")
print("Testing: dupecheck.add_to_file                         -")
print("--------------------------------------------------------")

os.system("echo "" > hash_test_file.txt")

dupecheck.add_to_file("hash_test_file.txt", "some_hash_to_write")

if 'some_hash_to_write' not in open("hash_test_file.txt").read():
    print("the string was not written to hash_test_file.txt")
    exit(1)

print('\x1b[6;30;42m' + 'OK' + '\x1b[0m')

print("--------------------------------------------------------")
print("Testing: dupecheck.is_duplicate                        -")
print("--------------------------------------------------------")

os.system("echo some_hash > hash_test_file.txt")

# Test when hash is in file
is_dupe = dupecheck.is_duplicate("hash_test_file.txt", "some_hash")
if not is_dupe:
    print("is_dupe should be True")
    exit(1)

# Test when hash is NOT in file
is_dupe = dupecheck.is_duplicate("hash_test_file.txt", "hash_not_in_file")
if is_dupe:
    print("is_dupe should be False")
    exit(1)

print('\x1b[6;30;42m' + 'OK' + '\x1b[0m')

print("--------------------------------------------------------")
print("Testing: dupecheck.hash_img_in_folder                  -")
print("--------------------------------------------------------")

# Creating a folder with some files to hash
os.system("mkdir test_download_folder")
os.system("echo file1 > test_download_folder/file1.txt")
os.system("echo file2 > test_download_folder/file2.txt")
os.system("echo file3 > test_download_folder/file3.txt")
os.system("echo "" > hash_test_file1.txt")
os.system("echo "" > hash_test_file2.txt")

dupecheck.hash_img_in_folder("test_download_folder", "hash_test_file1.txt", True)
if '5149d403009a139c7e085405ef762e1a' not in open("hash_test_file1.txt").read():
    print("file1 hash not in hash_test_file1.txt")
    exit(1)
if '3d709e89c8ce201e3c928eb917989aef' not in open("hash_test_file1.txt").read():
    print("file2 hash not in hash_test_file1.txt")
    exit(1)
if '60b91f1875424d3b4322b0fdd0529d5d' not in open("hash_test_file1.txt").read():
    print("file3 has not in hash_test_file1.txt")
    exit(1)

dupecheck.hash_img_in_folder("test_download_folder", "hash_test_file2.txt", False)
if 'not checking for duplicate' not in open("hash_test_file2.txt").read():
    print("'not checking for duplicate' should be in hash_test_file2.txt")
    exit(1)

print('\x1b[6;30;42m' + 'OK' + '\x1b[0m')

print('\x1b[6;30;42m' + 'All test OK for dupecheck.py' + '\x1b[0m')

print("Testing chan_info.py")

print("--------------------------------------------------------")
print("Testing: chan_info.get_chan_info                       -")
print("--------------------------------------------------------")

info_4chan = chan_info.get_chan_info("4chan")
if info_4chan[0] != "http://a.4cdn.org/":
    print("chan_base_url wrong for 4chan")
    exit(1)

if info_4chan[1] != "/thread/":
    print("chan_thread_subfolder wrong for 4chan")
    exit(1)

if info_4chan[2] != "/":
    print("chan_image_subfolder wrong for 4chan")
    exit(1)

if info_4chan[3] != "http://i.4cdn.org/":
    print("chan_image_base_url wrong for 4chan")
    exit(1)

info_lainchan = chan_info.get_chan_info("lainchan")
if info_lainchan[0] != "https://lainchan.org/":
    print("chan_base_url wrong for lainchan")
    exit(1)

if info_lainchan[1] != "/res/":
    print("chan_thread_subfolder wrong for lainchan")
    exit(1)

if info_lainchan[2] != "/src/":
    print("chan_image_subfolder wrong for lainchan")
    exit(1)

if info_lainchan[3] != "https://lainchan.org/":
    print("chan_image_base_url wrong for lainchan")
    exit(1)


info_uboachan = chan_info.get_chan_info("uboachan")
if info_uboachan[0] != "https://uboachan.net/":
    print("chan_base_url wrong for uboachan")
    exit(1)

if info_uboachan[1] != "/res/":
    print("chan_thread_subfolder wrong for uboachan")
    exit(1)

if info_uboachan[2] != "/src/":
    print("chan_image_subfolder wrong for uboachan")
    exit(1)

if info_uboachan[3] != "https://uboachan.net/":
    print("chan_image_base_url wrong for uboachan")
    exit(1)

print('\x1b[6;30;42m' + 'OK' + '\x1b[0m')

print('\x1b[6;30;42m' + 'All test OK for chan_info.py' + '\x1b[0m')

print("Testing download.py")

# Creating download object
condition = {"ext": False, "filename": False, "width": False, "height": False, }
download = downloader.downloader(list_of_threads[0], 'a',"4chan", ".", "testci", True, condition, True)

print("--------------------------------------------------------")
print("!!! download.load not tested yet !!!                   -")
print("--------------------------------------------------------")

print("--------------------------------------------------------")
print("Testing: download.create_dir                           -")
print("--------------------------------------------------------")

# Creating directory
download.create_dir("test_create_dir")
if not os.path.exists("test_create_dir"):
    print("'test_create_dir' was not created")
    exit(1)

# Testing again because the function should not crash if folder already exist
download.create_dir("test_create_dir")

print('\x1b[6;30;42m' + 'OK' + '\x1b[0m')

print("--------------------------------------------------------")
print("Testing: download.add_to_downloaded_log                -")
print("Testing: download.was_downloaded                       -")
print("--------------------------------------------------------")

os.system("echo "" > test_download_log.txt")
download.add_to_downloaded_log("my_filename")
if 'my_filename' not in open(download.downloaded_log).read():
    print("'my_filename' is not in {0}".format(download.downloaded_log))
    exit(1)

downloaded = download.was_downloaded("my_filename")
if not downloaded:
    print("'returned' should be True")
    exit(1)

downloaded = download.was_downloaded("other_filename")
if downloaded:
    print("'returned' should be False")
    exit(1)

print('\x1b[6;30;42m' + 'OK' + '\x1b[0m')

print("--------------------------------------------------------")
print("Testing: download.extension_condition                  -")
print("--------------------------------------------------------")

if not download.extension_condition([".jpg"], ".jpg"):
    print("same extension should return True")
    exit(1)

if download.extension_condition([".jpg"], ".png"):
    print("different extension should return False")
    exit(1)

print('\x1b[6;30;42m' + 'OK' + '\x1b[0m')

print("--------------------------------------------------------")
print("Testing: download.filename_condition                   -")
print("--------------------------------------------------------")

if not download.filename_condition(["IMG_"], "IMG_2345.jpg"):
    print("IMG_ is in IMG_2345, should return True")
    exit(1)

if download.filename_condition(["PIC"], "IMG_2345.jpg"):
    print("PIC is not in IMG_2345, should return False")
    exit(1)

print('\x1b[6;30;42m' + 'OK' + '\x1b[0m')

print("--------------------------------------------------------")
print("Testing: download.width_condition                      -")
print("--------------------------------------------------------")

if not download.width_condition("=100", 100):
    print("100 is equal to 100, should be True")
    exit(1)

if download.width_condition("=100", 101):
    print("100 is not equal to 101, should be False")
    exit(1)

if not download.width_condition(">100", 101):
    print("101 is greater than 100, should be True")
    exit(1)

if download.width_condition(">100", 99):
    print("99 is not greater than 100, should be False")
    exit(1)

if not download.width_condition("<100", 99):
    print("99 is lower than 100, should be True")
    exit(1)

if download.width_condition("<100", 101):
    print("101 is not lower than 100, should be False")
    exit(1)

print('\x1b[6;30;42m' + 'OK' + '\x1b[0m')


print("--------------------------------------------------------")
print("Testing: download.all_condition_check                  -")
print("--------------------------------------------------------")

all_true = [True, True, True, True]
one_false = [True, False, True, True]
all_false = [False, False, False, False]

if not download.all_condition_check(all_true):
    print("all conditions are True, should return True")
    exit(1)

if download.all_condition_check(one_false):
    print("one condition is False, should return False")
    exit(1)

if download.all_condition_check(all_false):
    print("all conditions are False, should return False")
    exit(1)

print('\x1b[6;30;42m' + 'OK' + '\x1b[0m')

print("--------------------------------------------------------")
print("!!! download.meet_dl_condition not tested yet !!!      -")
print("--------------------------------------------------------")

print("--------------------------------------------------------")
print("Testing: download.remove_if_duplicate                  -")
print("--------------------------------------------------------")

os.system("cp test/test_img.png duplicate.png")
os.system("echo b3ce9cb3aefc5e240b4295b406ce8b9a > {0}".format(download.img_hash_log))

download.remove_if_duplicate("duplicate.png")
if os.path.isfile("duplicate.png"):
    print("duplicate.png should have been deleted.")
    exit(1)

os.system("cp test/test_img.png not_duplicate.png")
os.system("echo not_our_img_md5 > {0}".format(download.img_hash_log))

download.remove_if_duplicate("not_duplicate.png")
if not os.path.isfile("not_duplicate.png"):
    print("not_duplicate.png should not have been deleted.")
    exit(1)

print('\x1b[6;30;42m' + 'OK' + '\x1b[0m')

print("--------------------------------------------------------")
print("!!! download.download_image not tested yet !!!         -")
print("--------------------------------------------------------")

#img_url= "https://github.com/Lacsap-/4scanner/raw/master/logo/"
#post_dic = {'tim': '4scanner128', 'ext': '.png'}

#file_path = download.download_image(img_url, post_dic, ".")
#if not os.path.isfile(file_path):
#    print("4scanner128.png should have been downloaded.")
#    exit(1)

print('\x1b[6;30;42m' + 'OK' + '\x1b[0m')

print("--------------------------------------------------------")
print("!!! download.download_thread not tested yet !!!        -")
print("--------------------------------------------------------")

print('\x1b[6;30;42m' + 'All test OK for download.py' + '\x1b[0m')
print('\x1b[6;30;42m' + 'SUCCESS' + '\x1b[0m')
