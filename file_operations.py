import checker

def parse_file_ips(file):
	ip_list = []
	with file as f:
		for line in f:
			start, end = line.strip().split('-')
			ip_list += checker.generate_ips(start, end)
	return ip_list

def dump_results(results, file):
	with file as f:
		f.writelines([f"{result['host']} - {result['players']} - {result['version']} - \"{result['description']}\"\n" 
			     	 for result in results if result is not None])
		