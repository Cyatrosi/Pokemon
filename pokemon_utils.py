import bs4
import requests			
import os
import pymysql

def AddToStatsTable(Pno,Name,HP,Attack,Defense,SpAttack,SpDefense,Speed,Total,Type_1,Type_2,Special,Special_Type,Sprite_Link):	
	conn = pymysql.connect(host = 'localhost',user = 'root',password = '',db = 'Pokemon')
	a = conn.cursor();
	#Query = "SELECT * FROM " + Table;	
	Name = Name.replace("'","#");
	Special = Special.replace("'","#");	
	Sprite_Link = Sprite_Link.replace("'","#");
	Query = "INSERT INTO `" + "Pokemon" + "` (`Pokedex_No`, `Name`, `HP`, `Attack`, `Defense`, `SpAttack`,`SpDefense`, `Speed`, `Total`, `Type 1`, `Type 2`, `Special`, `Special_Type`, `Sprite_Link`) VALUES ('" + str(Pno) + "', '" + Name + "', '" + HP + "','"+Attack+"', '"+Defense+"', '"+SpAttack+"', '"+SpDefense+"', '"+Speed+"', '"+Total+"','"+Type_1+"','"+Type_2+"', '"+Special+"', '"+Special_Type+"', '"+Sprite_Link+"');";		
	a.execute(Query);	

def AddToEvTable(Pno,HP,Attack,Defense,SpAttack,SpDefense,Speed,Special,Special_Type):	
	conn = pymysql.connect(host = 'localhost',user = 'root',password = '',db = 'Pokemon')
	a = conn.cursor();
	#Query = "SELECT * FROM " + Table;		
	Special = Special.replace("'","#");		
	Query = "INSERT INTO `" + "Ev" + "` (`Pokedex_No`, `HP`, `Attack`, `Defense`, `SpAttack`,`SpDefense`, `Speed`, `Special`, `Special_Type`) VALUES ('" + str(Pno) + "', '" + str(HP) + "','"+str(Attack)+"', '"+str(Defense)+"', '"+str(SpAttack)+"', '"+str(SpDefense)+"', '"+str(Speed)+"', '"+Special+"', '"+Special_Type+"');";		
	a.execute(Query);	

def AddToMovesTable(Pno,Name,Type,Cat,Power,Acc,Pp,TM,Effect,Prob):
	conn = pymysql.connect(host = 'localhost',user = 'root',password = '',db = 'Pokemon')
	a = conn.cursor();
	#Query = "SELECT * FROM " + Table;	
	Name = Name.replace("'","#");	
	Effect = Effect.replace("'","#");			
	Query = "INSERT INTO `" + "moves" + "` (`No`, `Name`, `Type`, `Category`, `Power`, `Accuracy`, `PP`, `TM`, `Effect`, `Probability`) VALUES ('" + str(Pno) + "', '" + Name + "','"+Type+"', '"+Cat+"', '"+Power+"', '"+Acc+"', '"+Pp+"', '"+TM+"', '"+Effect+"', '"+Prob+"');";		
	a.execute(Query);		

def getSpecialType(Type):
	if "Mega" in Type:
		return "Mega";
	if "Primal" in Type:
		return "Primal";
	else:
		return "Form";

def get_name_from_link(Link):
	return Link.split('/')[-1];	

def download_image(url,Path,Name):
	r2 = requests.get(url);	
	directory = Path + Name;
#	print Path;
#	print directory;
	if not os.path.exists(Path):
		os.makedirs(Path);	
	with open(directory, "wb") as f:
		f.write(r2.content);

def get_all_sprites(url,PokemonName):
	html = requests.get(url)
	soup=bs4.BeautifulSoup(html.text,'html.parser')
	Table = soup.findAll('table',{"class": "data-table sprites-table wide-table"})[0];
	tr = Table.findAll('tr')[1];
	Lap = 1;
	for td in tr.findAll('td'):
		images = td.findAll('img');
		Fname = "Default";
		if Lap == 2:
			Fname = "Normal";
		if Lap == 3:
			Fname = "Shiny";		
		Path = "PokemonSprites/"+ PokemonName + "/" + str(Fname) + "/";
		i = 0;
		for image in images:
			Link = image['data-original'];
			#SplitLink = Link.split('/');
			#Name1 = SplitLink[-1];
			Name1 = get_name_from_link(Link);
			Name = str(i+1) + "." + Name1.split('.')[1];				
			download_image(Link,Path,Name);
			i = i + 1;	
		Lap = Lap + 1;

