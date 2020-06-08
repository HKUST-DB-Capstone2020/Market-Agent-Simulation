# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 02:05:21 2020

@author: jackz
"""


import os
import sys
import time
sys.path.append(os.path.pardir)

# os.chdir("C:\\Users\\jackz\\Desktop\\0427")

from OMS.OMS import OrderManagementSystem 
from ZIAgent.ZIAgent import ZIAgent


if __name__ == "__main__":
    result = []
    count = 0
    for dir in ["buy"]:
        for pct in [0.1]:
            print(dir,pct)
            text = ""
            for i in range(10000):
                # if i % 10 == 0:
                print(i)
                # initial settings
                n = 200  # total number of price grids
                PriceGridSize = 0.1  # usually 1 or 0.1 or 0.01
                TimeHorizon = 100
                deltaT = 1
                qtysize = 1000

                price_ini =   9.7
                priceA_ini =  10.0
                priceB_ini =  9.8

                # parameters according to Cont paper
                Mu_Est = 0.94
                k_Est = 1.92
                Alpha_Est = 0.52
                Lambda_Est = [1.85,1.51,1.09,0.88,0.77]
                Theta_Est = [0.71,0.81,0.68,0.56,0.47]
                Lambda_PowerLaw = [k_Est/(pow(j,Alpha_Est)) for j in range(1,6)] # Arrival rates according to power law

                # set initial values for OMS and ZIAgent
                CurrentTime = 0
                OrderCount = 0
                ZIOrderBook = [[]]

                # ready for output
                OutputTxt = open("Output.txt","w")  # open the txt
                starttime=time.perf_counter()

                OMSTest = OrderManagementSystem(priceA_ini,priceB_ini,PriceGridSize,5,price_ini)
                OMSTest.record("strategy")
                ZIAgentTest = ZIAgent("ZIagent",OMSTest,n,PriceGridSize,Mu_Est,Lambda_Est,Theta_Est,\
                                      CurrentTime,OrderCount,ZIOrderBook)


                buy_list_price = []
                buy_list_volume = []
                avg_daily_vol = 187760
                vol_per_order = int(avg_daily_vol*pct / 10)
                # pct = 0.01
                target_vol = avg_daily_vol*pct
                # total_buy_vol = 0
                # during the trading period
                while (ZIAgentTest.CurrentTime <= TimeHorizon):
                    ZIAgentTest.Execute(OMSTest)     # execute ZIAgent generator
                    OMSTest.receive(ZIAgentTest.OrderIssued)  # output to OMS
                    ZIAgentTest.Update(OMSTest)  # update ZIAgentTest

                    time_prop = (0.01 * TimeHorizon + ZIAgentTest.CurrentTime) / TimeHorizon
                    rem_qty = target_vol - OMSTest.strategy_record.position
                    # print(ZIAgentTest.CurrentTime, OMSTest.strategy_record.position)
                    this_order_volume = min(vol_per_order * int((target_vol * time_prop - OMSTest.strategy_record.position) / vol_per_order), rem_qty)
                    if this_order_volume > 0:
                        OMSTest.receive(["strategy", "market", dir, this_order_volume, OMSTest.bid-OMSTest.tick])
                        # print(["strategy", "limit", dir, this_order_volume, OMSTest.bid-OMSTest.tick])
                        # OMSTest.receive(["strategy", "market", dir, this_order_volume, 0])
                        buy_list_price += OMSTest.execPrice
                        buy_list_volume += OMSTest.execQty
                        # print(ZIAgentTest.CurrentTime)
                        # print(min(int((target_vol-total_buy_vol)/(TimeHorizon-ZIAgentTest.CurrentTime)/10)+1,target_vol-total_buy_vol))

                    # ZIAgentTest.ZIAgentConsolePrint(OMSTest) # print order and book results into the console
                    # ZIAgentTest.ZIAgentFilePrint(OMSTest,OutputTxt)    # print order and book results into the txt file
                    # if (ZIAgentTest.OrderCount % 200 == 0 ):
                    #     print(ZIAgentTest.OrderCount, end=" ")   # show the progress

                # while ZIAgentTest.CurrentTime <= TimeHorizon:
                #     ZIAgentTest.Execute(OMSTest)  # execute ZIAgent generator
                #     OMSTest.receive(ZIAgentTest.OrderIssued)  # output to OMS
                #     ZIAgentTest.Update(OMSTest)
                #     rem_qty = int(target_vol - OMSTest.strategy_record.position)
                #     if rem_qty>0:
                #         OMSTest.receive(["strategy", "market", dir, rem_qty, OMSTest.bid - OMSTest.tick])
                #         # buy_list_price += OMSTest.execPrice
                #         # buy_list_volume += OMSTest.execQty
                # OutputTxt.close()
                # print("avg_price:",sum(buy_list_price[i]*buy_list_volume[i] for i in range(len(buy_list_price)))/sum(buy_list_volume))
                result.append(sum(buy_list_price[i]*buy_list_volume[i] for i in range(len(buy_list_price)))/sum(buy_list_volume))
                # print(sum(buy_list_volume) == target_vol, sum(OMSTest.trade_vol_record), buy_list_price)
                # print("target:%s, buy:%s"%(target_vol, sum(buy_list_volume)))
                # report general results
                endtime=time.perf_counter()

                # ZIAgentTest.ZIAgentPirceOrderPlot()
                # ZIAgentTest.ZIAgentPirceTimePlot()
                # ZIAgentTest.ZIAgentArrivalTimeFrequencyPlot()
                # ZIAgentTest.HistoryOrderBookPlot(10)      # after 10th order
                # print('4560987 in ask prices',ZIAgentTest.unique_index(ZIAgentTest.PricePathDF.AskPrice,4560987))
                # print('0 in bid prices',ZIAgentTest.unique_index(ZIAgentTest.PricePathDF.BidPrice,0))
                #
                # print("the running cost:",endtime-starttime, " seconds")
                # cost = 0
                # volume = 0
                # for i in OMSTest.strategy_record.filled_order:
                #     volume += i[2]
                #     cost += i[2]*i[1]
                text += "%s\n"%(result[-1])
                print(result[-1])
                if i % 100 == 99:
                    with open(f"result_paper/result_{dir}_{pct}_{count}.txt","w") as f:
                        f.write(text)
                    count += 1








