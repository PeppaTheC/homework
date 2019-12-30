#Answers:
1) Which system call will be used most often (strace)?

    command: `$ sudo strace -o trace_hw_2.txt -c ./hw_2.py  -p INPUT_PATH -s INPUT_SHA256`
    answer: system call `read`
    
2) Which part of the code is the “hottest”?  

    command: `$ python -m cProfile hw_2.py -p INPUT_PATH -s INPUT_SHA256`  
    answer: `_hashlib.openssl_sha256`  

3) Which system call consumed more time?
    
    answer: by strace system call is `read`

