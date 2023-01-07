# Telegram statistics
Exports statistics for a Telegram group chat

## How to run
First, in main repo directory, run the following code to add `src` to your `PYTHONPATH`:
'''
export PYTHONPATH=${PWD}
'''

Then, run:
'''
python src/chat_statistics/stats.py
'''

to generate the word cloud of json data in `DATA_DIR`