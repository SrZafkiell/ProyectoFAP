import datetime
import os
import sqlite3
import tkinter as tk

from tkinter import ttk

# Crea la ventana principal de Tkinter (Dicha ventana más adelante pasará a ser fullscreen e invisible.)
ventana = tk.Tk()


def check_primer_inicio():
    """
    1) Conecta a la base de datos y crea las tablas necesarias.
    2) Al ser el primer inicio le da al opción al usuario de crear una cuenta personalizada como "admin". Si el usuario no
    desea crear una cuenta personal con dicho rol, se creará una cuenta con usuario "admin" y contraseña "admin"
    :return:
    """
    conn = sqlite3.connect('fap.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS usuarios (identificacion INTEGER, pnombre TEXT, snombre TEXT, papellido TEXT, sapellido TEXT, correo TEXT, usuario TEXT, password TEXT, rol TEXT);')
    c.execute('CREATE TABLE IF NOT EXISTS banquito (identificacion INTEGER, ahorrado REAL, aprogramado REAL);')
    c.execute('CREATE TABLE IF NOT EXISTS prestamos (identificacion INTEGER, identificador INTEGER, prestamo REAL, valorcuota REAL, cuotas INTEGER, fechainicio DATE, abonado REAL);')
    c.execute('CREATE TABLE IF NOT EXISTS solicitudes (identificacion INTEGER, fecha DATETIME, tipo TEXT, monto REAL, cuotas INTEGER);')
    c.execute('CREATE TABLE IF NOT EXISTS movimientos (identificacion INTEGER, fecha DATETIME, id INTEGER PRIMARY KEY AUTOINCREMENT, transaccion INTEGER, monto REAL, detalle TEXT);')
    c.execute('CREATE TABLE IF NOT EXISTS counter (id INTEGER PRIMARY KEY AUTOINCREMENT, transaction_count INTEGER, date DATE);')
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    c.execute('INSERT INTO counter (transaction_count, date) VALUES (0, ?)', (current_date,))
    conn.commit()
    conn.close()

    """
    Inicia la creación de la ventana que da a elegir si crear o no una cuenta personalizada de superusuario o "admin"
    SI: Lo llevará al menú de registro con el identificador de "admin", al registrar la cuenta, tendrá el rol "admin"
    NO: Creará una cuenta default de admin
    """
    message_window = tk.Toplevel()
    message_window.title("Fondo de ahorro y pensiones (F A P)")
    message_window.geometry("350x175")
    message_window.config(bg="#21293c")
    message_window.lift()
    message_window.resizable(False, False)
    titulo = tk.Label(message_window, text="¿Desea crear un super usuario? ", bg="#21293c", foreground="white", pady="10")
    titulo.config(font=("Oficina", 11, ""))
    titulo.config()
    titulo.pack()

    titulo_tercero = tk.Label(message_window, text="Si no, se creará un usuario por defecto:", bg="#21293c", foreground="white", pady="5")
    titulo_tercero.config(font=("Futura", 11, ""))
    titulo_tercero.config()
    titulo_tercero.pack()
    titulo_segundo = tk.Label(message_window, text="Usuario: admin    Contraseña: admin", bg="#21293c", foreground="white", pady="5")
    titulo_segundo.config(font=("Futura", 11, ""))
    titulo_segundo.config()
    titulo_segundo.pack()

    # Botón SI
    button_si = tk.Button(message_window, text="SÍ ", bg="#6CBB3C", foreground="#21293c", command=lambda: (menu_registro("admin"), message_window.destroy(), message_window.update()))
    button_si.place(x=120, y=110)
    button_si.configure(font=("Futura", 10, ""))

    # Botón NO
    button_no = tk.Button(message_window, text="NO", bg="#F75D59", foreground="#21293c", command=lambda: (crear_usuario("000", "admin", "admin", "admin", "admin", "admin@admin", "admin", "admin", "admin"), message_window.destroy(), message_window.update()))
    button_no.place(x=200, y=110)
    button_no.configure(font=("Futura", 10, ""))


def error_message(mensaje):
    """
    Función que crea una ventana de error para mostrar información sobre el.
    :param mensaje: Información del error que será mostrado dentro de la ventana
    :return:
    """

    error_message_code = tk.Toplevel()
    error_message_code.title("Mensaje de Error")
    # error_message_code.geometry("300x150")
    error_message_code.config(bg="#E63946")
    error_message_code.lift()
    error_message_code.resizable(False, False)

    label_a = tk.Label(error_message_code, text="Oops, algo ha salido mal", bg="#E63946", fg="white", font=("Futura", 15))
    label_a.grid(row=0, column=0, padx=40, pady=10, sticky="ew")

    label_b = tk.Label(error_message_code, text=f"{mensaje}", bg="#E63946", fg="white", font=("Futura", 15))
    label_b.grid(row=1, column=0, padx=50, pady=10)

    accept_button = tk.Button(error_message_code, text="Aceptar", fg="white", bg="#E63946", font=("Futura", 15), command=error_message_code.destroy)
    accept_button.grid(row=2, column=0, padx=50, pady=10)


