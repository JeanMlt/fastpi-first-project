from fastapi import FastAPI, HTTPException
import requests
import json
import os

app = FastAPI()

@app.get("/")
def read_root():
    print("this is a root!")
    return {"Hello": "World"}
    
@app.post("/dog-fact/")
def post_dog_fact():
    response = requests.get("http://dog-api.kinduff.com/api/facts")
    data = response.content.decode()
    myjson = json.loads(data)
    with open('dog-facts.txt', 'a') as file:
        file.write(myjson["facts"][0] + "\n")
        return {"message": f"Dog fact added to the list "}
    
@app.get("/dog-fact/{fact_id}")
def get_dog_fact(fact_id : int):
    with open('dog-facts.txt', 'r') as file:
        for i, line in enumerate(file):
            if i == fact_id:  
                return line
    raise HTTPException(status_code=404, detail=f"fact index must belong to the list (max index = {len(file)}")

# PUT - Remplacer une line spécifique de dog-facts.txt en utilisant l'api 'dog-api.kinduff' pour obtenir un fait random
@app.put("/dog-facts/{fact_id}")
def put_dog_fact(fact_id: int):
    temp_file_path = 'temp.txt'
    dog_file_path = 'dog-facts.txt'
    if not os.path.exists(dog_file_path) or os.stat(dog_file_path).st_size == 0:
        raise HTTPException(status_code=404, detail="No dog facts found in the file.")

    with open(dog_file_path, 'r') as read_file, open(temp_file_path, 'w') as write_file:
        for i, line in enumerate(read_file):
            if i != fact_id:
                write_file.write(line)
            else:
                response = requests.get("http://dog-api.kinduff.com/api/facts")
                data = response.content.decode()
                myjson = json.loads(data)
                write_file.write(myjson["facts"][0] + "\n")
        if fact_id < 0 or fact_id > i :
            raise HTTPException(status_code=400, detail=f"Invalid index: {fact_id}. It must be between 0 and {i}.")
        os.replace(temp_file_path, 'dog-facts.txt')
        return {"message": f"Dog fact #{fact_id} modified"}     

# DELETE - Supprimer un fait sur les chiens
@app.delete("/dog-facts/{fact_id}")
def remove_dog_fact(fact_id: int):
    temp_file_path = 'temp.txt'
    dog_file_path = 'dog-facts.txt'

    if not os.path.exists(dog_file_path) or os.stat(dog_file_path).st_size == 0:
        raise HTTPException(status_code=404, detail="No dog facts found in the file.")

    with open(dog_file_path, 'r') as read_file, open(temp_file_path, 'w') as write_file:
        for i, line in enumerate(read_file):
            if i != fact_id:
                write_file.write(line)
        if fact_id < 0 or fact_id > i :
            raise HTTPException(status_code=400, detail=f"Invalid index: {fact_id}. It must be between 0 and {i}.")
        os.replace(temp_file_path, 'dog-facts.txt')
        return {"message": f"Dog fact #{fact_id} deleted"}  
    
        
