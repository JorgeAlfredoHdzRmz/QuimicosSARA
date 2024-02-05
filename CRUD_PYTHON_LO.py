from tkinter import *
from tkinter import ttk
from tkinter import messagebox as MessageBox
import ttkbootstrap
from os import getcwd
import pyodbc
import cv2
from tkinter import filedialog
from tkinter import PhotoImage
import os
from tkinter import Tk, Label, PhotoImage, Canvas
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime

#miConexion = mysql.connector.connect( host='localhost', user= 'root', passwd='ferrari08', db='quimicossarabd');
#cur = miConexion.cursor();


# Establece la información del servidor y la base de datos
server = 'MSI\\SQLEXPRESS'
database = 'tienda_quimicos'

# Construye la cadena de conexión para Windows Authentication
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'

# Establece la conexión
connection = pyodbc.connect(connection_string)

# Crea un cursor
cur = connection.cursor()


raiz = ttkbootstrap.Window(themename='yeti');

wtotal = raiz.winfo_screenwidth()
htotal = raiz.winfo_screenheight()
wapp = 1000;
happ = 650;

wapp = round((wtotal-wapp)/2)
happ = round((htotal-happ)/3)

raiz.geometry("1000x650"+"+"+str(wapp)+"+"+str(happ)); #("1300x650+18+30")
raiz.title("QUIMICOS PROCESADOS SA-RA");
raiz.resizable(False,False);

frame = Frame(raiz);
frame.config(width=500,height=350)
frame.place(x=250,y=220);

global username;
global password;
global password1;
global usertype;
global image_binary
username = StringVar();
password= StringVar();
password1= StringVar();
usertype = IntVar();
usertype.set(0);
image_binary = None;

global username2;
global password2;
global password12;
global usertype2;
global image_binary2;
username2 = StringVar();
password2= StringVar();
password12= StringVar();
usertype2 = IntVar();
usertype2.set(0);
image_binary2 = None;

global nomcli;
global apecli;
global emailcli;
global telcli;
nomcli = StringVar();
apecli = StringVar();
emailcli = StringVar();
telcli = StringVar();

global prodname;
global category;
global price;
global qty;

prodname = StringVar();
category = StringVar();
price = DoubleVar();
qty = IntVar();

global fecha;
global IDProducto;
global cliente;
global producto;
global total;
global cantidad;
global PrecioUnitario;

IDProducto = StringVar();
producto = StringVar();
fecha = StringVar();
cliente = IntVar();
total = DoubleVar();
cantidad = IntVar();
PrecioUnitario = DoubleVar();
fecha.set(datetime.now().strftime('%Y-%m-%d %H:%M:%S'));


def RegistrarSistema():
    frame1 = Frame(raiz);
    frame1.config(width=500,height=650)
    frame1.place(x=250,y=0);

    def regresar():
        username.set("");
        password.set("");
        nombreUsuarioCaja.focus();
        frame1.destroy();
    
    def tomar_foto():
        # Capturar una imagen desde la cámara
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        # Redimensionar la imagen a 180x180 píxeles
        resized_frame = cv2.resize(frame, (180, 180))

        # Convertir la imagen a datos binarios
        global image_binary;
        _, image_binary = cv2.imencode('.jpg', resized_frame)
        image_binary = image_binary.tobytes()
        mostrar_foto_en_label();

    def selectfoto():
        image_path = filedialog.askopenfilename(title="Selecciona un archivo", filetypes=[("Archivos de imagen", ("*.png", "*.jpg", "*.jpeg", "*.gif")), ("Todos los archivos", "*.*")]);
        # Leer la imagen como datos binarios
        with open(image_path, 'rb') as image_file:
            global image_binary;
            image_binary = image_file.read()
        mostrar_foto_en_label();
            
    def mostrar_foto_en_label():
        global image_binary
        try:
            # Convertir los datos binarios a un objeto BytesIO
            image_data = BytesIO(image_binary)
            # Abrir la imagen con PIL desde BytesIO
            image_pil = Image.open(image_data)
            # Convertir la imagen de PIL a PhotoImage de Tkinter
            tk_image = ImageTk.PhotoImage(image_pil)
            # Configurar el Label 'foto' con la nueva imagen
            foto.img = tk_image  # Almacenar una referencia para evitar que la imagen sea eliminada por el recolector de basura
            foto.config(image=tk_image)  # Usar config() para establecer la opción image
        except Exception as e:
            print(f"Error al mostrar la foto: {e}")

    def Registro(): #FUNCION PARA REGISTRAR UN USUARIO EN EL SISTEMA
        global image_binary;
        try:
            cur.execute('SELECT * FROM dbo.usuarios WHERE Username = ?;', (username.get(), ));
            if cur.fetchall():
                MessageBox.showerror("REGISTRO DE USUARIOS", "EL NOMBRE DE USUARIO ESTÁ ACTUALMENTE EN USO, INTENTALO DE NUEVO");
                username.set("");
                password.set("");
                password1.set("");
                usertype.set(0);
                image_binary = None;
                directorio_actual = os.path.dirname(os.path.realpath(__file__))
                # Combinar la ruta del directorio actual con el nombre de la imagen
                ruta_imagen = os.path.join(directorio_actual, 'sinfoto.png')

                tk_image = PhotoImage(file=ruta_imagen);

                foto.config(image=tk_image);
                foto.image = tk_image;
            elif (password.get() != password1.get()):
                MessageBox.showerror("REGISTRO DE USUARIOS", "LAS CONTRASEÑAS NO COINCIDEN");
                username.set("");
                password.set("");
                password1.set("");
                usertype.set(0);
                image_binary = None;
                directorio_actual = os.path.dirname(os.path.realpath(__file__))
                # Combinar la ruta del directorio actual con el nombre de la imagen
                ruta_imagen = os.path.join(directorio_actual, 'sinfoto.png')

                tk_image = PhotoImage(file=ruta_imagen);

                foto.config(image=tk_image);
                foto.image = tk_image;
            else:
                IngresarUsuario = "INSERT INTO usuarios(Username, Password, UserType, Image) VALUES (?, ?, ?, ?)"
                cur.execute(IngresarUsuario, (username.get(), password.get(), usertype.get(), image_binary));
                connection.commit();
                MessageBox.showinfo("REGISTRO DE USUARIOS", "USUARIO REGISTRADO CORRECTAMENTE");
                username.set("");
                password.set("");
                password1.set("");
                usertype.set(0);
                image_binary = None;
                directorio_actual = os.path.dirname(os.path.realpath(__file__))
                # Combinar la ruta del directorio actual con el nombre de la imagen
                ruta_imagen = os.path.join(directorio_actual, 'sinfoto.png')

                tk_image = PhotoImage(file=ruta_imagen);

                foto.config(image=tk_image);
                foto.image = tk_image;
        
        except Exception as e:
            MessageBox.showerror("REGISTRO DE USUARIOS", e);
            username.set("");
            password.set("");
            password1.set("");
            usertype.set(0);
            image_binary = None;


    EtiquetaIS= Label(frame1,text="REGISTRARSE",bg="#2a73b2",fg="white",font=("Arial", 40, "bold")).place(x=50,y=10);
    EtiquetanomU= Label(frame1,text="NOMBRE DE USUARIO",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=110,y=90);
    nombreUsuarioCaja = Entry(frame1, textvariable=username,bg="white",fg="black");
    nombreUsuarioCaja.place(x=270,y=90);
    EtiquetaContra= Label(frame1,text="CONTRASEÑA",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=110,y=130);
    ContraseñaCaja = Entry(frame1, textvariable=password,bg="white",fg="black", show="*").place(x=270,y=130);
    EtiquetaContra2 = Label(frame1,text="CONFIRMAR CONTRASEÑA",bg="#2a73b2",fg="white",font=("Arial", 8, "normal")).place(x=110,y=170);
    ContraseñaCaja2 = Entry(frame1, textvariable=password1,bg="white",fg="black", show="*").place(x=270,y=170);
    EtiquetaFoto = Label(frame1,text="FOTOGRAFÍA",bg="#2a73b2",fg="white",font=("Arial", 8, "normal")).place(x=110,y=210);
    botonF =Button(frame1,text="Seleccionar Foto",command=selectfoto,bg="green",fg="white",activebackground="lime",cursor="hand2", width=15).place(x=190,y=210);
    botonF1 =Button(frame1,text="Tomar Foto",command=tomar_foto,bg="green",fg="white",activebackground="lime",cursor="hand2", width=15).place(x=310,y=210);
    
    directorio_actual = os.path.dirname(os.path.realpath(__file__))
    # Combinar la ruta del directorio actual con el nombre de la imagen
    ruta_imagen = os.path.join(directorio_actual, 'sinfoto.png')

    tk_image = PhotoImage(file=ruta_imagen);
    
    global foto;

    foto = Label(frame1, image=tk_image);
    foto.image = tk_image;
    foto.config(width=180,height=180);
    foto.place(x=165,y=260);
    
    EtiquetaContra2 = Label(frame1,text="PERMISOS ADMINISTRADOR",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=140,y=460);
    checkAdmin = ttkbootstrap.Checkbutton(frame1,bootstyle="success",variable=usertype, onvalue=1, offvalue=0);
    checkAdmin.place(x=340,y=463)
    boton1 =Button(frame1,text="Ingresar",command=Registro,bg="green",fg="white",activebackground="lime",cursor="hand2", width=15).place(x=110,y=500);
    boton2 =Button(frame1,text="Cancelar",command=regresar,bg="red",fg="white",activebackground="#ff3737",cursor="hand2",  width=15).place(x=280,y=500);
    
