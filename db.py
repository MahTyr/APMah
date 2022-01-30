from collections import defaultdict


class ISDU:
    def insert(self, inp):
        inp[2] = inp[2].lower()
        try:
            if inp[1] != 'INTO' or inp[3] != 'VALUES' or inp[-1][-1] != ';':
                return 'INVALID SYNTAX FOR INSERT COMMAND!'
            if inp[2] not in self.tables:
                return 'TABLE NOT EXISTS!'
            vals = inp[-1][1:-2].split(',')
            if len(vals) != len(self.tables[inp[2]].keys()):
                return 'UNEXPECTED COUNT OF VALUES!'
            with open(inp[2] + '.txt', 'a') as table:
                db = self.read_db(inp[2])
                columns = db[0].split()
                uniques = {columns.index(k) for k, v in self.tables[inp[2]].items() if v[1]}
                for data in db[1:]:
                    data = data.split()
                    for u in uniques:
                        if vals[u] == data[u]:
                            return 'DATA IS NOT UNIQUE!'
                table.write(' '.join(vals) + '\n')
                self.indexes[inp[2]] += 1
                return 'INSERT SUCCESSFUL!'
        except:
            return 'INVALID COMMAND!'

    def select(self, inp):
        inp[2] = inp[2].lower()
        inp = [i.replace('(', '').replace(')', '').replace('"', '') for i in inp]
        try:
            if inp[1] != 'FROM' or inp[3] != 'WHERE' or inp[-1][-1] != ';':
                return 'INVALID SYNTAX FOR SELECT COMMAND!'
            ifs = inp[4:]
            ifs[-1] = ifs[-1][:-1]
            l = []
            ll = []
            for i in ifs:
                if '==' in i:
                    x = i.split('==')
                    l.append(x)
                    l[-1].append('==')
                elif '!=' in i:
                    x = i.split('!=')
                    l.append(x)
                    l[-1].append('!=')
                else:
                    ll.append(i)
            db = self.read_db(inp[2])
            columns = db[0].split()
            new_file_string = ""
            map_column_index = {k: columns.index(k) for k, v in self.tables[inp[2]].items()}
            sel_count = 0
            with open(inp[2] + '.txt', 'r') as table:
                for dta in db[1:]:
                    data = dta.split()
                    out = []
                    for st in l:
                        if (data[map_column_index[st[0]]] == st[1] and st[2] == '==') or (
                                data[map_column_index[st[0]]] != st[1] and st[2] == '!='):
                            out.append(True)
                        else:
                            out.append(False)
                    res = out[0]
                    j = 1
                    for op in ll:
                        if op == 'OR':
                            res = res or out[j]
                        elif op == 'AND':
                            res = res and out[j]
                        else:
                            return 'INVALID COMMAND!'
                        j += 1
                    if res:
                        new_file_string += (dta + '\n')
                        sel_count += 1
                return f'SELECT RETURN {sel_count} ROWS!\n' + new_file_string
        except:
            return 'INVALID COMMAND!'

    def delete(self, inp):
        inp[2] = inp[2].lower()
        inp = [i.replace('(', '').replace(')', '').replace('"', '') for i in inp]
        try:
            if inp[1] != 'FROM' or inp[3] != 'WHERE' or inp[-1][-1] != ';':
                return 'INVALID SYNTAX FOR DELETE COMMAND!'
            ifs = inp[4:]
            ifs[-1] = ifs[-1][:-1]
            l = []
            ll = []
            for i in ifs:
                if '==' in i:
                    x = i.split('==')
                    l.append(x)
                    l[-1].append('==')
                elif '!=' in i:
                    x = i.split('!=')
                    l.append(x)
                    l[-1].append('!=')
                else:
                    ll.append(i)
            db = self.read_db(inp[2])
            columns = db[0].split()
            new_file_string = db[0] + '\n'
            map_column_index = {k: columns.index(k) for k, v in self.tables[inp[2]].items()}
            del_count = 0
            with open(inp[2] + '.txt', 'w') as table:
                for dta in db[1:]:
                    data = dta.split()
                    out = []
                    for st in l:
                        if (data[map_column_index[st[0]]] == st[1] and st[2] == '==') or (
                                data[map_column_index[st[0]]] != st[1] and st[2] == '!='):
                            out.append(True)
                        else:
                            out.append(False)
                    res = out[0]
                    j = 1
                    for op in ll:
                        if op == 'OR':
                            res = res or out[j]
                        elif op == 'AND':
                            res = res and out[j]
                        else:
                            return 'INVALID COMMAND!'
                        j += 1
                    if not res:
                        new_file_string += (dta + '\n')
                    else:
                        del_count += 1
                table.write(new_file_string)
                return f'DELETE {del_count} ROWS SUCCESSFUL!'
        except:
            return 'INVALID COMMAND!'

    def update(self, inp):
        inp[1] = inp[1].lower()
        inp = [i.replace('(', '').replace(')', '').replace('"', '') for i in inp]
        try:
            if inp[-2] != 'VALUES' or inp[2] != 'WHERE' or inp[-1][-1] != ';':
                return 'INVALID SYNTAX FOR UPDATE COMMAND!'
            ifs = inp[3:-2]
            new_vals = ' '.join(inp[-1][:-1].split(','))
            l = []
            ll = []
            for i in ifs:
                if '==' in i:
                    x = i.split('==')
                    l.append(x)
                    l[-1].append('==')
                elif '!=' in i:
                    x = i.split('!=')
                    l.append(x)
                    l[-1].append('!=')
                else:
                    ll.append(i)
            db = self.read_db(inp[1])
            columns = db[0].split()
            new_file_string = db[0] + '\n'
            map_column_index = {k: columns.index(k) for k, v in self.tables[inp[1]].items()}
            up_count = 0
            with open(inp[1] + '.txt', 'w') as table:
                for dta in db[1:]:
                    data = dta.split()
                    out = []
                    for st in l:
                        if (data[map_column_index[st[0]]] == st[1] and st[2] == '==') or (
                                data[map_column_index[st[0]]] != st[1] and st[2] == '!='):
                            out.append(True)
                        else:
                            out.append(False)
                    res = out[0]
                    j = 1
                    for op in ll:
                        if op == 'OR':
                            res = res or out[j]
                        elif op == 'AND':
                            res = res and out[j]
                        else:
                            return 'INVALID COMMAND!'
                        j += 1
                    if res:
                        new_file_string += (new_vals + '\n')
                        up_count += 1
                    else:
                        new_file_string += (dta + '\n')
                table.write(new_file_string)
                return f'UPDATE {up_count} ROWS SUCCESSFUL!'
        except:
            return 'INVALID COMMAND!'


