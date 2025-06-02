PC Shutdown Scheduler / Programador de Apagado de PC
English
🖥️ PC Shutdown Scheduler

A simple and intuitive desktop application for Windows, macOS, and Linux that allows you to schedule your computer to shut down after a specified period. Created by xXESTEBANTRANXx.
✨ Features

    Predefined Timers: Quickly select common shutdown intervals like 15, 30, 45 minutes, 1 hour, etc.
    Custom Timer: Set a precise shutdown time in hours and minutes.
    Real-time Countdown: See the remaining time until shutdown directly in the application window.
    Cancel Option: Easily cancel any previously scheduled shutdown.
    Cross-Platform (Windows, macOS, Linux): Designed to work on major operating systems.
    Standalone Executable: Can be run without needing Python installed (after compilation with PyInstaller).

🚀 How to Use

    Download/Obtain the Application:
        If you have the compiled executable (.exe for Windows), simply double-click it.
        If you have the Python script (.pyw), ensure you have Python (3.x recommended) and Tkinter installed, then run the script.

    Choose a Shutdown Time:
        Select one of the predefined options (e.g., "15 minutes", "1 hour").
        Or, use the "Custom Time" section to enter specific hours and minutes using the input fields.

    Program the Shutdown:
        Click the "Programar Apagado" (Schedule Shutdown) button.
        Confirm your choice in the pop-up window.
        The application will display a countdown until the scheduled shutdown.

    Cancel the Shutdown:
        To cancel any active scheduled shutdown, simply click the "Cancelar Apagado" (Cancel Shutdown) button.

⚠️ Important Notes

    Administrator Permissions: For Windows and Linux/macOS systems, the application might require administrator/root privileges to schedule or cancel shutdowns. If you encounter issues, try running the application as an administrator.
    System Notifications: On Windows, if you schedule a shutdown for 10 minutes or less, the operating system might display its own pop-up warning message. This is normal Windows behavior.
    Saved State: The application remembers your last programmed shutdown time (by this specific application) even if you close and reopen it.

🛠️ Development & Compilation

This application is built using Python and Tkinter.

To create a standalone executable (e.g., .exe for Windows):

    Ensure you have Python and pyinstaller installed (pip install pyinstaller).
    Navigate to the directory containing python_apagar_pc.pyw and icon.ico in your terminal.
    Run the following command:
    Bash

    pyinstaller --onefile --noconsole --icon=icon.ico python_apagar_pc.pyw

    The executable will be generated in the dist folder.

Español
🖥️ Programador de Apagado de PC

Una aplicación de escritorio simple e intuitiva para Windows, macOS y Linux que te permite programar el apagado de tu computadora después de un período de tiempo especificado. Creado por xXESTEBANTRANXx.
✨ Características

    Temporizadores Predefinidos: Selecciona rápidamente intervalos comunes de apagado como 15, 30, 45 minutos, 1 hora, etc.
    Temporizador Personalizado: Establece un tiempo de apagado preciso en horas y minutos.
    Cuenta Regresiva en Tiempo Real: Ve el tiempo restante hasta el apagado directamente en la ventana de la aplicación.
    Opción de Cancelar: Cancela fácilmente cualquier apagado programado previamente.
    Multiplataforma (Windows, macOS, Linux): Diseñada para funcionar en los principales sistemas operativos.
    Ejecutable Autónomo: Puede ejecutarse sin necesidad de tener Python instalado (después de la compilación con PyInstaller).

🚀 Cómo Usar

    Descarga/Obtén la Aplicación:
        Si tienes el ejecutable compilado (.exe para Windows), simplemente haz doble clic en él.
        Si tienes el script de Python (.pyw), asegúrate de tener Python (se recomienda la versión 3.x) y Tkinter instalados, luego ejecuta el script.

    Elige un Tiempo de Apagado:
        Selecciona una de las opciones predefinidas (por ejemplo, "15 minutos", "1 hora").
        O, utiliza la sección "Tiempo personalizado" para introducir horas y minutos específicos usando los campos de entrada.

    Programar el Apagado:
        Haz clic en el botón "Programar Apagado".
        Confirma tu elección en la ventana emergente.
        La aplicación mostrará una cuenta regresiva hasta el apagado programado.

    Cancelar el Apagado:
        Para cancelar cualquier apagado programado activo, simplemente haz clic en el botón "Cancelar Apagado".

⚠️ Notas Importantes

    Permisos de Administrador: Para sistemas Windows y Linux/macOS, la aplicación podría requerir privilegios de administrador/root para programar o cancelar apagados. Si encuentras problemas, intenta ejecutar la aplicación como administrador.
    Notificaciones del Sistema: En Windows, si programas un apagado por 10 minutos o menos, el sistema operativo podría mostrar su propia ventana de advertencia. Este es un comportamiento normal de Windows.
    Estado Guardado: La aplicación recuerda tu último tiempo de apagado programado (por esta aplicación específica) incluso si la cierras y la vuelves a abrir.

🛠️ Desarrollo y Compilación

Esta aplicación está construida usando Python y Tkinter.

Para crear un ejecutable autónomo (por ejemplo, .exe para Windows):

    Asegúrate de tener Python y pyinstaller instalados (pip install pyinstaller).
    Navega al directorio que contiene python_apagar_pc.pyw e icon.ico en tu terminal.
    Ejecuta el siguiente comando:
    Bash

    pyinstaller --onefile --noconsole --icon=icon.ico python_apagar_pc.pyw

    El ejecutable se generará en la carpeta dist.




