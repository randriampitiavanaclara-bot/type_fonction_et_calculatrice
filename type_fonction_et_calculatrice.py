import tkinter as tk
from tkinter import ttk, messagebox
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ApplicationFonctions:
    def __init__(self, root):
        self.root = root
        self.root.title("Fonctions Mathématiques - Programmation Appliquée")
        self.root.geometry("1150x760")
        self.root.minsize(1000, 680)

        # ================= lohateny =================
        tk.Label(
            root,
            text="FONCTIONS MATHÉMATIQUES ET COURBES",
            font=("Arial", 18, "bold"),
            fg="#17365D"
        ).pack(pady=(8, 2))

        tk.Label(
            root,
            text="Choisir une fonction, entrer les paramètres puis afficher sa courbe",
            font=("Arial", 10),
            fg="#555555"
        ).pack(pady=(0, 8))

        # ================= varavarana lehibe iray misy ny zavatra rehetra dia ilay foncion sy courbes.ao anatiny daholo ny havia sy ankavanana  =================
        main = tk.Frame(root, bg="#eef3f8")
        main.pack(fill="both", expand=True, padx=10, pady=5)

        # ================= fampisehoana ilay ecran nozaraina roa dia ilay ilany havia izay ahitana ny type de fonction,parametre ary calculatrice=================
        left = tk.Frame(main, bg="#e3ebf5", bd=1, relief="solid", width=325)
        left.pack(side="left", fill="y", padx=(0, 8))
        left.pack_propagate(False)

        tk.Label(
            left,
            text="Type de fonction",
            font=("Arial", 13, "bold"),
            bg="#e3ebf5",
            fg="#17365D"
        ).pack(pady=(12, 5))

        self.combo = ttk.Combobox(
            left,
            state="readonly",
            width=29,
            values=[
                "affine (ax+b)",
                "linéaire (ax)",
                "polynôme (ax²+bx+c)",
                "puissance (x^n)",
                "exponentielle (a*e^x)",
                "logarithme (a*ln(x))"
            ]
        )
        self.combo.set("affine (ax+b)")
        self.combo.pack(pady=4)
        self.combo.bind("<<ComboboxSelected>>", self.changer_fonction)

        # fikirana kajy ny zavatra namboarina:loko,habe soratra,type calcule
        tk.Label(
            left,
            text="Paramètres",
            font=("Arial", 11, "bold"),
            bg="#e3ebf5",
            fg="#17365D"
        ).pack(pady=(8, 2))

        self.form = tk.Frame(left, bg="#e3ebf5")
        self.form.pack()
        self.entries = {}
        self.creer_champs()

        tk.Button(
            left,
            text="AFFICHER LA COURBE",
            command=self.calculer,
            bg="#1976D2",
            fg="white",
            activebackground="#0D47A1",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            width=24,
            relief="flat",
            cursor="hand2"
        ).pack(pady=8)

        self.info = tk.Label(
            left,
            text="",
            bg="#e3ebf5",
            fg="#137333",
            justify="left",
            wraplength=285,
            font=("Arial", 9, "bold")
        )
        self.info.pack(padx=8, pady=2)

        # ================= fanaovana ilay eo akaikin' ny sary toerana misy ilay calcul siantifika  =================
        calc_box = tk.Frame(
            left,
            bg="#172033",
            bd=1,
            relief="solid"
        )
        calc_box.pack(fill="x", padx=8, pady=(8, 8))

        tk.Label(
            calc_box,
            text="🧮 CALCULATRICE SCIENTIFIQUE",
            font=("Arial", 11, "bold"),
            bg="#172033",
            fg="white"
        ).pack(pady=(7, 5))

        self.calc_entry = tk.Entry(
            calc_box,
            font=("Arial", 14, "bold"),
            justify="right",
            bg="#F7F9FC",
            fg="#172033",
            insertbackground="#1976D2",
            relief="flat"
        )
        self.calc_entry.pack(fill="x", padx=8, pady=5, ipady=7)

        boutons = [
            ["C", "(", ")", "/", "√"],
            ["7", "8", "9", "*", "sin"],
            ["4", "5", "6", "-", "cos"],
            ["1", "2", "3", "+", "tan"],
            ["0", ".", "**", "=", "log"],
            ["π", "e", "exp", "log10", "%"]
        ]

        frame_buttons = tk.Frame(calc_box, bg="#172033")
        frame_buttons.pack(padx=5, pady=(2, 7))

        for r, ligne in enumerate(boutons):
            for c, texte in enumerate(ligne):
                couleur = "#263B63"
                texte_couleur = "white"

                if texte == "=":
                    couleur = "#1976D2"
                elif texte == "C":
                    couleur = "#D32F2F"
                elif texte in ["sin", "cos", "tan", "log", "√", "exp", "log10"]:
                    couleur = "#00897B"
                elif texte in ["+", "-", "*", "/", "**", "%"]:
                    couleur = "#F39C12"
                    texte_couleur = "#172033"
                elif texte in ["π", "e", "(", ")"]:
                    couleur = "#5E6F91"

                tk.Button(
                    frame_buttons,
                    text=texte,
                    width=4,
                    height=1,
                    font=("Arial", 9, "bold"),
                    bg=couleur,
                    fg=texte_couleur,
                    activebackground="#90CAF9",
                    activeforeground="black",
                    relief="flat",
                    cursor="hand2",
                    command=lambda t=texte: self.cliquer_calculatrice(t)
                ).grid(row=r, column=c, padx=2, pady=2)

        # ================= fampisehoana ilay courbe ankavanana araka izay tsindriana ao aminy ilay type du fonction=================
        right = tk.Frame(main, bg="white", bd=1, relief="solid")
        right.pack(side="left", fill="both", expand=True)

        tk.Label(
            right,
            text="Représentation graphique",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#17365D"
        ).pack(pady=8)

        self.graph_frame = tk.Frame(right, bg="white")
        self.graph_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.calculer()

    # ================= Fibaikoana ny endrikiny ny sary ankavanana izay afaka anovana ny valeur ilay na a,na b,c ka mampiova ilay sary courbe araka ny fanovana azy =================

    def creer_champ(self, nom, valeur, ligne):
        tk.Label(
            self.form, text=nom + " :",
            bg="#e3ebf5",
            font=("Arial", 9, "bold")
        ).grid(row=ligne, column=0, sticky="e", padx=3, pady=3)

        e = tk.Entry(
            self.form, width=9,
            justify="center",
            font=("Arial", 9)
        )
        e.insert(0, valeur)
        e.grid(row=ligne, column=1, padx=3, pady=3)
        self.entries[nom] = e

    def creer_champs(self):
        for w in self.form.winfo_children():
            w.destroy()

        self.entries = {}
        type_f = self.combo.get()

        if type_f == "affine (ax+b)":
            self.creer_champ("a", "2", 0)
            self.creer_champ("b", "3", 1)

        elif type_f == "linéaire (ax)":
            self.creer_champ("a", "2", 0)

        elif type_f == "polynôme (ax²+bx+c)":
            self.creer_champ("a", "1", 0)
            self.creer_champ("b", "-6", 1)
            self.creer_champ("c", "5", 2)

        elif type_f == "puissance (x^n)":
            self.creer_champ("n", "4", 0)

        elif type_f == "exponentielle (a*e^x)":
            self.creer_champ("a", "1", 0)

        elif type_f == "logarithme (a*ln(x))":
            self.creer_champ("a", "1", 0)

    def changer_fonction(self, event=None):
        self.creer_champs()
        self.info.config(text="")
        self.calculer()

    def afficher_graphique(self, X, Y, titre, points=None):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=100)
        fig.patch.set_facecolor("white")
        ax.set_facecolor("#fbfdff")

        ax.plot(X, Y, linewidth=2.5, label=titre)
        ax.axhline(0, color="#333333", linewidth=1)
        ax.axvline(0, color="#333333", linewidth=1)
        ax.grid(True, alpha=0.30)
        ax.set_title(titre, fontsize=13, fontweight="bold")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")

        if points:
            for x, y, couleur, nom in points:
                ax.plot(x, y, marker="o", color=couleur,
                        markersize=8, label=nom)

        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    def calculer(self):
        type_f = self.combo.get()

        try:
            points = None

            if type_f == "affine (ax+b)":
                a = float(self.entries["a"].get())
                b = float(self.entries["b"].get())
                X = np.linspace(-10, 10, 500)
                Y = a * X + b
                titre = f"f(x) = {a}x + {b}"

                if a != 0:
                    racine = -b / a
                    info = f"Pente a = {a}\nOrdonnée b = {b}\nRacine x = {racine:.2f}"
                else:
                    info = f"a = 0\nFonction constante : f(x) = {b}"

            elif type_f == "linéaire (ax)":
                a = float(self.entries["a"].get())
                X = np.linspace(-10, 10, 500)
                Y = a * X
                titre = f"f(x) = {a}x"
                info = f"Pente a = {a}\nLa droite passe par O(0,0)"

            elif type_f == "polynôme (ax²+bx+c)":
                a = float(self.entries["a"].get())
                b = float(self.entries["b"].get())
                c = float(self.entries["c"].get())

                if a == 0:
                    raise ValueError("a doit être différent de 0.")

                delta = b*b - 4*a*c
                xv = -b / (2*a)
                yv = a*xv*xv + b*xv + c

                X = np.linspace(xv - 7, xv + 7, 500)
                Y = a*X**2 + b*X + c
                titre = f"f(x) = {a}x² + {b}x + {c}"

                points = [(xv, yv, "red", "Sommet")]

                if delta > 0:
                    x1 = (-b - math.sqrt(delta)) / (2*a)
                    x2 = (-b + math.sqrt(delta)) / (2*a)
                    points += [(x1, 0, "green", "Racine"),
                               (x2, 0, "green", "Racine")]
                    info = f"Δ = {delta:.2f}\nS({xv:.2f} ; {yv:.2f})\nx₁ = {x1:.2f}   x₂ = {x2:.2f}"
                elif delta == 0:
                    points.append((xv, 0, "green", "Racine double"))
                    info = f"Δ = 0\nS({xv:.2f} ; {yv:.2f})\nRacine double = {xv:.2f}"
                else:
                    info = f"Δ = {delta:.2f}\nS({xv:.2f} ; {yv:.2f})\nAucune racine réelle"

            elif type_f == "puissance (x^n)":
                n = int(self.entries["n"].get())
                X = np.linspace(0, 5, 500)
                Y = X ** n
                titre = f"f(x) = x^{n}"
                info = f"Puissance n = {n}"

            elif type_f == "exponentielle (a*e^x)":
                a = float(self.entries["a"].get())
                X = np.linspace(-3, 3, 500)
                Y = a * np.exp(X)
                titre = f"f(x) = {a}eˣ"
                info = f"Coefficient a = {a}\nDomaine : R"

            elif type_f == "logarithme (a*ln(x))":
                a = float(self.entries["a"].get())
                X = np.linspace(0.05, 10, 500)
                Y = a * np.log(X)
                titre = f"f(x) = {a}ln(x)"
                info = f"Coefficient a = {a}\nDomaine : ]0 ; +∞["

            self.info.config(text=info)
            self.afficher_graphique(X, Y, titre, points)

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    # ================= fikajina scientifique rehefa manindry bokotra dia ity no mampandeha azy  ao amin'ilay fotsy kely ambonin'ilay bokotra =================

    def cliquer_calculatrice(self, t):
        if t == "C":
            self.calc_entry.delete(0, tk.END)
        elif t == "=":
            self.calculer_scientifique()
        elif t == "√":
            self.calc_entry.insert(tk.END, "sqrt(")
        elif t in ["sin", "cos", "tan", "log", "log10", "exp"]:
            self.calc_entry.insert(tk.END, t + "(")
        elif t == "π":
            self.calc_entry.insert(tk.END, str(math.pi))
        elif t == "e":
            self.calc_entry.insert(tk.END, str(math.e))
        else:
            self.calc_entry.insert(tk.END, t)

    def calculer_scientifique(self):
        try:
            expression = self.calc_entry.get()

            fonctions = {
                "sqrt": math.sqrt,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "log": math.log,
                "log10": math.log10,
                "exp": math.exp,
                "pi": math.pi,
                "e": math.e
            }

            resultat = eval(
                expression,
                {"__builtins__": None},
                fonctions
            )

            self.calc_entry.delete(0, tk.END)
            self.calc_entry.insert(0, str(resultat))

        except Exception:
            self.calc_entry.delete(0, tk.END)
            self.calc_entry.insert(0, "Erreur")


# ================= mampandehanana ilay kajy X sy Y izay tsy hita maso ny fikajiana azy fa mahatonga  ny sary hiseo rehefa manindry AFFICHER LA COURBE  =================

if __name__ == "__main__":
    root = tk.Tk()
    app = ApplicationFonctions(root)
    root.mainloop()
