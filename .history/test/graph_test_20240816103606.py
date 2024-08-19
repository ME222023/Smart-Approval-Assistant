### 绘制流程图
from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput
from pycallgraph2 import Config

class Demo():
    def __init__(self,name,gender,age):
        self.name = name
        self.age = age
        self.gender = gender

    def what_name(self):
        return self.name

    def what_gender(self):
        return self.gender

    def what_age(self):
        return self.age

    def who(self):
        name = self.what_name()
        gender = self.what_gender()
        age = self.what_age()


def main():
    graphviz = GraphvizOutput()
    graphviz.output_file = 'basicdemo.png'

    with PyCallGraph(output=graphviz):
        aa= Demo("小仔","男","18")
        aa.who()

if __name__ == '__main__':
    main()