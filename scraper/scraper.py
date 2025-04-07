import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape_motogp_classification(url):
    """
    Otevře zadanou URL (např. https://www.motogp.com/en/gp-results/2025/tha/motogp/rac/classification)
    v headless Chrome pomocí Selenia a vytáhne:
     - pozici (position)
     - body (points)
     - číslo jezdce (rider_number)
     - jméno jezdce (rider_name)
     - čas / gap (time_gap)
     - počasí (celkové, teplota vzduchu, stav trati, vlhkost, teplota země)

    Vrací tuple: (results_list, weather_dict)
      - results_list je list slovníků s klíči:
         {"position", "points", "rider_number", "rider_name", "time_gap"}
      - weather_dict je slovník s klíči:
         {"overall", "air_temp", "track_cond", "humidity", "ground_temp"}
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(3)  # čekáme, dokud se stránka plně nenačte

        # ================= POČASÍ =================
        weather_data = {
            "overall": None,
            "air_temp": None,
            "track_cond": None,
            "humidity": None,
            "ground_temp": None
        }
        try:
            weather_block = driver.find_element(By.CSS_SELECTOR, ".results-table__weather")
            columns = weather_block.find_elements(By.CSS_SELECTOR, ".results-table__weather-column")

            # První sloupec: celkové počasí a teplota vzduchu
            if len(columns) >= 1:
                header_1 = columns[0].find_elements(By.CSS_SELECTOR, ".results-table__weather-header")
                cell_1 = columns[0].find_elements(By.CSS_SELECTOR, ".results-table__weather-cell")
                if header_1 and cell_1:
                    weather_data["overall"] = header_1[0].text.strip()
                    weather_data["air_temp"] = cell_1[0].text.strip()

            # Druhý sloupec: stav trati
            if len(columns) >= 2:
                header_2 = columns[1].find_elements(By.CSS_SELECTOR, ".results-table__weather-header")
                cell_2 = columns[1].find_elements(By.CSS_SELECTOR, ".results-table__weather-cell")
                if header_2 and cell_2:
                    weather_data["track_cond"] = cell_2[0].text.strip()

            # Třetí sloupec: vlhkost
            if len(columns) >= 3:
                header_3 = columns[2].find_elements(By.CSS_SELECTOR, ".results-table__weather-header")
                cell_3 = columns[2].find_elements(By.CSS_SELECTOR, ".results-table__weather-cell")
                if header_3 and cell_3:
                    weather_data["humidity"] = cell_3[0].text.strip()

            # Čtvrtý sloupec: teplota země
            if len(columns) >= 4:
                header_4 = columns[3].find_elements(By.CSS_SELECTOR, ".results-table__weather-header")
                cell_4 = columns[3].find_elements(By.CSS_SELECTOR, ".results-table__weather-cell")
                if header_4 and cell_4:
                    weather_data["ground_temp"] = cell_4[0].text.strip()
        except Exception as e:
            print("Nepodařilo se najít/rozparsovat blok s počasím:", e)

        # ================= VÝSLEDKOVÁ TABULKA =================
        results = []
        try:
            table = driver.find_element(By.CSS_SELECTOR, ".results-table__table")
            rows = table.find_elements(By.CSS_SELECTOR, ".results-table__body-row")

            for row in rows:
                pos = None
                pts = None
                rider_number = None
                rider_name = None
                race_time = None

                try:
                    span_pos = row.find_element(By.CSS_SELECTOR,
                                                ".results-table__body-cell.results-table__body-cell--pos")
                    span_pts = row.find_element(By.CSS_SELECTOR,
                                                ".results-table__body-cell.results-table__body-cell--points")
                    pos = span_pos.text.strip()
                    pts = span_pts.text.strip()
                except Exception:
                    pass

                try:
                    rider_cell = row.find_element(By.CSS_SELECTOR, ".results-table__body-cell--rider")
                    rider_number = rider_cell.find_element(By.CSS_SELECTOR,
                                                           ".results-table__body-cell--number").text.strip()
                    rider_name = rider_cell.find_element(By.CSS_SELECTOR,
                                                         ".results-table__body-cell--full-name").text.strip()
                except Exception:
                    pass

                try:
                    time_cell = row.find_element(By.CSS_SELECTOR, ".results-table__body-cell--time")
                    race_time = time_cell.text.strip()
                except Exception:
                    pass

                results.append({
                    "position": pos,
                    "points": pts,
                    "rider_number": rider_number,
                    "rider_name": rider_name,
                    "time_gap": race_time
                })
        except Exception as e:
            print("Nepodařilo se najít tabulku s výsledky:", e)

        return results, weather_data

    finally:
        driver.quit()

def main(race):
    # Název CSV souboru, kam se uloží data ze všech sezón

    csv_filename = f'motogp_all_results__{race}.csv'
    # Otevřeme CSV soubor a zapíšeme hlavičku (včetně sloupce "season")
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "season", "position", "points", "rider_number", "rider_name", "time_gap",
            "weather_air_temp", "weather_track_cond", "weather_humidity"
        ])

        # Projde sezóny od 2025 do 2021
        for season in range(2024, 2020, -1):
            url = f"https://www.motogp.com/en/gp-results/{season}/{race}/motogp/rac/classification"
            print(f"Zpracovávám sezónu {season} z URL: {url}")
            results, weather = scrape_motogp_classification(url)

            for row in results:
                writer.writerow([
                    season,
                    row.get("position"),
                    row.get("points"),
                    row.get("rider_number"),
                    row.get("rider_name"),
                    row.get("time_gap"),
                    weather.get("track_cond"),
                    weather.get("humidity"),
                    weather.get("ground_temp")
                ])
            print(f"Sezóna {season} byla zpracována.\n")

    print(f"Hotovo! Data ze všech sezón byla uložena do {csv_filename}")

if __name__ == "__main__":
    main('qat')
