import tkinter as tk
from tkinter import ttk
import customtkinter
import mysql.connector
import dotenv
import os
import math

dotenv.load_dotenv()

#############################################
#                                           #
#             Fonction basique              #
#                                           #
#############################################
class Database:
	def __init__(self):
		self.connection = mysql.connector.connect(
			host=os.getenv("DB_HOST"),
			user=os.getenv("DB_USER"),
			password=os.getenv("DB_PASSWORD"),
			database=os.getenv("DB_NAME")
		)
		self.cursor = self.connection.cursor()

	def execute_query(self, query, params=None):
		try:
			self.cursor.execute(query, params)
			result = self.cursor.fetchall()  # Récupérer les résultats de la requête précédente
			self.connection.commit()
			return result
		except mysql.connector.Error as error:
			print("Erreur lors de l'exécution de la requête :", error)

	def close(self):
		self.cursor.close()
		self.connection.close()

class DataQuery:
	def __init__(self):
		self.db = Database()

	def get_clients(self):
		query = "SELECT * FROM clients"
		return self.db.execute_query(query)

	def get_client(self, id):
		query = "SELECT * FROM clients WHERE id = %s"
		return self.db.execute_query(query, (id,))
	
	def get_client_by_nom(self, nom):
		query = "SELECT * FROM clients WHERE nom = %s"
		return self.db.execute_query(query, (nom,))
	
	def get_client_by_prenom(self, prenom):
		query = "SELECT * FROM clients WHERE prenom = %s"
		return self.db.execute_query(query, (prenom,))
	
	def get_comptes(self):
		query = "SELECT * FROM comptes"
		return self.db.execute_query(query)
	
	def get_compte(self, id):
		query = "SELECT * FROM comptes WHERE id = %s"
		return self.db.execute_query(query, (id,))
	
	def get_operations(self):
		query = "SELECT * FROM operations"
		return self.db.execute_query(query)
	
	def get_operation(self, id):
		query = "SELECT * FROM operations WHERE id = %s"
		return self.db.execute_query(query, (id,))
	
	def get_operations_by_compte(self, compte_id):
		query = "SELECT * FROM operations WHERE compte_id = %s"
		return self.db.execute_query(query, (compte_id,))
	
	def get_operations_by_client(self, client_id):
		query = "SELECT * FROM operations WHERE client_id = %s"
		return self.db.execute_query(query, (client_id,))
	
	def create_client(self, nom, prenom, adresse, telephone):
		query = "INSERT INTO clients (nom, prenom, adresse, telephone) VALUES (%s, %s, %s, %s)"
		self.db.execute_query(query, (nom, prenom, adresse, telephone))

	def create_compte(self, client_id, solde):
		query = "INSERT INTO comptes (client_id, solde) VALUES (%s, %s)"
		self.db.execute_query(query, (client_id, solde))

	def create_operation(self, compte_id, client_id, type, montant):
		query = "INSERT INTO operations (compte_id, client_id, type, montant) VALUES (%s, %s, %s, %s)"
		self.db.execute_query(query, (compte_id, client_id, type, montant))

	def update_client(self, id, nom, prenom, adresse, telephone):
		query = "UPDATE clients SET nom = %s, prenom = %s, adresse = %s, telephone = %s WHERE id = %s"
		self.db.execute_query(query, (nom, prenom, adresse, telephone, id))

	def update_compte(self, id, client_id, solde):
		query = "UPDATE comptes SET client_id = %s, solde = %s WHERE id = %s"
		self.db.execute_query(query, (client_id, solde, id))

	def update_operation(self, id, compte_id, client_id, type, montant):
		query = "UPDATE operations SET compte_id = %s, client_id = %s, type = %s, montant = %s WHERE id = %s"
		self.db.execute_query(query, (compte_id, client_id, type, montant, id))

	def get_total_clients(self):
		query = "SELECT COUNT(*) FROM clients"
		result = self.db.execute_query(query)
		total_clients = result[0][0]  # Récupère la valeur de la première colonne de la première ligne
		return total_clients

	def get_all_money(self):
		query = "SELECT SUM(solde) FROM comptes"
		result = self.db.execute_query(query)
		total_money = result[0][0]  # Récupère la valeur de la première colonne de la première ligne
		return total_money

