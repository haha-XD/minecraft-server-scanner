import re
import socket
from ipaddress import ip_address

from mcstatus import MinecraftServer

def generate_ips(start, end):
    start_int = int(ip_address(start).packed.hex(), 16)
    end_int = int(ip_address(end).packed.hex(), 16)
    return [ip_address(ip).exploded for ip in range(start_int, end_int)]

def is_minecraft(host, check_population=False, check_version=None):
	try:
		server = MinecraftServer(host, 25565)
		status = server.status()
		players = status.players

		if check_population:
			if players.online == 0:
				return None

		if check_version is not None:
			if check_version not in status.version.name:
				return

		try:
			description = status.description['text']
		except (TypeError, KeyError) as e:
			if isinstance(e, KeyError):
				description = status.description['translate']

			else:
				description = status.description
	
		try:
			description = re.sub(r'§.|\n', '', description)
		except TypeError as e:
			print(type(description))
			print(description)

		description = ' '.join(description.split())

		return {'description':description, 
				'version':status.version.name,
				'players':f'{players.online}/{players.max}', 
				'host':server.host}

	except (socket.timeout, ConnectionRefusedError, OSError) as e:
		pass