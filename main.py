from flet import *
import useaction_table as ut
from datatable import my_table, table, call_db

import sqlite3
conn = sqlite3.connect("database/clients.db", check_same_thread=False)

def main(page:Page):
    ut.create_table()
    page.scroll = "auto"
    
    def show_input(e):
        input_cont.offset = transform.Offset(0, 0)
        page.update()
    
    def hide_con(e):
        input_cont.offset = transform.Offset(2, 0)
        page.update()
    
    def save_data(e):
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clients (name, last_name, birthdate, email) VALUES(?, ?, ?, ?)",
                      (name.value, last_name.value, birthdate.value, email.value))
            conn.commit()
            
            input_cont.offset = transform.Offset(2, 0)
            
            page.snack_bar = SnackBar(
                Text("Sucesso"),
                bgcolor="white"
            )
            
            page.snack_bar.open = True
            
            table.rows.clear()
            call_db()
            table.update()
            page.update()
            
        except Exception as e:
            print(e)      
    
    name = TextField(label="Name")
    last_name = TextField(label="Last name")
    birthdate = TextField(label="Birthdate")
    email = TextField(label="Email")
    
    input_cont = Card(
        offset = transform.Offset(2, 0),
        animate_offset = animation.Animation(600, curve="easeIn"),
        
        elevation = 30,
        content= Container(
            # bgcolor="green",
            padding=20,
            content=Column([
                Row([
                    Text("Novo cadastro", size=20, weight="bold"),
                    IconButton(icon="close", icon_size=30, on_click=hide_con),
                ]),
                name,
                last_name,
                birthdate,
                email,
                FilledButton("Salvar", on_click=save_data)
            ])
        )
    )
    
    page.add(
        Column([
            Text("CRUD em Python e Flet", size=30, weight="bold"),
            ElevatedButton("Cadastrar", on_click=show_input),
            my_table,
            input_cont
        ])
    )
    
app(target=main)