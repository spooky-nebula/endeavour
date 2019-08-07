import pygame as pg
import math

pg.init()

# Screen variables
width   = 1280
height  = 720
grassh  = 80
scale_f = 5

# Physics constants
g   = 9.80665
rho = 1.225

# Rocket constants
mflow   = 50
isp     = 310
v_exh   = isp * g
thrust  = mflow * v_exh
m_dry   = 10000
m_prop  = 1000
cd      = 0.03
S       = math.pi * 1.5 ** 2

# Rocket variables
vely    = 0
y       = 0
alpha   = 0 # TO BE USED FOR ROTATION

# Set up screen
res     = (width,height)
screen  = pg.display.set_mode(res)
scrrect = screen.get_rect()

# Set up screen font
pg.font.init()
myfont = pg.font.SysFont('Arial',14)

# Set up colours
col_grass   = (34,139,34)
col_sky     = (0,191,255)

# Set up rocket
rocket      = pg.image.load('testrocketsprite.png')
rocket = pg.transform.scale(rocket,(int(3*scale_f),int(3/11*52*scale_f)))
rocketrect  = rocket.get_rect()
thrusting   = False

# Set up time variables
tlast = 0.001*pg.time.get_ticks()

running = True

while running:
    dt = 0.001*pg.time.get_ticks() - tlast
    tlast = 0.001*pg.time.get_ticks()
    
    # Handling input events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
            thrusting = True
        elif event.type == pg.KEYUP and event.key == pg.K_UP:
            thrusting = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
            gimbalright = True
        elif event.type == pg.KEYUP and event.key == pg.K_RIGHT:
            gimbalright = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
            gimballeft = True # TO BE USED FOR ROTATION
        elif event.type == pg.KEYUP and event.key == pg.K_LEFT:
            gimballeft = False # TO BE USED FOR ROTATION
    
    # Physics:
    #   TODO:
    #       ROTATION:
    #           - CoM
    #           - MoI
    #           - Thrust vectoring
    #           - Moments around CoM
    #       REALISM:
    #           - Thrust fluctuations
    #           - Drag curves (i.e. drag divergence)
    #       VISUAL:
    #           - Thrust
    #           - Mach effects
    #           - Crash (explosion based on amount of fuel)



    
    # Ground collision
    if y < 0:
        y = 0
        vely = -0.3*vely

    # Thrust
    if thrusting and m_prop > 0:
        F_T = thrust
        m_prop = m_prop - mflow * dt
    else:
        F_T = 0

    # Gravity
    m_wet = m_prop + m_dry
    F_g = m_wet * g

    # Drag
    Q = 0.5 * rho * vely ** 2
    F_d = cd * Q * S

    # Numerical integration
    acc = (F_T - F_g - F_d) / m_wet
    vely = vely + acc * dt
    y = y + vely * dt

    # Converting physics coordinates to screen coordinates
    ypx = height - grassh - int(y * scale_f)
    
    # Drawing sky and ground
    pg.draw.rect(screen,col_sky,scrrect)
    pg.draw.rect(screen,col_grass,((0,height-grassh),(width,grassh)))

    # Drawing rocket
    rocketrect.midbottom = (int(width/2),ypx)
    screen.blit(rocket,rocketrect)

    # Displaying velocity & fuel qt
    veltext = myfont.render('V='+str(round(vely,1))+'m/s',False,(0,0,0))
    fueltext = myfont.render('FUEL='+str(round(m_prop,1))+'kg',False,(0,0,0))
    screen.blit(veltext,(0,0))
    screen.blit(fueltext,(0,18))
    
    
    
    
    # Displaying frame
    pg.display.flip()


pg.quit()
