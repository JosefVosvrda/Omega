import tkinter as tk
from tkinter import ttk,messagebox
from main import dnf,time,prediction
race_map = {
    'Thailand': 0, 'Spain': 1, 'San Marino': 2, 'Qatar': 3, 'Portugal': 4,
    'Nederlands': 5, 'Malaysia': 6, 'Japan': 7, 'Italia': 8, 'Indonesia': 9,
    'Germany': 10, 'England': 11, 'France': 12, 'Emilia-Romagna': 13,
    'Catalunya': 14, 'Österreich': 15, 'Australian': 16, 'Argentina': 17,
    'Aragon': 18, 'USA': 19
}

rider_map = {
    93: 'M. Marquez', 73: 'A. Marquez', 63: 'F. Bagnaia', 21: 'F. Morbidelli',
    79: 'A. Ogura', 72: 'M. Bezzecchi', 5: 'J. Zarco', 33: 'B. Binder',
    23: 'E. Bastianini', 49: 'F. Di Giannantonio', 43: 'J. Miller',
    10: 'L. Marini', 54: 'F. Aldeguer', 88: 'M. Oliveira', 20: 'F. Quartararo',
    12: 'M. Viñales', 42: 'A. Rins', 35: 'C. Crutchlow', 37: 'A. Fernandez',
    32: 'L. Savadori', 25: 'R. Fernandez', 36: 'J. Mir', 1: 'F. Bagnaia',
    89: 'J. Martin', 31: 'G. Gerloff', 41: 'A. Espargaro', 30: 'T. Nakagami',
    44: 'P. Espargaro', 9: 'D. Petrucci', 40: 'D. Binder', 45: 'T. Nagashima',
    87: 'R. Gardner', 46: 'V. Rossi', 4: 'A. Dovizioso', 27: 'I. Lecuona',
    6: 'S. Bradl', 26: 'D. Pedrosa', 94: 'J. Folger', 53: 'T. Rabat',
    92: 'K. Watanabe', 51: 'M. Pirro', 29: 'A. Iannone', 85: 'T. Tsuda',
    96: 'J. Dixon'
}

root = tk.Tk()
root.title("MotoGP Prediction")

tk.Label(root, text="Jezdec").grid(row=0, column=0, sticky="e", padx=5, pady=5)
rider_cb = ttk.Combobox(root, values=[f"{v} ({k})" for k, v in rider_map.items()], width=30)
rider_cb.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Závod").grid(row=1, column=0, sticky="e", padx=5, pady=5)
race_cb = ttk.Combobox(root, values=list(race_map.keys()), width=30)
race_cb.grid(row=1, column=1, padx=5, pady=5)

fields = {
    "Teplota vzduchu (cislo)": tk.Entry(root),
    "Kondice trati (0(wet)–1(dry))": tk.Entry(root),
    "Vlhkost (cislene % tj. 0.41)": tk.Entry(root),
    "Sezóna": tk.Entry(root)
}
for i, (label, entry) in enumerate(fields.items(), start=2):
    tk.Label(root, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)
    entry.grid(row=i, column=1, padx=5, pady=5)

label_dnf = tk.Label(root, text="DNF:")
label_dnf.grid(row=8, column=0, columnspan=2, pady=5)
label_time = tk.Label(root, text="Time in ss:")
label_time.grid(row=9, column=0, columnspan=2, pady=5)
label_pos = tk.Label(root, text="Odhadovaná pozice:")
label_pos.grid(row=10, column=0, columnspan=2, pady=5)

def run_prediction():
    try:
        rider_selected = rider_cb.get()
        race_selected = race_cb.get()
        if not rider_selected or not race_selected:
            raise ValueError("Vyber jezdce a závod.")

        rider_number = int(rider_selected.split("(")[-1].replace(")", ""))
        race_id = race_map[race_selected]

        air_temp = float(fields["Teplota vzduchu (cislo)"].get())
        track_cond = int(fields["Kondice trati (0(wet)–1(dry))"].get())
        humidity = float(fields["Vlhkost (cislene % tj. 0.41)"].get())
        season = int(fields["Sezóna"].get())

        inputs = {
            "season": season,
            "rider_number": rider_number,
            "air_temp": air_temp,
            "track_cond": track_cond,
            "humidity": humidity,
            "race_id": race_id
        }
        dnf_out = dnf(inputs)
        time_out = time(inputs)
        results = prediction(inputs)
        label_dnf.config(text=f"DNF: {dnf_out:.0f}")
        label_time.config(text=f"Time in ss: {time_out:.0f}")
        label_pos.config(text=f"Odhadovaná pozice: {results:.0f}")

    except Exception as e:
        messagebox.showerror("Chyba", f"Nastala chyba:\n{e}")

tk.Button(root, text="Spustit predikci", command=run_prediction).grid(row=11, column=0, columnspan=2, pady=10)

root.mainloop()