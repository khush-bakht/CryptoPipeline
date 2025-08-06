@echo off
cd /d E:\Neurog\New\cryptoPipeline
call myenv\Scripts\activate.bat
python -m data.main
call myenv\Scripts\deactivate.bat