import pygame
import socket




class Main():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = socket.gethostname()
        print("Remote IP address: ", self.address)
        print(self.s.connect(("192.168.4.1", 6500))) # Type your ESP Server details here

        
        pygame.init()
        self.res = (200,200)
        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption("PBL11 Violet Control Pad")
        self.done = False

        self.clock = pygame.time.Clock()

        self.loop()

        pygame.quit();

    def loop(self):
        while not self.done:
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    self.done = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.done = True
                    for i in range(1, 127):
                        if event.key == i:
                            print("Pressed Key")
                            self.s.sendall(bytes([i]))
                            if i in range(49, 57, 1):
                                self.s.sendall(bytes([116])) # Send keypress through to esp

                # Advanced key-up functionality:
                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_w) or (event.key == pygame.K_s):
                        print("Unpressed Key")
                        self.s.sendall(bytes([120])) # turn off motors


            self.clock.tick(30);
                        

# For more advanced control, think about this function:
def output(socket, info):

    print("sending output")

    # Send through lots of bytes at once
    socket.sendall(bytes([142, info[0], info[1], info[2], info[3], info[4], info[5], 10]))

    # See the bytes just sent in python terminal
    print(bytes([142, info[0], info[1], info[2], info[3], info[4], info[5], 10]))
    
    print("end output")



mainn = Main()