class DB(ISDU):
    def __init__(self):
        self.tables = defaultdict(dict)
        self.read_schema()
        self.indexes = self.set_index()

    def set_index(self):
        return {k: 1 for k in self.tables.keys()}

    @staticmethod
    def read_db(table):
        with open(table + '.txt', 'r') as tb:
            return tb.read().splitlines()

    def read_schema(self):
        with open('schema.txt', 'r') as schema:
            schema_lines = schema.read().splitlines()
            idx = 0
            while idx < len(schema_lines):
                tb_name = schema_lines[idx].lower()
                idx += 1
                while idx < len(schema_lines) and schema_lines[idx] != '':
                    line = [l.lower() for l in schema_lines[idx].split()]
                    self.tables[tb_name][line[0]] = (line[2], True) if len(line) == 3 else (line[1], False)
                    idx += 1
                with open(tb_name + '.txt', 'w') as table:
                    table.write(' '.join(self.tables[tb_name].keys()) + '\n')
                idx += 1

    def run_shell(self):
        while True:
            s = input()
            if s == '':
                continue
            s = s.split()
            if s[0] == "INSERT":
                print(self.insert(s))
            elif s[0] == "SELECT":
                print(self.select(s))
            elif s[0] == "DELETE":
                print(self.delete(s))
            elif s[0] == "UPDATE":
                print(self.update(s))
            elif s[0] == "exit":
                return 'GOOD LUCK!'


if __name__ == '__main__':
    db = DB()
    db.run_shell()
