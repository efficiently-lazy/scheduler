import argparse
from bin.scheduler import schedule_meetings

if __name__ == '__main__':
    print('Scheduler starting...')
    input_file = 'src/data/input.xlsx'
    output_path = 'src/data/output.xlsx'

    schedule_meetings(input_file, output_path)