def accion_exitosa_message(mensaje):
    """
    Muestra una ventana para evidenciar que una acción fue realizada con éxito
    :param mensaje: Mensaje con respecto de la acción exitosa que se realizó
    :return:
    """
    accion_exitosa = tk.Toplevel()
    accion_exitosa.title("Acción exitosa")
    # accion_exitosa.geometry("300x150")
    accion_exitosa.config(bg="#5BEF66")
    accion_exitosa.lift()
    accion_exitosa.resizable(False, False)

    label_a = tk.Label(accion_exitosa, text="¡Acción exitosa!", bg="#5BEF66", fg="white", font=("Futura", 15))
    label_a.grid(row=0, column=0, padx=40, pady=10, sticky="ew")

    label_b = tk.Label(accion_exitosa, text=f"{mensaje}", bg="#5BEF66", fg="white", font=("Futura", 15))
    label_b.grid(row=1, column=0, padx=50, pady=10)

    accept_button = tk.Button(accion_exitosa, text="Aceptar", fg="white", bg="#ABE171", font=("Futura", 15), command=accion_exitosa.destroy)
    accept_button.grid(row=2, column=0, padx=50, pady=20)


def generar_usuario(primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, numero_identificacion):
    """
    Generará un usuario para la persona que se está registrando siguiendo una de las posibles convinaciones dentro de la
    lista "usuarios"
    :param primer_nombre: Primer nombre del usuario que se está registrando
    :param segundo_nombre: Segundo nombre del usuario que se está registrando
    :param primer_apellido: Primer apellido del usuario que se está registrando
    :param segundo_apellido: Segundo apellido del usuario que se está registrando
    :param numero_identificacion: Identificación del usuario que se está registrando
    :return: El usuario generado para la persona específica o "NoUser-UR01" si no se pudo generar un usuario
    """
    conn = sqlite3.connect('fap.db')
    c = conn.cursor()
    # Lista de posibles convinaciones para el usuario
    usuarios = [primer_nombre + "." + primer_apellido, segundo_nombre + "." + primer_apellido,
                primer_nombre + "." + segundo_apellido, segundo_nombre + "." + segundo_apellido,
                primer_nombre + "." + primer_apellido + "." + segundo_apellido,
                segundo_nombre + "." + primer_apellido + "." + segundo_apellido,
                primer_nombre + "." + segundo_nombre + "." + primer_apellido + "." + segundo_apellido]
    # Variable que determina si el usuario ya se encontró o no
    usuario_encontrado = False
    # Por cada convinación de usuario dentro de la lista "usuarios"
    for usuario in usuarios:
        # Busca en la base de datos por el usuario
        c.execute('SELECT * FROM usuarios WHERE usuario=?', (usuario.lower(),))
        # Si no se encuentra
        if not c.fetchone():
            # Establece el usuario a la convinación no encontrada
            usuario_generado = usuario.lower()
            # Establece que ya se encontró el usuario
            usuario_encontrado = True
            break
    # Si no se pudo encontrar un usuario disponible dentro de las convinaciones
    if not usuario_encontrado:
        usuario = usuarios[0] + "." + str(numero_identificacion)
        c.execute('SELECT * FROM usuarios WHERE usuario=?', (usuario.lower(),))
        if not c.fetchone():
            usuario_generado = usuario.lower()
        else:
            usuario_generado = "NoUser-UR01"
    conn.close()
    return usuario_generado


def generate_transaction_id():
    """
    Genera un id de transacción en el formato de "YEAR MONTH DAY INCREMENTAL_NUM" sin espacios.
    Un ejemplo sería: "2301251" -> 23 (Año) 01 (Mes) 25 (Día) 1 (Transacción)
    :return: transaction_id -> El id de transacción disponible con el formato deseado
    """
    conn = sqlite3.connect('fap.db')
    c = conn.cursor()
    now = datetime.datetime.now()
    year = now.strftime('%y')
    month = now.strftime('%m')
    day = now.strftime('%d')
    current_date = now.strftime('%Y-%m-%d')
    c.execute("SELECT transaction_count, date FROM counter")
    result = c.fetchone()
    db_date = result[1]
    if db_date != current_date:
        transaction_num = "000001"
        c.execute("UPDATE counter SET transaction_count = 0, date = ?", (current_date,))
    else:
        transaction_num = str(result[0] + 1).zfill(6)
        c.execute("UPDATE counter SET transaction_count = transaction_count + 1")
    conn.commit()
    transaction_id = year+month+day+transaction_num
    conn.close()
    return transaction_id