def login():
    try:
        cur.execute('SELECT * FROM dbo.usuarios WHERE Username = ? AND Password = ?;', (username.get(), password.get()));
        if (rows:= cur.fetchone()) is not None:
            row = rows[3]
            user=rows[1]
            if(row == 0):

                frame2 = ttkbootstrap.Frame(raiz);
                frame2.config(width=1000,height=650)
                frame2.place(x=0,y=0);
            
                def menuCliente():
                    def volver():
                        botonr.destroy();
                        boton3.destroy();
                        boton5.destroy();
                        boton6.destroy();
                        label.destroy();

                    botonr =ttkbootstrap.Button(frame4,text="VOLVER",bootstyle="primary-outline",width=10,command=volver);
                    botonr.place(x=10,y=10);
                    label= Label(frame4,text="CLIENTES",bg="#2a73b2",fg="white",font=("Arial", 15, "bold"));
                    label.place(x=110,y=40);
                    boton3 =ttkbootstrap.Button(frame4,text="REGISTRAR",bootstyle="primary-outline",width=40);
                    boton3.place(x=20,y=138);
                    boton5 =ttkbootstrap.Button(frame4,text="ACTUALIZAR",bootstyle="primary-outline",width=40);
                    boton5.place(x=20,y=300);
                    boton6 =ttkbootstrap.Button(frame4,text="ELIMINAR",bootstyle="primary-outline",width=40);
                    boton6.place(x=20,y=480);
                
                def menuProducto():
                    def volver():
                        botonr.destroy();
                        boton3.destroy();
                        boton5.destroy();
                        boton6.destroy();
                        label.destroy();

                    botonr =ttkbootstrap.Button(frame4,text="VOLVER",bootstyle="primary-outline",width=10,command=volver);
                    botonr.place(x=10,y=10);
                    label= Label(frame4,text="PRODUCTOS",bg="#2a73b2",fg="white",font=("Arial", 15, "bold"));
                    label.place(x=90,y=40);
                    boton3 =ttkbootstrap.Button(frame4,text="REGISTRAR",bootstyle="primary-outline",width=40);
                    boton3.place(x=20,y=138);
                    boton5 =ttkbootstrap.Button(frame4,text="ACTUALIZAR",bootstyle="primary-outline",width=40);
                    boton5.place(x=20,y=300);
                    boton6 =ttkbootstrap.Button(frame4,text="ELIMINAR",bootstyle="primary-outline",width=40);
                    boton6.place(x=20,y=480);
                
                def menuVenta():
                    def volver():
                        botonr.destroy();
                        boton3.destroy();
                        boton5.destroy();
                        boton6.destroy();
                        label.destroy();

                    botonr =ttkbootstrap.Button(frame4,text="VOLVER",bootstyle="primary-outline",width=10,command=volver);
                    botonr.place(x=10,y=10);
                    label= Label(frame4,text="VENTAS",bg="#2a73b2",fg="white",font=("Arial", 15, "bold"));
                    label.place(x=110,y=40);
                    boton3 =ttkbootstrap.Button(frame4,text="REGISTRAR",bootstyle="primary-outline",width=40);
                    boton3.place(x=20,y=138);
                    boton5 =ttkbootstrap.Button(frame4,text="ACTUALIZAR",bootstyle="primary-outline",width=40);
                    boton5.place(x=20,y=300);
                    boton6 =ttkbootstrap.Button(frame4,text="ELIMINAR",bootstyle="primary-outline",width=40);
                    boton6.place(x=20,y=480);
                
                def menuUsuario():
                    def volver():
                        botonr.destroy();
                        boton3.destroy();
                        boton5.destroy();
                        boton6.destroy();
                        label.destroy();

                    botonr =ttkbootstrap.Button(frame4,text="VOLVER",bootstyle="primary-outline",width=10,command=volver);
                    botonr.place(x=10,y=10);
                    label= Label(frame4,text="USUARIOS",bg="#2a73b2",fg="white",font=("Arial", 15, "bold"));
                    label.place(x=100,y=40);
                    boton3 =ttkbootstrap.Button(frame4,text="REGISTRAR",bootstyle="primary-outline",width=40);
                    boton3.place(x=20,y=138);
                    boton5 =ttkbootstrap.Button(frame4,text="ACTUALIZAR",bootstyle="primary-outline",width=40);
                    boton5.place(x=20,y=300);
                    boton6 =ttkbootstrap.Button(frame4,text="ELIMINAR",bootstyle="primary-outline",width=40);
                    boton6.place(x=20,y=480);

                frame3 = ttkbootstrap.Frame(frame2);
                frame3.config(width=333,height=650)
                frame3.place(x=0,y=0);

                credenciales = ttkbootstrap.Frame(frame3, bootstyle="light");
                credenciales.config(width=180,height=180);
                credenciales.place(x=180,y=0);
                label= Label(credenciales,text=f"USUARIO:\n{str(user)}",fg="#2a73b2",font=("Arial", 10, "normal"), width=15);
                label.place(x=15,y=20);
                label= Label(credenciales,text=f"ROL:\nUSUARIO",fg="#2a73b2",font=("Arial", 10, "normal"), width=15);
                label.place(x=15,y=70);

                def logout():
                    frame2.destroy();
                    username.set("");
                    password.set("");
                    nombreUsuarioCaja.focus();

                btn = ttkbootstrap.Button(credenciales,bootstyle="danger", text="CERRAR SESIÓN", command=logout);
                btn.place(x=25,y=140)

                imagen = ttkbootstrap.Frame(frame3, bootstyle="light");
                imagen.config(width=180,height=180);
                imagen.place(x=0,y=0);

                if (rows[4] is None):
                    directorio_actual = os.path.dirname(os.path.realpath(__file__))
                    # Combinar la ruta del directorio actual con el nombre de la imagen
                    ruta_imagen = os.path.join(directorio_actual, 'sinfoto.png')

                    tk_image = PhotoImage(file=ruta_imagen);
                    label = Label(imagen, image=tk_image)
                    label.image = tk_image;
                    label.pack();
                else:
                     # Recuperar la imagen desde la base de datos
                    sql_query = "SELECT Image FROM dbo.usuarios WHERE username = ?"
                    cur.execute(sql_query, (user,))
                    raw = cur.fetchone()

                    if raw and raw[0] is not None:
                        # Convertir los datos binarios a un objeto BytesIO
                        image_data = BytesIO(raw[0])

                        # Abrir la imagen con PIL desde BytesIO
                        image = Image.open(image_data)

                        # Convertir la imagen de PIL a PhotoImage de Tkinter
                        tk_image = ImageTk.PhotoImage(image)

                        # Crear un widget Label para mostrar la imagen
                        label = Label(imagen, image=tk_image)
                        label.image = tk_image  # Referencia para evitar que la imagen sea eliminada por el recolector de basura
                        label.pack()
                    else:
                        print("No se encontró ninguna imagen en la base de datos.")



                boton3 =ttkbootstrap.Button(frame3,text="CLIENTES",bootstyle="primary-outline",width=40, command=menuCliente).place(x=35,y=210);
                boton4 =ttkbootstrap.Button(frame3,text="PRODUCTOS",bootstyle="primary-outline",width=40, command=menuProducto).place(x=35,y=320);
                boton5 =ttkbootstrap.Button(frame3,text="VENTAS",bootstyle="primary-outline",width=40, command=menuVenta).place(x=35,y=430);
                boton6 =ttkbootstrap.Button(frame3,text="USUARIOS",bootstyle="primary-outline",width=40, command=menuUsuario).place(x=35,y=540);

                frame4 = ttkbootstrap.Frame(frame2);
                frame4.config(width=667,height=650)
                frame4.place(x=333,y=0);
                

                # MessageBox.showinfo("INFO",f"EL USUARIO {rows[1]} NO TIENE PERMISOS DE ADMINISTRADOR");
                # username.set("");
                # password.set("");
                # nombreUsuarioCaja.focus();
            elif(row == 1):
                frame2 = ttkbootstrap.Frame(raiz);
                frame2.config(width=1000,height=650)
                frame2.place(x=0,y=0);
            
                def menuCliente():
                    def volver():
                        #botonr.destroy();
                        boton3.destroy();
                        boton5.destroy();
                        boton6.destroy();
                        label.destroy();
                    

                    def registrarCliente():
                        def cerrar():
                            frame5.destroy();
                            nomcli.set("");
                            apecli.set("");
                            emailcli.set("");
                            telcli.set("");
                        
                        def clientebd():
                            try:
                                IngresarCliente = "INSERT INTO Clientes(Nombre, Apellido, Email, Telefono) VALUES (?, ?, ?, ?)"
                                cur.execute(IngresarCliente, (nomcli.get(), apecli.get(), emailcli.get(), telcli.get()));
                                connection.commit();
                                MessageBox.showinfo("REGISTRO DE CLIENTES", "CLIENTE REGISTRADO CORRECTAMENTE");
                                nomcli.set("");
                                apecli.set("");
                                emailcli.set("");
                                telcli.set("");
                            except Exception as e:
                                MessageBox.showerror("REGISTRO DE CLIENTES", e);
                                nomcli.set("");
                                apecli.set("");
                                emailcli.set("");
                                telcli.set("");

                        frame5 = ttkbootstrap.Frame(frame4);
                        frame5.config(width=667,height=650)
                        frame5.place(x=0,y=0);
                

                        EtiquetaIS= Label(frame5,text="REGISTRAR CLIENTE",bg="#2a73b2",fg="white",font=("Arial", 20, "bold")).place(x=210,y=140);
                        EtiquetanomU= Label(frame5,text="NOMBRE",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=260,y=220);
                        nombreUsuarioCaja = Entry(frame5, textvariable=nomcli,bg="white",fg="black");
                        nombreUsuarioCaja.place(x=340,y=220);
                        EtiquetaContra= Label(frame5,text="APELLIDO",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=260,y=260);
                        ContraseñaCaja = Entry(frame5, textvariable=apecli,bg="white",fg="black").place(x=340,y=260);
                        EtiquetaContra2 = Label(frame5,text="CORREO",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=260,y=300);
                        ContraseñaCaja2 = Entry(frame5, textvariable=emailcli,bg="white",fg="black").place(x=340,y=300);
                        EtiquetaFoto = Label(frame5,text="TELEFONO",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=260,y=340);
                        ContraseñaCaja2 = Entry(frame5, textvariable=telcli,bg="white",fg="black").place(x=340,y=340);
                        boton1 =Button(frame5,text="Registrar",command=clientebd,bg="green",fg="white",activebackground="lime",cursor="hand2", width=15).place(x=240,y=420);
                        boton2 =Button(frame5,text="Cerrar",command=cerrar,bg="red",fg="white",activebackground="#ff3737",cursor="hand2",  width=15).place(x=370,y=420);


                    def BuscarClienteMenu():
                        # Variable global para realizar un seguimiento de si la ventana flotante está abierta
                        global ventana_flotante_abierta;
                        ventana_flotante_abierta = False
                        #treeCli.selection_remove(treeCli.selection())
                        frame5 = ttkbootstrap.Frame(frame4);
                        frame5.config(width=667,height=650)
                        frame5.place(x=0,y=0);
                        #-----------------------------------------------------------------------------------------------------------------
                        def BusCliElim(textvariable):            
                                if(Desp.get() == "Apellido"):
                                    IDClienteCaja.config(textvariable=apecli);
                                elif(Desp.get() == "Telefono"):
                                    IDClienteCaja.config(textvariable=telcli);
                                elif(Desp.get() == "Email"):
                                    IDClienteCaja.config(textvariable=emailcli);
                                else:
                                    IDClienteCaja.config(textvariable=nomcli);
                        def ElimBus():
                            if(Desp.get() == "Apellido"):
                                BuscarCli = "SELECT * FROM dbo.Clientes WHERE Apellido = ?";
                                cur.execute(BuscarCli, (apecli.get(),));
                                lista = cur.fetchone();
                                treeCli.delete(*treeCli.get_children());
                                while lista:
                                    values = tuple(lista)  # Excluye el IDCliente de la tupla
                                    treeCli.insert('', 'end', values=values)
                                    lista = cur.fetchone()
                            elif(Desp.get() == "Telefono"):
                                BuscarCli = "SELECT * FROM dbo.Clientes WHERE Telefono = ?";
                                cur.execute(BuscarCli, (telcli.get(),));
                                lista = cur.fetchone();
                                treeCli.delete(*treeCli.get_children());
                                while lista:
                                    values = tuple(lista)  # Excluye el IDCliente de la tupla
                                    treeCli.insert('', 'end', values=values)
                                    lista = cur.fetchone()
                            elif(Desp.get() == "Email"):
                                BuscarCli = "SELECT * FROM dbo.Clientes WHERE Email = ?";
                                cur.execute(BuscarCli, (emailcli.get(),));
                                lista = cur.fetchone();
                                treeCli.delete(*treeCli.get_children());
                                while lista:
                                    values = tuple(lista)  # Excluye el IDCliente de la tupla
                                    treeCli.insert('', 'end', values=values)
                                    lista = cur.fetchone()
                            else:
                                BuscarCli = "SELECT * FROM dbo.Clientes WHERE Nombre LIKE ?";
                                cur.execute(BuscarCli, (nomcli.get(),));
                                lista = cur.fetchone();
                                treeCli.delete(*treeCli.get_children());
                                while lista:
                                    values = tuple(lista)  # Excluye el IDCliente de la tupla
                                    treeCli.insert('', 'end', values=values)
                                    lista = cur.fetchone()

                        def editarMenu():
                            global ventana_flotante;
                            ventana_flotante.destroy();
                            cerrar_ventana_flotante()
                            treeCli.selection_remove(treeCli.selection())
                            def editarclientebd():
                                try:
                                    EditarCli = "UPDATE dbo.Clientes SET Nombre = ?, Apellido = ?, Email = ?, Telefono = ? WHERE IDCliente = ?;";
                                    cur.execute(EditarCli, (nomcli.get(), apecli.get(), emailcli.get(), telcli.get(),  IDcli,));
                                    connection.commit();
                                    MessageBox.showinfo("REGISTRO DE CLIENTES", "INFORMACIÓN DEL CLIENTE ACTUALIZADA CON ÉXITO");
                                    frame6.destroy();
                                    print(ventana_flotante_abierta);
                                    treeCli.selection_remove(treeCli.selection())
                                    nomcli.set("");
                                    apecli.set("");
                                    telcli.set("");
                                    emailcli.set("");
                                    treeCli.delete(*treeCli.get_children());
                                except Exception as e:
                                    MessageBox.showerror("REGISTRO DE CLIENTES", e);
                                    cur.execute('SELECT * FROM dbo.Clientes WHERE IDCliente = ?;', (IDcli, ));
                                    if (rows:= cur.fetchone()) is not None:
                                        nomcli.set(rows[1]);
                                        apecli.set(rows[2]);
                                        emailcli.set(rows[3]);
                                        telcli.set(rows[4]);
                            
                            selected = treeCli.focus();
                            idclave=treeCli.item(selected,'values');
                            IDcli=int(str(idclave[0]).join(caracter for caracter in idclave[0] if caracter.isdigit()));
                            cur.execute('SELECT * FROM Clientes WHERE IDCliente = ?;', (IDcli, ));
                            if (rows:= cur.fetchone()) is not None:
                                nomcli.set(rows[1]);
                                apecli.set(rows[2]);
                                emailcli.set(rows[3]);
                                telcli.set(rows[4]);

                            frame6 = ttkbootstrap.Frame(frame4);
                            frame6.config(width=667,height=650)
                            frame6.place(x=0,y=0);
                    

                            EtiquetaIS= Label(frame6,text="EDITAR CLIENTE",bg="#2a73b2",fg="white",font=("Arial", 20, "bold")).place(x=210,y=140);
                            EtiquetanomU= Label(frame6,text="NOMBRE",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=260,y=220);
                            nombreUsuarioCaja = Entry(frame6, textvariable=nomcli,bg="white",fg="black");
                            nombreUsuarioCaja.place(x=340,y=220);
                            EtiquetaContra= Label(frame6,text="APELLIDO",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=260,y=260);
                            ContraseñaCaja = Entry(frame6, textvariable=apecli,bg="white",fg="black").place(x=340,y=260);
                            EtiquetaContra2 = Label(frame6,text="CORREO",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=260,y=300);
                            ContraseñaCaja2 = Entry(frame6, textvariable=emailcli,bg="white",fg="black").place(x=340,y=300);
                            EtiquetaFoto = Label(frame6,text="TELEFONO",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=260,y=340);
                            ContraseñaCaja2 = Entry(frame6, textvariable=telcli,bg="white",fg="black").place(x=340,y=340);
                            boton1 =Button(frame6,text="Actualizar",command=editarclientebd,bg="green",fg="white",activebackground="lime",cursor="hand2", width=15).place(x=240,y=420);
                            boton2 =Button(frame6,text="Cerrar",command=frame6.destroy,bg="red",fg="white",activebackground="#ff3737",cursor="hand2",  width=15).place(x=370,y=420);

                        def ElimCliente():
                            try:
                                selected = treeCli.focus();
                                idclave=treeCli.item(selected,'values');
                                IDcli=int(str(idclave[0]).join(caracter for caracter in idclave[0] if caracter.isdigit()));
                                cur.execute('SELECT * FROM Clientes WHERE IDCliente = ?;', (IDcli, ));
                                if (rows:= cur.fetchone()) is not None:
                                    row = rows[0];
                                if (row == 0):
                                    MessageBox.showwarning("REGISTRO DE CLIENTES", "DEBES SELECCIONAR UN CLIENTE");
                                else:
                                    DATOS = idclave[1] + " " + idclave[2];
                                    a=MessageBox.askquestion("ELIMINAR CLIENTE","¿DESEAS ELIMINAR EL CLIENTE SELECCIONADO?\n" + DATOS)
                                    if(a == MessageBox.YES):
                                        EliminarCliente = "DELETE FROM clientes WHERE IDCliente = ?";
                                        cur.execute(EliminarCliente, (IDcli,));
                                        connection.commit();
                                        MessageBox.showinfo("REGISTRO DE CLIENTES", "CLIENTE ELIMINADO CON ÉXITO");
                                        treeCli.delete(selected);
                                        nomcli.set("");
                                        apecli.set("");
                                        telcli.set("");
                                        emailcli.set("");
                            except Exception as e:
                                MessageBox.showerror("REGISTRO DE CLIENTES", e);

                        def mostrar_ventana_flotante(event):
                            global ventana_flotante_abierta
                            if not ventana_flotante_abierta:
                                x, y = raiz.winfo_pointerxy()
                                crear_ventana_flotante(x, y)

                        def cerrar_ventana_flotante():
                            global ventana_flotante_abierta
                            if ventana_flotante_abierta:
                                ventana_flotante_abierta = False
                                ventana_flotante.destroy()

                        def crear_ventana_flotante(x,y):
                            global ventana_flotante
                            global ventana_flotante_abierta
                            ventana_flotante = Toplevel()
                            ventana_flotante.title("Ventana Flotante")
                            ventana_flotante.geometry(f"+{x}+{y}")
                            # Quital la barra de título
                            ventana_flotante.overrideredirect(True)
                            # Agrega contenido a la ventana flotante
                            btnedit = ttkbootstrap.Button(ventana_flotante,bootstyle="info", text="EDITAR", command=editarMenu, width=10);
                            btnelim = ttkbootstrap.Button(ventana_flotante,bootstyle="info", text="ELIMINAR", command=ElimCliente, width=10);
                            btnclose = ttkbootstrap.Button(ventana_flotante,bootstyle="info", text="CERRAR", command=cerrar_ventana_flotante, width=10);
                            btnedit.pack()
                            btnelim.pack()
                            btnclose.pack()
                                # Asigna una función para cerrar la ventana flotante
                            ventana_flotante.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana_flotante())
                            ventana_flotante_abierta = True;

                        

                        #-----------------------------------------------------------------------------------------------------------------
                        def volver_bus():
                            frame5.destroy();
                        botonr =ttkbootstrap.Button(frame5,text="VOLVER",bootstyle="danger-outline",width=10,command=volver_bus);
                        botonr.grid(row=0, column=0, sticky="news");
                        EtiquetaEC= Label(frame5,text="BUSCAR CLIENTES",bg="#2a73b2",fg="white",font=("Arial", 20, "bold")).grid(row=0, column=1, sticky="news", columnspan=3);
                        EtiquetaIDC= Label(frame5,text="Buscar Por",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).grid(row=1, column=0, sticky="news");
                        Desp = ttkbootstrap.Combobox(frame5, state="readonly", values=["Nombre", "Apellido","Telefono","Email"], width=15, bootstyle="primary")
                        Desp.current(0);
                        Desp.bind("<<ComboboxSelected>>",BusCliElim)
                        Desp.grid(row=1, column=1, sticky="news");
                        EtiquetaIDC= Label(frame5,text="Buscar Por",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).grid(row=1, column=0, sticky="news",padx=10);
                        IDClienteCaja = Entry(frame5,textvariable=nomcli,bg="white",fg="black", width=50);
                        IDClienteCaja.grid(row=1, column=2, sticky="news");
                        boton4 =Button(frame5,text="Buscar",command=ElimBus,bg="white",fg="black",activebackground="lime",cursor="hand2", width=10).grid(row=1, column=3, sticky="news",padx=10);
                        columns = ('ID CLIENTE', 'NOMBRE', 'APELLIDO', 'TELEFONO', 'EMAIL');
                        treeCli = ttkbootstrap.Treeview(frame5, height=34, columns=columns, show='headings', bootstyle="info")
                        treeCli.grid(row=2, column=0, sticky='news', columnspan=4,padx=(30,0));

                        
                        # Cambia a <<TreeviewSelect>> para el evento de selección del Treeview
                        treeCli.bind("<<TreeviewSelect>>", mostrar_ventana_flotante)

                        # menu_contextual = Menu(frame5, tearoff=0)
                        # menu_contextual.add_command(label="Acción Personalizada", command=accion_personalizada)

                        # setup columns attributes
                        for col in columns:
                            treeCli.heading(col, text=col)
                            treeCli.column(col, width=100, anchor=CENTER)
                            
                        sb = ttkbootstrap.Scrollbar(frame5, orient=VERTICAL, command=treeCli.yview, bootstyle="primary-round")
                        sb.grid(row=2, column=4, sticky='ns')
                        treeCli.config(yscrollcommand=sb.set)


                        # btn1 = Button(frame5, text='REESTABLECER', command=limpiar, width=30, height=2, bd=2, fg='white',bg="blue", activebackground="white", font=("Arial", 9, "bold"));
                        # btn1.grid(row=3, column=0, columnspan=2,sticky="news");
                        # btn = Button(frame5, text='CERRAR', command=frame5.destroy, width=30, height=2, bd=2, fg='white',bg="red", activebackground="white", font=("Arial", 9, "bold"));
                        # btn.grid(row=3, column=2, columnspan=3,sticky="news"); 

                    #botonr =ttkbootstrap.Button(frame4,text="VOLVER",bootstyle="danger-outline",width=10,command=volver);
                    #botonr.place(x=10,y=10);
                    label= Label(frame4,text="CLIENTES",bg="#2a73b2",fg="white",font=("Arial", 15, "bold"));
                    label.place(x=310,y=40);
                    boton3 =ttkbootstrap.Button(frame4,text="REGISTRAR",bootstyle="primary-outline",width=40, command=registrarCliente);
                    boton3.place(x=220,y=138);
                    boton5 =ttkbootstrap.Button(frame4,text="ACTUALIZAR",bootstyle="primary-outline",width=40, command=BuscarClienteMenu);
                    boton5.place(x=220,y=300);
                    boton6 =ttkbootstrap.Button(frame4,text="CERRAR",bootstyle="danger-outline",width=40, command=volver);
                    boton6.place(x=220,y=480);
                
                def menuProducto():
                    def volver():
                        #botonr.destroy();
                        boton3.destroy();
                        boton5.destroy();
                        boton6.destroy();
                        label.destroy();
                    

                    def registrarProducto():
                        def cerrar():
                            frame5.destroy();
                            prodname.set("");
                            category.set("");
                            price.set(0);
                            qty.set(0);
                        
                        def productobd():
                            try:
                                IngresarProducto = "INSERT INTO Productos(Nombre, Categoria, Precio, Cantidad) VALUES (?, ?, ?, ?)"
                                cur.execute(IngresarProducto, (prodname.get(), category.get(), price.get(), qty.get()));
                                connection.commit();
                                MessageBox.showinfo("REGISTRO DE PRODUCTOS", "PRODUCTO REGISTRADO CORRECTAMENTE");
                                prodname.set("");
                                category.set("");
                                price.set(0);
                                qty.set(0);
                            except Exception as e:
                                MessageBox.showerror("REGISTRO DE PRODUCTOS", e);
                                prodname.set("");
                                category.set("");
                                price.set(0);
                                qty.set(0);

                        frame5 = ttkbootstrap.Frame(frame4);
                        frame5.config(width=667,height=650)
                        frame5.place(x=0,y=0);
                

                        EtiquetaIS= Label(frame5,text="REGISTRAR PRODUCTO",bg="#2a73b2",fg="white",font=("Arial", 20, "bold")).place(x=210,y=140);
                        EtiquetanomU= Label(frame5,text="NOMBRE",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=260,y=220);
                        nombreUsuarioCaja = Entry(frame5, textvariable=prodname,bg="white",fg="black");
                        nombreUsuarioCaja.place(x=340,y=220);
                        EtiquetaContra= Label(frame5,text="CATEGORÍA",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=260,y=260);
                        ContraseñaCaja = Entry(frame5, textvariable=category,bg="white",fg="black").place(x=340,y=260);
                        EtiquetaContra2 = Label(frame5,text="PRECIO",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=260,y=300);
                        ContraseñaCaja2 = Entry(frame5, textvariable=price,bg="white",fg="black").place(x=340,y=300);
                        EtiquetaFoto = Label(frame5,text="CANTIDAD",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=260,y=340);
                        ContraseñaCaja2 = Entry(frame5, textvariable=qty,bg="white",fg="black").place(x=340,y=340);
                        boton1 =Button(frame5,text="Registrar",command=productobd,bg="green",fg="white",activebackground="lime",cursor="hand2", width=15).place(x=240,y=420);
                        boton2 =Button(frame5,text="Cerrar",command=cerrar,bg="red",fg="white",activebackground="#ff3737",cursor="hand2",  width=15).place(x=370,y=420);


                    def BuscarProductoMenu():
                        # Variable global para realizar un seguimiento de si la ventana flotante está abierta
                        global ventana_flotante_abierta;
                        ventana_flotante_abierta = False
                        #treeCli.selection_remove(treeCli.selection())
                        frame5 = ttkbootstrap.Frame(frame4);
                        frame5.config(width=667,height=650)
                        frame5.place(x=0,y=0);
                        #-----------------------------------------------------------------------------------------------------------------
                        def BusCliElim(textvariable):            
                                if(Desp.get() == "Categoria"):
                                    IDClienteCaja.config(textvariable=category);
                                else:
                                    IDClienteCaja.config(textvariable=prodname);
                        def ElimBus():
                            if(Desp.get() == "Categoria"):
                                BuscarCli = "SELECT * FROM dbo.productos WHERE Categoria = ?";
                                cur.execute(BuscarCli, (category.get(),));
                                lista = cur.fetchone();
                                treeCli.delete(*treeCli.get_children());
                                while lista:
                                    values = tuple(lista)  # Excluye el IDCliente de la tupla
                                    treeCli.insert('', 'end', values=values)
                                    lista = cur.fetchone()
                            else:
                                BuscarCli = "SELECT * FROM dbo.productos WHERE Nombre LIKE ?";
                                cur.execute(BuscarCli, (prodname.get(),));
                                lista = cur.fetchone();
                                treeCli.delete(*treeCli.get_children());
                                while lista:
                                    values = tuple(lista)  # Excluye el IDCliente de la tupla
                                    treeCli.insert('', 'end', values=values)
                                    lista = cur.fetchone()

                        def editarMenu():
                            global ventana_flotante;
                            ventana_flotante.destroy();
                            cerrar_ventana_flotante()
                            treeCli.selection_remove(treeCli.selection())
                            def editarproductobd():
                                try:
                                    EditarCli = "UPDATE dbo.productos SET Nombre = ?, Categoria = ?, Precio = ?, Cantidad = ? WHERE ID_Prod = ?;";
                                    cur.execute(EditarCli, (prodname.get(), category.get(), price.get(), qty.get(),  IDcli,));
                                    connection.commit();
                                    MessageBox.showinfo("REGISTRO DE PRODUCTOS", "INFORMACIÓN DEL PRODUCTO ACTUALIZADA CON ÉXITO");
                                    frame6.destroy();
                                    print(ventana_flotante_abierta);
                                    treeCli.selection_remove(treeCli.selection())
                                    prodname.set("");
                                    category.set("");
                                    price.set(0);
                                    qty.set(0);
                                    treeCli.delete(*treeCli.get_children());
                                except Exception as e:
                                    MessageBox.showerror("REGISTRO DE PRODUCTOS", e);
                                    cur.execute('SELECT * FROM dbo.productos WHERE ID_Prod = ?;', (IDcli, ));
                                    if (rows:= cur.fetchone()) is not None:
                                        prodname.set(rows[1]);
                                        category.set(rows[2]);
                                        price.set(rows[3]);
                                        qty.set(rows[4]);
                            
                            selected = treeCli.focus();
                            idclave=treeCli.item(selected,'values');
                            IDcli=int(str(idclave[0]).join(caracter for caracter in idclave[0] if caracter.isdigit()));
                            cur.execute('SELECT * FROM productos WHERE ID_Prod = ?;', (IDcli, ));
                            if (rows:= cur.fetchone()) is not None:
                                prodname.set(rows[1]);
                                category.set(rows[2]);
                                price.set(rows[3]);
                                qty.set(rows[4]);

                            frame6 = ttkbootstrap.Frame(frame4);
                            frame6.config(width=667,height=650)
                            frame6.place(x=0,y=0);
                    

                            EtiquetaIS= Label(frame6,text="EDITAR PRODUCTO",bg="#2a73b2",fg="white",font=("Arial", 20, "bold")).place(x=210,y=140);
                            EtiquetanomU= Label(frame6,text="NOMBRE",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=260,y=220);
                            nombreUsuarioCaja = Entry(frame6, textvariable=prodname,bg="white",fg="black");
                            nombreUsuarioCaja.place(x=340,y=220);
                            EtiquetaContra= Label(frame6,text="CATEGORÍA",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=260,y=260);
                            ContraseñaCaja = Entry(frame6, textvariable=category,bg="white",fg="black").place(x=340,y=260);
                            EtiquetaContra2 = Label(frame6,text="PRECIO",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=260,y=300);
                            ContraseñaCaja2 = Entry(frame6, textvariable=price,bg="white",fg="black").place(x=340,y=300);
                            EtiquetaFoto = Label(frame6,text="CANTIDAD",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=260,y=340);
                            ContraseñaCaja2 = Entry(frame6, textvariable=qty,bg="white",fg="black").place(x=340,y=340);
                            boton1 =Button(frame6,text="Actualizar",command=editarproductobd,bg="green",fg="white",activebackground="lime",cursor="hand2", width=15).place(x=240,y=420);
                            boton2 =Button(frame6,text="Cerrar",command=frame6.destroy,bg="red",fg="white",activebackground="#ff3737",cursor="hand2",  width=15).place(x=370,y=420);

                        def ElimProducto():
                            try:
                                selected = treeCli.focus();
                                idclave=treeCli.item(selected,'values');
                                IDcli=int(str(idclave[0]).join(caracter for caracter in idclave[0] if caracter.isdigit()));
                                cur.execute('SELECT * FROM productos WHERE ID_Prod = ?;', (IDcli, ));
                                if (rows:= cur.fetchone()) is not None:
                                    row = rows[0];
                                if (row == 0):
                                    MessageBox.showwarning("REGISTRO DE PRODUCTOS", "DEBES SELECCIONAR UN PRODUCTO");
                                else:
                                    DATOS = idclave[1]
                                    a=MessageBox.askquestion("ELIMINAR PRODUCTO","¿DESEAS ELIMINAR EL PRODUCTO SELECCIONADO?\n" + DATOS)
                                    if(a == MessageBox.YES):
                                        EliminarProducto = "DELETE FROM productos WHERE ID_Prod = ?";
                                        cur.execute(EliminarProducto, (IDcli,));
                                        connection.commit();
                                        MessageBox.showinfo("REGISTRO DE PRODUCTOS", "PRODUCTO ELIMINADO CON ÉXITO");
                                        treeCli.delete(selected);
                                        prodname.set(rows[1]);
                                        category.set(rows[2]);
                                        price.set(rows[3]);
                                        qty.set(rows[4]);
                            except Exception as e:
                                MessageBox.showerror("REGISTRO DE PRODUCTOS", e);

                        def mostrar_ventana_flotante(event):
                            global ventana_flotante_abierta
                            if not ventana_flotante_abierta:
                                x, y = raiz.winfo_pointerxy()
                                crear_ventana_flotante(x, y)

                        def cerrar_ventana_flotante():
                            global ventana_flotante_abierta
                            if ventana_flotante_abierta:
                                ventana_flotante_abierta = False
                                ventana_flotante.destroy()

                        def crear_ventana_flotante(x,y):
                            global ventana_flotante
                            global ventana_flotante_abierta
                            ventana_flotante = Toplevel()
                            ventana_flotante.title("Ventana Flotante")
                            ventana_flotante.geometry(f"+{x}+{y}")
                            # Quital la barra de título
                            ventana_flotante.overrideredirect(True)
                            # Agrega contenido a la ventana flotante
                            btnedit = ttkbootstrap.Button(ventana_flotante,bootstyle="info", text="EDITAR", command=editarMenu, width=10);
                            btnelim = ttkbootstrap.Button(ventana_flotante,bootstyle="info", text="ELIMINAR", command=ElimProducto, width=10);
                            btnclose = ttkbootstrap.Button(ventana_flotante,bootstyle="info", text="CERRAR", command=cerrar_ventana_flotante, width=10);
                            btnedit.pack()
                            btnelim.pack()
                            btnclose.pack()
                                # Asigna una función para cerrar la ventana flotante
                            ventana_flotante.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana_flotante())
                            ventana_flotante_abierta = True;

                        

                        #-----------------------------------------------------------------------------------------------------------------
                        def volver_bus():
                            frame5.destroy();
                        botonr =ttkbootstrap.Button(frame5,text="VOLVER",bootstyle="danger-outline",width=10,command=volver_bus);
                        botonr.grid(row=0, column=0, sticky="news");
                        EtiquetaEC= Label(frame5,text="BUSCAR PRODUCTOS",bg="#2a73b2",fg="white",font=("Arial", 20, "bold")).grid(row=0, column=1, sticky="news", columnspan=3);
                        EtiquetaIDC= Label(frame5,text="Buscar Por",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).grid(row=1, column=0, sticky="news");
                        Desp = ttkbootstrap.Combobox(frame5, state="readonly", values=["Nombre", "Categoría"], width=15, bootstyle="primary")
                        Desp.current(0);
                        Desp.bind("<<ComboboxSelected>>",BusCliElim)
                        Desp.grid(row=1, column=1, sticky="news");
                        EtiquetaIDC= Label(frame5,text="Buscar Por",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).grid(row=1, column=0, sticky="news",padx=10);
                        IDClienteCaja = Entry(frame5,textvariable=prodname,bg="white",fg="black", width=50);
                        IDClienteCaja.grid(row=1, column=2, sticky="news");
                        boton4 =Button(frame5,text="Buscar",command=ElimBus,bg="white",fg="black",activebackground="lime",cursor="hand2", width=10).grid(row=1, column=3, sticky="news",padx=10);
                        columns = ('ID PRODUCTO', 'NOMBRE', 'CATEGORIA', 'PRECIO', 'CANTIDAD');
                        treeCli = ttkbootstrap.Treeview(frame5, height=34, columns=columns, show='headings', bootstyle="info")
                        treeCli.grid(row=2, column=0, sticky='news', columnspan=4,padx=(30,0));

                        
                        # Cambia a <<TreeviewSelect>> para el evento de selección del Treeview
                        treeCli.bind("<<TreeviewSelect>>", mostrar_ventana_flotante)

                        # menu_contextual = Menu(frame5, tearoff=0)
                        # menu_contextual.add_command(label="Acción Personalizada", command=accion_personalizada)

                        # setup columns attributes
                        for col in columns:
                            treeCli.heading(col, text=col)
                            treeCli.column(col, width=100, anchor=CENTER)
                            
                        sb = ttkbootstrap.Scrollbar(frame5, orient=VERTICAL, command=treeCli.yview, bootstyle="primary-round")
                        sb.grid(row=2, column=4, sticky='ns')
                        treeCli.config(yscrollcommand=sb.set)

                    #botonr =ttkbootstrap.Button(frame4,text="VOLVER",bootstyle="danger-outline",width=10,command=volver);
                    #botonr.place(x=10,y=10);
                    label= Label(frame4,text="PRODUCTOS",bg="#2a73b2",fg="white",font=("Arial", 15, "bold"));
                    label.place(x=300,y=40);
                    boton3 =ttkbootstrap.Button(frame4,text="REGISTRAR",bootstyle="primary-outline",width=40, command=registrarProducto);
                    boton3.place(x=220,y=138);
                    boton5 =ttkbootstrap.Button(frame4,text="ACTUALIZAR",bootstyle="primary-outline",width=40, command=BuscarProductoMenu);
                    boton5.place(x=220,y=300);
                    boton6 =ttkbootstrap.Button(frame4,text="CERRAR",bootstyle="danger-outline",width=40, command=volver);
                    boton6.place(x=220,y=480);
                
                def menuVenta():
                    def volver():
                        botonr.destroy();
                        boton3.destroy();
                        boton5.destroy();
                        boton6.destroy();
                        label.destroy();
                        #frame4.destroy();
                    
                    def registrarVenta():
                        def cerrar():
                            frame5.destroy();
                            nomcli.set("");
                            apecli.set("");
                            emailcli.set("");
                            telcli.set("");
                        
                        def ventabd():
                            try:
                                global DespCli
                                print(f'Valor de DespCli.get(): {DespCli.get()}')
                                cur.execute('SELECT IDCliente FROM Clientes WHERE Nombre + ' ' + Apellido = ?;',(DespCli.get() ));
                                if (rows:= cur.fetchone()) is not None:
                                    IDCliente = rows[0];
                                    print(f'IDCliente encontrado: {IDCliente}')
                                    
                                IngresarCliente = "INSERT INTO dbo.Ventas(Fecha, ClienteID, Total) VALUES (?, ?, ?)"
                                cur.execute(IngresarCliente, (fecha.get(), IDCliente, total.get(),));
                                connection.commit();

                                cur.execute('SELECT TOP 1 VentaID FROM Ventas ORDER BY VentaID DESC;');
                                if (rows:= cur.fetchone()) is not None:
                                    IDVenta = rows[0];

                                # productos_reg = treeCli.get_children()

                                # for detalle in productos_reg:
                                #     cur.execute('INSERT INTO DetallesVenta (VentaID, ProductoID, Cantidad, PrecioUnitario) VALUES (?, ?, ?, ?)',
                                #                 (IDVenta, detalle[IDProducto.get()], detalle[Canti.get()], detalle[PrecioUnitario.get()]))
                                #     connection.commit()

                                MessageBox.showinfo("REGISTRO DE VENTAS", "VENTA REGISTRADO CORRECTAMENTE");
                            
                            except Exception as e:
                                #MessageBox.showerror("REGISTRO DE VENTAS", e);
                                print(e);

                        frame5 = ttkbootstrap.Frame(frame4);
                        frame5.config(width=667,height=650)
                        frame5.place(x=0,y=0);
                

                        EtiquetaIS= Label(frame5,text="REGISTRAR VENTA",bg="#2a73b2",fg="white",font=("Arial", 20, "bold")).place(x=210,y=20);
                        
                        global listado_combobox_nombrecliente
                        listado_combobox_nombrecliente = [];
                        listado_bd_nombrecliente = [];
                        cur.execute('SELECT Nombre, Apellido FROM Clientes');
                        listado_bd_nombrecliente = cur.fetchall();
                        for prod in listado_bd_nombrecliente:
                            nombre_completo = f"{prod[0]} {prod[1]}"
                            listado_combobox_nombrecliente.append(nombre_completo);

                        EtiquetanomU= Label(frame5,text="CLIENTE",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=20,y=60);
                        global DespCli
                        DespCli = ttkbootstrap.Combobox(frame5, state="readonly", values=listado_combobox_nombrecliente, width=85, bootstyle="primary")
                        DespCli.place(x=90,y=60);
                        global total_prod
                        total_prod = 0;

                        global listado_combobox_producto
                        listado_combobox_producto = [];
                        listado_bd_producto = [];
                        cur.execute('SELECT Nombre FROM productos');
                        listado_bd_producto = cur.fetchall();
                        for prod in listado_bd_producto:
                            listado_combobox_producto.append(prod[0]);
                            
                        
                        
                        def agregar_producto():
                            global total_prod
                            nombre_producto = Desp.get();
                            cur.execute('SELECT * FROM productos WHERE Nombre = ?;', (nombre_producto, ));
                            if (rows:= cur.fetchone()) is not None:
                                IDProducto.set(rows[0]);
                                producto.set(rows[1]);
                                PrecioUnitario.set(rows[3]);

                            id_valor = IDProducto.get();
                            producto_valor = producto.get()
                            cantidad_valor = Canti.get()
                            precio_valor = PrecioUnitario.get();

                            treeCli.insert("", "end", values=(id_valor, producto_valor, precio_valor, cantidad_valor))
                            total_prod = total_prod + float(int(cantidad_valor)*float(precio_valor));
                            total.set(total_prod)

                            # Verificar si los campos no están vacíos antes de proceder
                            if not (cantidad_valor and producto_valor):
                                MessageBox.showwarning("Campos incompletos", "Por favor ingresa el producto y la cantidad")
                                return

                    
                        EtiquetaContra= Label(frame5,text="PRODUCTO",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=20,y=100);
                        Desp = ttkbootstrap.Combobox(frame5, state="readonly", values=listado_combobox_producto, width=30, bootstyle="primary")
                        Desp.place(x=110,y=100);
                        EtiquetaContra= Label(frame5,text="CANTIDAD",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=330,y=100);
                        Canti = ttkbootstrap.Spinbox(frame5, width=5, bootstyle="primary")
                        Canti.place(x=400,y=100);
                        boton1 =Button(frame5,text="Agregar", command=agregar_producto,bg="green",fg="white",activebackground="lime",cursor="hand2", width=15).place(x=490,y=100);

                        columns = ('ID PRODUCTO', 'NOMBRE PRODUCTO', 'CANTIDAD', 'PRECIO UNITARIO');
                        treeCli = ttkbootstrap.Treeview(frame5, height=20, columns=columns, show='headings', bootstyle="info")
                        treeCli.place(x=20, y=150)
                        for col in columns:
                            treeCli.heading(col, text=col)
                            treeCli.column(col, width=149, anchor=CENTER)
                            
                        sb = ttkbootstrap.Scrollbar(frame5, orient=VERTICAL, command=treeCli.yview, bootstyle="primary-round")
                        sb.place(x=615,y=150);
                        
                        EtiquetaContra2 = Label(frame5,text="TOTAL",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=430,y=490);
                        ContraseñaCaja2 = Entry(frame5, textvariable=total,bg="white",fg="black").place(x=493,y=490);
                        
                        #ContraseñaCaja = Entry(frame5, textvariable=apecli,bg="white",fg="black").place(x=340,y=260);
                        # EtiquetaContra2 = Label(frame5,text="CANTIDAD",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=260,y=300);
                        # ContraseñaCaja2 = Entry(frame5, textvariable=emailcli,bg="white",fg="black").place(x=340,y=300);
                        # EtiquetaFoto = Label(frame5,text="FECHA",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=260,y=340);
                        # ContraseñaCaja2 = Entry(frame5, textvariable=telcli,bg="white",fg="black").place(x=340,y=340);
                        boton1 =Button(frame5,text="Registrar",command=ventabd,bg="green",fg="white",activebackground="lime",cursor="hand2", width=15).place(x=240,y=560);
                        boton2 =Button(frame5,text="Cerrar",command=cerrar,bg="red",fg="white",activebackground="#ff3737",cursor="hand2",  width=15).place(x=370,y=560);

                    botonr =ttkbootstrap.Button(frame4,text="VOLVER",bootstyle="primary-outline",width=10,command=volver);
                    botonr.place(x=10,y=10);
                    label= Label(frame4,text="VENTAS",bg="#2a73b2",fg="white",font=("Arial", 15, "bold"));
                    label.place(x=110,y=40);
                    boton3 =ttkbootstrap.Button(frame4,text="REGISTRAR",bootstyle="primary-outline",width=40, command=registrarVenta);
                    boton3.place(x=220,y=138);
                    boton5 =ttkbootstrap.Button(frame4,text="BUSCAR",bootstyle="primary-outline",width=40);
                    boton5.place(x=220,y=300);
                    boton6 =ttkbootstrap.Button(frame4,text="CERRAR",bootstyle="danger-outline",width=40, command=volver);
                    boton6.place(x=220,y=480);
                
                def menuUsuario():
                    def volver():
                        #frame4.destroy();
                        #botonr.destroy();
                        boton3.destroy();
                        boton5.destroy();
                        boton6.destroy();
                        label.destroy();
                    
                    def RegistrarSistema():
                        frame1 = Frame(frame4);
                        frame1.config(width=667,height=650)
                        frame1.place(x=0,y=0);

                        def regresar():
                            username.set("");
                            password.set("");
                            nombreUsuarioCaja.focus();
                            frame1.destroy();
                        
                        def tomar_foto():
                            # Capturar una imagen desde la cámara
                            cap = cv2.VideoCapture(0)
                            ret, frame = cap.read()
                            cap.release()

                            # Redimensionar la imagen a 180x180 píxeles
                            resized_frame = cv2.resize(frame, (180, 180))

                            # Convertir la imagen a datos binarios
                            global image_binary;
                            _, image_binary = cv2.imencode('.jpg', resized_frame)
                            image_binary = image_binary.tobytes()
                            mostrar_foto_en_label();

                        def selectfoto():
                            image_path = filedialog.askopenfilename(title="Selecciona un archivo", filetypes=[("Archivos de imagen", ("*.png", "*.jpg", "*.jpeg", "*.gif")), ("Todos los archivos", "*.*")]);
                            # Leer la imagen como datos binarios
                            with open(image_path, 'rb') as image_file:
                                global image_binary;
                                image_binary = image_file.read()
                            mostrar_foto_en_label();
                                
                        def mostrar_foto_en_label():
                            global image_binary
                            try:
                                # Convertir los datos binarios a un objeto BytesIO
                                image_data = BytesIO(image_binary)
                                # Abrir la imagen con PIL desde BytesIO
                                image_pil = Image.open(image_data)
                                # Convertir la imagen de PIL a PhotoImage de Tkinter
                                tk_image = ImageTk.PhotoImage(image_pil)
                                # Configurar el Label 'foto' con la nueva imagen
                                foto.img = tk_image  # Almacenar una referencia para evitar que la imagen sea eliminada por el recolector de basura
                                foto.config(image=tk_image)  # Usar config() para establecer la opción image
                            except Exception as e:
                                print(f"Error al mostrar la foto: {e}")

                        def Registro(): #FUNCION PARA REGISTRAR UN USUARIO EN EL SISTEMA
                            global image_binary;
                            try:
                                cur.execute('SELECT * FROM dbo.usuarios WHERE Username = ?;', (username.get(), ));
                                if cur.fetchall():
                                    MessageBox.showerror("REGISTRO DE USUARIOS", "EL NOMBRE DE USUARIO ESTÁ ACTUALMENTE EN USO, INTENTALO DE NUEVO");
                                    username.set("");
                                    password.set("");
                                    password1.set("");
                                    usertype.set(0);
                                    image_binary = None;
                                    directorio_actual = os.path.dirname(os.path.realpath(__file__))
                                    # Combinar la ruta del directorio actual con el nombre de la imagen
                                    ruta_imagen = os.path.join(directorio_actual, 'sinfoto.png')

                                    tk_image = PhotoImage(file=ruta_imagen);

                                    foto.config(image=tk_image);
                                    foto.image = tk_image;
                                elif (password.get() != password1.get()):
                                    MessageBox.showerror("REGISTRO DE USUARIOS", "LAS CONTRASEÑAS NO COINCIDEN");
                                    username.set("");
                                    password.set("");
                                    password1.set("");
                                    usertype.set(0);
                                    image_binary = None;
                                    directorio_actual = os.path.dirname(os.path.realpath(__file__))
                                    # Combinar la ruta del directorio actual con el nombre de la imagen
                                    ruta_imagen = os.path.join(directorio_actual, 'sinfoto.png')

                                    tk_image = PhotoImage(file=ruta_imagen);

                                    foto.config(image=tk_image);
                                    foto.image = tk_image;
                                else:
                                    IngresarUsuario = "INSERT INTO usuarios(Username, Password, UserType, Image) VALUES (?, ?, ?, ?)"
                                    cur.execute(IngresarUsuario, (username.get(), password.get(), usertype.get(), image_binary));
                                    connection.commit();
                                    MessageBox.showinfo("REGISTRO DE USUARIOS", "USUARIO REGISTRADO CORRECTAMENTE");
                                    username.set("");
                                    password.set("");
                                    password1.set("");
                                    usertype.set(0);
                                    image_binary = None;
                                    directorio_actual = os.path.dirname(os.path.realpath(__file__))
                                    # Combinar la ruta del directorio actual con el nombre de la imagen
                                    ruta_imagen = os.path.join(directorio_actual, 'sinfoto.png')

                                    tk_image = PhotoImage(file=ruta_imagen);

                                    foto.config(image=tk_image);
                                    foto.image = tk_image;
                            
                            except Exception as e:
                                MessageBox.showerror("REGISTRO DE USUARIOS", e);
                                username.set("");
                                password.set("");
                                password1.set("");
                                usertype.set(0);
                                image_binary = None;


                        EtiquetaIS= Label(frame1,text="REGISTRARSE",bg="#2a73b2",fg="white",font=("Arial", 40, "bold")).place(x=140,y=10);
                        EtiquetanomU= Label(frame1,text="NOMBRE DE USUARIO",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=200,y=90);
                        nombreUsuarioCaja = Entry(frame1, textvariable=username,bg="white",fg="black");
                        nombreUsuarioCaja.place(x=360,y=90);
                        EtiquetaContra= Label(frame1,text="CONTRASEÑA",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=200,y=130);
                        ContraseñaCaja = Entry(frame1, textvariable=password,bg="white",fg="black", show="*").place(x=360,y=130);
                        EtiquetaContra2 = Label(frame1,text="CONFIRMAR CONTRASEÑA",bg="#2a73b2",fg="white",font=("Arial", 8, "normal")).place(x=200,y=170);
                        ContraseñaCaja2 = Entry(frame1, textvariable=password1,bg="white",fg="black", show="*").place(x=360,y=170);
                        EtiquetaFoto = Label(frame1,text="FOTOGRAFÍA",bg="#2a73b2",fg="white",font=("Arial", 8, "normal")).place(x=200,y=210);
                        botonF =Button(frame1,text="Seleccionar Foto",command=selectfoto,bg="green",fg="white",activebackground="lime",cursor="hand2", width=15).place(x=280,y=210);
                        botonF1 =Button(frame1,text="Tomar Foto",command=tomar_foto,bg="green",fg="white",activebackground="lime",cursor="hand2", width=15).place(x=400,y=210);
                        
                        directorio_actual = os.path.dirname(os.path.realpath(__file__))
                        # Combinar la ruta del directorio actual con el nombre de la imagen
                        ruta_imagen = os.path.join(directorio_actual, 'sinfoto.png')

                        tk_image = PhotoImage(file=ruta_imagen);
                        
                        global foto;

                        foto = Label(frame1, image=tk_image);
                        foto.image = tk_image;
                        foto.config(width=180,height=180);
                        foto.place(x=245,y=260);
                        
                        EtiquetaContra2 = Label(frame1,text="PERMISOS ADMINISTRADOR",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=230,y=460);
                        checkAdmin = ttkbootstrap.Checkbutton(frame1,bootstyle="success",variable=usertype, onvalue=1, offvalue=0);
                        checkAdmin.place(x=430,y=463)
                        boton1 =Button(frame1,text="Ingresar",command=Registro,bg="green",fg="white",activebackground="lime",cursor="hand2", width=15).place(x=200,y=500);
                        boton2 =Button(frame1,text="Cancelar",command=regresar,bg="red",fg="white",activebackground="#ff3737",cursor="hand2",  width=15).place(x=370,y=500);

                    #botonr =ttkbootstrap.Button(frame4,text="VOLVER",bootstyle="primary-outline",width=10,command=volver);
                    #botonr.place(x=10,y=10);
                    label= Label(frame4,text="USUARIOS",bg="#2a73b2",fg="white",font=("Arial", 15, "bold"));
                    label.place(x=310,y=40);
                    boton3 =ttkbootstrap.Button(frame4,text="REGISTRAR",bootstyle="primary-outline",width=40, command=RegistrarSistema);
                    boton3.place(x=220,y=138);
                    boton5 =ttkbootstrap.Button(frame4,text="ACTUALIZAR",bootstyle="primary-outline",width=40, command=BuscarUsuarioMenu);
                    boton5.place(x=220,y=300);
                    boton6 =ttkbootstrap.Button(frame4,text="CERRAR",bootstyle="primary-outline",width=40, command=volver);
                    boton6.place(x=220,y=480);

                frame3 = ttkbootstrap.Frame(frame2);
                frame3.config(width=333,height=650)
                frame3.place(x=0,y=0);

                credenciales = ttkbootstrap.Frame(frame3);
                credenciales.config(width=180,height=180);
                credenciales.place(x=180,y=0);
                label= Label(credenciales,text=f"USUARIO:\n{str(user)}",fg="#2a73b2",font=("Arial", 10, "normal"), width=15);
                label.place(x=15,y=20);
                label= Label(credenciales,text=f"ROL:\nADMINISTRADOR",fg="#2a73b2",font=("Arial", 10, "normal"), width=15);
                label.place(x=15,y=70);

                def logout():
                    frame2.destroy();
                    username.set("");
                    password.set("");
                    nombreUsuarioCaja.focus();

                btn = ttkbootstrap.Button(credenciales,bootstyle="danger", text="CERRAR SESIÓN", command=logout);
                btn.place(x=25,y=140)

                imagen = ttkbootstrap.Frame(frame3, bootstyle="light");
                imagen.config(width=180,height=180);
                imagen.place(x=0,y=0);

                if (rows[4] is None):
                    directorio_actual = os.path.dirname(os.path.realpath(__file__))
                    # Combinar la ruta del directorio actual con el nombre de la imagen
                    ruta_imagen = os.path.join(directorio_actual, 'sinfoto.png')

                    tk_image = PhotoImage(file=ruta_imagen);
                    label = Label(imagen, image=tk_image)
                    label.image = tk_image;
                    label.pack();
                else:
                     # Recuperar la imagen desde la base de datos
                    sql_query = "SELECT Image FROM dbo.usuarios WHERE username = ?"
                    cur.execute(sql_query, (user,))
                    raw = cur.fetchone()

                    if raw and raw[0] is not None:
                        # Convertir los datos binarios a un objeto BytesIO
                        image_data = BytesIO(raw[0])

                        # Abrir la imagen con PIL desde BytesIO
                        image = Image.open(image_data)

                        # Convertir la imagen de PIL a PhotoImage de Tkinter
                        tk_image = ImageTk.PhotoImage(image)

                        # Crear un widget Label para mostrar la imagen
                        label = Label(imagen, image=tk_image)
                        label.image = tk_image  # Referencia para evitar que la imagen sea eliminada por el recolector de basura
                        label.pack()
                    else:
                        print("No se encontró ninguna imagen en la base de datos.")

                def BuscarUsuarioMenu():
                        # Variable global para realizar un seguimiento de si la ventana flotante está abierta
                        global ventana_flotante_abierta;
                        ventana_flotante_abierta = False
                        #treeCli.selection_remove(treeCli.selection())
                        frame5 = ttkbootstrap.Frame(frame4);
                        frame5.config(width=667,height=650)
                        frame5.place(x=0,y=0);
                        #-----------------------------------------------------------------------------------------------------------------
                        def BusCliElim(textvariable):            
                                if(Desp.get() == "Tipo Usuario"):
                                    IDClienteCaja.config(textvariable=usertype2);
                                else:
                                    IDClienteCaja.config(textvariable=username2);
                        def ElimBus():
                            if(Desp.get() == "Tipo Usuario"):
                                BuscarCli = "SELECT ID_User, Username, Usertype FROM dbo.usuarios WHERE Usertype = ?";
                                cur.execute(BuscarCli, (usertype2.get(),));
                                lista = cur.fetchone();
                                treeCli.delete(*treeCli.get_children());
                                while lista:
                                    values = tuple(lista)  # Excluye el IDCliente de la tupla
                                    treeCli.insert('', 'end', values=values)
                                    lista = cur.fetchone()
                            else:
                                BuscarCli = "SELECT ID_User, Username, Usertype FROM dbo.usuarios WHERE Username LIKE ?";
                                cur.execute(BuscarCli, (username2.get(),));
                                lista = cur.fetchone();
                                treeCli.delete(*treeCli.get_children());
                                while lista:
                                    values = tuple(lista)  # Excluye el IDCliente de la tupla
                                    treeCli.insert('', 'end', values=values)
                                    lista = cur.fetchone()

                        def editarMenu():
                            global ventana_flotante;
                            ventana_flotante.destroy();
                            cerrar_ventana_flotante()
                            global image_binary2;
                            treeCli.selection_remove(treeCli.selection())
                            def editarusuariobd():
                                global image_binary2;
                                try:
                                    EditarCli = "UPDATE dbo.usuarios SET Username = ?, Password = ?, Usertype = ?, Image = ? WHERE ID_User = ?;";
                                    cur.execute(EditarCli, (username2.get(), password2.get(), usertype2.get(), image_binary2,  IDcli,));
                                    connection.commit();
                                    MessageBox.showinfo("REGISTRO DE USUARIOS", "INFORMACIÓN DEL USUARIO ACTUALIZADA CON ÉXITO");
                                    frame6.destroy();
                                    print(ventana_flotante_abierta);
                                    treeCli.selection_remove(treeCli.selection())
                                    username2.set("");
                                    password2.set("");
                                    password12.set("");
                                    usertype2.set(0);
                                    image_binary2 = None;
                                    treeCli.delete(*treeCli.get_children());
                                except Exception as e:
                                    MessageBox.showerror("REGISTRO DE USUARIOS", e);
                                    cur.execute('SELECT * FROM dbo.usuarios WHERE ID_User = ?;', (IDcli, ));
                                    if (rows:= cur.fetchone()) is not None:
                                        username2.set(rows[1]);
                                        password2.set(rows[2]);
                                        usertype2.set(rows[3]);
                                        image_binary2 = rows[4];
                                        traerFoto();
                            
                            selected = treeCli.focus();
                            idclave=treeCli.item(selected,'values');
                            IDcli=int(str(idclave[0]).join(caracter for caracter in idclave[0] if caracter.isdigit()));
                            cur.execute('SELECT * FROM usuarios WHERE ID_User = ?;', (IDcli, ));
                            if (rows:= cur.fetchone()) is not None:
                                username2.set(rows[1]);
                                password2.set(rows[2]);
                                password12.set("");
                                usertype2.set(rows[3]);
                                image_binary2 = rows[4];

                            frame6 = ttkbootstrap.Frame(frame4);
                            frame6.config(width=667,height=650)
                            frame6.place(x=0,y=0);
                    
                            def tomar_foto():
                                # Capturar una imagen desde la cámara
                                cap = cv2.VideoCapture(0)
                                ret, frame = cap.read()
                                cap.release()

                                # Redimensionar la imagen a 180x180 píxeles
                                resized_frame = cv2.resize(frame, (180, 180))

                                # Convertir la imagen a datos binarios
                                global image_binary2;
                                _, image_binary2 = cv2.imencode('.jpg', resized_frame)
                                image_binary2 = image_binary2.tobytes()
                                mostrar_foto_en_label();

                            def selectfoto():
                                image_path = filedialog.askopenfilename(title="Selecciona un archivo", filetypes=[("Archivos de imagen", ("*.png", "*.jpg", "*.jpeg", "*.gif")), ("Todos los archivos", "*.*")]);
                                # Leer la imagen como datos binarios
                                with open(image_path, 'rb') as image_file:
                                    global image_binary2;
                                    image_binary2 = image_file.read()
                                mostrar_foto_en_label();
                                    
                            def mostrar_foto_en_label():
                                global image_binary2
                                try:
                                    # Convertir los datos binarios a un objeto BytesIO
                                    image_data = BytesIO(image_binary2)
                                    # Abrir la imagen con PIL desde BytesIO
                                    image_pil = Image.open(image_data)
                                    # Convertir la imagen de PIL a PhotoImage de Tkinter
                                    tk_image = ImageTk.PhotoImage(image_pil)
                                    # Configurar el Label 'foto' con la nueva imagen
                                    foto.img = tk_image  # Almacenar una referencia para evitar que la imagen sea eliminada por el recolector de basura
                                    foto.config(image=tk_image)  # Usar config() para establecer la opción image
                                except Exception as e:
                                    print(f"Error al mostrar la foto: {e}")

                            def traerFoto():
                                global image_binary2;
                                IDcli=int(str(idclave[0]).join(caracter for caracter in idclave[0] if caracter.isdigit()));
                                cur.execute('SELECT Image FROM usuarios WHERE ID_User = ?;', (IDcli, ));
                                if (rows:= cur.fetchone()) is not None:
                                    image_binary2 = rows[0];
                                mostrar_foto_en_label();

                            EtiquetaIS= Label(frame6,text="EDITAR USUARIO",bg="#2a73b2",fg="white",font=("Arial", 40, "bold")).place(x=140,y=10);
                            EtiquetanomU= Label(frame6,text="NOMBRE DE USUARIO",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=200,y=90);
                            nombreUsuarioCaja = Entry(frame6, textvariable=username2,bg="white",fg="black");
                            nombreUsuarioCaja.place(x=360,y=90);
                            EtiquetaContra= Label(frame6,text="CONTRASEÑA",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=200,y=130);
                            ContraseñaCaja = Entry(frame6, textvariable=password2,bg="white",fg="black", show="*").place(x=360,y=130);
                            EtiquetaContra2 = Label(frame6,text="CONFIRMAR CONTRASEÑA",bg="#2a73b2",fg="white",font=("Arial", 8, "normal")).place(x=200,y=170);
                            ContraseñaCaja2 = Entry(frame6, textvariable=password12,bg="white",fg="black", show="*").place(x=360,y=170);
                            EtiquetaFoto = Label(frame6,text="FOTOGRAFÍA",bg="#2a73b2",fg="white",font=("Arial", 8, "normal")).place(x=200,y=210);
                            botonF =Button(frame6,text="Seleccionar Foto",command=selectfoto,bg="green",fg="white",activebackground="lime",cursor="hand2", width=15).place(x=280,y=210);
                            botonF1 =Button(frame6,text="Tomar Foto",command=tomar_foto,bg="green",fg="white",activebackground="lime",cursor="hand2", width=15).place(x=400,y=210);
                            
                            directorio_actual = os.path.dirname(os.path.realpath(__file__))
                            # Combinar la ruta del directorio actual con el nombre de la imagen
                            ruta_imagen = os.path.join(directorio_actual, 'sinfoto.png')

                            tk_image = PhotoImage(file=ruta_imagen);
                            
                            global foto;

                            foto = Label(frame6, image=tk_image);
                            foto.image = tk_image;
                            foto.config(width=180,height=180);
                            foto.place(x=245,y=260);

                            traerFoto();
                            
                            EtiquetaContra2 = Label(frame6,text="PERMISOS ADMINISTRADOR",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=230,y=460);
                            checkAdmin = ttkbootstrap.Checkbutton(frame6,bootstyle="success",variable=usertype2, onvalue=1, offvalue=0);
                            checkAdmin.place(x=430,y=463)
                            boton1 =Button(frame6,text="Ingresar",command=editarusuariobd,bg="green",fg="white",activebackground="lime",cursor="hand2", width=15).place(x=200,y=500);
                            boton2 =Button(frame6,text="Cancelar",command=frame6.destroy,bg="red",fg="white",activebackground="#ff3737",cursor="hand2",  width=15).place(x=370,y=500);

                        def ElimUsuario():
                            try:
                                selected = treeCli.focus();
                                idclave=treeCli.item(selected,'values');
                                IDcli=int(str(idclave[0]).join(caracter for caracter in idclave[0] if caracter.isdigit()));
                                cur.execute('SELECT * FROM usuarios WHERE ID_User = ?;', (IDcli, ));
                                if (rows:= cur.fetchone()) is not None:
                                    row = rows[0];
                                if (row == 0):
                                    MessageBox.showwarning("REGISTRO DE USUARIOS", "DEBES SELECCIONAR UN USUARIO");
                                else:
                                    DATOS = idclave[1]
                                    a=MessageBox.askquestion("ELIMINAR USUARIO","¿DESEAS ELIMINAR EL USUARIO SELECCIONADO?\n" + DATOS)
                                    if(a == MessageBox.YES):
                                        EliminarProducto = "DELETE FROM usuarios WHERE ID_User = ?";
                                        cur.execute(EliminarProducto, (IDcli,));
                                        connection.commit();
                                        MessageBox.showinfo("REGISTRO DE USUARIOS", "USUARIO ELIMINADO CON ÉXITO");
                                        treeCli.delete(selected);
                                        username2.set(rows[1]);
                                        password2.set(rows[2]);
                                        usertype2.set(rows[3]);
                                        image_binary2 = rows[4];
                            except Exception as e:
                                MessageBox.showerror("REGISTRO DE USUARIOS", e);

                        def mostrar_ventana_flotante(event):
                            global ventana_flotante_abierta
                            if not ventana_flotante_abierta:
                                x, y = raiz.winfo_pointerxy()
                                crear_ventana_flotante(x, y)

                        def cerrar_ventana_flotante():
                            global ventana_flotante_abierta
                            if ventana_flotante_abierta:
                                ventana_flotante_abierta = False
                                ventana_flotante.destroy()

                        def crear_ventana_flotante(x,y):
                            global ventana_flotante
                            global ventana_flotante_abierta
                            ventana_flotante = Toplevel()
                            ventana_flotante.title("Ventana Flotante")
                            ventana_flotante.geometry(f"+{x}+{y}")
                            # Quital la barra de título
                            ventana_flotante.overrideredirect(True)
                            # Agrega contenido a la ventana flotante
                            btnedit = ttkbootstrap.Button(ventana_flotante,bootstyle="info", text="EDITAR", command=editarMenu, width=10);
                            btnelim = ttkbootstrap.Button(ventana_flotante,bootstyle="info", text="ELIMINAR", command=ElimUsuario, width=10);
                            btnclose = ttkbootstrap.Button(ventana_flotante,bootstyle="info", text="CERRAR", command=cerrar_ventana_flotante, width=10);
                            btnedit.pack()
                            btnelim.pack()
                            btnclose.pack()
                                # Asigna una función para cerrar la ventana flotante
                            ventana_flotante.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana_flotante())
                            ventana_flotante_abierta = True;

                        

                        #-----------------------------------------------------------------------------------------------------------------
                        def volver_bus():
                            frame5.destroy();
                        botonr =ttkbootstrap.Button(frame5,text="VOLVER",bootstyle="danger-outline",width=10,command=volver_bus);
                        botonr.grid(row=0, column=0, sticky="news");
                        EtiquetaEC= Label(frame5,text="BUSCAR USUARIOS",bg="#2a73b2",fg="white",font=("Arial", 20, "bold")).grid(row=0, column=1, sticky="news", columnspan=3);
                        EtiquetaIDC= Label(frame5,text="Buscar Por",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).grid(row=1, column=0, sticky="news");
                        Desp = ttkbootstrap.Combobox(frame5, state="readonly", values=["Nombre", "Tipo Usuario"], width=15, bootstyle="primary")
                        Desp.current(0);
                        Desp.bind("<<ComboboxSelected>>",BusCliElim)
                        Desp.grid(row=1, column=1, sticky="news");
                        EtiquetaIDC= Label(frame5,text="Buscar Por",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).grid(row=1, column=0, sticky="news",padx=10);
                        IDClienteCaja = Entry(frame5,textvariable=username2,bg="white",fg="black", width=50);
                        IDClienteCaja.grid(row=1, column=2, sticky="news");
                        boton4 =Button(frame5,text="Buscar",command=ElimBus,bg="white",fg="black",activebackground="lime",cursor="hand2", width=10).grid(row=1, column=3, sticky="news",padx=10);
                        columns = ('ID USUARIO', 'NOMBRE USUARIO', 'TIPO DE USUARIO');
                        treeCli = ttkbootstrap.Treeview(frame5, height=34, columns=columns, show='headings', bootstyle="info")
                        treeCli.grid(row=2, column=0, sticky='news', columnspan=4,padx=(30,0));

                        
                        # Cambia a <<TreeviewSelect>> para el evento de selección del Treeview
                        treeCli.bind("<<TreeviewSelect>>", mostrar_ventana_flotante)

                        # menu_contextual = Menu(frame5, tearoff=0)
                        # menu_contextual.add_command(label="Acción Personalizada", command=accion_personalizada)

                        # setup columns attributes
                        for col in columns:
                            treeCli.heading(col, text=col)
                            treeCli.column(col, width=100, anchor=CENTER)
                            
                        sb = ttkbootstrap.Scrollbar(frame5, orient=VERTICAL, command=treeCli.yview, bootstyle="primary-round")
                        sb.grid(row=2, column=4, sticky='ns')
                        treeCli.config(yscrollcommand=sb.set)

                boton3 =ttkbootstrap.Button(frame3,text="CLIENTES",bootstyle="primary-outline",width=40, command=menuCliente).place(x=35,y=210);
                boton4 =ttkbootstrap.Button(frame3,text="PRODUCTOS",bootstyle="primary-outline",width=40, command=menuProducto).place(x=35,y=320);
                boton5 =ttkbootstrap.Button(frame3,text="VENTAS",bootstyle="primary-outline",width=40, command=menuVenta).place(x=35,y=430);
                boton6 =ttkbootstrap.Button(frame3,text="USUARIOS",bootstyle="primary-outline",width=40, command=menuUsuario).place(x=35,y=540);

                frame4 = ttkbootstrap.Frame(frame2);
                frame4.config(width=667,height=650)
                frame4.place(x=333,y=0);
                
                # MessageBox.showinfo("INFO",f"EL USUARIO {rows[1]} CUENTA CON PERMISOS DE ADMINISTRADOR");
                # username.set("");
                # password.set("");
                # nombreUsuarioCaja.focus();
        else:
            MessageBox.showerror("LOGIN INCORRECTO", "LOS DATOS INGRESADOS NO SON CORRECTOS, INTENTALO DE NUEVO");
            username.set("");
            password.set("");
            nombreUsuarioCaja.focus();
    except Exception as e:
        MessageBox.showerror("Error", str(e));

