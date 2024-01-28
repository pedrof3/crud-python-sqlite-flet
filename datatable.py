from flet import *
import sqlite3
conn = sqlite3.connect('database/clients.db', check_same_thread=False)

table = DataTable(
    columns=[
        DataColumn(Text("Actions")),
        DataColumn(Text("Name")),
        DataColumn(Text("Last name")),
        DataColumn(Text("Birthdate")),
        DataColumn(Text("Email")),
    ],
    rows=[]
)

def show_delete(e):
    try:
        my_id = int(e.control.data)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients WHERE id=?", (my_id,))
        conn.commit()
        conn.close()
        print("Deletado com sucesso")
        table.rows.clear()
        call_db()
        table.update()
        
    except Exception as e:
        print(e)

id_edit = Text()
name_edit = TextField(label="Name")
last_name_edit = TextField(label="Last name")
birthdate_edit = TextField(label="Birthdate")
email_edit = TextField(label="Email")

def hide_dlg(e):
    dlg.visible = False
    dlg.update()


def save_update(e):
    try:
        my_id = id_edit.value
        cursor = conn.cursor()
        cursor.execute("UPDATE clients SET name=?, last_name=?, birthdate=?, email=? WHERE id=?",
                       (name_edit.value, last_name_edit.value, birthdate_edit.value, email_edit.value, my_id))
        conn.commit()
        conn.close()
        print("Cadastro alterado!")
        
        table.rows.clear()
        call_db()
        dlg.visible = False
        dlg.update()
        table.update()
    
    except Exception as e:
        print(e)    

dlg = Container(
    border=border.all(2, "blue"),
    border_radius=20,
    padding=10,
    content= Column([
        
        Row([
            Text("Editar dados", size=20, weight="bold"),
            IconButton(icon="close", on_click=hide_dlg)
        ], alignment="spaceBetween"),
        name_edit,
        last_name_edit,
        birthdate_edit,
        email_edit,
        ElevatedButton("Salvar edição", color="white", bgcolor="blue", on_click=save_update),
    ])
)

def show_edit(e):
    data_edit = e.control.data
    id_edit.value = data_edit['id']
    name_edit.value = data_edit['name']
    last_name_edit.value = data_edit['last_name']
    birthdate_edit.value = data_edit['birthdate']
    email_edit.value = data_edit['email']
    
    dlg.visible = True
    dlg.update()


def call_db():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    print(clients)
    
    if not clients == "":
        keys = ['id', 'name', 'last_name', 'birthdate', 'email']
        result = [dict(zip(keys, values)) for values in clients]
        
        for x in result:
            table.rows.append(
                DataRow(
                    cells = [
                        DataCell(
                            Row([
                                IconButton(
                                    icon = "create",
                                    icon_color="green",
                                    data = x,
                                    on_click= show_edit,
                                    ),
                                IconButton(
                                    icon = "delete",
                                    icon_color="red",
                                    data = x['id'],
                                    on_click= show_delete,
                                    ),
                                ]
                            )
                        ),
                        DataCell(Text(x['name'])),
                        DataCell(Text(x['last_name'])),
                        DataCell(Text(x['birthdate'])),
                        DataCell(Text(x['email'])),
                    ],
                ),
            )
            
call_db()
dlg.visible = False

my_table = Column([
    dlg,
    Row([table], scroll="always")
])