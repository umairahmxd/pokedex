import tkinter as tk
from tkinter import ttk
import requests
from io import BytesIO
from PIL import Image, ImageTk

# API
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"

# Define type weaknesses
TYPE_WEAKNESSES = {
    "Normal": ["Fighting"],
    "Fire": ["Water", "Rock", "Ground"],
    "Water": ["Electric", "Grass"],
    "Electric": ["Ground"],
    "Grass": ["Fire", "Ice", "Poison", "Flying", "Bug"],
    "Ice": ["Fire", "Fighting", "Rock", "Steel"],
    "Fighting": ["Flying", "Psychic", "Fairy"],
    "Poison": ["Ground", "Psychic"],
    "Ground": ["Water", "Ice", "Grass"],
    "Flying": ["Electric", "Ice", "Rock"],
    "Psychic": ["Bug", "Ghost", "Dark"],
    "Bug": ["Fire", "Flying", "Rock"],
    "Rock": ["Water", "Grass", "Fighting", "Ground", "Steel"],
    "Ghost": ["Ghost", "Dark"],
    "Dragon": ["Ice", "Dragon", "Fairy"],
    "Dark": ["Fighting", "Bug", "Fairy"],
    "Steel": ["Fire", "Fighting", "Ground"],
    "Fairy": ["Poison", "Steel"],
}

# Define type advantages (2x damage)
TYPE_ADVANTAGES = {
    "Normal": [],
    "Fire": ["Grass", "Ice", "Bug", "Steel"],
    "Water": ["Fire", "Ground", "Rock"],
    "Electric": ["Water", "Flying"],
    "Grass": ["Water", "Ground", "Rock"],
    "Ice": ["Grass", "Ground", "Flying", "Dragon"],
    "Fighting": ["Normal", "Ice", "Rock", "Dark", "Steel"],
    "Poison": ["Grass", "Fairy"],
    "Ground": ["Fire", "Electric", "Poison", "Rock", "Steel"],
    "Flying": ["Grass", "Fighting", "Bug"],
    "Psychic": ["Fighting", "Poison"],
    "Bug": ["Grass", "Psychic", "Dark"],
    "Rock": ["Fire", "Ice", "Flying", "Bug"],
    "Ghost": ["Psychic", "Ghost"],
    "Dragon": ["Dragon"],
    "Dark": ["Ghost", "Psychic"],
    "Steel": ["Ice", "Rock", "Fairy"],
    "Fairy": ["Fighting", "Dragon", "Dark"],
}

def fetch_pokemon_list(limit):
    # Fetch a list of Pokémon with the specified limit
    pokemon_list_url = f"{POKEAPI_BASE_URL}/pokemon?limit={limit}"
    response = requests.get(pokemon_list_url)
    if response.status_code == 200:
        data = response.json()
        pokemon_names = [entry['name'].capitalize() for entry in data['results']]
        return pokemon_names
    else:
        return ["Failed to fetch Pokémon list"]

def fetch_pokemon_data(name):
    # Fetch Pokémon details
    pokemon_url = f"{POKEAPI_BASE_URL}/pokemon/{name.lower()}"
    response = requests.get(pokemon_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def load_pokemon_image(image_url):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            image_data = BytesIO(response.content)
            image = Image.open(image_data)
            # Resize the image to 200x200
            image = image.resize((200, 200))
            return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Error loading image: {e}")
    return None

def on_listbox_select(event):
    selected_index = listbox.curselection()
    if selected_index:
        selected_name = listbox.get(selected_index[0])
        selected_pokemon = fetch_pokemon_data(selected_name)
        display_pokemon_details(selected_pokemon)

def display_pokemon_details(pokemon_data):
    # Display Pokémon details in the UI
    if pokemon_data:
        # Set the Pokémon name
        name_label.config(text=pokemon_data['name'].capitalize())

        # Load and display Pokémon image
        image_url = pokemon_data['sprites']['front_default']
        image = load_pokemon_image(image_url)
        if image:
            image_label.config(image=image)
            image_label.image = image

        # Get and display Pokémon types
        types = [t['type']['name'].capitalize() for t in pokemon_data['types']]
        type_str = ", ".join(types)
        type_label.config(text=f"Type: {type_str}")

        # Calculate weaknesses based on types and display them
        weaknesses = []
        for pokemon_type in types:
            weaknesses.extend(TYPE_WEAKNESSES.get(pokemon_type, []))
        weaknesses = list(set(weaknesses))
        weak_to_label.config(text=f"Weak To: {', '.join(weaknesses)}")

        # Calculate advantages (2x damage) based on types and display them
        advantages = []
        for pokemon_type in types:
            advantages.extend(TYPE_ADVANTAGES.get(pokemon_type, []))
        advantages = list(set(advantages))
        advantages_label.config(text=f"Advantages: {', '.join(advantages)}")

        # Get and display Pokémon stats
        stats = [f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}" for stat in pokemon_data['stats']]
        stats_str = "\n".join(stats)
        stats_label.config(text=f"Stats:\n{stats_str}")

# Create the main window
root = tk.Tk()
root.title("Pokémon App")
root.geometry("1200x600")  # Set window size

# Create a frame for the listbox
frame = ttk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Create a scrollbar for the listbox
scrollbar = ttk.Scrollbar(frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

# Create a listbox with scrollbar
listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE, font=("Arial", 16))
pokemon_names = fetch_pokemon_list(1010)
for name in pokemon_names:
    listbox.insert(tk.END, name)
listbox.pack(fill="both", expand=True)

# Configure the scrollbar to scroll the listbox
scrollbar.config(command=listbox.yview)

# Bind listbox selection to the event handler
listbox.bind("<<ListboxSelect>>", on_listbox_select)

# Create a frame for displaying Pokémon details
detail_frame = ttk.Frame(root)
detail_frame.grid(row=0, column=1, padx=10, pady=10)

# Create a label for displaying Pokémon image
image_label = ttk.Label(detail_frame)
image_label.grid(row=0, column=0, padx=10, pady=10)

# Create a label for displaying Pokémon name
name_label = ttk.Label(detail_frame, text="", font=("Arial", 20, "bold"))
name_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Create labels for displaying Pokémon type, weaknesses, advantages, and stats
type_label = ttk.Label(detail_frame, text="", font=("Arial", 16))
type_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

weak_to_label = ttk.Label(detail_frame, text="", font=("Arial", 16))
weak_to_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

advantages_label = ttk.Label(detail_frame, text="", font=("Arial", 16))
advantages_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

stats_label = ttk.Label(detail_frame, text="", font=("Arial", 16))
stats_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

# Start the Tkinter main loop
root.mainloop()
