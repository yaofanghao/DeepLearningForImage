@echo off
set old_folder_name=%1
set new_folder_name=%2
ren %old_folder_name% %new_folder_name%
mkdir img_out