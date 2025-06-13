import typer

app=typer.Typer(name="iLectric Car")

@app.command()
def drive(miles:int,direction:str):
    print(f"Driving for {miles} miles {direction}")

@app.command()
def stop():
    print("Stopping the vehicle")

if __name__ == "__main__":
    typer.run(app)
