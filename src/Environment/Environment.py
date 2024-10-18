VariableNotFoundError = {"Error" : "1"}

class Environment:
    def __init__(self, Parent = None):
        self.Variables: dict = {}
        self.Parent = Parent



    def DecVar(self, VarName: str, Info : dict):
        self.Variables[VarName] = Info
    
    def GetVar(self, VarName: str) -> dict:
        if(VarName in list(self.Variables.keys())):
            return self.Variables[VarName]
        else:
            if(self.Parent == None):
                return VariableNotFoundError
            else:
                return self.Parent.GetVar(VarName)
            