import os
import pymysql
import csv
import random

def AddToStatsTable(id,stat_id,base_stat,effort):	
	conn = pymysql.connect(host = 'localhost',user = 'root',password = '',db = 'Pokemon_new')
	a = conn.cursor();		
	Query = "INSERT INTO `" + "stat" + "` (`id`, `stat_id`, `base_stat`, `effort`) VALUES ('" + id + "', '" + stat_id + "', '" + base_stat + "','" + effort + "');";		
	a.execute(Query);	

def AddToTypesTable(id,Type):	
	conn = pymysql.connect(host = 'localhost',user = 'root',password = '',db = 'Pokemon_new')
	a = conn.cursor();		
	Query = "INSERT INTO `" + "types" + "` (`id`, `identifier`) VALUES ('" + id + "', '" + Type + "');";		
	a.execute(Query);	

def AddToMovesTable(id,identifier,generation_id,type_id,power,pp,accuracy,priority,target_id,damage_class_id,effect_id,effect_chance):	
	conn = pymysql.connect(host = 'localhost',user = 'root',password = '',db = 'Pokemon_new')
	a = conn.cursor();		
	Query = "INSERT INTO `" + "moves" + "` (`id`, `identifier`, `generation_id`, `type_id`, `power`, `pp`, `accuracy`, `priority`, `target_id`, `damage_class_id`, `effect_id`, `effect_chance`) VALUES ('" + id + "', '" + identifier + "', '" + generation_id + "', '" + type_id + "', '" + power + "', '" + pp + "', '" + accuracy + "', '" + priority + "', '" + target_id + "', '" + damage_class_id + "', '" + effect_id + "', '" + effect_chance + "');";		
	a.execute(Query);	

def AddToPokemonMovesTable(pokemon_id,move_id,pokemon_move_method_id,level,order):	
	conn = pymysql.connect(host = 'localhost',user = 'root',password = '',db = 'Pokemon_new')
	a = conn.cursor();		
	if pokemon_move_method_id == "1":
		TableName = "pokemon_moves_level_up";
	elif pokemon_move_method_id == "2":
		TableName = "pokemon_moves_egg";
	elif pokemon_move_method_id == "2":
		TableName = "pokemon_moves_tutor";
	else:
		TableName = "pokemon_moves_TM";	

	Query = "INSERT INTO `" + TableName + "` (`pokemon_id`, `move_id`, `pokemon_move_method_id`, `level`, `order_`) VALUES ('" + pokemon_id + "', '" + move_id + "', '" + pokemon_move_method_id + "', '" + level + "', '" + order + "');";		
	a.execute(Query);	

def AddToPokemonInfoTable(id,identifier,height,weight,base_experience,order,is_default):	
	conn = pymysql.connect(host = 'localhost',user = 'root',password = '',db = 'Pokemon_new')
	a = conn.cursor();		
	Query = "INSERT INTO `" + "pokemon_info" + "` (`id`, `identifier`, `height`, `weight`, `base_experience`, `order_`, `is_default`) VALUES ('" + id + "', '" + identifier + "', '" + height + "', '" + weight + "', '" + base_experience + "', '" + order + "', '" + is_default + "');";		
	a.execute(Query);	

def AddToPokemonSpeciesTable(id,identifier,generation_id,evolves_from_species_id,evolution_chain_id,color_id,shape_id,habitat_id,gender_rate,capture_rate,base_happiness,is_baby,hatch_counter,has_gender_differences,growth_rate_id,forms_switchable,order):	
	conn = pymysql.connect(host = 'localhost',user = 'root',password = '',db = 'Pokemon_new')
	a = conn.cursor();		
	Query = "INSERT INTO `" + "pokemon_species" + "` (`id`, `identifier`, `generation_id`, `evolves_from_species_id`, `evolution_chain_id`, `color_id`, `shape_id`, `habitat_id`, `gender_rate`, `capture_rate`, `base_happiness`, `is_baby`, `hatch_counter`, `has_gender_differences`, `growth_rate_id`, `forms_switchable`, `order_`) VALUES ('" + id + "', '" + identifier + "', '" + generation_id + "', '" + evolves_from_species_id + "', '" + evolution_chain_id + "', '" + color_id + "', '" + shape_id + "', '" + habitat_id + "', '" + gender_rate + "', '" + capture_rate + "', '" + base_happiness + "', '" + is_baby + "', '" + hatch_counter + "', '" + has_gender_differences + "', '" + growth_rate_id + "', '" + forms_switchable + "', '" + order + "');";		
	a.execute(Query);

def getAllMoves():
	conn = pymysql.connect(host = 'localhost',user = 'root',password = '',db = 'Pokemon')
	cur = conn.cursor();			
	Query = "SELECT Name FROM moves";	
	cur.execute(Query);		
	val = {};
	i = 1;
	for move in cur.fetchall():
		move1 = str(move).replace("#","'");	
		a = move1[2:-3];
		val[a] = i;
		i = i+1;
	return val;

def getPokemons():
	conn = pymysql.connect(host = 'localhost',user = 'root',password = '',db = 'Pokemon')
	cur = conn.cursor();			
	Query = "SELECT Pokedex_No,Sprite_Link FROM pokemon";	
	cur.execute(Query);		
	L = [];	
	for move in cur.fetchall():
		L.append(move);		
	return L;

def takesecond(e):
	return e[1];