def crawl_sprites(Url):
	Base = Url[:-7];
	html = requests.get(Url)
	soup=bs4.BeautifulSoup(html.text,'html.parser')
	Cards = soup.findAll('span',{"class": "infocard"});
	Count = 0;
	for card in Cards:
		Cdata = card.find('span',{"class": "infocard-data"});
		Link = Base + Cdata.find('a')['href'];
		Name = get_name_from_link(Link);
		#print Name,Link; 
		#PokemonName = "venusaur";
		url = Url + "/" + Name;
		print url;
		get_all_sprites(url,Name);
		Count = Count + 1;
	print Count;		

def crawl_stats(url):
	'''
	DB Structure --> 
	Pokedex No. :
	Name :
	HP :
	Attack :
	Defense :
	SpAttack :
	SpDefense :
	Speed :
	Total : 
	Type 1 :
	Type 2 :
	Special :
	Special Type :
	Sprite Link : ---
	'''
	U = url[:-3];
	#b = [];
	html = requests.get(url)
	soup=bs4.BeautifulSoup(html.text,'html.parser')
	table = soup.find("table",id = "pokedex");
	tr = table.find_all("tr");	
	for row in tr:
		values = [];
		Special = "None"
		SpecialType = "None";
		Type1 = "None";
		Type2 = "None";
		InfoLink = "None";
		i = 0;
		for val in row.find_all("td"):
			values.append(val.text.encode('ascii','ignore'))
			if i == 1:				
				InfoLink = U + val.a['href'].split("/")[2];				
				if val.small != None:										
					Special = val.small.text.encode('ascii','ignore');
					SpecialType = getSpecialType(val.small.text.encode('ascii','ignore'));
			if i == 2:
				Types = val.find_all('a');				
				if len(Types)>0:
					Type1 = Types[0].text.encode('ascii','ignore');
				if len(Types)>1:
					Type2 = Types[1].text.encode('ascii','ignore');				
			i = i + 1;
		#print values;		
		if len(values)>1:
			Pno = int(values[0]);
			Name = values[1];			
			Total = values[3];
			HP = values[4];
			Attack = values[5];
			Defense = values[6];
			SpAttack = values[7];
			SpDefense = values[8];			
			Speed = values[9];
			#crawl_pokemon_moves(InfoLink,Pno);						
			#b.append({Pno,Special,SpecialType});
			#print Pno,Name,HP,Attack,Defense,SpAttack,SpDefense,Speed,Total,Type1,Type2,Special,SpecialType,InfoLink;
			AddToStatsTable(Pno,Name,HP,Attack,Defense,SpAttack,SpDefense,Speed,Total,Type1,Type2,Special,SpecialType,InfoLink);			
	#return b;

def crawl_ev(url):
	U = url[:-3];
	#b = [];
	html = requests.get(url)
	soup=bs4.BeautifulSoup(html.text,'html.parser')
	table = soup.find("table",{"class": "data-table block-wide"});	
	tr = table.find_all("tr");
	for row in tr:
		values = [];
		Special = "None"
		SpecialType = "None";
		Type1 = "None";
		Type2 = "None";
		InfoLink = "None";
		i = 0;
		for val in row.find_all("td"):
			values.append(val.text.encode('ascii','ignore'))			
			if i == 1:								
				if val.small != None:										
					Special = val.small.text.encode('ascii','ignore');
					SpecialType = getSpecialType(val.small.text.encode('ascii','ignore'));			
			i = i + 1;
		#print values;		
		if len(values)>1:				
			Pno = int(values[0]);						
			if values[2] != '':
				Hp = int(values[2]);
			else:
				Hp = 0;
			if values[3] != '':	
				Attack = int(values[3]);
			else:
				Attack = 0;
			if values[4] != '':				
				Defense = int(values[4]);
			else:
				Defense = 0;
			if values[5] != '':
				SpAttack = int(values[5]);
			else:
				SpAttack = 0;
			if values[6] != '':				
				SpDefense = int(values[6]);			
			else:
				SpDefense = 0;
			if values[7] != '':
				Speed = int(values[7]);
			else:
				Speed = 0;
			Special,SpecialType;
			#b.append({Pno,Special,SpecialType});			
			#print Pno,Hp,Attack,Defense,SpAttack,SpDefense,Speed,Special,SpecialType;
			AddToEvTable(Pno,Hp,Attack,Defense,SpAttack,SpDefense,Speed,Special,SpecialType);
	#return b;
	
