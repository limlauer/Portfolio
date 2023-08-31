import pandas as pd
from selenium import webdriver
driver = webdriver.Chrome()
from bs4 import BeautifulSoup

# We need to initialize some variables and change some hardcoded stuff like the file name

all_columns = ['Kills','Deaths','Kill / Death','Kill / Round','Rounds with kills','Kill - Death difference',
'Total opening kills','Total opening deaths','Opening kill ratio','Opening kill rating','Team win percent after first kill','First kill in won rounds',
'0 kill rounds','1 kill rounds','2 kill rounds','3 kill rounds','4 kill rounds','5 kill rounds',
'Rifle kills','Sniper kills','SMG kills','Pistol kills','Grenade','Other', 'Event link']
empty_individual_df = pd.DataFrame(columns = all_columns)

def extract_individual_stats(csv_name, Player_Names_List, Overwrite, Start_index = 0, Ending_index = 0, File_save_iter = 5, filename = 'player_individual_stats.csv'):
    try:
        loaded_df = pd.read_csv(csv_name)
        print("Loaded existing CSV.")
    except FileNotFoundError:
        print("CSV file not found. Creating a new DataFrame.")
        loaded_df = empty_individual_df
    Output_DF = loaded_df
    
    if (Ending_index == 0):
        Ending_index = len(Player_Names_List)

    print(f"Preparing to search for {Ending_index} players...")
    processing_list = Player_Names_List[Start_index:Ending_index]

    existing_player_ids = list(Output_DF['Player ID']) # EXISTENTES
    existing_event_ids = list(Output_DF['event_ID']) # EXISTENTES
    total_rows = len(Player_Names_List) + 1
    save_index = 0 # File_save_iter is the max


    for index, row in processing_list.iterrows():
        player_id = row['Player ID']
        event_id = row['event_ID']
        player_name = row['name']

        if (not Overwrite) and (player_id in existing_player_ids) and (event_id in existing_event_ids):
            print(f"[{index}/{Ending_index} | {total_rows}] Skipping Player ID {player_id} in event {event_id} (already exists)")
            continue
        
        URL = f"https://www.hltv.org/stats/players/individual/{player_id}/{player_name.lower()}?event={event_id}"
        driver = webdriver.Chrome()
        driver.get(URL)
        page_source = driver.page_source
        driver.quit()

        soup1 = BeautifulSoup(page_source, "html.parser")
        soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

        stats_rows = soup2.find_all('div', class_='stats-row')
        stat_dict = {}  # Create a new empty dictionary
        print(f"[{index}/{Ending_index} | {total_rows}] Extracting data for {player_name}...")
        stat_dict['name'] = player_name
        stat_dict['Player ID'] = player_id
        stat_dict['event_ID'] = event_id
        stat_dict['Event link'] = f"https://www.hltv.org/stats/players/individual/{player_id}/{player_name}?event={event_id}"
        for row in stats_rows:
            stat_name = row.find('span').text.strip()
            stat_value = row.find_all('span')[1].text.strip()
            stat_dict[stat_name] = stat_value  # Add to dictionary
        
        stat_dict['Kill - Death difference'] = int(stat_dict['Kills']) - int(stat_dict['Deaths'])

        Output_DF = pd.concat([Output_DF, pd.DataFrame([stat_dict])], ignore_index=True)
        print(f"[{index}/{Ending_index} | {total_rows}] Added statistics for Player {player_name} with ID {player_id} in event {event_id}")
        save_index += 1
        if save_index >= File_save_iter:
            Output_DF.to_csv(filename, index=False)
            print(f"[SAVED] > File saved after {File_save_iter} iterations, as {filename}")
            save_index = 0
        
    Output_DF.to_csv(filename, index=False)
    print(f"[SAVED] > File saved as {filename}")