import argparse
from functools import partial
from concurrent.futures import ThreadPoolExecutor

from checker import is_minecraft
from file_operations import parse_file_ips, dump_results

def main():
	parser = argparse.ArgumentParser(description='Scans given iprange for minecraft servers on port 25565.')
	parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default='input.txt', 
						help='The input file of ipranges.')
	parser.add_argument('outfile', nargs='?', type=argparse.FileType('w+', encoding='utf-8'), default='output.txt', 
						help='The output file of ipranges. **Erases file data!**')
	parser.add_argument('-w', '--max-workers', type=int, default=800, 
						help='The max amount of workers used in the pool.')
	parser.add_argument('-p', '--check-population', type=bool, default=False, 
						help='Limiting scan to populated (>0 players online servers')
	parser.add_argument('-v', '--check-version', default=None, 
						help='Limiting the scan to a specified version. (e.g. 1.15.2)')
	args = parser.parse_args()

	print(f'Parsing ips from file "{args.infile.name}"')
	ips = parse_file_ips(args.infile)

	print(f'Starting scan of ipranges with {args.max_workers} workers')
	with ThreadPoolExecutor(max_workers = args.max_workers) as executor:
		results = executor.map(partial(is_minecraft, 
									   check_population=args.check_population,
									   check_version=args.check_version), ips)

	print(f'Dumping results into file "{args.outfile.name}"')
	dump_results(results, args.outfile)

if __name__ == '__main__':
	main()