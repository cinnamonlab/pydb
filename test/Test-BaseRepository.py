from repositories.unit_of_work import UnitOfWork

## SQL SCRIPTS
# CREATE DATABASE pets;
# USE pets;
# CREATE TABLE cats
# (
#   id              INT unsigned NOT NULL AUTO_INCREMENT,
#   name            VARCHAR(150) NOT NULL,
#   owner           VARCHAR(150) NOT NULL,
#   birth           DATE NOT NULL,
#   modified           DATE NOT NULL,
#   PRIMARY KEY     (id)
# );
# INSERT INTO cats ( name, owner, birth, modified) VALUES
#   ( 'Sandy', 'Lennon', '2015-01-03', '2015-01-03' ),
#   ( 'Cookie', 'Casey', '2013-11-13', '2013-11-13' ),
#   ( 'Charlie', 'River', '2016-05-21', '2016-05-21' );
##

petRepo = UnitOfWork().petRepo()

print("First run!")
petRepo.begin_transaction()
petRepo.insert_object({"name": "Soi",
                        "owner": "Nah",
                        "birth": "2017-01-03",
                        "modified": "2017-03-28"})
records = petRepo.get_objects()
firstRecord = petRepo.get_first_object()
petRepo.insert_object({"name": "Jerry",
                        "owner": "Hungry",
                        "birth": "2017-11-03",
                        "modified": "2017-11-28"})
petRepo.update_object(where={"name": "Soi"}, setFields={"name": "Cao"})
petRepo.delete_object(where={"name": ["Cao", "Soi", "Jerry"]})
petRepo.end_transaction()
print("Records: ", records)
print("First: ", firstRecord)
print("\n")



print("get_objects")
print(petRepo.get_objects())
print(petRepo.get_objects(where={"name":"Sandy", "owner":["Nah", "Hungry", "Lennon"], "id": 1}))
print(petRepo.get_objects(orderBy={"birth": "ASC", "modified": "DESC"}))
print(petRepo.get_objects(limit=100, page=2))
print(petRepo.get_objects(where={"name":"Soi", "owner":["Nah", "Hungry"], "id": 1},
                    orderBy={"birth": "ASC", "modified": "DESC"},
                    limit=100, page=0))
print(petRepo.get_objects(where={"id": 1}))
print("\n")



print("get_first_object")
print(petRepo.get_first_object())
print(petRepo.get_first_object(where={"name":"Sandy", "owner":["Nah", "Hungry", "Lennon"], "id": 1}))
print(petRepo.get_first_object(orderBy={"birth": "ASC", "modified": "DESC"}))
print(petRepo.get_first_object(where={"name":"Soi", "owner":["Nah", "Hungry"], "id": 1},
                                orderBy={"birth": "ASC", "modified": "DESC"}))
print(petRepo.get_first_object_by_id(1))
print("\n")



print("update_object")
petRepo.begin_transaction()
# print(petRepo.update_object()) #E
# print(petRepo.update_object(where={}, setFields={})) #E
# print(petRepo.update_object(where={"name":"Sandy", "owner":["Nah", "Hungry", "Lennon"]})) #E
# print(petRepo.update_object(setFields={"name": "Nah111"})) #E
petRepo.update_object(setFields={"name": "Nah111"}, where={"name": "Soi", "owner": ["Nah", "Hungry"]})
petRepo.update_object_by_id(id='2', setFields={"name": "Nah111"})
petRepo.end_transaction()
print("\n")



print("insert_object")
petRepo.begin_transaction()
petRepo.insert_object({"name": "Abc",
                        "owner": "Hungry",
                        "birth": "2017-11-03",
                        "modified": "2017-11-28"})
petRepo.insert_object({"name": "Def",
                        "owner": "Hungry",
                        "birth": "2017-11-03",
                        "modified": "2017-11-28"})
# petRepo.insert_object({}) #E
# petRepo.insert_object() #E
petRepo.end_transaction()
print("\n")



print("delete_object")
petRepo.begin_transaction()
# petRepo.delete_object() #E
# petRepo.delete_object({}) #E
petRepo.delete_object({"name": "Abc", "owner": ["Hungry", "Nah"]})
petRepo.end_transaction()
print("\n")




