from Tolkenizer import *
import re

class Parser:
    tolk = Tolkenizer()
    abriu = False
    def filtra(linha:str):
        return linha.split('#')[0].strip()

    def leitura(nome:str):
        with open(nome) as f:
            contents=''
            for line in f:
                contents += Parser.filtra(line)+'\n'

        return contents

    def parseBlock():
        filhos = []
        Parser.tolk.selectNext()
        while Parser.tolk.next.type != 'EOF':
            filhos.append(Parser.parseStatment())
            Parser.tolk.selectNext()
        return Block('',filhos)
        
    def parseStatment():

        if Parser.tolk.next.type == 'sta':
            Parser.tolk.selectNext()
            valor = Parser.tolk.next.value
            Parser.tolk.selectNext()
            if Parser.tolk.next.type == 'virgula':
                Parser.tolk.selectNext()
                filho = Parser.parseRelExpr()
                return Assigment('',[Identifier(valor,[]),filho])
     
        elif Parser.tolk.next.type == 'function':
            Parser.tolk.selectNext()
            nome_func = Parser.tolk.next.value
            Parser.tolk.selectNext()
            args = []
            if Parser.tolk.next.type == 'virgula':
                Parser.tolk.selectNext()
                while Parser.tolk.next.type != 'break':
                    nome=Parser.tolk.next.value
                    Parser.tolk.selectNext()
                    if Parser.tolk.next.type == 'virgula':
                        Parser.tolk.selectNext()
                    args.append(Createvar("Int", [Identifier(nome,[])]))

                    if Parser.tolk.next.type == "break":
                        Parser.tolk.selectNext()
                        filhos = []
                        while Parser.tolk.next.type != 'end':
                            filhos.append(Parser.parseStatment())
                            Parser.tolk.selectNext()
                            if (Parser.tolk.next.type == 'EOF'):
                                raise('FIM DE ARQUIVO INESPERADO')
                        Parser.tolk.selectNext()
                        return FuncDec("Int",[Identifier(nome_func,[])]+ args +[Block('',filhos)])

        elif Parser.tolk.next.type == 'jump':
            Parser.tolk.selectNext()
            nome_func = Parser.tolk.next.value
            Parser.tolk.selectNext()
            args = []
            if Parser.tolk.next.type == 'virgula':
                Parser.tolk.selectNext()
                while Parser.tolk.next.type != 'break':
                    args.append(Parser.parseRelExpr())
                    # Parser.tolk.selectNext()
                    if Parser.tolk.next.type == 'virgula':
                        Parser.tolk.selectNext()
            return FuncCall(nome_func,args)
        
        
        elif Parser.tolk.next.type == 'print':
            Parser.tolk.selectNext()
            filho = Parser.parseFactor()
            return Println('',[filho])
        
        elif Parser.tolk.next.type == 'read':
            Parser.tolk.selectNext()
            valor = Parser.tolk.next.value
            Parser.tolk.selectNext()
            return Assigment('',[Identifier(valor,[]),Readln('',[])])

        
        elif Parser.tolk.next.type == 'if':
            Parser.tolk.selectNext()
            condicao = Parser.parseRelExpr()
            Parser.tolk.selectNext()
            filhos = []
            linha = False
            status = True
            while status:
                if Parser.tolk.next.type == 'break':
                    linha = True
                    Parser.tolk.selectNext()
                if linha and (Parser.tolk.next.type == 'end' or Parser.tolk.next.type == 'else'):
                    status = False
                if status:
                    filhos.append(Parser.parseStatment())
            filho1= Block('',filhos)
            if Parser.tolk.next.type == 'else':
                Parser.tolk.selectNext()
                if Parser.tolk.next.type == 'break':
                    Parser.tolk.selectNext()
                    filhos2 = []
                    while Parser.tolk.next.type != 'end':
                        filhos2.append(Parser.parseStatment())  
                        Parser.tolk.selectNext()             
                    if Parser.tolk.next.type == 'end':
                        Parser.tolk.selectNext()    
                        filho2= Block('',filhos2)         
                        return IfOp('',[condicao,filho1,filho2])                
                    else:
                        raise Exception('Algo de estranho aconteceu, confira a entrada')
            else:
                return IfOp('',[condicao,filho1])

        elif Parser.tolk.next.type == 'while':
            Parser.tolk.selectNext()
            condicao = Parser.parseRelExpr()
            Parser.tolk.selectNext()
            filhos = []
            while Parser.tolk.next.type != 'end':
                filhos.append(Parser.parseStatment())
                Parser.tolk.selectNext()
                if (Parser.tolk.next.type == 'EOF'):
                    raise('FIM DE ARQUIVO INESPERADO')
            filho1= Block('',filhos)
            return WhileOp('',[condicao,filho1])    
        
        elif Parser.tolk.next.type == 'break':
            return NoOp('',[])
        
        else:
            raise Exception("sla deu merda",Parser.tolk.next.type,Parser.tolk.next.value)
    
    
    def parseRelExpr():
        filho1 = Parser.parseExepresion()
        while True:               
            if (Parser.tolk.next.type == 'comp') or (Parser.tolk.next.type == 'maior') or (Parser.tolk.next.type == 'menor'):
                tipo = Parser.tolk.next.type
                Parser.tolk.selectNext() 
                filho2 =Parser.parseExepresion()
                atual  =Binop (tipo,[filho1,filho2])

            elif (Parser.tolk.next.type in ['EOF','break','virgula']) or ((Parser.tolk.next.type == 'C_par')and(Parser.abriu)):
                atual=filho1
                break     
            else:
                    raise Exception(Parser.tolk.next.type,Parser.tolk.next.value)
            filho1 = atual
        return atual
        
    def parseExepresion():
        filho1 = Parser.parseTerm()
        while True:   
            if (Parser.tolk.next.type == 'plus') or (Parser.tolk.next.type == 'minus') or (Parser.tolk.next.type == 'or') or (Parser.tolk.next.type == 'concat'):
                tipo = Parser.tolk.next.type
                Parser.tolk.selectNext() 
                filho2 =Parser.parseTerm()
                atual  =Binop (tipo,[filho1,filho2])

            else:
                atual = filho1
                break
            filho1 = atual
            filho1 = atual
        return atual

    def parseTerm():
        filho1 = Parser.parseFactor()
        while True:
            if (Parser.tolk.next.type == 'div') or (Parser.tolk.next.type == 'times') or (Parser.tolk.next.type == 'and'):
                tipo = Parser.tolk.next.type
                Parser.tolk.selectNext() 
                filho2 =Parser.parseFactor()
                atual  =Binop (tipo,[filho1,filho2])    
            else:
                atual = filho1
                break
            filho1 = atual
        return atual

    def parseFactor():
        if Parser.tolk.next.type == 'int':
            ret = Intvar(int(Parser.tolk.next.value),[]) 
            Parser.tolk.selectNext()
            return ret
        elif Parser.tolk.next.type == 'string':
            ret = Stringvar(Parser.tolk.next.value,[])
            Parser.tolk.selectNext()
            return ret
        elif Parser.tolk.next.type == 'var':
            # return Identifier(Parser.tolk.next.value,[])
            nome = Parser.tolk.next.value
            filhos  = []
            Parser.tolk.selectNext()
            if Parser.tolk.next.type == 'O_par':
                Parser.abriu =True
                Parser.tolk.selectNext()
                filhos.append(Parser.parseRelExpr())
                while Parser.tolk.next.type != 'C_par':
                    Parser.tolk.selectNext()
                    filhos.append(Parser.parseRelExpr())
                Parser.tolk.selectNext()
                return FuncCall(nome,filhos)
            else:
                return Identifier(nome,[])

        elif (Parser.tolk.next.type == 'minus') or (Parser.tolk.next.type == 'plus') or (Parser.tolk.next.type == 'not'):
            tipo = Parser.tolk.next.type
            Parser.tolk.selectNext()
            return UnOp(tipo, [Parser.parseFactor()])
        elif  Parser.tolk.next.type == 'O_par':
                Parser.abriu =True
                Parser.tolk.selectNext()
                salva = Parser.parseRelExpr()
                if (Parser.tolk.next.type == 'C_par'):
                    Parser.tolk.selectNext()
                    return salva
                else:
                    raise Exception("s",Parser.tolk.next.type,Parser.tolk.next.value)
  
    def run(self, s):
        ss = Parser.leitura(s)
        l = Parser.filtra(ss)
        Parser.tolk.cria(l)
        return Parser.parseBlock()