import pyparsing as pp
class Examiner:
    def __init__(self):
        pass

    def ParseCondition(self, cond):
        cond = self.ParseCondition(cond)
        newCondition=cond[:]
        operator = pp.Regex(">=|<=|!=|>|<|=").setName("operator")
        number = pp.Regex(r"[0-9,a-z,\-,\_]*")
        condition = pp.Group(number + operator + number)
        condition2 = pp.Group(number + operator + number + operator + number)
        expr = pp.operatorPrecedence(condition2|condition, [
            ("and", 2, pp.opAssoc.LEFT,),
            ("or", 2, pp.opAssoc.LEFT,),
        ])
        return expr.parseString(newCondition)[0]

