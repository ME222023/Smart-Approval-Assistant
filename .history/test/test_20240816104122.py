# import configparser

# config = configparser.ConfigParser()

# config.read("/home/hezp1/AI/app_weichat/config.ini")

# print(config.sections())
# print(config.get("server", "admin_list"))

import sys
sys.path.append("/home/hezp1/AI/app_weichat")

from utils.config import Config
from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput

def main():
    graphviz = GraphvizOutput()
    graphviz.output_file = 'basicdemo.png'

    with PyCallGraph(output=graphviz):
        aa= Demo("小仔","男","18")
        aa.who()

if __name__ == '__main__':
    main()