def crawl_moves(url):
	U = url[:-3];
	#b = [];
	html = requests.get(url)
	soup=bs4.BeautifulSoup(html.text,'html.parser')
	table = soup.find("table",id = "moves");	
	tr = table.find_all("tr");
	row_no = 1;
	for row in tr:
		values = [];
		Special = "None"
		SpecialType = "None";
		Type1 = "None";
		Type2 = "None";
		InfoLink = "None";
		i = 0;
		for val in row.find_all("td"):
			if i == 2:
				V = val['data-sort-value'];
				values.append(V.encode('ascii','ignore'))
			else:	
				values.append(val.text.encode('ascii','ignore'))						
			i = i + 1;
		#print values;		
		if len(values)>1:				
			Pno = row_no;						
			Name = values[0];
			Type = values[1];
			if values[2] == '':
				Cat = "Z-Move";
			else:
				Cat = values[2];					
			Power = values[3];						
			Acc = values[4];						
			Pp = values[5];		
			if values[6] == '':
				TM = "None"
			else:	
				TM = values[6];
			Effect = values[7];						
			if values[8] == '':
				Prob = "None";
			else:
				Prob = values[8];											
			#b.append({Pno,Special,SpecialType});			
			#print Pno,Name,Type,Cat,Power,Acc,Pp,TM,Effect,Prob;
			row_no = row_no + 1;
			AddToMovesTable(Pno,Name,Type,Cat,Power,Acc,Pp,TM,Effect,Prob);		
	#return b;

def check_for_move_availability(url):	
	html = requests.get(url)
	soup=bs4.BeautifulSoup(html.text,'html.parser');
	divs = soup.find_all("div",{"class": "grid-row"});
	div = divs[5];	
	#print div;
	paras1 = div.find_all("p");	
	paras = paras1[:4];	
	l = [];	
	for x in paras:		
		if 'does not' in x.text.encode('ascii','ignore'):
			l.append(0);
		else:
			l.append(1);
	if len(l)<4:
		diff = 4-len(l);
		for i in range(diff):
			l.append(0);
	print l;
	return l;

def crawl_pokemon_moves(url,index,moveMap):
	U = url[:-3];	
	html = requests.get(url)
	soup=bs4.BeautifulSoup(html.text,'html.parser')
	tables = soup.find_all("table",{"class": "data-table"});		
	available = check_for_move_availability(url);
	Path = "Pokemon Moves\\";	
	Pindex = 0;
	# Learnt Moves
#	print "Learn Moves ######################";
	fname = Path + str(index) + "_learnt_moves";
	f = open(fname,"w")
	table = tables[Pindex];
	tr = table.find_all("tr");	
	if len(tr)>0 and available[0] == 1:
		Pindex = Pindex + 1;
		for row in tr:
			values = [];		
			i = 0;
			for val in row.find_all("td"):						
				if i == 3:				
					V = val['data-sort-value'];
					values.append(V.encode('ascii','ignore'))
				else:	
					values.append(val.text.encode('ascii','ignore'))									
				i = i + 1;		
			if len(values)>1:				
				Level = values[0];
				Move = values[1];
				Type = values[2];				
				Cat = values[3];	
				if values[4] == '':
					Power = "---"
				else:		
					Power = values[4];
				if values[5] == '':
					Acc = "---";
				else:
					Acc = values[5];																	
				#b.append({Pno,Special,SpecialType});							
				#print Level,Move,Type,Cat,Power,Acc;
				MoveIndex =  moveMap[Move];
				#w = Level + "#" + Move + "#" + Type + "#" + Cat + "#" + Power + "#" + Acc + "\n";			
				w = Level + "#" + str(MoveIndex);
				f.write(w);
				#AddToMovesTable(Pno,Name,Type,Cat,Power,Acc,Pp,TM,Effect,Prob);			

	# Egg Moves