def cancelar():
    username.set("");
    password.set("");
    nombreUsuarioCaja.focus();

EtiquetaIS= Label(frame,text="INICIAR SESIÓN",bg="#2a73b2",fg="white",font=("Arial", 40, "bold")).place(x=50,y=10);
EtiquetanomU= Label(frame,text="NOMBRE DE USUARIO",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=110,y=90);
nombreUsuarioCaja = Entry(frame, textvariable=username,bg="white",fg="black");
nombreUsuarioCaja.place(x=270,y=90);
EtiquetaContra= Label(frame,text="CONTRASEÑA",bg="#2a73b2",fg="white",font=("Arial", 10, "normal")).place(x=110,y=130);
ContraseñaCaja = Entry(frame, textvariable=password,bg="white",fg="black", show="*").place(x=270,y=130);
boton1 =Button(frame,text="Ingresar",command=login,bg="green",fg="white",activebackground="lime",cursor="hand2", width=15).place(x=110,y=170);
boton2 =Button(frame,text="Cancelar",command=cancelar,bg="red",fg="white",activebackground="#ff3737",cursor="hand2",  width=15).place(x=280,y=170);
boton3 =Button(frame,text="Registrarse", command=RegistrarSistema,bg="blue",fg="white",activebackground="skyblue",cursor="hand2", width=40).place(x=110,y=210);

raiz.mainloop();
connection.close()
cur.close()