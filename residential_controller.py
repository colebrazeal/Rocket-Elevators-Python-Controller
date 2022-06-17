# from contextlib import nullcontext


elevatorID = 1
floorRequestButtonID = 1
callButtonID = 1

 #----------------------------COLUMN----------------------------#

class Column:
    def __init__(self, _id, _amountOfFloors, _amountOfElevators):
        self.ID = _id
        self.status = "0"
        self.amountOfFloors = _amountOfFloors
        self.amountOfFloors = _amountOfElevators
        self.elevatorList = []
        self.callButtonList = []

        self.createElevators(_amountOfFloors, _amountOfElevators)
        self.createCallButtons(_amountOfFloors)

    #----------------------------METHODS----------------------------#

    def createCallButtons(self, _amountOfFloors):
        buttonFloor = 1
        global callButtonID
        for i in range(_amountOfFloors):
            if(buttonFloor < _amountOfFloors):
                callUpButton = CallButton(callButtonID, buttonFloor, "up")
                self.callButtonList.append(callUpButton)
                callButtonID += 1
            
    
            if(buttonFloor > 1):
                callDownButton = CallButton(callButtonID, buttonFloor, "down")
                self.callButtonList.append(callDownButton)
                callButtonID += 1
            
            buttonFloor += 1

    def createElevators(self, _amountOfFloors, _amountOfElevators):
        for i in range(_amountOfElevators): 
            global elevatorID
            elevator = Elevator(elevatorID, _amountOfFloors)
            self.elevatorList.append(elevator)
            elevatorID += 1  
        
    ##Simulate when a user press a button outside the elevator

    def requestElevator(self, floor, direction):
        elevator = self.findElevator(floor, direction)
        elevator.floorRequestList.append(floor)
        elevator.sortFloorList()
        elevator.move()
        elevator.operateDoors()
    
        return elevator
    
    ##We use a score system depending on the current elevators state. Since the bestScore and the referenceGap are 
    ##higher values than what could be possibly calculated, the first elevator will always become the default bestElevator, 
    ##before being compared with to other elevators. If two elevators get the same score, the nearest one is prioritized.

    def findElevator(self, requestedFloor, requestedDirection):
            bestElevatorInformations = {
            "bestElevator": None,
            "bestScore": 5,
            "referenceGap": 10000000
           }

            for elevator in self.elevatorList:
                ##The elevator is at my floor and going in the direction I want
                if (requestedFloor == elevator.currentFloor and elevator.status == "stopped" and requestedDirection == elevator.direction): 
                    bestElevatorInformations = self.checkIfElevatorIsBetter(1, elevator, bestElevatorInformations, requestedFloor)
                    #The elevator is lower than me, is coming up and I want to go up
                elif (requestedFloor > elevator.currentFloor and elevator.direction == "up" and requestedDirection == elevator.direction):
                    bestElevatorInformations = self.checkIfElevatorIsBetter(2, elevator, bestElevatorInformations, requestedFloor)
                    #The elevator is higher than me, is coming down and I want to go down
                elif (requestedFloor < elevator.currentFloor and elevator.direction == "down" and requestedDirection == elevator.direction):
                    bestElevatorInformations = self.checkIfElevatorIsBetter(2, elevator, bestElevatorInformations, requestedFloor)
                    #The elevator is idle
                elif (elevator.status == "idle"):
                    bestElevatorInformations = self.checkIfElevatorIsBetter(3, elevator, bestElevatorInformations, requestedFloor)
                    #The elevator is not available, but still could take the call if nothing better is found
                else:
                    bestElevatorInformations = self.checkIfElevatorIsBetter(4, elevator, bestElevatorInformations, requestedFloor)
            
                
            
            return bestElevatorInformations["bestElevator"]

    def checkIfElevatorIsBetter(self, scoreToCheck, newElevator, bestElevatorInformations, floor):
        if (scoreToCheck < bestElevatorInformations["bestScore"]):
            bestElevatorInformations["bestScore"] = scoreToCheck
            bestElevatorInformations["bestElevator"] = newElevator
            bestElevatorInformations["referenceGap"] = abs(newElevator.currentFloor - floor)
        elif (bestElevatorInformations["bestScore"] == scoreToCheck):
            gap = abs(newElevator.currentFloor - floor)
            if (bestElevatorInformations["referenceGap"] > gap):
                bestElevatorInformations["bestScore"] = scoreToCheck
                bestElevatorInformations["bestElevator"] = newElevator
                bestElevatorInformations["referenceGap"] = gap
                            
        return bestElevatorInformations; 

#----------------------------COLUMN----------------------------# 

#----------------------------ELEVATOR----------------------------# 

class Elevator:
    def __init__(self, _id, _amountOfFloors,):
        self.ID = _id
        self.status = ""
        self.amountOfFloors = _amountOfFloors
        self.currentFloor = 1
        self.direction = None 
        self.door = Door(_id)
        self.floorRequestButtonList = []
        self.floorRequestList = []
        self.createFloorRequestButton(_amountOfFloors)

    def createFloorRequestButton(self, _amountOfFloors):
        buttonFloor = 1
        global floorRequestButtonID
        for i in range(_amountOfFloors):
            floorRequestButton = FloorRequestButton(floorRequestButtonID, buttonFloor)
            self.floorRequestButtonList.append(floorRequestButton)
            buttonFloor += 1
            floorRequestButtonID += 1 
        
    #Simulate when a user press a button inside the elevator

    def requestFloor(self, floor):
        self.floorRequestList.append(floor)
        self.sortFloorList()
        self.move()
        self.operateDoors()

    def move(self):
        global screenDisplay
        while(len(self.floorRequestList)):
            destination = self.floorRequestList[0]
            screenDisplay = 0
            self.status = "moving"
            if(self.currentFloor < destination):
                self.direction = "up"

                while(self.currentFloor < destination):
                    self.currentFloor += 1
                    screenDisplay = self.currentFloor
                
            elif(self.currentFloor > destination):
                self.direction = "down"

                while self.currentFloor > destination:
                    self.currentFloor -= 1
                    screenDisplay = self.currentFloor
                
            
            self.status = "stopped"
            self.floorRequestList.pop()

            
        self.status = "idle"
        
    def sortFloorList(self):
        if (self.direction == "up"):
            self.floorRequestList.sort()
        else: 
            self.floorRequestList.sort(reverse = True)
            

    def operateDoors(self):
        #self.door = Door()
        self.door.status = "opened"
    
#----------------------------ELEVATOR----------------------------#      

#----------------------------CALL BUTTON----------------------------#

class CallButton:
    def __init__(self, _id, _floor, _direction):
        self.ID = _id
        self.floor = _floor
        self.direction = _direction
        self.status = ""

#----------------------------CALL BUTTON----------------------------#

#----------------------------FLOOR REQUEST BUTTON----------------------------#

class FloorRequestButton:
    def __init__(self, _id, _floor):
        self.ID = _id
        self.floor = _floor
        self.status = ""

#----------------------------FLOOR REQUEST BUTTON----------------------------#

#----------------------------DOOR----------------------------#

class Door:
    def __init__(self, _id):
        self.ID = _id
        self.status = ""

#----------------------------DOOR----------------------------#

##module.exports = { Column, Elevator, CallButton, FloorRequestButton, Door }