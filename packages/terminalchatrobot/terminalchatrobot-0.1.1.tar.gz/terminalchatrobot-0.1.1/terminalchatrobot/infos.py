# 输入输出各种颜色的字体
from colors import color_msg

def printinfos():
    infos = '''
   .______            ______     .______       ______     .___________. 
    |   _  \         /  __  \    |   _  \     /  __  \    |           | 
    |  |_)  |       |  |  |  |   |  |_)  |   |  |  |  |   `---|  |----` 
    |      /        |  |  |  |   |   _  <    |  |  |  |       |  |      
    |  |\  \----.   |  `--'  |   |  |_)  |   |  `--'  |       |  |      
    | _| `._____|    \______/    |______/     \______/        |__|      


                        ---- 👽   A chat-robot which runs in terminal
    @author Encounter (me@xingbofeng.com)
                                    last_update 2017-05-23 03:10

                                    '''
                                    
    print(color_msg('blue', infos))
