from repositories.unit_of_work import UnitOfWork

petRepo = UnitOfWork().petRepo()
print(petRepo.get_objects(where={"name":"Sandy", "column":["Nah", "Hungry", "Lennon"], "id": 1}))