import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
import calendar


class DateTimePicker(tk.Frame):
    """
    DateTime picker simple (pas de saisie libre)
    Format garanti : YYYY-MM-DD HH:MM
    Gère automatiquement les dates impossibles (31/02, etc.)
    """

    def __init__(self, parent, initial: str = ""):
        super().__init__(parent)

        now = datetime.now()
        y, m, d, hh, mm = now.year, now.month, now.day, now.hour, now.minute

        # Tentative de pré-remplissage
        try:
            dt = datetime.strptime(initial.strip(), "%Y-%m-%d %H:%M")
            y, m, d, hh, mm = dt.year, dt.month, dt.day, dt.hour, dt.minute
        except Exception:
            pass

        # Date → IntVar (pas de souci ici)
        self.var_year = tk.IntVar(value=y)
        self.var_month = tk.IntVar(value=m)
        self.var_day = tk.IntVar(value=d)

        # Heure / minute → StringVar (CRUCIAL)
        self.var_hour = tk.StringVar(value=f"{hh:02d}")
        self.var_minute = tk.StringVar(value=f"{mm:02d}")

        # ------------------- Widgets -------------------

        ttk.Label(self, text="Jour").grid(row=0, column=0, padx=(0, 4))
        self.sp_day = tk.Spinbox(
            self, from_=1, to=31, width=4,
            textvariable=self.var_day
        )
        self.sp_day.grid(row=0, column=1, padx=(0, 8))

        ttk.Label(self, text="Mois").grid(row=0, column=2, padx=(0, 4))
        self.sp_month = tk.Spinbox(
            self, from_=1, to=12, width=4,
            textvariable=self.var_month
        )
        self.sp_month.grid(row=0, column=3, padx=(0, 8))

        ttk.Label(self, text="Année").grid(row=0, column=4, padx=(0, 4))
        self.sp_year = tk.Spinbox(
            self, from_=2000, to=2900, width=6,
            textvariable=self.var_year
        )
        self.sp_year.grid(row=0, column=5, padx=(0, 12))

        ttk.Label(self, text="Heure").grid(row=0, column=6, padx=(0, 4))
        self.sp_hour = tk.Spinbox(
            self, from_=0, to=23, width=4,
            textvariable=self.var_hour,
            command=self._format_hour
        )
        self.sp_hour.grid(row=0, column=7, padx=(0, 8))

        ttk.Label(self, text="Min").grid(row=0, column=8, padx=(0, 4))
        self.sp_min = tk.Spinbox(
            self, from_=0, to=59, width=4,
            textvariable=self.var_minute,
            command=self._format_minute
        )
        self.sp_min.grid(row=0, column=9)

        # Sécurité : mise à jour automatique des jours du mois
        self.var_month.trace_add("write", self._on_month_or_year_change)
        self.var_year.trace_add("write", self._on_month_or_year_change)

        self._update_day_range()
        self._format_hour()
        self._format_minute()

    # -------------------------------------------------
    #   FORMATAGE HEURE / MINUTE (clé de la stabilité)
    # -------------------------------------------------
    def _format_hour(self):
        try:
            v = int(self.var_hour.get())
            self.var_hour.set(f"{v:02d}")
        except Exception:
            self.var_hour.set("00")

    def _format_minute(self):
        try:
            v = int(self.var_minute.get())
            self.var_minute.set(f"{v:02d}")
        except Exception:
            self.var_minute.set("00")

    # -------------------------------------------------
    #   GESTION DES DATES
    # -------------------------------------------------
    def _on_month_or_year_change(self, *_):
        self._update_day_range()

    def _update_day_range(self):
        try:
            year = int(self.var_year.get())
            month = int(self.var_month.get())
        except Exception:
            return

        max_day = calendar.monthrange(year, month)[1]
        self.sp_day.config(to=max_day)

        try:
            day = int(self.var_day.get())
        except Exception:
            day = 1

        if day > max_day:
            self.var_day.set(max_day)
        elif day < 1:
            self.var_day.set(1)

    # -------------------------------------------------
    #   SORTIE MÉTIER
    # -------------------------------------------------
    def get_value(self) -> str:
        """
        Retourne une string compatible avec Affaire.date
        """
        self._update_day_range()
        self._format_hour()
        self._format_minute()

        y = int(self.var_year.get())
        m = int(self.var_month.get())
        d = int(self.var_day.get())
        hh = int(self.var_hour.get())
        mm = int(self.var_minute.get())

        return f"{y:04d}-{m:02d}-{d:02d} {hh:02d}:{mm:02d}"
