import argparse
from bin.scheduler import schedule_meetings

if __name__ == '__main__':
    print('Scheduler starting...\n')
    input_file = 'src/data/input.xlsx'
    availability_file = 'src/data/availability.xlsx'
    output_path = 'src/data/output.xlsx'

    schedule_meetings(input_file, availability_file, output_path)
