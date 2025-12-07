class foo:
    def __init__(self):
        self.aaa="hats"
    def __str__(self):
        return "hats"
    
f=foo()
fee={"hats":{"hi","hello"}}
fii={"hearts":{"hi","hello"}}
ththth=[fee,fii]

for page in ththth:
    if f.aaa in page.keys():
        if('hello' in page[f.aaa]):
            print("gg")
        else:
            print("no")