#	print "Egg Moves ######################";
	fname = Path + str(index) + "_egg_moves";
	f = open(fname,"w")
	table = tables[Pindex];
	tr = table.find_all("tr");		
	if len(tr)>0 and available[1] == 1:
		Pindex = Pindex + 1;
		for row in tr:
			values = [];		
			i = 0;
			for val in row.find_all("td"):			
				if i == 2:				
					V = val['data-sort-value'];
					values.append(V.encode('ascii','ignore'))
				else:	
					values.append(val.text.encode('ascii','ignore'))						
				i = i + 1;		
			if len(values)>1:				
				Move = values[0];
				Type = values[1];
				Cat = values[2];	
				if values[3] == '':					
					Power = "---";
				else:
					Power = values[3];			
				if values[4] == '':
					Acc = "---";
				else:
					Acc = values[4];									
				#b.append({Pno,Special,SpecialType});			
				#print Move,Type,Cat,Power,Acc;		
				MoveIndex =  moveMap[Move];	
				#w = Move + "#" + Type + "#" + Cat + "#" + Power + "#" + Acc + "\n";			
				w = str(MoveIndex);
				f.write(w);
				#AddToMovesTable(Pno,Name,Type,Cat,Power,Acc,Pp,TM,Effect,Prob);			
		
	# Tutor Moves
#	print "Tutor Moves ######################";
	fname = Path + str(index) + "_tutor_moves";
	f = open(fname,"w")
	table = tables[Pindex];
	tr = table.find_all("tr");		
	if len(tr)>0 and available[2] == 1:
		Pindex = Pindex + 1;
		for row in tr:
			values = [];		
			i = 0;
			for val in row.find_all("td"):			
				if i == 2:
					V = val['data-sort-value'];
					values.append(V.encode('ascii','ignore'))
				else:	
					values.append(val.text.encode('ascii','ignore'))						
				i = i + 1;		
			if len(values)>1:				
				Move = values[0];
				Type = values[1];
				Cat = values[2];				
				if values[3] == '':					
					Power = "---";
				else:
					Power = values[3];			
				if values[4] == '':
					Acc = "---";
				else:
					Acc = values[4];									
				#b.append({Pno,Special,SpecialType});			
				#print Move,Type,Cat,Power,Acc;			
				MoveIndex =  moveMap[Move];
				#w = Move + "#" + Type + "#" + Cat + "#" + Power + "#" + Acc + "\n";			
				w = str(MoveIndex);
				f.write(w);
				#AddToMovesTable(Pno,Name,Type,Cat,Power,Acc,Pp,TM,Effect,Prob);			
		
	# TM Moves
#	print "TM Moves ######################";
	fname = Path + str(index) + "_tm_moves";
	f = open(fname,"w")
	table = tables[Pindex];
	tr = table.find_all("tr");		
	if len(tr)>0 and available[3] == 1:
		Pindex = Pindex + 1;
		for row in tr:
			values = [];		
			i = 0;
			for val in row.find_all("td"):						
				if i == 3:
					V = val['data-sort-value'];
					values.append(V.encode('ascii','ignore'))
				else:	
					values.append(val.text.encode('ascii','ignore'))									
				i = i + 1;		
			if len(values)>1:				
				TM = values[0];
				Move = values[1];
				Type = values[2];				
				Cat = values[3];	
				if values[4] == '':
					Power = "---"
				else:		
					Power = values[4];
				if values[5] == '':
					Acc = "---";
				else:
					Acc = values[5];																	
				#b.append({Pno,Special,SpecialType});			
				#print TM,Move,Type,Cat,Power,Acc;			
				MoveIndex =  moveMap[Move];
				#w = TM + "#" + Move + "#" + Type + "#" + Cat + "#" + Power + "#" + Acc + "\n";			
				w = TM + "#" + str(MoveIndex);
				f.write(w);
				#AddToMovesTable(Pno,Name,Type,Cat,Power,Acc,Pp,TM,Effect,Prob);			

def get_all_moves():
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

def get_Pokemons():
	conn = pymysql.connect(host = 'localhost',user = 'root',password = '',db = 'Pokemon')
	cur = conn.cursor();			
	Query = "SELECT Pokedex_No,Sprite_Link FROM pokemon";	
	cur.execute(Query);		
	L = [];	
	for move in cur.fetchall():
		L.append(move);		
	return L;