def crear_usuario(identificacion, pnombre, snombre, papellido, sapellido, correo, usuario, password, rol):
    """
    Crear el usuario dentro de la base de datos, guarda todos los datos enviados.
    Si el usuario es válido se registra y se imprime una ventana informando de la acción existosa, si no es válido se
    imprimirá una ventana de error.
    :param identificacion: Cedula
    :param pnombre: Primer nombre
    :param snombre: Segundo nombre
    :param papellido: Primer apellido
    :param sapellido: Segundo apellido
    :param correo: Correo
    :param usuario: Usuario generado en generar_usuario()
    :param password: Contraseña
    :param rol: Rol del usuario
    :return:
    """
    if usuario == "NoUser-UR01":
        error_message("No se ha podido asignar un usuario automáticamente. \n"
                      "Por favor asegurate de escribir correctamente tus datos\n\n "
                      "Si presentas problemas en la, contacta con un empleado para "
                      "que te ayude con el registro \n\n ERROR UR01")
    else:
        conn = sqlite3.connect('fap.db')
        c = conn.cursor()
        c.execute('INSERT INTO usuarios VALUES (?,?,?,?,?,?,?,?,?)', (identificacion, pnombre, snombre, papellido, sapellido, correo, usuario, password, rol))
        conn.commit()
        conn.close()
        accion_exitosa_message(f"{pnombre}, tu cuenta se ha creado con éxito \n Tu usuario para ingresar es: {usuario}")


def iniciar_sesion(usuario, password):
    """
    Se conecta a la base de datos para comprobar que el usuario dado existe, si existe comrpueba que la contraseña dada
    para ese usuario sea igual a la que se encuentra en la base de datos. Si es igual, buscará en un diccionario cual
    es el menú para ese usuario.
    Si una de las dos entradas no es igual imprimirá un mensaje de error avisando si la contraseña o el usuario es
    incorrecto.
    :param usuario: Usuario generado en generar_usuario()
    :param password: Contraseña
    :return:
    """
    try:
        conn = sqlite3.connect('fap.db')
        c = conn.cursor()

        # check if the user exists in the table "usuarios"
        c.execute("SELECT password, rol FROM usuarios WHERE usuario=?", (usuario,))
        result = c.fetchone()

        if result:
            db_password, db_rol = result
            if password == db_password:
                roles = {
                    "usuario": menu_usuario,
                    "socio": menu_usuario,
                    "admin": menu_admin
                }
                execute_respectivo = roles.get(db_rol)
                execute_respectivo(usuario)
            else:
                menu_inicio_sesion()
                error_message("Contraseña incorrecta")
        else:
            menu_inicio_sesion()
            error_message("Usuario no encontrado")
    except sqlite3.Error as e:
        print("Error: ", e)
        error_message(e)
    finally:
        conn.close()


def crear_prestamo(identificacion, valor_prestamo, cuotas, tasa):
    """
    Crea un prestado dentro de la base de datos para una persona específica
    :param identificacion: Cedula del usuario
    :param valor_prestamo: Valor del prestamo
    :param cuotas: Cuotas definidas para prestamo
    :param tasa: Tasa de interes del prestamo presentada en real (0,01)
    :return:
    """
    conn = sqlite3.connect('fap.db')
    c = conn.cursor()
    valor_cuotas = (valor_prestamo * tasa) + (valor_prestamo/cuotas)
    c.execute('INSERT INTO prestamos VALUES (?,?,?,?,?,?)', (identificacion, valor_prestamo, valor_cuotas, cuotas, datetime.date.today(), 0))
    accion_exitosa_message("Prestamo creado con exito")
    conn.commit()
    conn.close()


def menu_ahorro_programado():
    pass


def menu_admin_manejo_usuarios():
    pass


