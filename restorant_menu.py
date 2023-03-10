import dataclasses
import json
from dataclasses import dataclass
from typing import Optional, List
import psycopg2 as psycopg2
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
app = FastAPI()


@dataclass
class Menu:
    # id: int
    title: str
    description: str


@dataclass
class Dish:
    submenu_id: int
    title: str
    description: str
    price: int


@dataclass
class Submenu:
    menu_id: int
    title: str
    description: str
    # dishes: List[Dish]


@dataclass
class SubmenuDTO(Submenu):
    dishes_count: int


@dataclass
class MenuDTO(Menu):
    submenus_count: int
    dishes_count: int


def get_connection():
    conn = psycopg2.connect(  # данные для подключения к базе данных
        host='localhost',
        user='postgres',
        password='123',
        database='postgres',
    )
    conn.autocommit = True  # метод для внесения изменений в БД
    return conn


@app.get('/api/v1/menus')
def get_all_person_data():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM menus;"""
            )
            response = cursor.fetchall()
            print(response)
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")
            return response


@app.post('/api/v1/menus')
def insert_person(menu: Menu):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            a = cursor.execute(
                f"""INSERT INTO menus (title, description)
                        VALUES('{menu.title}', '{menu.description}');"""
            )
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
        raise HTTPException(status_code=404, detail="Item not found")
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")
            return JSONResponse(content=dataclasses.asdict(menu), status_code=201)

@app.get('/api/v1/menus/{id}')
def get_person_data(id: int):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM menus WHERE id = {id};"""
            )
            response = cursor.fetchall()
            # menu: Menu = Menu(*response[0])
            menu: Menu = Menu(*response[0][1:])
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
        raise HTTPException(status_code=404, detail="Item not found")
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")
            # return response
            return menu
            # return JSONResponse(content=dataclasses.asdict(menu), status_code=201)
            # return dataclasses.asdict(menu)

@app.post('/api/v1/menus/{target_menu_id}/submenus')
def insert_person(menu: Menu):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            a = cursor.execute(
                f"""INSERT INTO menus (title, description)
                        VALUES('{menu.title}', '{menu.description}');"""
            )
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
        raise HTTPException(status_code=404, detail="Item not found")
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")
            return JSONResponse(content=dataclasses.asdict(menu), status_code=201)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
