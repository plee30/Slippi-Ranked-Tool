# Slippi-Ranked-Tool

WIP Tool to automatically get opponent's Slippi Online ELO in a ranked match

Currently works by tracking folder where .slp files are created for new files (currently assumes user has them in D:\Documents\Slippi\, and separates files by month-year folders), reading a new file that is created, and making an API Request with the extracted connection-code found.