def menu_admin(usuario):
    user_window = tk.Toplevel()
    user_window.title("Fondo de ahorro y pensiones (F A P)")
    user_window.geometry("300x300")
    user_window.config(bg="#21293c")  # Color de la ventana
    user_window.lift()
    user_window.resizable(False, False)

    titulo_user = tk.Label(user_window, text="Total ahorrado", bg="#21293c", foreground="white", pady="5")
    titulo_user.config(font=("Oficina", 12, ""))
    titulo_user.config()
    titulo_user.pack()

    conn = sqlite3.connect('fap.db')
    c = conn.cursor()
    c.execute('SELECT * FROM banquito')
    result = c.fetchall()
    total_ahorrado = 0.0
    for socio in result:
        total_ahorrado += socio[1]
    conn.close()

    titulo_user_ahorro = tk.Label(user_window, text=f"{total_ahorrado}", bg="#21293c", foreground="white", pady="5")
    titulo_user_ahorro.config(font=("Oficina", 12, ""))
    titulo_user_ahorro.config()
    titulo_user_ahorro.pack()

    button = tk.Button(user_window, text="Manejo de usuarios ", bg="#e8ff03", foreground="#21293c", padx="4")
    button.place(x=80, y=80)
    button.configure(font=("Futura", 10, ""))

    button = tk.Button(user_window, text="Crear préstamos ", bg="#e8ff03", foreground="#21293c", padx="10")
    button.place(x=80, y=120)
    button.configure(font=("Futura", 10, ""))

    button = tk.Button(user_window, text="Abrir como usuario ", bg="#e8ff03", foreground="#21293c", padx="5", command=lambda: (user_window.destroy(), menu_usuario(usuario), user_window.update()))
    button.place(x=80, y=160)
    button.configure(font=("Futura", 10, ""))
    close_button = tk.Button(user_window, text="Cerrar", fg="white", bg="#E63946", font=("Futura", 15),
                             command=lambda: (user_window.destroy(), user_window.update()))
    close_button.place(x=110, y=210)



def menu_usuario(usuario):
    conn = sqlite3.connect('fap.db')
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios WHERE usuario=?', (usuario,))
    result = c.fetchall()[0]
    identificacion = result[0]
    nombre_usuario = result[1]+" "+result[2]
    rol = result[8]
    conn.close()

    user_window = tk.Toplevel()
    user_window.lift()
    user_window.title("Fondo de ahorro y pensiones (F A P)")
    user_window.geometry("300x300")
    user_window.config(bg="#21293c")  # Color de la ventana
    user_window.resizable(False, False)

    titulo_user = tk.Label(user_window, text=f"Bienvenido {nombre_usuario}", bg="#21293c", foreground="white", pady="10")  # foreground: para cambiar color al texto
    nombre_user = tk.Label(user_window, text=f"[{rol}]", bg="#21293c", foreground="white", pady="5")
    titulo_user.config(font=("Oficina", 12, ""))
    nombre_user.config(font=("Oficina", 12, ""))
    titulo_user.config()
    nombre_user.config()
    titulo_user.pack()
    nombre_user.pack()

    if rol == "socio":
        # BOTÓN PEDIR
        button = tk.Button(user_window, text="Ahorro programado", bg="#e8ff03", foreground="#21293c", padx="5", command=lambda: (menu_ahorro_programado()))
        button.place(x=80, y=80)
        button.configure(font=("Futura", 10, ""))

    # BOTÓN ABONAR
    button_pedir = tk.Button(user_window, text="Abonar a un préstamo", bg="#e8ff03", foreground="#21293c", padx="5", command=lambda: (menu_usuario_abonar(identificacion)))
    button_pedir.place(x=80, y=120)
    button_pedir.configure(font=("Futura", 10, ""))

    # PRESTAMOS ACTIVOS
    button = tk.Button(user_window, text="Préstamos activos ", bg="#e8ff03", foreground="#21293c", padx="5", command=lambda: (menu_usuario_prestamos_check(identificacion)))
    button.place(x=80, y=160)
    button.configure(font=("Futura", 10, ""))

    # ULTIMOS MOVIMIENTOS
    button = tk.Button(user_window, text="Últimos movimientos ", bg="#e8ff03", foreground="#21293c", padx="5", command=lambda: (menu_usuario_last_movements(identificacion)))
    button.place(x=80, y=200)
    button.configure(font=("Futura", 10, ""))


