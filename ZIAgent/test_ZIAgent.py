# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 23:44:23 2020

@author: Lenovo
"""

import numpy as np
import pytest
import os
import random
os.chdir("C:\\Users\\Lenovo\\Desktop")
from ZIAgent import ZIAgent
from OMS.OMS import OrderManagementSystem 

deltaT = 10
n = 100000
Mu_Est = 0.94
Lambda_Est = [1.85,1.51,1.09,0.88,0.77]
Theta_Est = [0.71,0.81,0.68,0.56,0.47]
OMSTest = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
ZIAgentTest = ZIAgent("ZIagent",OMSTest,200, 0.1,Mu_Est,Lambda_Est,Theta_Est,1,\
                          CurrentTime = 0, OrderCount = 0, ZIOrderBook = [[]])

class Estimator:
    
    def DeathRateEst(self, Est, length, deltaT, n):       
        artime = []
        for i in range(n):
            artime.append(ZIAgentTest.OneShotBirthDeath(length, 0, length*Est, deltaT = 10)[1])
            
        Test = [1/(length*np.mean(artime)),1/(length*np.std(artime))]
    
        return Test
    
    def BirthRateEst(self, Est, length, deltaT, n):
        artime = []
        for i in range(n):
            artime.append(ZIAgentTest.OneShotBirthDeath(length, Est, 0, deltaT = 10)[1])
            
        Test = [1/np.mean(artime),1/np.std(artime)]
    
        return Test



Test_est = Estimator()



class TestClass:
    def test_Mu(self):
        mu_test = Test_est.BirthRateEst(Mu_Est, 0, deltaT, n)
        assert abs(mu_test[0]-Mu_Est) <= 0.01
        assert abs(mu_test[1]-Mu_Est) <= 0.01
        
    def test_Theta(self):
        Theta_test = [[]]
        for j in range(len(Theta_Est)):
           Theta_test.append(Test_est.DeathRateEst(Theta_Est[j], 10, deltaT, n))
        
        Theta_test.pop(0)
        for i in range(len(Theta_test)):
            for j in range(len(Theta_test[i])):
                assert abs(Theta_Est[i]-Theta_test[i][j]) <= 0.01
                   
                

    def test_Lambda(self):
        Lambda_test = [[]]
        for j in range(len(Lambda_Est)):
             Lambda_test.append(Test_est.BirthRateEst(Lambda_Est[j], 0, deltaT, n))
        
        Lambda_test.pop(0)
        for i in range(len(Lambda_test)):
            for j in range(len(Lambda_test[i])):
                assert abs(Lambda_Est[i]-Lambda_test[i][j]) <= 0.01
                   
        


if __name__ == "__main__":
    
    pytest.main()
