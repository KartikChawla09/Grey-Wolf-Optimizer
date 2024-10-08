import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import messagebox

def initialization (PopSize,D,LB,UB):
    SS_Boundary = len(LB) if isinstance(UB,(list,np.ndarray)) else 1
    if SS_Boundary ==1:
        Positions = np.random.rand(PopSize,D)*(UB-LB)+LB
    else:
        Positions = np.zeros((PopSize,D))
        for i in range(D):
            Positions[:,i]=np.random.rand(PopSize)*(UB[i]-LB[i])+LB[i]
    return Positions

def GWO(PopSize,MaxT,LB,UB,D,Fobj):
    Alpha_Pos = np.zeros(D)
    Alpha_Fit = np.inf
    Beta_Pos = np.zeros(D)
    Beta_Fit = np.inf
    Delta_Pos = np.zeros(D)
    Delta_Fit = np.inf

    Positions = initialization(PopSize,D,UB,LB)
    Convergence_curve = np.zeros(MaxT)

    l = 0
    while l<MaxT:
        for i in range (Positions.shape[0]):
            BB_UB = Positions[i,:]>UB 
            BB_LB = Positions[i,:]<LB
            Positions[i,:] = (Positions[i,:]*(~(BB_UB+BB_LB)))+UB*BB_UB+LB*BB_LB
            Fitness = Fobj(Positions[i,:])

            if Fitness<Alpha_Fit:
                Alpha_Fit=Fitness
                Alpha_Pos=Positions[i,:]

            if Fitness>Alpha_Fit and Fitness<Beta_Fit:
                Beta_Fit=Fitness
                Beta_Pos=Positions[i,:]
            
            if Fitness>Alpha_Fit and Fitness>Beta_Fit and Fitness<Delta_Fit:
                Delta_Fit=Fitness
                Delta_Pos=Positions[i,:]
        
        a = 2-1*(2/MaxT)
        for i in range (Positions.shape[0]):
            for j in range (Positions.shape[1]):
                r1=np.random.random()
                r2=np.random.random()

                A1 = 2*a*r1-a
                C1 = 2 * r2

                D_Alpha = abs(C1*Alpha_Pos[j]-Positions[i,j])
                X1 = Alpha_Pos[j]-A1*D_Alpha
                
                r1=np.random.random()
                r2=np.random.random()

                A2 = 2*a*r1-a
                C2=2*r2

                D_Beta = abs(C2*Beta_Pos[j]-Positions[i,j])
                X2 = Beta_Pos[j]-A2*D_Beta

                r1 = np.random.random()
                r2 = np.random.random()

                A3 = 2*a*r1-a
                C3 = 2*r2

                D_Delta = abs(C3 * Delta_Pos[j] - Positions[i,j])
                X3 = Delta_Pos[j] - A3 * D_Delta

                Positions[i,j] = (X1 + X2 + X3) / 3
        l += 1
        Convergence_curve[l - 1] = Alpha_Fit
    return Alpha_Fit, Alpha_Pos, Convergence_curve

if __name__ == "__main__":
    def F1(x):
        return np.sum(x ** 2)

    Fun_name = F1
    LB = -100
    UB = 100
    D = 30
    PopSize= 100
    MaxT = 100

    bestfit, bestsol, convergence_curve = GWO(PopSize,MaxT,LB,UB,D,Fun_name)
    print("Best Fitness =", bestfit)
    print("Best Solution = ",bestsol)

# Show the final result in a message box
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("GWO Result", f"Best Fitness: {bestfit}\nBest Solution: {bestsol}")