def abonar_prestamo(id_prestamo, valor_abono):
    """
    La función manejará el abono dentro de la tabla "prestamos", calculará si el abono está dentro de lo acordado por
    cuota, si pagas de más y cuando pagas por completo.
    :param id_prestamo: Identificador del prestamo en la base de datos
    :param valor_abono: Valor total del abono a ser realizado
    :return:
    """
    conn = sqlite3.connect('fap.db')
    c = conn.cursor()
    c.execute('SELECT * FROM prestamos WHERE identificador=? and prestamo != abonado', (id_prestamo,))
    data = c.fetchall()[0]
    codigo_prestamo = float(id_prestamo)
    abonado = float(valor_abono)
    valor_prestamo = float(data[2])
    valor_cuota = float(data[3])
    total_abonado_hasta_ahora = float(data[6])
    if abonado >= valor_cuota:
        if total_abonado_hasta_ahora+abonado >= valor_prestamo:
            accion_exitosa_message(f"Pago completado con éxito \n Has pagado por completo el prestamo con id: {id_prestamo}")
            c.execute('UPDATE prestamos SET abonado = ? WHERE identificador=?', (valor_prestamo, codigo_prestamo))
            devuelta = (abonado+total_abonado_hasta_ahora)-valor_prestamo
            if devuelta > 0:
                accion_exitosa_message(f"Has pagado {devuelta} de más \n Se te devolverá el dinero pagado de más")
        else:
            accion_exitosa_message(f"Pago completado con éxito")
            c.execute('UPDATE prestamos SET abonado = ? WHERE identificador=?', (abonado+total_abonado_hasta_ahora, codigo_prestamo))

        identificacion = int(data[0])
        fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if total_abonado_hasta_ahora + abonado > valor_prestamo:
            abono = valor_prestamo - total_abonado_hasta_ahora
        else:
            abono = valor_abono
        c.execute('INSERT INTO movimientos (identificacion, fecha, transaccion, monto, detalle) VALUES (?,?,?,?,?)', (identificacion, fecha, "Abono a prestamo", abono, f"Prestamo: {int(codigo_prestamo)}"))

    else:
        error_message(f"Estás intentando pagar menos de lo acordado por cuota \n Debes pagar un total de {valor_cuota} o más por cuota")
    conn.commit()
    conn.close()


def menu_usuario_abonar(identificacion):
    """
    Menu encargado de preguntarle al usuario el id del prestamo a abonar y la cantidad.
    Al finalizar se ejecuta abonar_prestamo() con los datos extraidos
    :param identificacion: Identificacion de la persona
    :return:
    """
    conn = sqlite3.connect('fap.db')
    c = conn.cursor()
    c.execute('SELECT * FROM prestamos WHERE identificacion=? and prestamo != abonado', (identificacion,))
    data = c.fetchall()
    conn.close()
    if not data:
        error_message("No tienes prestamos por abonar")
    else:
        # menu_usuario_prestamos_check(identificacion)
        menu_abonar_prestamo = tk.Toplevel()
        menu_abonar_prestamo.title("Fondo de ahorro y pensiones (F A P)")
        menu_abonar_prestamo.geometry("400x250")
        menu_abonar_prestamo.config(bg="#21293c")
        menu_abonar_prestamo.lift()
        menu_abonar_prestamo.resizable(False, False)
        titulo = tk.Label(menu_abonar_prestamo, text="A B O N A R  P R E S T A M O", bg="#21293c", foreground="white", pady="15")
        titulo.config(font=("Arial", 11, ""))
        titulo.config()
        titulo.pack()

        register_frame = tk.Frame(menu_abonar_prestamo, width=400, height=400, pady="10", bg="#dfe2e7", )
        register_frame.pack()
        register_frame.config(relief="ridge")
        register_frame.config(cursor="hand2")

        id_prestamo_label = tk.Label(register_frame, text="ID Prestamo", bg="#dfe2e7",
                                       foreground="#21293c")  # cuadro de texto
        id_prestamo_label.grid(row=0, column=0, sticky="e", padx="10", pady="5")
        id_prestamo_entry = tk.Entry(register_frame)
        id_prestamo_entry.grid(row=0, column=1, padx="10", pady="10")

        valor_abono_label = tk.Label(register_frame, text="Abono", bg="#dfe2e7", foreground="#21293c")
        valor_abono_label.grid(row=1, column=0, sticky="e", padx="10", pady="5")
        valor_abono_entry = tk.Entry(register_frame)
        valor_abono_entry.grid(row=1, column=1, padx="10", pady="10")

        button = tk.Button(menu_abonar_prestamo, text="ABONAR", bg="#e8ff03", foreground="#21293c", command=lambda: (
            menu_abonar_prestamo.withdraw(),
            abonar_prestamo(id_prestamo_entry.get(), valor_abono_entry.get()),
            menu_abonar_prestamo.destroy(),
            menu_abonar_prestamo.update()
        ))
        button.place(x=160, y=160)
        button.configure(font=("Futura", 10, ""))
        print(f"Prestamos: {data}")


