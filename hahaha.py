import time
import json
import jsonlines
from PyQt5.QtWidgets import QMessageBox

class Car(object):
    def __init__(self, plate, type, stime):
        self.plate = plate
        self.type = type
        self.stime = stime
    def obj_json(self, obj_instance):
        #print(type(obj_instance))
        return{
            'plate':obj_instance.plate,
            'type':obj_instance.type,
            'stime':obj_instance.stime
        }

def jsonToClass(car):
    return Car(car['plate'], car['type'], car['stime'])

class CarMesDb(object):
    __filename = ""
    def __init__(self, fileName):
        self.__filename = fileName
    def addCar(self, car):
        with open(self.__filename, 'a') as f:
            f.write(json.dumps(car, default=car.obj_json))
            f.write('\n')
    def getCarSTime(self, platea):
        with open(self.__filename, "r") as f:
            cars_json = jsonlines.Reader(f)
            for car in cars_json:
                if car['plate'] == platea:
                    return car['stime']
        return ""
    def delCar(self, platea):
        plate = platea
        set = []
        with open(self.__filename, "r") as f:
            cars_json = jsonlines.Reader(f)
            for car in cars_json:
                #print(type(car))
                #print(car)
                #print(car['plate'])
                if car['plate'] != plate:
                    set.append(car)
        with open(self.__filename, 'w') as f:
            for car in set:
                f.write(json.dumps(car))
                f.write('\n')

    def isExist(self, platea):
        with open(self.__filename, "r") as f:
            cars_json = jsonlines.Reader(f)
            for car in cars_json:
                if car['plate'] == platea:
                    return True
        return False
def carIsLocal(platea):
    with open("localcars.json", 'r') as f:
        cars_json = jsonlines.Reader(f)
        for car in cars_json:
            if car['plate'] == platea:
                return True
    return False
if __name__ == "__main__":
    carMesDb = CarMesDb("data.json")
    carMesDb.addCar(Car("豫WE456", "小型车", time.time()))
    print(carMesDb.getCarSTime("豫WE456"))
    #carMesDb.delCar("豫WE456")
    print(carMesDb.isExist("豫WE456"))
    print(carMesDb.isExist("粤WE456"))
    print(carIsLocal("豫WE456"))
    print(carIsLocal("豫C66666"))
