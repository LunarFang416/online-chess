pygame.init()

ScreenWidth=800
ScreenHeight=800

screen=pygame.display.set_mode((ScreenWidth,ScreenHeight))
blackorWhite=[]

class Square:
    def __init__(self,xpos,ypos,length):

        self.x=xpos
        self.y=ypos
        self.grid=length
        isWhite=1;

    def initialize(self,x,y,is_white):

            grid_width=ScreenWidth/8
            grid_height=ScreenHeight/8

            x_coordinate=x*grid_width
            y_coordinate=y*grid_height

            return (x_coordinate,y_coordinate)
    
    def createBoard(self):
        board=[]
        isWhite=1;
        for y in range(8):
            row=[]
            for x in range(8):
                row.append(self.initialize(x,y,isWhite))
                isWhite*=-1
                if(isWhite==1):
                    blackorWhite.append(0)
                else:
                    blackorWhite.append(1)
            board.append(row)


            


    def boardGUI(self):
        color=(255,255,255)
        grid=int (ScreenWidth/8)
        print(grid)
        counter=0
        isWhite=1
        for i in range(8):

            for j in range(8):

                if(isWhite==1):
                    color=(255,255,255)
                else :
                    color=(0,0,0)

                print(i*grid,j*grid,grid,grid,color)
                    
                isWhite*=-1
                pygame.draw.rect(screen,color,pygame.Rect(i*grid,j*grid,grid,grid))
                
                pygame.display.flip()


                pygame.display.update()
            isWhite*=-1


pygame.time.delay(2)
b=Square(0,0,100)
print(b.createBoard())
print(b.boardGUI())
#pygame.quit()

