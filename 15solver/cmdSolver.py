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

        
A = Sector([4,10])
B = Sector([11, 15])
C = Sector([13, 16])
exp = "( x in A ) or ( x in B and x in C )"#input()
print(eval(exp.replace("x", "14")))

class Solver:
    def __init__(self, exp:str, sector_variables:dict[str, Sector]):
        self.eps = 0.001
        self.sector_variables = sector_variables
        self.exp, running_variables, self.sectors_in_exp = self._get_correct_exp(exp)
        if len(running_variables) != 1: raise ValueError("Фигню а не выражение вы подали, господа")
        self.running_variable:str = running_variables[0]
        
        self.possible_values:list[float|int] = self._get_all_values(sector_variables)
        self.running_sector:str = self._get_running_sector()
        self.bad_values:list[float|int] = self._get_bad_values()

        mn_ind = self.bad_values[0][0]
        mx_ind = self.bad_values[-1][0]

        self.left_border = list(set( self.possible_values[x] for x in range(max(0, mn_ind - 1), min(len(self.possible_values, mn_ind + 2)))))
        self.right_border = list(set( self.possible_values[x] for x in range(max(0, mx_ind - 1), min(len(self.possible_values, mx_ind + 2)))))


    def _get_correct_exp(self,exp)->tuple[str, list, list]:
        ops = ["and", "or", "not", "<=", "==", "!=", "in", "(", ")"]
        new_exp = exp
        for op in ops:
            new_exp = new_exp.replace(op, f" {op} ")
        variables = [x for x in new_exp.split() if x not in ops and x]
        sector_variables = [x for x in variables if any(l.isupper() for l in x)]
        running_variables = [x for x in variables if x.islower()]
        return new_exp, sorted(set(running_variables)), sorted(set(sector_variables))
    
    def _get_all_values(self)->list[float]:
        line = []
        for sector in self.sector_variables.values():
            for num in sector:
                line += [num - 1, num - self.eps, num, num + self.eps, num + 1]
        return sorted(set(line))

    def _get_running_sector(self)->str:
        names = []
        for sect_name in self.sectors_in_exp:
            if sect_name not in self.sector_variables:
                names.append(sect_name)
        if len(names) != 1: raise ValueError("Фигню а не выражение вы подали, господа")
        return names[0]
    
    def _check_num(self, running_variables:dict[str, int|float])->bool:
        new_exp = self.exp
        for var, val in running_variables.items():
            new_exp = new_exp.replace(var, str(val))
        for var in self.sector_variables.keys():
            new_exp = new_exp.replace(var, f"sector_variables['{var}']")
        
        ans = eval(new_exp)
        return ans
    
    def _get_bad_values(self)->list[float|int]:#чек всех x
        sector_variables = self.sector_variables
        sector_variables[self.running_sector] = Sector([min(self.possible_values), min(self.possible_values)])#impossible_sector
        not_in_sect: list[list[int, float]] = []
        for i, val in enumerate(self.possible_values):
            if not self._check_num(running_variables={self.running_variable:val}):
                not_in_sect.append([i, val])
        return not_in_sect

    def minimize_sect(self)->Sector:
        pass


def solve(exp:str, sector_variables:dict[str, Sector])->Sector:
    pass

#Ещё совсем не доделано