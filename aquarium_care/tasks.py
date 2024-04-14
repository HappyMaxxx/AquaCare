from background_task import background

@background(schedule=60)  # Запускати завдання кожну хвилину
def update_aquarium_pollution():
    print("Updating aquarium pollution")