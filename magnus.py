from visual.controls import *
import random
scene.autoscale=False
scene.width=638
scene.height=768

goal=box(pos=(22,1.25,0),size=(3,2.5,7), opacity=0.5)
floor=box(pos=(0,-0.0005,0),length=100,width=50,height=0.001, color=color.green)
channel=cylinder(pos=(0,10,0), radius=0.3, length=2, axis=(0,0,1), visible=False, opacity=0.5)
luck=sphere(pos=channel.pos, radius=channel.radius, visible=False)
welcome='Welcome to my free-kick simulator. '
print '\n'
print welcome
print '\n'
print 'Created by Rui Marques'
print '\n'
print 'Starting up...Please follow the instructions above'
print '\n'
print 'To zoom, hold both mouse buttons at the same time. To rotate camera, hold righ button.'
c=controls(title='Controls', width=683, height=384, range=100)
reset=toggle(pos=(-30,0), text1='SHOOT', text0='RESET', color=color.red)
cvel=slider(pos=(-30,30), text='Speed', color=color.red, min=0, max=200, value=0)
lvel=button(pos=(-80,40), text='Speed', color=color.red, size=(20,10))
cspin=slider(pos=(-30,-30), text='Spin', size=(50,50), color=color.green, min=0, max=20, value=0)
lspin=button(pos=(-80,-20), text='Spin', color=color.green, size=(20,10))
distance=button(pos=(20,0), text='Distance', size=(50,10))
def fkick():
    chance=False
    cvel.value=0
    cspin.value=0
    reset.value=0
    k=0.006
    t=-1
    g=9.81
    dt=0.01
    c=0.7
    scale=0.03
    scale2=0.5
    shot=False
    shot2=False
    shot3=False
    shot4=False
    print '\n'
    print '1-Select the ball position on the field, by clicking on it.'
    print '\n'
    while shot3==False:
            if scene.mouse.clicked:
                m = scene.mouse.getclick()
                ball=sphere(radius=0.2,make_trail=True, material=materials.earth, pos=m.project(normal=(0,1,0)))
                ball.pos.y+=0.2
                print ball.pos
                shot3=True
    print '2-Reset ball position using directional keys.Confirm ball position by pressing backspace.'
    print 'Ball position settled'
    print '\n'
    while shot4==False:
            if scene.kb.keys:
                s = scene.kb.getkey()
                distance.text=str(mag(vector(ball.pos-goal.pos)))
                if s=='left':
                    ball.pos.z+=-0.2
                if s=='right':
                    ball.pos.z+=0.2
                if s=='up':
                    ball.pos.x+=0.2
                if s=='down':
                    ball.pos.x-=0.2
                if s=='backspace':
                    shot4=True
    scene.center=ball.pos
    ball.vel=vector(1,0,0)
    ball.rot=vector(1,0,0)
    print '3-Select the speed direction with a left click on the target'
    while shot==False:
        if scene.mouse.clicked:
            m = scene.mouse.getclick()
            loc = m.project(normal=(1,0,0), point=(22,0,0))
            mark1=sphere(pos=loc, radius=0.1, color=color.red)
            shot=True
    ball.vel=vector(loc-ball.pos)
    speed=arrow(pos=ball.pos,axis=ball.vel*scale,color=color.red)
    print ball.vel
    print '\n'
    print '4-Select the spin direction (using the right-hand-rule, left click)'
    while shot2==False:
        if scene.mouse.clicked:
            m = scene.mouse.getclick()
            loc2 = m.pos
            mark2=sphere(pos=loc2, radius=0.01, color=color.cyan)
            shot2=True
    ball.rot=vector(loc2-ball.pos)
    rotation=arrow(pos=ball.pos, axis=ball.rot*scale2, color=color.cyan)
    print ball.rot
    print '\n'
    channel.pos=ball.pos
    channel.pos.z-=(channel.length)/2
    channel.pos.y+=2
    luck.pos=channel.pos
    luck.pos.z=ball.pos.z
    channel.visible=True
    luck.visible=True
    n=0
    dn=0.01
    mark3=ring(pos=luck.pos, axis=(0,0,1), radius=channel.radius+0.1, thickness=0.1, color=color.red)
    print '5-Press backspace once again, when the ball is closer to the ring for maximum accuracy.'
    while chance==False:
        rate(100)
        n+=dn
        luck.pos.z=mark3.pos.z+(channel.length/2)*sin(n*(pi))
        if scene.kb.keys:
                s = scene.kb.getkey()
                if s=='backspace':
                    r=(luck.pos.z-mark3.pos.z)/((channel.length)/2)
                    print 'Accuracy: '+str(r)
                    chance=True
    print '\n'
    channel.visible=False
    mark3.visible=False
    luck.visible=False
    ball.vel.x*(random.uniform(1-r,1+r))
    ball.vel.y*(random.uniform(1-r,1+r))
    ball.vel.z*(random.uniform(1-r,1+r))
    ball.rot.x*(random.uniform(1-r,1+r))
    ball.rot.y*(random.uniform(1-r,1+r))
    ball.rot.z*(random.uniform(1-r,1+r))
    r=r/2
    def change1(x):
        ball.vel.mag=(x*1000)/3600*(1+r)
    def change2(x):
        ball.rot.mag=x*2*pi*(1+r)
    print '6-Use the slider to select speed and spin values in km/h and Hz, respectively.'
    print '\n'
    print '7-Click on the toggle switch to shoot. Toggle it again for reset.'
    while reset.value==0:
        lvel.text=str(cvel.value)
        lspin.text=str(cspin.value)
        cvel.action=lambda: change1(cvel.value)
        cspin.action=lambda: change2(cspin.value)
    mark1.visible=False
    mark2.visible=False
    speed.visible=False
    rotation.visible=False
    phi=mag(ball.rot)
    score=False
    print '\n'
    while t<10:
        rate(20)
        scene.center=ball.pos
        t+=dt
        magnus=cross(ball.rot,ball.vel)*k
        ball.vel+=vector(0,-g,0)*dt
        if ball.pos.y>=ball.radius:
            ball.vel+=magnus*dt
        ball.pos+=ball.vel*dt
        phi+=-dt
        ball.rotate(angle=phi*dt,axis=ball.rot, origin=ball.pos)
        if ball.pos.y-ball.radius<0:
            ball.pos.y=ball.radius
            ball.vel.y=-ball.vel.y*c
            ball.vel.x=ball.vel.x*0.9
            ball.vel.z=ball.vel.z*0.9
            phi=phi*c
        elif ball.pos.x-ball.radius<=-25:
            ball.vel.x=-ball.vel.x*c
            phi=phi*c
        elif ball.pos.z+ball.radius>=25 or ball.pos.z-ball.radius<=-25:
            ball.vel.z=-ball.vel.z*c
            phi=phi*c
        if  goal.pos.z-3.5<=ball.pos.z+ball.radius<=goal.pos.z+3.5 and ball.pos.y+ball.radius<=goal.pos.y+1.25 and goal.pos.x+1.5>=ball.pos.x+ball.radius>=goal.pos.x-1.5:
            if score==False:
                print 'GOAL!!!!!'
                score=True
            if goal.pos.z-3>=ball.pos.z+ball.radius or ball.pos.z+ball.radius>=goal.pos.z+3 or ball.pos.y+ball.radius>=goal.pos.y+1 or goal.pos.x+1<=ball.pos.x+ball.radius:
                ball.vel=-ball.vel*0.5
        if mag(ball.vel)<=0.3 or reset.value==0:
            break
    if score==False:
        print 'You suck.'
    ball.make_trail=False
    ball.visible=False
    scene.center=(0,0,0)
    print 'Game Over'
    print '\n'

while True:
    fkick()
    
    
