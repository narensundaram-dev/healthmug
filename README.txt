|============================|
|To list all the categories: |
|============================|

    - python3.6 healthmug.py -lc
    - Output:
        sno | category | count | pages
        ------------------------------
        1. homeopathy - 34510 - 1726
        2. ayurveda - 9738 - 487
        3. unani - 1896 - 95
        4. nutrition - 2879 - 144
        5. personalcare - 4306 - 216
        6. babycare - 121 - 7
        7. fitness - 670 - 34

|============================|
|To get data for a category: |
|============================|

    - python3.6 -c babycare -p1 1 -p2 7
    - Output:
        - Stored in excel: "<script-dir>/output/babycare/babycare_1_7.xlsx"
        - Filename format: <category-name>_<page_from>_<page_to>.xlsx

|=============================|
|To merge all the xlsx files: |
|=============================|

    - python3.6 healthmug.py --merge-xlsx
    - Output:
        - Stored in excel: "<script-dir>/healthmug.xlsx"

|================|
|To get help:    |
|================|

    - python3.6 healthmug.py -h
    - Output:
        usage: healthmug.py [-h] [-lc]
                    [-c {homeopathy,ayurveda,unani,nutrition,personalcare,babycare,fitness}]
                    [-p1 PAGE_FROM] [-p2 PAGE_TO] [-log-level {INFO,DEBUG}]

        optional arguments:
        -h, --help            show this help message and exit
        -lc, --list_category
        -c {homeopathy,ayurveda,unani,nutrition,personalcare,babycare,fitness}, --category {homeopathy,ayurveda,unani,nutrition,personalcare,babycare,fitness}
        -p1 PAGE_FROM, --page_from PAGE_FROM
        -p2 PAGE_TO, --page_to PAGE_TO
        -log-level {INFO,DEBUG}, --log_level {INFO,DEBUG}
