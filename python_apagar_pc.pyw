import os
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import re
import subprocess
import datetime
import json

class ShutdownScheduler:
    CONFIG_FILE = "shutdown_config.json"

    def __init__(self, master):
        self.master = master
        master.title("Programador de Apagado del PC")
        master.geometry("550x600")
        master.resizable(False, False)

        # Establece el icono usando el archivo ICO con manejo de errores
        try:
            # Asegúrate de que la ruta sea correcta.
            # os.path.abspath(__file__) obtiene la ruta del script actual.
            # os.path.join() construye una ruta segura para diferentes sistemas operativos.
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
            
            if not os.path.exists(icon_path):
                print(f"ERROR: El archivo de icono no se encontró en: {icon_path}")
                # Puedes mostrar un messagebox si quieres alertar al usuario
                # messagebox.showerror("Error de Icono", f"El archivo de icono 'icon.ico' no se encontró en la ruta esperada: {icon_path}")
            else:
                self.master.iconbitmap(icon_path)
        except tk.TclError as e: # Captura errores específicos de Tkinter/Tcl
            print(f"ERROR Tkinter al cargar el icono: {e}")
            print("Posiblemente el archivo .ico está dañado o no es válido.")
            # Puedes mostrar un messagebox aquí también
            # messagebox.showerror("Error de Icono", f"No se pudo cargar el icono: {e}\nAsegúrate de que 'icon.ico' sea un archivo de icono válido.")
        except Exception as e: # Captura cualquier otro error inesperado
            print(f"ERROR GENERAL al cargar el icono: {e}")
            # messagebox.showerror("Error de Icono", f"Ocurrió un error inesperado al cargar el icono: {e}")

        # Inicialización de las variables StringVar
        self.tiempo_seleccionado_var = tk.StringVar(value="15")
        self.horas_personalizadas_var = tk.StringVar(value="00")
        self.minutos_personalizadas_var = tk.StringVar(value="00")

        self._countdown_job_id = None

        self.setup_styles()
        self.create_widgets()
        self.load_scheduled_shutdown()
        self.update_countdown_display()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TLabel", font=("Segoe UI", 11), foreground="#333333")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("TRadiobutton", font=("Segoe UI", 10))
        style.configure("TFrame", background="#f0f0f0")
        style.configure("Countdown.TLabel", font=("Segoe UI", 14, "bold"), foreground="#007bff")

        style.map("Execute.TButton",
                  background=[('active', '#0056b3')],
                  foreground=[('active', 'white')])

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.pack(expand=True, fill="both")

        self.countdown_label = ttk.Label(main_frame, text="No hay apagado programado por este script.", style="Countdown.TLabel")
        self.countdown_label.pack(pady=(0, 20))

        ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=10)

        ttk.Label(main_frame, text="1. Selecciona una opción de tiempo predefinida:").pack(pady=(10, 5), anchor="w")

        options_frame = ttk.Frame(main_frame)
        options_frame.pack(pady=5, fill="x")

        self.tiempos_predefinidos = {
            "15 minutos": 15,
            "30 minutos": 30,
            "45 minutos": 45,
            "1 hora": 60,
            "1 hora 30 min": 90,
            "2 horas": 120
        }

        col_idx = 0
        row_idx = 0
        for text, minutes in self.tiempos_predefinidos.items():
            rb = ttk.Radiobutton(options_frame,
                                 text=text,
                                 variable=self.tiempo_seleccionado_var,
                                 value=str(minutes * 60))
            rb.grid(row=row_idx, column=col_idx, sticky="w", padx=10, pady=3)
            col_idx += 1
            if col_idx > 1:
                col_idx = 0
                row_idx += 1

        ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=15)

        ttk.Label(main_frame, text="2. O configura un tiempo personalizado (HH:MM):").pack(pady=(10, 5), anchor="w")

        custom_time_frame = ttk.Frame(main_frame)
        custom_time_frame.pack(pady=10)

        ttk.Label(custom_time_frame, text="Horas:").grid(row=0, column=0, padx=5)
        self.horas_label = ttk.Label(custom_time_frame, textvariable=self.horas_personalizadas_var, font=("Segoe UI", 16, "bold"), width=3, anchor="center", relief="solid", borderwidth=1)
        self.horas_label.grid(row=0, column=1, padx=5)
        ttk.Button(custom_time_frame, text="+", command=self.incrementar_horas, width=2).grid(row=0, column=2, padx=5)

        ttk.Label(custom_time_frame, text=":").grid(row=0, column=3, padx=5)

        ttk.Label(custom_time_frame, text="Minutos:").grid(row=0, column=4, padx=5)
        self.minutos_label = ttk.Label(custom_time_frame, textvariable=self.minutos_personalizadas_var, font=("Segoe UI", 16, "bold"), width=3, anchor="center", relief="solid", borderwidth=1)
        self.minutos_label.grid(row=0, column=5, padx=5)
        ttk.Button(custom_time_frame, text="+10", command=self.incrementar_minutos, width=4).grid(row=0, column=6, padx=5)

        self.horas_personalizadas_var.trace_add("write", self.update_custom_time_radio)
        self.minutos_personalizadas_var.trace_add("write", self.update_custom_time_radio)

        self.custom_radio_value = "custom"
        self.custom_radio = ttk.Radiobutton(options_frame,
                                            text="Tiempo personalizado (HH:MM)",
                                            variable=self.tiempo_seleccionado_var,
                                            value=self.custom_radio_value)
        self.custom_radio.grid(row=row_idx + 1, column=0, columnspan=2, sticky="w", padx=10, pady=3)

        ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=15)

        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=10)

        self.btn_programar = ttk.Button(buttons_frame, text="Programar Apagado", command=self.iniciar_apagado, style="Execute.TButton")
        self.btn_programar.grid(row=0, column=0, padx=10, pady=5)

        self.btn_cancelar = ttk.Button(buttons_frame, text="Cancelar Apagado", command=self.cancelar_apagado)
        self.btn_cancelar.grid(row=0, column=1, padx=10, pady=5)

    def increment_time_value(self, current_str_var, increment_by, is_minutes=False):
        current_value = int(current_str_var.get())
        new_value = current_value + increment_by

        if is_minutes:
            if new_value >= 60:
                new_value = 0
                self.incrementar_horas()
            current_str_var.set(f"{new_value:02d}")
        else:
            current_str_var.set(f"{new_value:02d}")
        self.update_custom_time_radio()

    def incrementar_horas(self):
        self.increment_time_value(self.horas_personalizadas_var, 1)

    def incrementar_minutos(self):
        current_min = int(self.minutos_personalizadas_var.get())
        current_hours = int(self.horas_personalizadas_var.get())

        new_min = current_min + 10
        new_hours = current_hours

        if new_min >= 60:
            new_min = 0
            new_hours += 1

        self.minutos_personalizadas_var.set(f"{new_min:02d}")
        self.horas_personalizadas_var.set(f"{new_hours:02d}")
        self.update_custom_time_radio()

    def update_custom_time_radio(self, *args):
        self.tiempo_seleccionado_var.set(self.custom_radio_value)

    def get_seconds_to_shutdown(self):
        selected_option = self.tiempo_seleccionado_var.get()

        if selected_option == self.custom_radio_value:
            try:
                horas = int(self.horas_personalizadas_var.get())
                minutos = int(self.minutos_personalizadas_var.get())
                total_segundos = (horas * 3600) + (minutos * 60)
                if total_segundos <= 0:
                    messagebox.showerror("Error de Entrada", "El tiempo personalizado debe ser mayor que cero.")
                    return None, None
                mensaje_tiempo = f"{horas:02d}h {minutos:02d}m"
                return total_segundos, mensaje_tiempo
            except ValueError:
                messagebox.showerror("Error de Entrada", "Por favor, ingresa un tiempo personalizado válido (números).")
                return None, None
        else:
            segundos = int(selected_option)
            for text, min_val in self.tiempos_predefinidos.items():
                if str(min_val * 60) == selected_option:
                    return segundos, text
            return segundos, f"{segundos // 60} minutos"

    def iniciar_apagado(self):
        segundos_a_apagar, mensaje_tiempo = self.get_seconds_to_shutdown()

        if segundos_a_apagar is None:
            return

        self._ejecutar_comando_cancelar_silencioso()
        self.clear_scheduled_shutdown()

        confirmar = messagebox.askyesno("Confirmar Apagado",
                                        f"¿Estás seguro de que quieres programar el apagado en {mensaje_tiempo}?")
        if not confirmar:
            messagebox.showinfo("Cancelado", "El apagado ha sido cancelado.")
            return

        comando = ""
        plataforma = sys.platform

        if plataforma == "win32":
            comando = f"shutdown /s /t {segundos_a_apagar}"
            mensaje_sistema = f"Tu PC con Windows se apagará en {segundos_a_apagar} segundos."
        elif plataforma == "darwin":
            minutos_retraso = (segundos_a_apagar + 59) // 60
            comando = f"sudo shutdown -h +{minutos_retraso}"
            mensaje_sistema = f"Tu Mac se apagará en aproximadamente {minutos_retraso} minutos."
        elif plataforma.startswith("linux"):
            minutos_retraso = (segundos_a_apagar + 59) // 60
            comando = f"sudo shutdown -h +{minutos_retraso}"
            mensaje_sistema = f"Tu PC con Linux se apagará en aproximadamente {minutos_retraso} minutos."
        else:
            messagebox.showerror("Error", "Sistema operativo no compatible para el apagado directo.")
            return

        try:
            if plataforma == "darwin" or plataforma.startswith("linux"):
                messagebox.showinfo("Requiere Contraseña", "Por favor, ingresa tu contraseña de administrador en la terminal para confirmar el apagado.")
                subprocess.run(comando, shell=True, check=True)
            else:
                os.system(comando)

            self.save_scheduled_shutdown(segundos_a_apagar)

            messagebox.showinfo("Apagado Programado", f"¡Apagado programado exitosamente!\n{mensaje_sistema}")
            self.update_countdown_display()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error de Permisos/Comando",
                                 f"El comando de apagado falló. Error: {e}\n\n"
                                 "Asegúrate de que tienes permisos de administrador y el comando es correcto.")
        except Exception as e:
            messagebox.showerror("Error al programar apagado", f"Ocurrió un error inesperado: {e}")

    def _ejecutar_comando_cancelar_silencioso(self):
        comando_cancelar = ""
        plataforma = sys.platform

        if plataforma == "win32":
            comando_cancelar = "shutdown /a"
            subprocess.run(comando_cancelar, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        elif plataforma == "darwin":
            comando_cancelar = "sudo shutdown -c"
            try:
                subprocess.run(comando_cancelar, shell=True, check=False, timeout=2)
            except subprocess.TimeoutExpired:
                pass
        elif plataforma.startswith("linux"):
            comando_cancelar = "sudo shutdown -c"
            try:
                subprocess.run(comando_cancelar, shell=True, check=False, timeout=2)
            except subprocess.TimeoutExpired:
                pass

    def cancelar_apagado(self):
        self._ejecutar_comando_cancelar_silencioso()
        self.clear_scheduled_shutdown()

        messagebox.showinfo("Apagado Cancelado", "¡Cualquier apagado programado ha sido cancelado!")
        self.update_countdown_display()

    def save_scheduled_shutdown(self, total_seconds):
        scheduled_time = datetime.datetime.now() + datetime.timedelta(seconds=total_seconds)
        config = {
            "scheduled_timestamp": scheduled_time.timestamp(),
            "total_duration_seconds": total_seconds
        }
        try:
            with open(self.CONFIG_FILE, "w") as f:
                json.dump(config, f)
        except IOError as e:
            print(f"Error al guardar la configuración del apagado: {e}")

    def load_scheduled_shutdown(self):
        self.scheduled_shutdown_time = None
        self.initial_total_seconds = 0
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "r") as f:
                    config = json.load(f)
                    timestamp = config.get("scheduled_timestamp")
                    total_duration = config.get("total_duration_seconds")
                    if timestamp and total_duration is not None:
                        self.scheduled_shutdown_time = datetime.datetime.fromtimestamp(timestamp)
                        self.initial_total_seconds = total_duration
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error al cargar la configuración del apagado: {e}")
                self.clear_scheduled_shutdown()
        return self.scheduled_shutdown_time is not None

    def clear_scheduled_shutdown(self):
        self.scheduled_shutdown_time = None
        self.initial_total_seconds = 0
        if os.path.exists(self.CONFIG_FILE):
            try:
                os.remove(self.CONFIG_FILE)
            except OSError as e:
                print(f"Error al eliminar el archivo de configuración: {e}")
            self.update_countdown_display()

    def update_countdown_display(self):
        if self._countdown_job_id:
            self.master.after_cancel(self._countdown_job_id)
            self._countdown_job_id = None

        if self.scheduled_shutdown_time:
            time_remaining = self.scheduled_shutdown_time - datetime.datetime.now()
            total_seconds_remaining = int(time_remaining.total_seconds())

            if total_seconds_remaining > 0:
                hours = total_seconds_remaining // 3600
                minutes = (total_seconds_remaining % 3600) // 60
                seconds = total_seconds_remaining % 60
                self.countdown_label.config(text=f"Apagado programado: {hours:02d}h {minutes:02d}m {seconds:02d}s restantes")
                self._countdown_job_id = self.master.after(1000, self.update_countdown_display)
            else:
                self.countdown_label.config(text="Apagado programado: ¡AHORA!")
                self.clear_scheduled_shutdown()
        else:
            self.countdown_label.config(text="No hay apagado programado por este script.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShutdownScheduler(root)
    root.mainloop()