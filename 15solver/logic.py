class Sector(list):
    def __contains__(self, item):
        if len(self) == 0: return False
        try:
            return min(self) <= item <= max(self)
        except Exception:
            return False
    def size(self)->int:
        if len(self) == 0: return 0
        return max(self) - min(self)
    def cnt(self, step:float=1):
        if step <= 0: return 0
        return (max(self) - min(self) + 1)//step

class Solver:
    def __init__(self):
        self.eps:float = 0.001
        self.exp:str = ""
        self.sectors_in_exp: list[str] = list()
        self.running_variable:str = ""

    def getSectorNames(self)->list[str]: return self.sectors_in_exp
    
    def setExp(self, exp:str)->None:
        self.exp, running_variables, self.sectors_in_exp = self._get_correct_exp(exp)
        if len(running_variables) != 1: raise ValueError("Фигню а не выражение вы подали, господа")
        self.running_variable = running_variables[0]



    def solve(self, sector_variables:dict[str, Sector])->Sector:
        self.sector_variables = sector_variables
        self.possible_values, self.possible_borders_values = self._get_all_values()
        self.running_sector:str = self._get_running_sector()
        self.bad_values:list[float|int] = self._get_bad_values()

        mn_ind = self.bad_values[0][0]
        mx_ind = self.bad_values[-1][0]

        self.left_borders = list(set( self.possible_values[x] for x in range(max(0, mn_ind - 1), min(len(self.possible_values), mn_ind + 2))))
        self.right_borders = list(set( self.possible_values[x] for x in range(max(0, mx_ind - 1), min(len(self.possible_values), mx_ind + 2))))

        ans = self._minimize_sect()
        return ans

    def _get_correct_exp(self,exp)->tuple[str, list[str], list[str]]:
        ops_to_change = {'^': "and", "|": "or", "||": "or", "&": "and", "&&": "and", "->": "<=", "~": "not"}
        ops = ["and", "or", "not", "<=", "==", "!=", "in", "(", ")"]
        new_exp = exp
        for op, correct_op in ops_to_change.items():
            new_exp = new_exp.replace(op, correct_op)
        for op in ops:
            new_exp = new_exp.replace(op, f" {op} ")
        variables = [x for x in new_exp.split() if x not in ops and x]
        sector_variables = [x for x in variables if any(l.isupper() for l in x)]
        running_variables = [x for x in variables if x.islower()]
        return new_exp, sorted(set(running_variables)), sorted(set(sector_variables))
    
    def _get_all_values(self)->tuple[list[float], list[float]]:
        line = []
        line_for_borders = []
        for sector in self.sector_variables.values():
            for num in sector:
                line += [num - 1, num - self.eps, num, num + self.eps, num + 1]
                line_for_borders += [num]
        return sorted(set(line)), sorted(set(line_for_borders))

    def _get_running_sector(self)->str:
        names = []
        for sect_name in self.sectors_in_exp:
            if sect_name not in self.sector_variables:
                names.append(sect_name)
        if len(names) != 1: raise ValueError("Фигню а не выражение вы подали, господа")
        return names[0]
    
    def _check_num(self, running_variables:dict[str, int|float], sector_variables:dict[str, Sector])->bool:
        new_exp = self.exp
        for var, val in running_variables.items():
            new_exp = new_exp.replace(var, str(val))
        for var in sector_variables.keys():
            new_exp = new_exp.replace(var, f"sector_variables['{var}']")
        #print(new_exp, sector_variables)
        ans = False
        try:
            ans = eval(new_exp)
        except Exception as e:
            print(e)
        return ans
    
    def _get_bad_values(self)->list[float|int]:#чек всех x
        sector_variables = self.sector_variables
        sector_variables[self.running_sector] = Sector([min(self.possible_values), min(self.possible_values)])#impossible_sector
        not_in_sect: list[list[int, float]] = []
        for i, val in enumerate(self.possible_values):
            if not self._check_num(running_variables={self.running_variable:val}, sector_variables=sector_variables):
                not_in_sect.append([i, val])
        return not_in_sect

    def _check_sect(self, sect:Sector)->bool:
        try:
            if sect[0] not in self.possible_borders_values or sect[1] not in self.possible_borders_values:
                return False
        except Exception as e:
            print(e)
            return False
        sector_variables = self.sector_variables
        sector_variables[self.running_sector] = sect
        return all(self._check_num(running_variables={self.running_variable: val}, sector_variables=sector_variables) for val in self.possible_values)

    def _minimize_sect(self)->Sector:
        sectors = []
        for l in self.left_borders:
            for r in self.right_borders:
                sector = Sector([l, r])
                if self._check_sect(sector):
                    sectors.append(sector)
        sectors = sorted(sectors, key = lambda x: x.size())
        if len(sectors) == 0: raise RuntimeError("Произошла какая-то хрень в поиске минимального отрезка")
        return sectors[0]


# A = Sector([4,10])
# B = Sector([11, 15])
# C = Sector([13, 16])
# exp = "( x in A ) or ( x in B and x in C )"#input()
# print(eval(exp.replace("x", "14")))

s = Solver()
exp = "(x in D) -> ( ( (not (x in C)) and (not (x in A)) ) -> (not (x in D)))"
s.setExp(exp)
sectors = {"D": Sector([17, 58]),
           "C":Sector([29, 80])}
print(s.solve(sectors))