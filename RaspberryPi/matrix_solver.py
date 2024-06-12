from main_controller import Calculator


class MatrixSolver(Calculator):
    def __init__(self,matA,matB,matC,matD,matE):
        super().__init__()
        self.matA = matA
        self.matB = matB
        self.matC = matC
        self.matD = matD
        self.matE = matE
        self.result = ""
        self.showing_exp = "|"
        self.pointer = 0

    def linear_solver(self,matA,matB,matC,matD,matE,result):
        self.matA = matA
        self.matB = matB
        self.matC = matC
        self.matD = matD
        self.matE = matE
        if matA in result:
            result = result.replace(matA, self.matA)
        if matB in result:
            result = result.replace(matB, self.matB)
        if matC in result:
            result = result.replace(matC, self.matC)
        if matD in result:
            result = result.replace(matD, self.matD)
        if matE in result:
            result = result.replace(matE, self.matE)
        result = eval(result)
        return result



        

    def user_input(self, key):
        if key == "AC":
            self.result = ""
            self.showing_exp = "|"
            self.pointer = 0
        elif key == "DEL":
            if len(self.result) > 0:
                self.result = self.result[:self.pointer-1] + self.result[self.pointer:]
                self.pointer -= 1
                self.convert_to_understandable()
                return
            else:
                self.result = ""
                self.showing_exp = "|"
                self.pointer = 0
        elif key == "=":
            if not self.degrees:
                for key in self.mappings_for_degrees.keys():
                    self.result = self.result.replace(key, self.mappings_for_degrees[key])
            else:
                for key in self.mappings.keys():
                    self.result = self.result.replace(key, self.mappings[key])
            
            open_brackets = self.result.count("(")
            close_brackets = self.result.count(")")
            if open_brackets > close_brackets:
                self.result += ")" * (open_brackets - close_brackets)
            if self.result == "":
                self.showing_exp = "|"
                return
            indicator = self.result[:self.pointer]+"|"+self.result[self.pointer:]
            try:
                self.result = str(self.safe_eval(self.result))
            except ZeroDivisionError:
                self.result = "Can not divide by zero"
            except SyntaxError:
                self.result = "Syntax error"
            except:
                self.result = "Error"
            
        elif key == "left":
            if self.pointer > 0:
                self.pointer -= 1
            if self.pointer == 0:
                self.pointer = len(self.result)
            self.convert_to_understandable()
            return
        elif key == "right":
            if self.pointer < len(self.result):
                self.pointer += 1
            if self.pointer == len(self.result):
                self.pointer = 0
            self.convert_to_understandable()
            return

        elif key in self.keys:
            if self.pointer !=0 and key in self.functions:
                if self.result[self.pointer-1] not in self.operations:
                    self.result = self.result[:self.pointer] +"*"+ self.keys[key] + self.result[self.pointer:]
                    self.pointer += 2
                    self.convert_to_understandable()
                    return
            self.result = self.result[:self.pointer] + self.keys[key] + self.result[self.pointer:]
            self.pointer += 1
            self.convert_to_understandable()
            return
        else:
            self.convert_to_understandable()
            return
        
    def convert_to_understandable(self):
        return super().convert_to_understandable()
