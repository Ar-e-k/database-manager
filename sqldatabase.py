import os
import sys
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkInterfacev1  import *

class manager(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master=master
        self.master.title=("Database manager")
        self.open_database=None
        self.open_database_name=None
        self.current_screen=None
        self.table_edited=None
        self.main_screen()

    def main_screen(self):
        try:
            self.current_screen.clear_screen()
        except AttributeError:
            pass
        self.current_screen=screen(self,
                buttons=[
                ["Create new", self.create_new, {"side":"top"}],
                ["Open", self.open_existing, {"fill":"x"}],
                ["Close", self.close, {"side":"bottom", "fill":"x"}]
                ]
                )

    #Small functions
    def error(self, message, source): #Returns a error screen and then goes back to where the error accured
        self.current_screen.clear_screen()
        self.current_screen=screen(self,
                lables=[
                [message, {"side":"top"}]
                ],
                buttons=[
                ["Ok", source, {"side":"bottom", "fill":"x"}]
                ]
                )

    def confirm(self, source, output):
        self.current_screen.clear_screen()
        self.current_screen=screen(self,
                lables=[
                ["Are you sure", {"side":"top", "fill":"x"}]
                ],
                buttons=[
                ["Yes", output, {"side":"left"}],
                ["No", source, {"side":"right"}]
                ]
                )

    def close(self): #Closes the database manager
        sys.exit()
    #End of Small functions

    #Opening a database
    def create_new(self): #Creates a new database
        self.current_screen.clear_screen()
        self.current_screen=screen(self,
                lables=[
                ["Name your database", {"side":"top"}]
                ],
                entries=[
                ["table_name", {"fill":"x"}]
                ],
                buttons=[
                ["Add", self.verify_new, {"side":"top", "fill":"x"}],
                ["Cancle", self.main_screen, {"side":"bottom", "fill":"x"}]
                ]
                )

    def verify_new(self): #Veryfies the new database name
        text=self.current_screen.get_text()
        new_name=list(text.values())
        if new_name==[""]:
            self.error("Cannot assign no name", self.create_new)
        else:
            pass
        files=[]
        for (dirpath, dirnames, filenames) in os.walk("Databases"):
            files.append(filenames)
        if [str(str(new_name[0])+".db")] in files or [str(new_name[0])] in files:
            self.error("Name already exists", self.create_new)
        else:
            print(text, list(text.values())[0])
            self.open(str(list(text.values())[0]))

    def open_existing(self): #Allows to open one of the existing databases
        self.current_screen.clear_screen()
        buttons=[]
        file=None
        for (dirpath, dirnames, filenames) in os.walk("Databases"):
            file=filenames
        buttons.append(["Cancle", self.main_screen, {"side":"bottom", "fill":"x"}])
        self.current_screen=screen(self,
                choices=[
                ["Database name", file, {"side":"top"}]
                ],
                buttons=[
                ["Cancle", self.main_screen, {"side":"bottom", "fill":"x"}],
                ["Ok", self.open, {"side":"bottom", "fill":"x"}]
                ]
                )

    def open(self, name=None): #Opens the database
        self.entry=[]
        try:
            self.open_database_name=self.current_screen.get_choice()["Database name"]
        except KeyError:
            if name==None:
                pass
            else:
                self.open_database_name=name
        self.current_screen.clear_screen()
        self.open_database=database(self.open_database_name)
        self.current_screen=screen(self,
                lables=[
                [str("Currently open: "+self.open_database_name), {"fill":"x", "side":"top"}]
                ],
                buttons=[
                ["Add table", self.add_table_collumn, {"fill":"x", "side":"top"}],
                ["View table", self.view_table_menu, {"fill":"x", "side":"top"}],
                ["Close database", self.close_database, {"fill":"x", "side":"bottom"}]
                ]
                )
    #End of Opening a databese

    #Adding a new table to a database
    def add_table_collumn(self):
        self.current_screen.clear_screen()
        self.current_screen=screen(self,
                lables=[
                [str("Currently open: "+self.open_database_name), {"fill":"x", "side":"top"}],
                ["Name", {"side":"top"}],
                ["Type", {"side":"bottom"}]
                ],
                buttons=[
                ["Cancle", self.open, {"side":"bottom", "fill":"x"}],
                ["More attributes", lambda: self.more_collumns(self.add_table_collumn), {"side":"bottom", "fill":"x"}],
                ["Create", self.add_table, {"side":"bottom", "fill":"x"}]
                ],
                choices=[
                ["Type", self.open_database.valid_datatypes, {"side":"bottom", "fill":"x"}]
                ],
                entries=[
                ["Attribute", {"side":"top", "fill":"x"}],
                ],
                order=[2, 3, 0, 1]
                )

    def add_table(self):
        cell=[self.current_screen.get_text(), self.current_screen.get_choice()]
        if cell[1]["Type"]=="":
            self.error("No datatype selected", self.add_table_collumn)
            return None
        elif cell[0]["Attribute"]=="":
            self.error("No column name selected", self.add_table_collumn)
            return None
        self.entry.append(cell)
        self.current_screen.clear_screen()
        self.current_screen=screen(self,
                lables=[
                [str("Currently open: "+self.open_database_name), {"fill":"x", "side":"top"}],
                ["Table name", {"fill":"x"}]
                ],
                entries=[
                ["Name", {"side":"top", "fill":"x"}]
                ],
                buttons=[
                ["Ok", self.add_table_send, {"side":"top", "fill":"x"}],
                ["Cancle", self.open, {"side":"bottom", "fill":"x"}]
                ]
                )

    def add_table_send(self):
        out=self.open_database.add_table(self.current_screen.get_text(), self.entry)
        if out==("Operation successfull"):
            self.error(out, self.open)
        else:
            self.error(out, self.add_table_collumn)

    def more_collumns(self, action):
        cell=[self.current_screen.get_text(), self.current_screen.get_choice()]
        if cell[1]["Type"]=="":
            self.error("No datatype selected", action)
            return None
        elif cell[0]["Attribute"]=="":
            self.error("No column name selected", action)
            return None
        self.entry.append(cell)
        action()
    #End of Adding a new table to a database

    #Table view

    #Viewing a table
    def view_table_menu(self):
        tables=self.open_database.show_tables()
        self.current_screen.clear_screen()
        tables_avaliable=[]
        for table in tables:
            if table[0]==("sqlite_sequence"):
                continue
            tables_avaliable.append(table[0])
        self.current_screen=screen(self,
                choices=[
                ["Table name", tables_avaliable, {"side":"top"}]
                ],
                buttons=[
                ["Cancle", self.open, {"side":"bottom", "fill":"x"}],
                ["Ok", self.table_view, {"side":"bottom", "fill":"x"}]
                ]
                )

    def table_view(self):
        self.entry=[]
        try:
            self.table_edited=self.current_screen.get_choice()["Table name"]
            if self.table_edited=="":
                self.error("No input", self.view_table_menu)
                return None
        except KeyError:
            pass
        self.current_screen.clear_screen()
        self.current_screen=screen(self,
                lables=[
                [str("Viewing table: "+ self.table_edited), {"fill":"x", "side":"top"}]
                ],
                buttons=[
                ["Search results", self.search_table_menu, {"fill":"x"}],
                ["Edit columns", self.edit_col_menu, {"fill":"x"}],
                ["Edit data", self.edit_data_menu, {"fill":"x"}],
                ["Delete table", lambda: self.confirm(self.table_view, self.delete_table), {"fill":"x", "side":"top"}],
                ["Close table", self.close_table, {"fill":"x", "side":"bottom"}]
                ]
                )

    def search_table_menu(self):
        self.current_screen.clear_screen()
        self.current_screen=screen(self,
                lables=[
                [str("Viewing table: "+ self.table_edited), {"fill":"x", "side":"top"}]
                ],
                buttons=[
                ["Show all", self.all_data, {"fill":"x"}],
                ["Show a columns", self.one_column, {"fill":"x"}],
                ["Search a column", self.one_row, {"fill":"x"}],
                ["Cancle", self.table_view, {"fill":"x", "side":"bottom"}]
                ]
                )

    def edit_col_menu(self):
        self.current_screen.clear_screen()
        self.current_screen=screen(self,
                lables=[
                [str("Viewing table: "+ self.table_edited), {"fill":"x", "side":"top"}]
                ],
                buttons=[
                ["Add", self.add_table_collumn_l, {"fill":"x"}],
                ["Edit names", self.rename_col, {"fill":"x"}],
                ["Cancle", self.table_view, {"fill":"x"}]
                ]
                )

    def edit_data_menu(self):
        self.current_screen.clear_screen()
        self.current_screen=screen(self,
                lables=[
                [str("Viewing table: "+ self.table_edited), {"fill":"x", "side":"top"}]
                ],
                buttons=[
                ["Add", self.add_row, {"fill":"x"}],
                ["Replace", lambda:self.find_col(self.edit_record), {"fill":"x"}],
                ["Delete", lambda:self.find_col(self.del_record), {"fill":"x"}],
                ["Cancle", self.table_view, {"fill":"x"}]
                ]
                )
    #End of Viewing a table

    #Displaying data
    def all_data(self):
        self.display_data(self.open_database.column_search(self.table_edited, "*"))

    def one_column(self):
        self.display_data_picker(self.open_database.show_table_headers(self.table_edited), "display")

    def one_row(self):
        self.display_data_picker(self.open_database.show_table_headers(self.table_edited), "choose1")

    def display_data_picker(self, choice, where, data=None):
        self.current_screen.clear_screen()
        self.current_screen=screen(self,
                lables=[
                [str("Viewing table: "+ self.table_edited), {"fill":"x", "side":"top"}]
                ],
                choices=[
                ["Choice", choice, {"side":"top"}]
                ],
                buttons=[
                ["Close", self.table_view, {"fill":"x", "side":"bottom"}],
                ["Ok", lambda:self.get_choice_data(where, data), {"fill":"x", "side":"bottom"}]
                ]
                )

    def get_choice_data(self, where, data=None):
        choice=self.current_screen.get_choice()["Choice"]
        if choice=="":
            self.error("nothing selected", self.search_table_menu)
            return None
        if where=="display":
            if data==None:
                self.display_data(self.open_database.column_search(self.table_edited, choice))
            else:
                self.display_data(self.open_database.column_search(self.table_edited, "*", [data, choice]))
        elif where=="choose1":
            self.display_data_picker(self.open_database.column_search(self.table_edited, choice), "display", choice)

    def display_data(self, data):
        self.current_screen.clear_screen()
        self.current_screen=screen(self,
                lables=[
                [str("Viewing table: "+ self.table_edited), {"fill":"x", "side":"top"}]
                ],
                choices=[
                ["Displayed data", data, {"side":"top"}]
                ],
                buttons=[
                ["Close", self.table_view, {"fill":"x", "side":"bottom"}]
                ]
                )
    #End of Displaying data

    #Deleting a table
    def delete_table(self):
        self.open_database.del_table(self.table_edited)
        self.table_edited=None
        self.open()
    #End of deleting a table

    #Adding columns
    def add_table_collumn_l(self):
        self.current_screen.clear_screen()
        self.current_screen=screen(self,
                lables=[
                [str("Viewing table: "+ self.table_edited), {"fill":"x", "side":"top"}],
                ["Name", {"side":"top"}],
                ["Type", {"side":"bottom"}]
                ],
                buttons=[
                ["Cancle", self.table_view, {"side":"bottom", "fill":"x"}],
                ["More attributes", lambda: self.more_collumns(self.add_table_collumn_l), {"side":"bottom", "fill":"x"}],
                ["Add", self.col_add_send, {"side":"bottom", "fill":"x"}]
                ],
                choices=[
                ["Type", self.open_database.valid_datatypes, {"side":"bottom", "fill":"x"}]
                ],
                entries=[
                ["Attribute", {"side":"top", "fill":"x"}],
                ],
                order=[2, 3, 0, 1]
                )

    def col_add_send(self):
        cell=[self.current_screen.get_text(), self.current_screen.get_choice()]
        print(cell)
        if cell[1]["Type"]=="":
            self.error("No datatype selected", self.add_table_collumn)
            return None
        elif cell[0]["Attribute"]=="":
            self.error("No column name selected", self.add_table_collumn)
            return None
        self.entry.append(cell)
        name={"Name":self.table_edited}
        for entry in self.entry:
            out=self.open_database.add_column(name, entry)
            if out==("Operation successfull"):
                pass
            else:
                self.error(out, self.table_view)
        self.error(out, self.table_view)
    #End of Adding columns

    #Reanaming a column
    def rename_col(self):
        self.current_screen.clear_screen()
        self.current_screen=screen(self,
                lables=[
                [str("Viewing table: "+ self.table_edited), {"fill":"x", "side":"top"}],
                ["Old name", {"side":"top"}],
                ["New name", {"side":"bottom"}]
                ],
                buttons=[
                ["Cancle", self.table_view, {"side":"bottom", "fill":"x"}],
                ["Change", self.rename_col_send, {"side":"bottom", "fill":"x"}]
                ],
                choices=[
                ["Old", self.open_database.show_table_headers(self.table_edited), {"side":"top", "fill":"x"}]
                ],
                entries=[
                ["New", {"side":"bottom", "fill":"x"}],
                ],
                order=[2, 1, 0, 3]
                )

    def rename_col_send(self):
        cell=[self.current_screen.get_choice(), self.current_screen.get_text()]
        print(cell)
        if cell[0]["Old"]=="":
            self.error("No column name selected", self.raname)
            return None
        elif cell[1]["New"]=="" or cell[1]["New"] in self.open_database.show_table_headers(self.table_edited):
            self.error("Invalid new column name", self.rename_col)
            return None
        out=self.open_database.change_col_name(self.table_edited, cell[0]["Old"], cell[1]["New"])
        self.error(out, self.table_view)
    #End of ranaming a column

    #Adding data
    def add_row(self):
        self.headers=self.open_database.show_table_headers(self.table_edited)
        self.headers=self.headers[1:len(self.headers)]
        if len(self.headers)==1:
            self.headers.pop(self.headers.index("None"))
        else:
            pass
        self.data=[]
        self.pos=0
        self.add_cell_data(self.headers[self.pos])
        self.pos+=1

    def add_cell_data(self, header):
        self.current_screen.clear_screen()
        self.current_screen=screen(self,
                lables=[
                [str("Add too row "+ header), {"side":"top", "fill":"x"}]
                ],
                entries=[
                ["Value", {"side":"top", "fill":"x"}]
                ],
                buttons=[
                ["Cancle", self.table_view, {"side":"bottom", "fill":"x"}],
                ["Ok", self.add_cell, {"side":"bottom", "fill":"x"}]
                ]
                )

    def add_cell(self):
        data=self.current_screen.get_text()
        self.data.append(data["Value"])
        if len(self.data)==len(self.headers):
            out=self.open_database.add_data(self.table_edited, self.data)
            self.data=None
            del self.pos
            del self.headers
            self.table_view()
        else:
            self.add_cell_data(self.headers[self.pos])
            self.pos+=1
    #End of Adding data

    #Editing and deleating data
    def find_col(self, action):
        data=self.open_database.show_table_headers(self.table_edited)[1:]
        self.current_screen.clear_screen()
        self.current_screen=screen(self,
                lables=[
                [str("Viewing table: "+ self.table_edited), {"fill":"x", "side":"top"}]
                ],
                choices=[
                ["Choice", data, {"side":"top"}]
                ],
                buttons=[
                ["Cancle", self.table_view, {"fill":"x", "side":"bottom"}],
                ["Ok", lambda:self.find_record(action), {"fill":"x", "side":"bottom"}]
                ]
                )

    def find_record(self, action):
        data=self.current_screen.get_choice()["Choice"]
        if data=="":
            self.error("nothing selected", self.search_table_menu)
            return None
        col=data
        data=self.open_database.column_search(self.table_edited, data)
        for i in range(0, len(data)):
            data[i]=str(i)+" "+str(data[i][0])
        self.current_screen.clear_screen()
        self.current_screen=screen(self,
                lables=[
                [str("Viewing table: "+ self.table_edited), {"fill":"x", "side":"top"}]
                ],
                choices=[
                ["Choice", data, {"side":"top"}]
                ],
                buttons=[
                ["Cancle", self.table_view, {"fill":"x", "side":"bottom"}],
                ["Ok", lambda: action(col), {"fill":"x", "side":"bottom"}]
                ]
                )

    def edit_record(self, col):
        data=self.current_screen.get_choice()["Choice"]
        if data=="":
            self.error("nothing selected", self.search_table_menu)
            return None
        data=data[0]
        self.current_screen.clear_screen()
        self.current_screen=screen(self,
                lables=[
                [str("Viewing table: "+ self.table_edited), {"fill":"x", "side":"top"}]
                ],
                entries=[
                ["New value", {"side":"top", "fill":"x"}]
                ],
                buttons=[
                ["Cancle", self.table_view, {"fill":"x", "side":"bottom"}],
                ["Ok", lambda: self.send_edit(col, data), {"fill":"x", "side":"bottom"}]
                ]
                )

    def send_edit(self, col, id):
        n_value=self.current_screen.get_text()["New value"]
        result=self.open_database.edit_data([self.table_edited, col, id], n_value)
        self.error(result, self.table_view)

    def del_record(self, col):
        id=self.current_screen.get_choice()["Choice"]
        if id=="":
            self.error("nothing selected", self.search_table_menu)
            return None
        id=id[0]
        self.del_data=[self.table_edited, id]
        self.confirm(self.table_view, self.send_del)

    def send_del(self):
        result=self.open_database.del_row(self.del_data)
        self.error(result, self.table_view)
        del self.del_data
    #End of Editing and deleating data

    #Closing table
    def close_table(self):
        self.table_edited=None
        self.open()
    #End of Closing talbe

    #End of Talbe view

    def close_database(self): #Closes the database and goes back to main screen
        self.open_database.close()
        self.open_database=None
        self.open_database_name=None
        self.main_screen()

    def debug_log(self):
        print(self.open_database.show_table_headers(self.table_edited))

class database:

    def __init__(self, name):
        if (".db") in name:
            self.database=sqlite3.connect(str("Databases/"+name))
        else:
            self.database=sqlite3.connect(str("Databases/"+name+".db"))
        self.cursor=self.database.cursor()
        self.valid_datatypes=["TEXT", "REAL", "INTEGER", "BLOB"]

    #New table
    def add_table(self, name, collumns):
        try:
            self.cursor.execute('''CREATE TABLE {na} (rowid INTEGER PRIMARY KEY AUTOINCREMENT)'''.format(na=name["Name"]))
        except sqlite3.OperationalError:
            return ("error-table exists or table name invalid")
        if len(collumns)==1:
            collumns.append([{"Attribute":None}, {"Type":"TEXT"}])
        for collumn in collumns:
            result=self.add_column(name, collumn)
            if result!=("Operation successfull"):
                return result
        self.database.commit()
        return ("Operation successfull")
    #End of New table

    #Editing table
    def add_data(self, table, data):
        #try:
        heads=self.show_table_headers(table)[1:len(self.show_table_headers(table))]
        if len(data)==1:
            heads=(heads[0], "None")
            data=(data[0], "None")
            self.cursor.execute("INSERT INTO {tab} {headers} VALUES{data}".format(tab=table, headers=heads, data=data))
            self.database.commit()
            return ("Operation successfull")
        heads=tuple(heads)
        data=tuple(data)
        self.cursor.execute("INSERT INTO {tab} {headers} VALUES{data}".format(tab=table, headers=heads, data=data))
        self.database.commit()
        return ("Operation successfull")

    def edit_data(self, position, data):
        if data.isnumeric():
            self.cursor.execute('UPDATE {tab} SET {col} = {data} where rowid = {id}'.format(tab=position[0], col=position[1], id=position[2], data=data))
        else:
            self.cursor.execute('UPDATE {tab} SET {col} = "{data}" where rowid = {id}'.format(tab=position[0], col=position[1], id=position[2], data=data))
        self.database.commit()
        return ("Operation successfull")

    def del_row(self, position):
        self.cursor.execute('DELETE from {tab} where rowid = {id}'.format(tab=position[0], id=position[1]))
        self.database.commit()
        return ("Operation successfull")

    def add_column(self, name, collumn):
        print(collumn)
        c_name=collumn[0]["Attribute"]
        c_type=collumn[1]["Type"]
        try:
            self.cursor.execute('''ALTER TABLE {na} ADD COLUMN "{cn}" {ct}'''.format(na=name["Name"], cn=c_name, ct=c_type))
            self.database.commit()
            return ("Operation successfull")
        except sqlite3.OperationalError:
            return ("error-row exists")

    def change_col_name(self, table, col_name, n_name):
        #try:
        self.cursor.execute('ALTER TABLE {tab} RENAME COLUMN {o_nam} TO {n_nam}'.format(tab=table, o_nam=col_name, n_nam=n_name))
        self.database.commit()
        return ("Operation successfull")
        #except:
        #retrun ("Error")

    def del_table(self, name):
        self.cursor.execute('DROP table {tab}'.format(tab=name))
        self.database.commit()
    #End of Editing table

    #Displays data that needs to be dispayed
    def column_search(self, table, column, row=None):
        if row==None:
            self.cursor.execute('SELECT {col} FROM {tab}'.format(col=column, tab=table))
        else:
            self.cursor.execute('SELECT {col} FROM {tab} WHERE {row}={val}'.format(col=column, tab=table, row=row[0], val=row[1]))
        return self.cursor.fetchall()
    #End of Displaying data

    def show_tables(self):
        self.cursor.execute('SELECT name from sqlite_master WHERE type= "table"')
        return self.cursor.fetchall()

    def show_table_headers(self, table):
        curs=self.database.execute('SELECT * FROM {tab}'.format(tab=table))
        headers=[description[0] for description in curs.description]
        return headers

    def close(self):
        self.database.close()

def main():
    root=tk.Tk()
    root.resizable(False, False)
    app=manager(root)
    root.mainloop()

if __name__==("__main__"):
    main()