class SplashScreen:
	def __init__(self, root):
		self.root = root
		self.root.title("Banque Dubois - Écran de démarrage")

		# Définir la couleur de fond de la fenêtre
		self.root.configure(bg="#333333")

		# Définir la taille de la fenêtre
		self.root.geometry("400x300")

		# Centrer la fenêtre à l'écran
		self.center_window()

		# Ajouter un label pour le texte du SplashScreen
		splash_label = tk.Label(root, text="Banque Dubois", font=("Helvetica", 24, "bold"), bg="#333333", fg="#FFFFFF")
		splash_sublabel = tk.Label(root, text="Chargement . . .", font=("Helvetica", 12, "bold"), bg="#333333", fg="#FFFFFF")
		splash_version = tk.Label(root, text="Version 1.0", font=("Helvetica", 12, "bold"), bg="#333333", fg="#FFFFFF")

		# Centrer le label sur l'écran
		splash_label.pack(expand=True)
		splash_label.place(relx=0.5, rely=0.3, anchor='center')
		splash_sublabel.pack(expand=True)
		splash_sublabel.place(relx=0.5, rely=0.4, anchor='center')
		splash_version.pack(expand=True)
		splash_version.place(relx=0.5, rely=0.9, anchor='center')

		# Ajouter une barre de progression
		self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
		self.progress_bar.pack(expand=True)
		self.progress_bar.place(relx=0.5, rely=0.6, anchor='center')

		# Mettre à jour la valeur de la barre de progression à intervalles réguliers
		self.update_progress_bar()

	def update_progress_bar(self):
		value = self.progress_bar["value"]
		if value < 100:
			value += 25
			self.progress_bar["value"] = value
			self.root.after(500, self.update_progress_bar)
		else:
			self.close()


	def center_window(self):
		# Mettre à jour la géométrie de la fenêtre
		self.root.update_idletasks()

		# Obtenir la taille de l'écran
		screen_width = self.root.winfo_screenwidth()
		screen_height = self.root.winfo_screenheight()

		# Obtenir la taille de la fenêtre
		window_width = self.root.winfo_width()
		window_height = self.root.winfo_height()

		# Calculer les coordonnées pour centrer la fenêtre
		x = (screen_width - window_width) // 2
		y = (screen_height - window_height) // 2

		# Centrer la fenêtre à l'écran
		self.root.geometry("+{}+{}".format(x, y))

	def close(self):
		# Fermer la fenêtre d'écran de démarrage et ouvrir la page principale
		self.root.destroy()
		MainApplication()