def menu_usuario_prestamos_check(identificacion):
    """
    Funcion encargada de si un usuario tiene prestamos, si los tiene los imprimirá en una nueva ventana en forma de lista
    ordenada de forma descendente por antiguedad. (Más antiguo hasta arriba)
    :param identificacion: Identificacion de la persona
    :return:
    """
    conn = sqlite3.connect('fap.db')
    c = conn.cursor()
    c.execute('SELECT * FROM prestamos WHERE identificacion=? and prestamo != abonado', (identificacion,))
    data = c.fetchall()
    conn.close()
    if not data:
        error_message("No se han encontrado prestamos a tu nombre")
    else:
        lista_prestamos = tk.Toplevel()
        lista_prestamos.title("Ultimos Movimientos")
        lista_prestamos.config(bg="#21293c")
        lista_prestamos.lift()
        lista_prestamos.resizable(False, False)

        tittle = tk.Label(lista_prestamos, text="FAPBANK", fg="white", bg="#21293c", font=("Futura", 20))
        tittle.grid(row=0, column=0)

        tittle_two = tk.Label(lista_prestamos, text="Prestamos activos", fg="white", bg="#21293c",
                                       font=("Futura", 15))
        tittle_two.grid(row=1, column=0, padx=10, pady=10)

        # Tabla
        heads = ("ID PRESTAMO", "PRESTAMO", "VALOR CUOTA", "# CUOTAS", "FECHA INICIO", "TOTAL ABONADO")

        listBox = ttk.Treeview(lista_prestamos, columns=heads, show='headings')
        for head in heads:
            listBox.heading(head, text=head)
        listBox.grid(row=2, column=0, padx=10, pady=10, columnspan=1)
        data = sorted(data, key=lambda x: datetime.datetime.strptime(x[5], '%Y-%m-%d'), reverse=False)
        for row in data:
            listBox.insert("", "end", values=row[1:])
        close_button = tk.Button(lista_prestamos, text="Cerrar", fg="white", bg="#E63946", font=("Futura", 15),
                                 command=lista_prestamos.destroy)
        close_button.grid(row=3, column=0, padx=10, pady=10)


