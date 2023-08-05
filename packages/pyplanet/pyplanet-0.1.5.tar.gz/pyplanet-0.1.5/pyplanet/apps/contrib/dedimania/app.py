import asyncio
import logging
import uuid

from requests.exceptions import ConnectionError as RequestsConnectionError

from pyplanet.apps.config import AppConfig
from pyplanet.apps.contrib.dedimania.api import DedimaniaAPI, DedimaniaRecord
from pyplanet.apps.contrib.dedimania.exceptions import DedimaniaException, DedimaniaTransportException
from pyplanet.apps.core.trackmania import callbacks as tm_signals
from pyplanet.apps.core.maniaplanet import callbacks as mp_signals
from pyplanet.contrib.setting import Setting
from pyplanet.utils import times

from .views import DedimaniaRecordsWidget, DedimaniaRecordsListView

logger = logging.getLogger(__name__)


class Dedimania(AppConfig):
	game_dependencies = ['trackmania']
	app_dependencies = ['core.maniaplanet', 'core.trackmania']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.widget = None
		self.api = None

		self.lock = asyncio.Lock()
		self.current_records = []
		self.player_info = dict()
		self.server_max_rank = None
		self.map_status = False

		self.setting_server_login = Setting(
			'server_login', 'Dedimania Server Login', Setting.CAT_KEYS, type=str,
			description='Only fill in when you want to override the auto-detected server login!',
			default=None
		)
		self.setting_dedimania_code = Setting(
			'dedimania_code', 'Dedimania Server Code', Setting.CAT_KEYS, type=str,
			description='The secret dedimania code. Get one at $lhttp://dedimania.net/tm2stats/?do=register',
			default=None
		)

		self.login = self.code = self.server_version = self.pack_mask = None

	def is_mode_supported(self, mode):
		return mode.startswith('TimeAttack') or mode.startswith('Rounds') or mode.startswith('Team') or \
			   mode.startswith('Laps') or mode.startswith('Cup')

	async def on_start(self):
		# Init settings.
		await self.context.setting.register(self.setting_server_login, self.setting_dedimania_code)

		# Check setting + return errors if not correct!
		self.login = await self.setting_server_login.get_value(refresh=True) or self.instance.game.server_player_login
		self.code = await self.setting_dedimania_code.get_value(refresh=True)
		if not self.code:
			message = '$z$s$fff»» $0f3Error: No dedimania code was provided, please edit the settings and restart PyPlanet (//settings)'
			logger.error('Dedimania Code not configured! Please configure with //settings and restart PyPlanet!')
			await self.instance.gbx.execute('ChatSendServerMessage', message)
			return

		# Init API (execute this in a non waiting future).
		self.api = DedimaniaAPI(
			self.instance,
			self.login, self.code, self.instance.game.server_path, self.instance.map_manager.current_map.environment,
			self.instance.game.dedicated_version, self.instance.game.dedicated_build
		)
		asyncio.ensure_future(self.initiate_api())

		# Register signals
		self.instance.signal_manager.listen(mp_signals.map.map_begin, self.map_begin)
		self.instance.signal_manager.listen(mp_signals.map.map_start, self.map_start)
		self.instance.signal_manager.listen(mp_signals.map.map_end, self.map_end)

		self.instance.signal_manager.listen(tm_signals.finish, self.player_finish)
		self.instance.signal_manager.listen(mp_signals.player.player_connect, self.player_connect)
		self.instance.signal_manager.listen(mp_signals.player.player_disconnect, self.player_disconnect)

		# Load initial data.
		self.widget = DedimaniaRecordsWidget(self)

	async def initiate_api(self):
		await self.api.on_start()
		try:
			await self.api.authenticate()
		except RequestsConnectionError as e:
			logger.error('Can\'t connect to dedimania! Dedimania down or blocked by your host? {}'.format(str(e)))
			return
		except ConnectionRefusedError as e:
			logger.error('Can\'t connect to dedimania! Dedimania down or blocked by your host? {}'.format(str(e)))
			return
		except Exception as e:
			logger.exception(e)
			logger.error('Dedimania app unloaded!')
			print(type(e))
			return

		await self.map_begin(self.instance.map_manager.current_map)

	async def show_records_list(self, player, data = None, **kwargs):
		"""
		Show record list view to player.

		:param player: Player instance.
		:param data: -
		:param kwargs: -
		:type player: pyplanet.apps.core.maniaplanet.models.Player
		:return: view instance or nothing when there are no records.
		"""
		if not len(self.current_records):
			message = '$z$s$fff» $i$f00There are currently no dedimania records on this map!'
			await self.instance.gbx.execute('ChatSendServerMessageToLogin', message, player.login)
			return

		# TODO: Move logic to view class.
		index = 1
		view = DedimaniaRecordsListView(self)
		view_data = []

		async with self.lock:
			first_time = self.current_records[0].score
			for item in self.current_records:
				record_time_difference = ''
				if index > 1:
					record_time_difference = '$f00 + ' + times.format_time((item.score - first_time))
				view_data.append({'index': index, 'nickname': item.nickname,
								  'record_time': times.format_time(item.score),
								  'record_time_difference': record_time_difference})
				index += 1
		view.objects_raw = view_data
		view.title = 'Dedimania Records on {}'.format(self.instance.map_manager.current_map.name)
		await view.display(player=player.login)
		return view

	async def map_start(self, map, restarted, **kwargs):
		if restarted:
			await self.map_end(map)
			await self.map_begin(map)

	async def map_begin(self, map):
		# Reset retries.
		self.api.retries = 0

		# Set map status.
		self.map_status = map.time_author > 6200 or map.num_checkpoints > 0

		# Fetch records + update widget.
		await self.refresh_records()
		await self.chat_current_record()
		await self.widget.display()

	async def map_end(self, map):
		if not self.map_status:
			logger.warning('Don\'t send dedi records, map not supported or we are offline!')
			return

		# Get data, prepare for sending.
		async with self.lock:
			await self.api.set_map_times(
				map, 'TA' if 'TimeAttack' in await self.instance.mode_manager.get_current_script() else 'Rounds',
				self.current_records
			)

	async def refresh_records(self):
		try:
			async with self.lock:
				self.server_max_rank, modes, player_infos, self.current_records = await self.api.get_map_details(
					self.instance.map_manager.current_map,
					'TA' if 'TimeAttack' in await self.instance.mode_manager.get_current_script() else 'Rounds',
					server_name=self.instance.game.server_name, server_comment='', is_private=self.instance.game.server_is_private,
					max_players=self.instance.game.server_max_players['CurrentValue'], max_specs=self.instance.game.server_max_specs['CurrentValue'],
					players=await self.instance.gbx.execute('GetPlayerList', -1, 0),
					server_login=self.instance.game.server_player_login
				)
		except DedimaniaTransportException as e:
			if 'Max retries exceeded' in str(e):
				message = '$z$s$fff»» $f00Error: Dedimania seems down?'
			else:
				message = '$z$s$fff»» $f00Error: Dedimania error occured!'
				logger.exception(e)
			await self.instance.gbx.execute('ChatSendServerMessage', message)
			return
		except Exception as e:
			logger.exception(e)
			async with self.lock:
				self.current_records = []
			return

		for info in player_infos:
			self.player_info[info['Login']] = dict(
				banned=False, login=info['Login'], max_rank=info['MaxRank'],
			)

	async def player_connect(self, player, is_spectator, **kwargs):
		try:
			await self.widget.display(player=player)
			res = await self.instance.gbx.execute('GetDetailedPlayerInfo', player.login)
			p_info = await self.api.player_connect(
				player.login, player.nickname, res['Path'], is_spectator
			)
			if p_info:
				self.player_info[player.login] = p_info
		except ConnectionRefusedError:
			return
		except TimeoutError:
			return
		except DedimaniaException:
			return

	async def player_disconnect(self, player, **kwargs):
		try:
			del self.player_info[player.login]
		except:
			pass
		try:
			await self.api.player_disconnect(player.login, '')
		except:
			pass

	async def player_finish(self, player, race_time, lap_time, lap_cps, flow, raw, **kwargs):
		if not self.map_status:
			return
		if player.login not in self.player_info:
			logger.warning('Player info not (yet) retrieved from dedimania for the player {}'.format(player.login))
			return
		player_info = self.player_info[player.login]
		current_records = [x for x in self.current_records if x.login == player.login]
		score = lap_time
		if len(current_records) > 0:
			current_record = current_records[0]
			previous_index = self.current_records.index(current_record) + 1

			if score < current_record.score:
				previous_time = current_record.score

				# Determinate new rank.
				async with self.lock:
					new_rank = 1
					for idx, record in enumerate(self.current_records):
						new_rank = idx + 1
						if score <= record.score:
							break

				# Check if the player or server allows this player to finish with his max_rank.
				if new_rank > int(self.server_max_rank) and new_rank > int(player_info['max_rank']):
					logger.debug('Ignore time, not within server or player max_rank.')
					return

				try:
					if new_rank == 1:
						# We need the ghost replay too.
						current_record.ghost_replay, current_record.virtual_replay = await self.get_replays(player.login, ghost=True, virtual=True)
					else:
						# Get virtual replay.
						_, current_record.virtual_replay = await self.get_replays(current_record.login, ghost=False, virtual=True)
				except:
					return

				# Update score + infos.
				async with self.lock:
					current_record.score = score
					current_record.cps = lap_cps
					self.current_records.sort(key=lambda x: x.score)

				if new_rank < previous_index:
					message = '$z$s$fff»» $fff{}$z$s$0f3 gained the $fff{}.$0f3 Dedimania Record, with a time of $fff\uf017 {}$0f3 ($fff{}.$0f3 $fff-{}$0f3).'.format(
						player.nickname, new_rank, times.format_time(score), previous_index,
						times.format_time((previous_time - score))
					)
				else:
					message = '$z$s$fff»» $fff{}$z$s$0f3 improved the $fff{}.$0f3 Dedimania Record, with a time of $fff\uf017 {}$0f3 ($fff-{}$0f3).'.format(
						player.nickname, new_rank, times.format_time(score),
						times.format_time((previous_time - score))
					)

				await asyncio.gather(
					self.instance.gbx.execute('ChatSendServerMessage', message),
					self.widget.display()
				)

			elif score == current_record.score:
				message = '$z$s$fff»» $fff{}$z$s$0f3 equalled the $fff{}.$0f3 Dedimania Record, with a time of $fff\uf017 {}$0f3.'.format(
					player.nickname, previous_index, times.format_time(score)
				)
				await self.instance.gbx.execute('ChatSendServerMessage', message)

		else:
			new_record = DedimaniaRecord(
				login=player.login, nickname=player.nickname, score=score, rank=None, max_rank=player_info['max_rank'],
				cps=lap_cps, vote=-1
			)

			# Determinate new rank.
			async with self.lock:
				new_rank = 1
				for idx, record in enumerate(self.current_records):
					new_rank = idx + 1
					if score <= record.score:
						break

			# Check if the player or server allows this player to finish with his max_rank.
			if new_rank > int(self.server_max_rank) and new_rank > int(player_info['max_rank']):
				logger.debug('Ignore time, not within server or player max_rank.')
				return

			try:
				if new_rank == 1:
					new_record.ghost_replay, new_record.virtual_replay = await self.get_replays(player.login, ghost=True, virtual=True)
				else:
					_, new_record.virtual_replay = await self.get_replays(player.login, ghost=False, virtual=True)
			except:
				return

			async with self.lock:
				self.current_records.append(new_record)
				self.current_records.sort(key=lambda x: x.score)
				new_index = self.current_records.index(new_record) + 1
			message = '$z$s$fff»» $fff{}$z$s$0f3 drove the $fff{}.$0f3 Dedimania Record, with a time of $fff\uf017 {}$0f3.'.format(
				player.nickname, new_index, times.format_time(score)
			)
			await asyncio.gather(
				self.instance.gbx.execute('ChatSendServerMessage', message),
				self.widget.display()
			)

	async def get_replays(self, player_login, ghost=False, virtual=True):
		replay_name = 'dedimania_{}.Replay.Gbx'.format(uuid.uuid4().hex)
		calls = list()
		if virtual:
			calls.append(self.instance.gbx.prepare('GetValidationReplay', player_login))
		if ghost:
			calls.append(self.instance.gbx.prepare('SaveBestGhostsReplay', player_login, replay_name))

		results = await self.instance.gbx.multicall(*calls)

		if ghost:
			try:
				async with self.instance.storage.open('UserData/Replays/{}'.format(replay_name)) as ghost_file:
					ghost_base = ghost_file.read()
					if virtual:
						return ghost_base, results[0]
					return ghost_base, None
			except FileNotFoundError as e:
				message = '$z$s$fff»» $f00Error: Dedimania requires you to have file access on the server. We can\'t fetch' \
						  'the driven replay!'
				logger.error('Please make sure we can access the dedicated files. Configure your storage driver correctly! '
							 '{}'.format(str(e)))
				await self.instance.gbx.execute('ChatSendServerMessage', message)
				raise DedimaniaException('Can\'t access files')
			except PermissionError as e:
				message = '$z$s$fff»» $f00Error: Dedimania requires you to have file access on the server. We can\'t fetch' \
						  'the driven replay because of an permission problem!'
				logger.error('We can\'t read files in the dedicated folder, your permissions don\'t allow us to read it! '
							 '{}'.format(str(e)))
				await self.instance.gbx.execute('ChatSendServerMessage', message)
				raise DedimaniaException('Can\'t access files due to permission problems')
		return None, results[0]

	async def chat_current_record(self):
		records_amount = len(self.current_records)
		if records_amount > 0:
			first_record = self.current_records[0]
			message = '$z$s$fff»» $0f3Current Dedimania Record: $fff\uf017 {}$z$s$0f3 by $fff{}$z$s$0f3 ($fff{}$0f3 records)'.format(
				times.format_time(first_record.score), first_record.nickname, records_amount
			)
			calls = list()
			calls.append(self.instance.gbx.prepare('ChatSendServerMessage', message))
			for player in self.instance.player_manager.online:
				calls.append(self.chat_personal_record(player))
			await self.instance.gbx.multicall(*calls)
		else:
			message = '$z$s$fff»» $0f3There is no Dedimania Record on this map yet.'
			await self.instance.gbx.execute('ChatSendServerMessage', message)

	async def chat_personal_record(self, player):
		async with self.lock:
			record = [x for x in self.current_records if x.login == player.login]

		if len(record) > 0:
			message = '$z$s$fff» $0f3You currently hold the $fff{}.$0f3 Dedimania Record: $fff\uf017 {}'.format(
				self.current_records.index(record[0]) + 1, times.format_time(record[0].score)
			)
			return self.instance.gbx.prepare('ChatSendServerMessageToLogin', message, player.login)
		else:
			message = '$z$s$fff» $0f3You don\'t have a Dedimania Record on this map yet.'
			return self.instance.gbx.prepare('ChatSendServerMessageToLogin', message, player.login)
