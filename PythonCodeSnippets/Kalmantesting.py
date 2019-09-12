# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 10:35:43 2019

@author: ezhu2
"""

import numpy as np
import matplotlib.pyplot as plt

#Position,speed,acceleration
x = np.array([[0.0, 0.0, 0.0]]).T 
print(x, x.shape)
n=x.size # States

P = np.diag([5.0,  1.0, 1.0]) # Uncertainty, mostly randodm values
print(P, P.shape)

dt = 0.1 # Time Step between Filter Steps

A= np.array([[1,dt,.5*dt**2],[0,1,dt],[0,0,1]])
print(A, A.shape)


H = np.array([[1.0,0,0],[0,0,1]]  ) # We only have a laser sensor and accelorometer, no velocity detection.
print(H,H.shape)

#Measurement noise R
ra = 20 # Assuming the uncertainty of acceleration
rp = 5 #Uncertainty of laser

R = np.array([[rp,0],[0,ra]])

print(R,R.shape)

# Q = process noise, = G* G^T * acceleration process noise

apn = .001
G = np.array([[.5 *dt**2],
             [dt],
             [1]])
Q = G * G.T * apn**2

print (Q,Q.shape)


#Identity matrix
I = np.eye(n)
print(I, I.shape)

m = 500 # Measurements

sp= 1.0 # Sigma for position
px= 0.0 # x Position
py= 0.0 # y Position

mpx = np.array(px+sp*np.random.randn(m))
mpy = np.array(py+sp*np.random.randn(m))

# Generate Laser check
laser=np.ndarray(m,dtype='bool')
laser[0]=True
# Less new position updates
for i in range(1,m):
    if i%10==0:
        laser[i]=True
    else:
        mpx[i]=mpx[i-1]
        mpy[i]=mpy[i-1]
        laser[i]=False
        
#Acceleration
sa = .1
ax = 0.0
ay = 0.0

mx = np.array(ax+sa*np.random.randn(m))
my = np.array(ay+sa*np.random.randn(m))

measurements = np.vstack((mpx,mpy,mx,my))
print(measurements.shape)

# Preallocation for Plotting
xt = []
dxt= []
ddxt=[]
Zx = []
Px = []
Pdx= []
Pddx=[]
Kx = []
Kdx= []
Kddx=[]


def savestates(x, Z, P, K):
    xt.append(float(x[0]))
    dxt.append(float(x[1]))
    ddxt.append(float(x[2]))
    Zx.append(float(Z[0]))
    Px.append(float(P[0,0]))
    Pdx.append(float(P[1,1]))
    Pddx.append(float(P[2,2]))
    Kx.append(float(K[0,0]))
    Kdx.append(float(K[1,0]))
    Kddx.append(float(K[2,0]))

for filterstep in range(m):
    
    # Project the state ahead
    x = A*x
    
    # Project next P
    P = A*P*A.T + Q    
    
    
    # ===============================
    # check if laser measurement is available
    if laser[filterstep]:
        # Compute the Kalman Gain
        S = H@P@H.T + R
        K = (P@H.T) @ np.linalg.pinv(S)
    
        
        # Update the estimate via z
        Z = measurements[:,filterstep].reshape(H.shape[0],1)
        y = Z - (H*x)                            # Innovation or Residual
        x = x + (K*y)
        
        # Update the error covariance
        P = (I - (K*H))*P

   
    
    # Save states for Plotting
    savestates(x, Z, P, K)
