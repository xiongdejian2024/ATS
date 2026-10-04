import json

class Ccp_get:
    def __init__(self):
        self.f = open('ccp.json', 'r', encoding='utf-8')
        self.content = self.f.read()
        self.a = json.loads(self.content)
        self.ccp_dict = {}
        self.ccp_list = []

    def run(self):
        for i in range (1558):
            #print(a[i]["待写入CCP值"].split('=')[0],end='')
            self.ccp_dict[i]= self.a[i]["待写入CCP值"]
            self.ccp_list.append(self.ccp_dict[i])

        str = "".join(self.ccp_list)
        self.f.close()
        print(str)
        return str

if __name__ == '__main__':
    example = Ccp_Get()
    example.run()