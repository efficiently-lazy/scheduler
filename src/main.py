import argparse
from bin.scheduler import schedule_meetings

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Schedule Meetings between Product Managers and Developers")
    parser.add_argument('--input', type=str, required=True, help='Path to input Excel file')
    parser.add_argument('--output', type=str, required=True, help='Path to output Excel file')
    args = parser.parse_args()

    schedule_meetings(args.input, args.output)