def GetStatsDb(id):	
	conn = pymysql.connect(host = 'localhost',user = 'root',password = '',db = 'Pokemon_new')
	cur = conn.cursor();		
	Query = "SELECT * from stat where id = " + id + ";";			
	res =  cur.execute(Query);		
	L = [];	
	for move in cur.fetchall():
		L.append(move);		
	L.sort(key = takesecond)
	# Hp,Atk,Def,SpAtk,SpDef,Speed	
	return L;

def GetPokemonNameDb(id):	
	conn = pymysql.connect(host = 'localhost',user = 'root',password = '',db = 'Pokemon_new')
	cur = conn.cursor();		
	Query = "SELECT identifier from pokemon_info where id = " + id + ";";			
	cur.execute(Query);			
	return cur.fetchone();

def get4RandomMoves(Moves):
	if len(Moves)<=4:
		return Moves;
	else:
		newL = [];
		for i in range(4):
			Index = random.randint(1,len(Moves)) - 1;
			newL.append(Moves[Index]);
			Moves.pop(Index);
		return newL;



def getPokemonMovesDb(id,level):	
	conn = pymysql.connect(host = 'localhost',user = 'root',password = '',db = 'Pokemon_new')
	cur = conn.cursor();		
	Query = "SELECT a.move_id,b.identifier from pokemon_moves_level_up a,moves b where a.pokemon_id = " + id + " and a.level<=" + level + " and a.move_id = b.id";			
	cur.execute(Query);		
	L = [];	
	for move in cur.fetchall():
		if move not in L:
			L.append(move);
	return get4RandomMoves(L);

def fill_in_stats():
	with open('Pokemon\pokedex\pokedex\data\csv\pokemon_stats.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0;
		for row in csv_reader:
			if line_count == 0:
				print row;
				line_count += 1
			else:
				print row;
				AddToStatsTable(row[0],row[1],row[2],row[3]);
				line_count += 1    			

def fill_in_types():
	with open('Pokemon\pokedex\pokedex\data\csv\\types.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0;
		for row in csv_reader:
			if line_count == 0:
				print row;
				line_count += 1
			else:
				print row;
				AddToTypesTable(row[0],row[1]);
				line_count += 1    			
	
def fill_in_moves():
	with open('Pokemon\pokedex\pokedex\data\csv\moves.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0;
		for row in csv_reader:
			if line_count == 0:
				print row;
				line_count += 1
			else:
				print row;
				AddToMovesTable(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11]);
				line_count += 1    			

def fill_in_pokemon_moves():
	with open('Pokemon\pokedex\pokedex\data\csv\pokemon_moves.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0;
		for row in csv_reader:
			if line_count == 0:
				print row;
				line_count += 1
			else:
				#print row;
				if row[3] == "1":
					with open('Pokemon\pokedex\pokedex\data\csv\\nilesh_pokemon_moves.csv', mode='ab+') as qw:
						qw = csv.writer(qw, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						#qw.writerow(row);
						qw.writerow([row[0],row[2],row[4],row[5]]);
					#AddToPokemonMovesTable(row[0],row[2],row[3],row[4],row[5]);
				if row[3] == "2":
					with open('Pokemon\pokedex\pokedex\data\csv\\nilesh_pokemon_moves_egg.csv', mode='ab+') as qw:
						qw = csv.writer(qw, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						#qw.writerow(row);
						qw.writerow([row[0],row[2],row[5]]);
					#AddToPokemonMovesTable(row[0],row[2],row[3],row[4],row[5]);				
				if row[3] == "3":
					with open('Pokemon\pokedex\pokedex\data\csv\\nilesh_pokemon_moves_tutor.csv', mode='ab+') as qw:
						qw = csv.writer(qw, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						#qw.writerow(row);
						qw.writerow([row[0],row[2],row[5]]);
					#AddToPokemonMovesTable(row[0],row[2],row[3],row[4],row[5]);
				if row[3] == "4":
					with open('Pokemon\pokedex\pokedex\data\csv\\nilesh_pokemon_moves_TM.csv', mode='ab+') as qw:
						qw = csv.writer(qw, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						#qw.writerow(row);
						qw.writerow([row[0],row[2],row[5]]);
					#AddToPokemonMovesTable(row[0],row[2],row[3],row[4],row[5]);				
				line_count += 1    				
	print line_count;

def fill_in_pokemon_species():
	with open('Pokemon\pokedex\pokedex\data\csv\pokemon_species.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0;
		for row in csv_reader:
			if line_count == 0:
				print row;
				line_count += 1
			else:
				print row;
				AddToPokemonSpeciesTable(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16]);
				line_count += 1    			

def fill_in_pokemon_info():
	with open('Pokemon\pokedex\pokedex\data\csv\pokemon.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0;
		for row in csv_reader:
			if line_count == 0:
				print row;
				line_count += 1
			else:
				print row;
				AddToPokemonInfoTable(row[0],row[1],row[3],row[4],row[5],row[6],row[7]);
				line_count += 1    	
						
def get_random_pokemon(id,level):
	res =  GetStatsDb(str(id));
	res_info = GetPokemonNameDb(str(id));
	res_info = res_info[0];	
	Moves = getPokemonMovesDb(str(id),str(level));	
	L = [];	
	L.append(res_info);
	for x in res:
		L.append(x[2]);
	L = L + Moves;
	print L;