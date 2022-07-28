from tkinter import ttk
from tkinter import *
import sqlite3


class Producto:
    db = "database/productos.db"

    def __init__(self, root):  # hacemos este producto la ppal
        self.ventana = root  # todas las configuraciones de la ventana lo hacemos desde este parametro de la clase, tkinter nos pide q las manipulaciones se hagan a través de un objeto
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(1,1)
        # Significa q se puede redimensionar en las dos dimensiones, 0,0 para desactivarlas
        self.ventana.wm_iconbitmap("recursos/M6_P2_icon.ico")

        #  Creacion del contenedor  Frame ppal
        frame = LabelFrame(self.ventana, text=" Registrar un nuevo producto", font=('Bahnschrift', 12))
        frame.grid(row=0, column=4, columnspan=4)

        # Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ", font=('Bahnschrift', 10))
        self.etiqueta_nombre.grid(row=1, column=0, sticky=E)

        #  Entry Nombre
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1, sticky=W)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ", font=('Bahnschrift', 10))
        self.etiqueta_precio.grid(row=2, column=0, sticky=E)
        #  Entry Precio
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1, sticky=W)

        # Label Categoria
        self.etiqueta_categoria = Label(frame, text="Categoría: ", font=('Bahnschrift', 10))
        self.etiqueta_categoria.grid(row=3, column=0, sticky=E)
        #  Entry Categoria
        self.categoria = Entry(frame)
        self.categoria.grid(row=3, column=1, sticky=W)

        # Label Stock
        self.etiqueta_stock = Label(frame, text="Stock: ", font=('Bahnschrift', 10))
        self.etiqueta_stock.grid(row=4, column=0, sticky=E)
        #  Entry Categoria
        self.stock = Entry(frame)
        self.stock.grid(row=4, column=1, sticky=W)

        #  Boton Añadir Producto
        style = ttk.Style()
        style.configure('C.TButton', font=("Bahnschrift", 11), foreground = 'green')
        self.boton_aniadir = ttk.Button(frame, style='C.TButton', text="Guardar Producto", command=self.add_producto)
        self.boton_aniadir.grid(row=6, columnspan=4, sticky=W + E)

        self.mensaje = Label(frame, text="", fg="red", font=('Bahnschrift', 10))
        self.mensaje.grid(row=5, column=0, columnspan=2, sticky=W + E)

        #  Tabla productos
        style = ttk.Style()
        # Estilo personalizado para la tabla style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Bahnschrift', 11))  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading",
                        font=('Bahnschrift', 12, 'bold'))  # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Eliminamos los bordes

        #  Estructura de la tabla
        self.tabla = ttk.Treeview(frame, height=20, columns=('#1', '#2','#3'), style="mystyle.Treeview")
        self.tabla.grid(row=7, column=0, columnspan=2)
        self.tabla.heading("#0", text="Nombre", anchor=W)
        self.tabla.heading("#1", text="Precio", anchor=W)
        self.tabla.heading("#2", text="Categoria", anchor=W)
        self.tabla.heading("#3", text="Stock", anchor=W)

        # Botones de Eliminar y Editar
        s = ttk.Style()
        s.configure('my.TButton', font=('Bahnschrift', 14), foreground = 'red')

        boton_eliminar = ttk.Button(text = 'ELIMINAR', style="my.TButton", command=self.del_producto)
        boton_eliminar.grid(row = 2, column = 2, columnspan=6, sticky=EW)

        a = ttk.Style()
        a.configure('my2.TButton', font=('Bahnschrift', 14), foreground='blue')
        boton_editar = ttk.Button(text='EDITAR', style="my2.TButton", command=self.edit_producto)
        boton_editar.grid(row = 5, column = 2, columnspan=6, sticky=EW)

        self.get_productos()

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):
        #  Primero limpiamos los datos residuales que queden en la tabla
        registros_tabla = self.tabla.get_children()  # Obtenemos todos los datos de la tabla
        for fila in registros_tabla:
            self.tabla.delete(fila)
        # Consulta SQL
        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_consulta(query)
        # Print los datos en pantalla
        for fila in registros:
            print("print get_productos",fila)
            self.tabla.insert("", 0, text=fila[1], values=[fila[2], fila[3], fila[4]])

    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0

    def validacion_precio(self):
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0

    def validacion_categoria(self):
        categoria_introducido_por_usuario = self.categoria.get()
        return len(categoria_introducido_por_usuario) != 0

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria():
            query = "INSERT INTO producto VALUES(NULL, ?, ?, ?,?)"  # Consulta SQL sin los datos
            parametros = (self.nombre.get(), self.precio.get(), self.categoria.get(), self.stock.get())  # Parametros de la consulta SQL
            self.db_consulta(query, parametros)
            self.mensaje['text'] = "Producto {} añadido con éxito".format(self.nombre.get())
            self.nombre.delete(0,END)  # Borrar el campo nombre del formulario
            self.precio.delete(0, END) # Borrar el campo precio del formulario
            self.categoria.delete(0, END)  # Borrar el campo categoria del formulario
            self.stock.delete(0, END)  # Borrar el campo stock del formulario

            #  Para Debug, ya hemos visto que funciona y no nos hacen falta estos print
            #  print(self.nombre.get())
            #  print(self.precio.get())

        elif self.validacion_nombre() and self.validacion_precio() == False and self.validacion_categoria():
            print("El precio es obligatorio")
            self.mensaje["text"]="El precio es obligatorio"
        elif self.validacion_nombre() == False and self.validacion_precio() and self.validacion_categoria():
            print("El nombre es obligatorio")
            self.mensaje["text"] = "El nombre es obligatorio"
        elif self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria()==False:
            print("la categoría es obligatoria")
            self.mensaje["text"] = "la categoría es obligatoria"
        elif self.validacion_nombre() and self.validacion_precio()==False and self.validacion_categoria() == False:
            print("la categoría y el precio son obligatorios")
            self.mensaje["text"] = "la categoría y el precio son obligatorios"
        elif self.validacion_nombre()==False and self.validacion_precio()  and self.validacion_categoria() == False:
            print("la categoría y el nombre son obligatorios")
            self.mensaje["text"] = "la categoría y el nombre son obligatorios"
        elif self.validacion_nombre()==False and self.validacion_precio()==False and self.validacion_categoria():
            print("El nombre y el precio son obligatorios")
            self.mensaje["text"] = "El nombre y el precio son obligatorios"

        else:
            print("El nombre, precio y la categoría son obligatorios")
            self.mensaje["text"] = "El nombre, precio y la categoría son obligatorios"

        self.get_productos()

    def del_producto(self):
        # Debug
        # #print(self.tabla.item(self.tabla.selection()))
        # #print(self.tabla.item(self.tabla.selection())['text'])
        # #print(self.tabla.item(self.tabla.selection())['values'])
        # #print(self.tabla.item(self.tabla.selection())['values'][0])

        self.mensaje['text'] = ''
        # Mensaje inicialmente vacio # Comprobacion de que se seleccione un producto para poder eliminarlo
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return
        self.mensaje["text"]=""
        nombre = self.tabla.item(self.tabla.selection())["text"]
        query = "DELETE FROM producto WHERE nombre = ?"
        self.db_consulta(query, (nombre,))
        self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
        self.get_productos()

    def edit_producto(self):
        self.mensaje['text'] = ''
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return
        nombre = self.tabla.item(self.tabla.selection())['text']
        old_precio = self.tabla.item(self.tabla.selection())["values"][0]
        old_categoria= self.tabla.item(self.tabla.selection())["values"][1]
        old_stock = self.tabla.item(self.tabla.selection())["values"][2]

        self.ventana_editar = Toplevel()  # Crear una ventana por delante de la principal
        self.ventana_editar.title = "Editar Producto"
        self.ventana_editar.resizable(1,1)
        self.ventana_editar.wm_iconbitmap("recursos/M6_P2_icon.ico")

        titulo = Label(self.ventana_editar, text='Edición de Producto', font=('Bahnschrift', 25, 'bold'))
        titulo.grid(column=4, row=0, columnspan=4, sticky=W+E)

        # Creacion del contenedor Frame de la ventana de Editar Producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto", font=("Bahnschrift", 11)) #
        #  frame_ep: Frame Editar Producto
        frame_ep.grid(row=1, column=4, columnspan=20, pady=40)

        # Label Nombre antiguo
        self.etiqueta_nombre_antiuguo = Label(frame_ep, text = "Nombre antiguo: ", font=("Bahnschrift", 10))
        # Etiqueta de texto ubicada en el frame
        self.etiqueta_nombre_antiuguo.grid(row=2, column=0)
        # Posicionamiento a traves de grid
        # Entry Nombre antiguo (texto que no se podra modificar)
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar,
                                                                           value=nombre), state='readonly', font=("Bahnschrift", 10))
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ", font=("Bahnschrift", 10))
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)
        # Entry Nombre nuevo (texto que si se podra modificar)
        self.input_nombre_nuevo = Entry(frame_ep)
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus() # Para que el foco del raton vaya a este Entry al inicio

        # Label Precio antiguo
        self.etiqueta_precio_anituguo = Label(frame_ep,text="Precio antiguo: ",font=("Bahnschrift", 10))
        # Etiqueta de texto ubicada en el frame
        self.etiqueta_precio_anituguo.grid(row=4, column=0)
        # Posicionamiento a traves de grid
        # Entry Precio antiguo (texto que no se podra modificar)
        self.input_precio_antiguo = Entry(frame_ep,textvariable=StringVar(self.ventana_editar, value=old_precio),
                                          state='readonly', font=("Bahnschrift", 10))
        self.input_precio_antiguo.grid(row=4, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ", font=("Bahnschrift", 10))
        self.etiqueta_precio_nuevo.grid(row=5, column=0)
        # Entry Precio nuevo (texto que si se podra modificar)
        self.input_precio_nuevo = Entry(frame_ep, )
        self.input_precio_nuevo.grid(row=5, column=1)

        # Label Categoría antiguo
        self.etiqueta_categoria_anitigua = Label(frame_ep, text="Categoría antigua: ", font=("Bahnschrift", 10))
        # Etiqueta de texto ubicada en el frame
        self.etiqueta_categoria_anitigua.grid(row=6, column=0)
        # Posicionamiento a traves de grid
        # Entry Precio antiguo (texto que no se podra modificar)
        self.input_categoria_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_categoria),
                                          state='readonly', font=("Bahnschrift", 10))
        self.input_categoria_antiguo.grid(row=6, column=1)

        # Label Categoría nueva
        self.etiqueta_categoria_nuevo = Label(frame_ep, text="Categoría nueva: ", font=("Bahnschrift", 10))
        self.etiqueta_categoria_nuevo.grid(row=7, column=0)
        # Entry Categoría nuevo (texto que si se podra modificar)
        self.input_categoria_nuevo = Entry(frame_ep)
        self.input_categoria_nuevo.grid(row=7, column=1)

        # Label Stock antiguo
        self.etiqueta_stock_anitigua = Label(frame_ep, text="Stock antiguo: ", font=("Bahnschrift", 10))
        # Etiqueta de texto ubicada en el frame
        self.etiqueta_stock_anitigua.grid(row=8, column=0)
        # Posicionamiento a traves de grid
        # Entry Stock antiguo (texto que no se podra modificar)
        self.input_stock_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_stock),
                                             state='readonly', font=("Bahnschrift", 10))
        self.input_stock_antiguo.grid(row=8, column=1)

        # Label Stock nueva
        self.etiqueta_stock_nuevo = Label(frame_ep, text="Stock nuevo: ", font=("Bahnschrift", 10))
        self.etiqueta_stock_nuevo.grid(row=9, column=0)
        # Entry Stock nuevo (texto que si se podra modificar)
        self.input_stock_nuevo = Entry(frame_ep)
        self.input_stock_nuevo.grid(row=9, column=1)

        # Boton Actualizar Producto

        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto", style='C.TButton', command=lambda:
        self.actualizar_productos(self.input_nombre_nuevo.get(),
                                  self.input_nombre_antiguo.get(),
                                  self.input_precio_nuevo.get(),
                                  self.input_precio_antiguo.get(),
                                  self.input_categoria_nuevo.get(),
                                  self.input_categoria_antiguo.get(),
                                  self.input_stock_nuevo.get(),
                                  self.input_stock_antiguo.get()))
        self.boton_actualizar.grid(row=10, columnspan=2, sticky=W + E)

    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio, nueva_categoria, antigua_categoria, nuevo_stock, antiguo_stock):
        producto_modificado = False
        query = 'UPDATE producto SET nombre = ?, precio = ?, categoria = ?, stock= ?  WHERE nombre = ? AND precio = ? AND categoria = ? AND stock = ?'
        if nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria == '' and nuevo_stock == '':
            parametros = (nuevo_nombre, antiguo_precio, antigua_categoria, antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock == '':
            parametros = (antiguo_nombre, nuevo_precio, antigua_categoria, antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio== '' and nueva_categoria != '' and nuevo_stock == '':
            parametros = (antiguo_nombre, antiguo_precio, nueva_categoria, antiguo_stock, antiguo_nombre, antiguo_precio,antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nueva_categoria == '' and nuevo_stock != '':
            parametros = (antiguo_nombre, antiguo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock == '':
            parametros = (nuevo_nombre, nuevo_precio, antigua_categoria, antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria != '' and nuevo_stock == '':
            parametros = (nuevo_nombre, antiguo_precio, nueva_categoria, antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria == '' and nuevo_stock != '':
            parametros = (nuevo_nombre, antiguo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock == '':
            parametros = (antiguo_nombre, nuevo_precio, nueva_categoria, antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock != '':
            parametros = (antiguo_nombre, nuevo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nueva_categoria != '' and nuevo_stock != '':
            parametros = (antiguo_nombre, antiguo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock == '':
            parametros = (nuevo_nombre, nuevo_precio, nueva_categoria, antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock != '':
            parametros = (nuevo_nombre, nuevo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria != '' and nuevo_stock != '':
            parametros = (nuevo_nombre, antiguo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock != '':
            parametros = (antiguo_nombre, nuevo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock != '':
            parametros = (nuevo_nombre, nuevo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True


        if(producto_modificado):
            self.db_consulta(query, parametros) # Ejecutar la consulta
            self.ventana_editar.destroy() # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(antiguo_nombre) # Mostrar mensaje para el usuario
            self.get_productos() # Actualizar la tabla de productos
        else:
            self.ventana_editar.destroy() # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} NO ha sido actualizado'.format(antiguo_nombre) # Mostrar mensaje para el usuario



if __name__ == "__main__":
    root = Tk()  # Constructor de ventana gráfica. Instancia de la ventana ppal
    app = Producto(root)
    root.mainloop()  # Para que la ventana de nuestra app se quede viva en pantalla