def menu_usuario_last_movements(identificacion):
    """
    Muestra los ultimos movimientos para un indicado usuario
    :param identificacion: Identificacion de la persona
    :return:
    """
    conn = sqlite3.connect('fap.db')
    c = conn.cursor()
    c.execute('SELECT * FROM movimientos WHERE identificacion=?', (identificacion,))
    data = c.fetchall()
    conn.close()
    if not data:
        error_message("No se pudo encontrar movimientos")
    else:
        last_movements = tk.Toplevel()
        last_movements.title("Ultimos Movimientos")
        last_movements.config(bg="#21293c")
        last_movements.lift()
        last_movements.resizable(False, False)

        tittle = tk.Label(last_movements, text="FAPBANK", fg="white", bg="#21293c", font=("Futura", 20))
        tittle.grid(row=0, column=0)

        tittle_two = tittle = tk.Label(last_movements, text="Ultimos Movimientos", fg="white", bg="#21293c", font=("Futura", 15))
        tittle_two.grid(row=1, column=0, padx=10, pady=10)

        # Tabla
        heads = ("FECHA Y HORA", "ID", "TRANSACCIÓN", "MONTO", "DETALLE")

        listBox = ttk.Treeview(last_movements, columns=heads, show='headings')
        for head in heads:
            listBox.heading(head, text=head)
        listBox.grid(row=2, column=0, padx=10, pady=10, columnspan=1)
        data = sorted(data, key=lambda x: datetime.datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S'), reverse=True)
        for row in data:
            listBox.insert("", "end", values=row[1:])
        close_button = tk.Button(last_movements, text="Cerrar", fg="white", bg="#E63946", font=("Futura", 15), command=last_movements.destroy)
        close_button.grid(row=3, column=0, padx=10, pady=10)


def menu_registro(tipo_usuario):
    """
    Interfaz de registro para un usuario
    :param tipo_usuario: El tipo de usuario a crear: "admin", "socio", "usuario"
    :return:
    """
    register_window = tk.Toplevel()
    register_window.title("Fondo de ahorro y pensiones (F A P)")
    register_window.geometry("400x450")
    register_window.config(bg="#21293c")  # Color de la ventana
    register_window.lift()
    register_window.resizable(False, False)
    titulo = tk.Label(register_window, text="R E G I S T R O", bg="#21293c", foreground="white", pady="15")  # foreground: para cambiar color al texto
    titulo.config(font=("Arial", 11, ""))
    titulo.config()
    titulo.pack()

    register_frame = tk.Frame(register_window, width=400, height=400, pady="10", bg="#dfe2e7", )  # Tamañano de la ventana
    register_frame.pack()
    register_frame.config(relief="ridge")
    register_frame.config(cursor="hand2")

    # PRIMER NOMBRE
    primer_nombre_label = tk.Label(register_frame, text="Primer nombre", bg="#dfe2e7", foreground="#21293c")  # cuadro de texto
    primer_nombre_label.grid(row=0, column=0, sticky="e", padx="10", pady="5")
    primer_nombre_entry = tk.Entry(register_frame)  # Cuadro para ingresar usuario
    primer_nombre_entry.grid(row=0, column=1, padx="10", pady="10")
    # nombreLabel.configure(font=( "Futura",9, ""))

    # SEGUNDO NOMBRE
    segundo_nombre_label = tk.Label(register_frame, text="Segundo nombre", bg="#dfe2e7", foreground="#21293c")
    segundo_nombre_label.grid(row=1, column=0, sticky="e", padx="10", pady="5")
    segundo_nombre_entry = tk.Entry(register_frame)  # Cuadro para ingresar usuario
    segundo_nombre_entry.grid(row=1, column=1, padx="10", pady="10")
    # nombre2Label.configure(font=( "Futura",9, ""))

    # PRIMER APELLIDO
    primer_apellido_label = tk.Label(register_frame, text="Primer apellido", bg="#dfe2e7", foreground="#21293c")  # cuadro de texto
    primer_apellido_label.grid(row=2, column=0, sticky="e", padx="10", pady="5")
    primer_apellido_entry = tk.Entry(register_frame)
    primer_apellido_entry.grid(row=2, column=1, padx="10", pady="10")
    # ape1Label.configure(font=( "Futura",9, ""))

    # SEGUNDO APELLIDO
    segundo_apellido_label = tk.Label(register_frame, text="Segundo apellido", bg="#dfe2e7", foreground="#21293c")  # cuadro de texto
    segundo_apellido_label.grid(row=3, column=0, sticky="e", padx="10", pady="5")
    segundo_apellido_entry = tk.Entry(register_frame)
    segundo_apellido_entry.grid(row=3, column=1, padx="10", pady="10")
    # ape2Label.configure(font=( "Futura",9, ""))

    # IDENTIFICACION
    identificacion_label = tk.Label(register_frame, text="No. de identificación", bg="#dfe2e7", foreground="#21293c")  # cuadro de texto
    identificacion_label.grid(row=4, column=0, sticky="e", padx="10", pady="5")
    identificacion_entry = tk.Entry(register_frame)  # Cuadro para ingresar usuario
    identificacion_entry.grid(row=4, column=1, padx="10", pady="10")

    # CORREO ELECTRÓNICO
    correo_label = tk.Label(register_frame, text="Correo electrónico", bg="#dfe2e7", foreground="#21293c")  # cuadro de texto
    correo_label.grid(row=5, column=0, sticky="e", padx="10", pady="5")
    correo_entry = tk.Entry(register_frame)  # Cuadro para ingresar usuario
    correo_entry.grid(row=5, column=1, padx="10", pady="10")

    # CONTRASEÑA
    password_label = tk.Label(register_frame, text="Contraseña", bg="#dfe2e7", foreground="#21293c")  # cuadro de texto
    password_label.grid(row=6, column=0, sticky="e", padx="10", pady="5")
    password_entry = tk.Entry(register_frame, show="*")  # Cuadro para ingresar usuario
    password_entry.grid(row=6, column=1, padx="10", pady="10")

    # BOTÓN REGISTRARSE
    button = tk.Button(register_window, text="Registrarse", bg="#e8ff03", foreground="#21293c", command=lambda: (
                           crear_usuario(
                               identificacion_entry.get(),
                               primer_nombre_entry.get(),
                               segundo_nombre_entry.get(),
                               primer_apellido_entry.get(),
                               segundo_apellido_entry.get(),
                               correo_entry.get(),
                               generar_usuario(
                                   primer_nombre_entry.get(),
                                   segundo_nombre_entry.get(),
                                   primer_apellido_entry.get(),
                                   segundo_apellido_entry.get(),
                                   identificacion_entry.get()),
                               password_entry.get(),
                               tipo_usuario),
                           register_window.destroy(), main_menu(), register_window.update()

                       ))
    button.place(x=160, y=360)
    button.configure(font=("Futura", 10, ""))


def menu_inicio_sesion():
    """
    Interfaz de inicio de sesion
    :return:
    """
    login_window = tk.Toplevel()
    login_window.title("Fondo de ahorro y pensiones (F A P)")
    login_window.geometry("300x250")
    login_window.config(bg="#21293c")  # Color de la ventana
    login_window.lift()
    login_window.resizable(False, False)
    titulo = tk.Label(login_window, text="INICIO SESIÓN", bg="#21293c", foreground="white", pady="15")  # foreground: para cambiar color al texto
    titulo.config(font=("Arial", 11, ""))
    titulo.config()
    titulo.pack()

    login_frame = tk.Frame(login_window, width=400, height=400, pady="10", bg="#dfe2e7", )  # Tamañano de la ventana
    login_frame.pack()
    login_frame.config(relief="ridge")
    login_frame.config(cursor="hand2")

    # USUARIO
    user_label = tk.Label(login_frame, text="Usuario", bg="#dfe2e7", foreground="#21293c")  # cuadro de texto
    user_label.grid(row=0, column=0, sticky="e", padx="10", pady="5")
    user_entry = tk.Entry(login_frame)  # Cuadro para ingresar usuario
    user_entry.grid(row=0, column=1, padx="10", pady="10")  # padx: distancia hacia los lados, pady: distancia de arriba y abajo
    # nombreLabel.configure(font=( "Futura",9, ""))

    # CONTRASEÑA
    password_label = tk.Label(login_frame, text="Contraseña", bg="#dfe2e7", foreground="#21293c")  # cuadro de texto
    password_label.grid(row=6, column=0, sticky="e", padx="10", pady="5")
    password_entry = tk.Entry(login_frame, show="*")  # Cuadro para ingresar usuario
    password_entry.grid(row=6, column=1, padx="10", pady="10")
    # BOTÓN INICIO SESION
    button = tk.Button(login_window, text="Iniciar sesión", bg="#e8ff03", foreground="#21293c", command=lambda: (login_window.withdraw(), iniciar_sesion(user_entry.get(), password_entry.get()), login_window.destroy(), login_window.update()))
    button.place(x=110, y=170)
    button.configure(font=("Futura", 10, ""))


def terminate_program():
    ventana.quit()


def main_menu():
    ventana.title("Banquito")
    ventana.wm_attributes('-fullscreen', 'true')
    ventana.attributes('-alpha', 0)

    main_menu_gui = tk.Toplevel(ventana)
    main_menu_gui.title("Banquito")
    main_menu_gui.lift(ventana)
    main_menu_gui.resizable(False, False)
    main_menu_gui.geometry("350x350")
    main_menu_gui.config(bg="#21293c")

    titulo = tk.Label(main_menu_gui, text="FAPBANK", fg="white", bg="#21293c", font=("Futura", 40))
    titulo.place(x=50, y=40)

    boton_inicio_sesion = tk.Button(main_menu_gui, text="Iniciar", fg="black", bg="#e8ff03", font=("Futura", 18), command=lambda: (ventana.withdraw(), main_menu_gui.destroy(), menu_inicio_sesion(), main_menu_gui.update()))
    boton_inicio_sesion.place(x=130, y=150, width=100, height=40)

    boton_registro = tk.Button(main_menu_gui, text="Registro", fg="black", bg="#e8ff03", font=("Futura", 18), command=lambda: (ventana.withdraw(), main_menu_gui.destroy(), menu_registro("usuario"), main_menu_gui.update()))
    boton_registro.place(x=120, y=200, width=120, height=40)


def test_insert():
    conn = sqlite3.connect('fap.db')
    c = conn.cursor()
    test_data = [
        ("1107529755", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1, "Deposito", 1000, "Deposito inicial"),
        ("1107529755", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 2, "Retiro", 500, "Retiro de efectivo"),
        ("1107529755", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 3, "Transferencia", 200,
         "Transferencia a otra cuenta")]
    for row in test_data:
        c.execute(
            'INSERT INTO movimientos (identificacion, fecha, id, transaccion, monto, detalle) VALUES (?, ?, ?, ?, ?, ?)',
            row)
    conn.commit()
    conn.close()


def test_insert_prestamos():
    conn = sqlite3.connect('fap.db')
    c = conn.cursor()
    test_data = [
        (1107529755, 230125000001, 1000.0, 100.0, 10, '2022-01-01', 0.0),
        (1107529755, 230125000002, 2000.0, 200.0, 15, '2022-02-01', 500.0),
        (1107529755, 230125000003, 3000.0, 300.0, 20, '2022-03-01', 1500.0),
        (1107529755, 230125000004, 4000.0, 400.0, 25, '2022-04-01', 2500.0),
        (1107529755, 230125000005, 5000.0, 500.0, 30, '2022-05-01', 3500.0)
    ]
    for row in test_data:
        c.execute('INSERT INTO prestamos (identificacion, identificador, prestamo, valorcuota, cuotas, fechainicio, abonado) VALUES (?,?,?,?,?,?,?)', row)
    conn.commit()
    conn.close()


def insert_test_socios():
    # Connect to or create the database
    conn = sqlite3.connect('fap.db')
    c = conn.cursor()

    # Insert test data
    c.execute("INSERT INTO banquito VALUES (1, 25000, 25000)")
    c.execute("INSERT INTO banquito VALUES (2, 50000, 50000)")
    c.execute("INSERT INTO banquito VALUES (3, 150000, 150000)")
    c.execute("INSERT INTO banquito VALUES (4, 45000, 45000)")
    c.execute("INSERT INTO banquito VALUES (5, 25000, 25000)")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def main():
    main_menu()
    if os.path.exists('fap.db') and os.stat("fap.db").st_size == 0 or not os.path.exists('fap.db'):
        check_primer_inicio()


main()
ventana.mainloop()