class MainApplication(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Banque Dubois")
		self.geometry("960x540")
		self.center_window()

		self.grid_columnconfigure(1, weight=1)
		self.grid_columnconfigure((2, 3), weight=0)
		self.grid_rowconfigure((0, 1, 2), weight=1)

		self.sidebar_frame = customtkinter.CTkFrame(self, width=200, height=540, corner_radius=0)
		self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
		self.sidebar_frame.grid_rowconfigure(4, weight=1)

		self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Banque Dubois", font=customtkinter.CTkFont(size=20, weight="bold"))
		self.logo_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
		
		self.accueil_button = customtkinter.CTkButton(self.sidebar_frame, text="Accueil", command=self.show_accueil)
		self.accueil_button.grid(row=1, column=0, padx=20, pady=10)

		self.clients_button = customtkinter.CTkButton(self.sidebar_frame, text="Clients", command=self.show_clients)
		self.clients_button.grid(row=2, column=0, padx=20, pady=10)

		self.bourse_button = customtkinter.CTkButton(self.sidebar_frame, text="Bourse", command=self.show_bourse)
		self.bourse_button.grid(row=3, column=0, padx=20, pady=10)

		self.parametres_button = customtkinter.CTkButton(self.sidebar_frame, text="Paramètres", command=self.show_parametres)
		self.parametres_button.grid(row=7, column=0, padx=20, pady=10)

		self.pages = {
			"accueil": PageAccueil(self),
			"clients": PageClients(self),
			"bourse": PageBourse(self),
			"parametres": PageParametres(self)
		}

		# show Accueil page by default
		self.show_page("accueil")

	def center_window(self):
		self.update_idletasks()
		screen_width = self.winfo_screenwidth()
		screen_height = self.winfo_screenheight()
		window_width = self.winfo_width()
		window_height = self.winfo_height()
		x = (screen_width - window_width) // 2
		y = (screen_height - window_height) // 2
		self.geometry("+{}+{}".format(x, y))

	def show_page(self, page_name):
		for page in self.pages.values():
			page.grid_forget()
		self.pages[page_name].grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nw")

	def show_accueil(self):
		self.show_page("accueil")

	def show_clients(self):
		self.show_page("clients")

	def show_bourse(self):
		self.show_page("bourse")

	def show_parametres(self):
		self.show_page("parametres")

#############################################
#                                           #
#                Les pages                  #
#                                           #
#############################################
class PageAccueil(customtkinter.CTkFrame):
	def __init__(self, parent):
		super().__init__(parent, corner_radius=20, height=540, width=760)
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(0, weight=1)
		self.data_query = DataQuery()

		# Widget to display the title of the page
		label_title = customtkinter.CTkLabel(self, text="Accueil", font=customtkinter.CTkFont(size=20, weight="bold"))
		label_title.grid(row=0, column=1, padx=20, pady=20)

		# Add other widgets for the Accueil page here
	
		# Widget to display the total number of clients - CircularProgressBarClients
		label_total_clients = customtkinter.CTkLabel(self, text="Nombre de clients", font=customtkinter.CTkFont(size=20, weight="bold"))
		label_total_clients.grid(row=1, column=0, padx=20, pady=20)
		total_clients_bar = CircularProgressBarClients(self, size=200, bg_color='#2b2b2b', fill_color='#00aaff')
		total_clients_bar.grid(row=2, column=0, padx=20, pady=20)
		total_clients = self.data_query.get_total_clients()
		total_clients_bar.update_progress(int(total_clients), int(os.getenv("LIMITE_CLIENTS")),)

		# Widget to display the total money in bank - CircularProgressBarMoney
		label_total_money = customtkinter.CTkLabel(self, text="Argent Total", font=customtkinter.CTkFont(size=20, weight="bold"))
		label_total_money.grid(row=1, column=2, padx=20, pady=20)
		total_money_bar = CircularProgressBarMoney(self, size=200, bg_color='#2b2b2b', fill_color='#00aaff')
		total_money_bar.grid(row=2, column=2, padx=20, pady=20)
		total_money = self.data_query.get_all_money()
		total_money_bar.update_progress(int(total_money), int(os.getenv("LIMITE_ARGENT")),)

class PageClients(customtkinter.CTkFrame):
	def __init__(self, parent):
		super().__init__(parent, corner_radius=20, height=540, width=760)
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(0, weight=1)

		

		# Add other widgets for the Clients page here

class PageBourse(customtkinter.CTkFrame):
	def __init__(self, parent):
		super().__init__(parent, corner_radius=20, height=540, width=760)
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(0, weight=1)

		# Add other widgets for the Bourse page here

class PageParametres(customtkinter.CTkFrame):
	def __init__(self, parent):
		super().__init__(parent, corner_radius=20, height=540, width=760)
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(0, weight=1)

		# Add other widgets for the Parametres page here

#############################################
#                                           #
#           Fonction des pages              #
#                                           #
#############################################
class CircularProgressBarClients(tk.Canvas):
	def __init__(self, parent, size, bg_color='#2b2b2b', fill_color='#00aaff'):
		super().__init__(parent, width=size, height=size, bg=bg_color, highlightthickness=0)
		self.size = size
		self.bg_color = bg_color
		self.fill_color = fill_color

	def update_progress(self, current, total):
		angle = 360 * current / total
		self.delete("progress")
		self.create_arc((5, 5, self.size-5, self.size-5), start=90, extent=-angle, outline='', fill=self.fill_color, tags="progress")
		self.create_oval((40, 40, self.size-40, self.size-40), fill=self.bg_color, outline='')
		self.create_text((self.size//2, self.size//2), text=f"{current}", fill=self.fill_color, font=customtkinter.CTkFont(size=24, weight="bold"))

class CircularProgressBarMoney(tk.Canvas):
	def __init__(self, parent, size, bg_color='#2b2b2b', fill_color='#00aaff'):
		super().__init__(parent, width=size, height=size, bg=bg_color, highlightthickness=0)
		self.size = size
		self.bg_color = bg_color
		self.fill_color = fill_color

	def update_progress(self, current, total):
		angle = 360 * current / total
		self.delete("progress")
		self.create_arc((5, 5, self.size-5, self.size-5), start=90, extent=-angle, outline='', fill=self.fill_color, tags="progress")
		self.create_oval((40, 40, self.size-40, self.size-40), fill=self.bg_color, outline='')
		self.create_text((self.size//2, self.size//2), text=f"{current}$", fill=self.fill_color, font=customtkinter.CTkFont(size=24, weight="bold"))

if __name__ == "__main__":
	root = tk.Tk()
	splash = SplashScreen(root)
	root.mainloop()