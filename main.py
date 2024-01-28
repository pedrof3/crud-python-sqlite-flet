import re
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
        
    def hide_invalid(e):
        invalid_input.offset = transform.Offset(2, 0)
        page.update()
    
    def save_data(e):
        valid_date = bool(re.search(r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$', birthdate.value))
        valid_email = bool(re.search(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email.value))

        if valid_date == False or valid_email == False:
            print("Invalid data type in Birthdate or Email")
            invalid_input.offset = transform.Offset(0, 0)
            table.rows.clear()
            call_db()
            table.update()
            page.update()
        else:
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
    
    name = TextField(label="Name", border_radius=30,)
    last_name = TextField(label="Last name", border_radius=30)
    birthdate = TextField(label="Birthdate", border_radius=30,)
    email = TextField(label="Email", border_radius=30)
        
    input_cont = Card(
        offset = transform.Offset(2, 0),
        animate_offset = animation.Animation(600, curve="easeIn"),
        elevation = 30,
        content= Container(
            bgcolor="black300",
            border=border.all(2, "blue"),
            border_radius=20,
            alignment=alignment.center,
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
                ElevatedButton("Salvar", color="white", bgcolor="blue", on_click=save_data)
            ]),
        )
    )
    
    invalid_input = Card(
        offset = transform.Offset(2, 0),
        animate_offset = animation.Animation(600, curve="easeIn"),
        elevation = 30,
        content= Container(
            bgcolor="black300",
            border=border.all(2, "red"),
            border_radius=20,
            alignment=alignment.center,
            padding=20,
            content=Column([
                Row([
                    Text("Invalid data type in Birthdate or Email", size=20, weight="bold", color="red"),
                    IconButton(icon="close", icon_size=30, on_click=hide_invalid),
                ]),
            ]),
        )
    )
    
    page.add(
        Column([
            
            Text("CRUD em Python e Flet", size=30, weight="bold"),
            ElevatedButton("Cadastrar", color="white", bgcolor="blue", on_click=show_input),
            my_table,
            invalid_input,
            input_cont,
        ])
    )
    
app(target=main)