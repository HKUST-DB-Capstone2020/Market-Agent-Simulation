# Market-Agent-Simulation

### Instructor: 
Dr. Andrew Royal

### Group members: (sorted alphabetically)
MO, Zi

SHEN, Kanchao

WANG, Boyu

ZHOU, Zhen

This is the first part of the capstone project supported by HKUST and Deutsche Bank. 

### 0. Introduction
The market agent aims to emulate the statistical properties and empirical characteristics of the real equity market. In terms of the type of agent, there are various choices. Here we use a simple yet effective one, zero intelligence agent. Apart from the ZI-agent, an order management system is indispensable in the simulation environment. The two following sections detail the design of the two main parts.

### 1. Order Management System

The OMS acts as an exchange and clearing house. It interacts with the ZI-agent and deals with all types of orders, incluing limit order and market order. Two modules are contrived for the functionality of the system.

(1) Limit Order Book: (Author: WANG, Boyu)

The limit order book not only contains all orders remaining on the book, but also enables operations to manipulate itself, including inserting, canceling, executing, etc. 

(2) Order Manager: (Author: SHEN, Kanchao)

The OMS recieves all the requests from agents, matches the orders and maintains the LOB. Also, there is some public information that all traders can get from OMS.

### 2. Zero Intelligence Agent
(Author: ZHOU, Zhen and MO, Zi)

The Zero-Intelligence agent is an order generator which follows a stochastic model based on the paper [Cont et al. (2011)](http://www.columbia.edu/~ww2040/orderbook.pdf). It will output an order when it is given the current limit order book situation, and records the orders it has generated and how the limit order book changes.

### 3. How to use simulator to test you strategy

For a demo, please see *SimulationEnvironment*.

**Step 1:** Write your own strategy. e.g. see Strategies.py

**Step 2:** Add your strategies in the Simulator.py

**Step 3:** Hit "run", and have fun! 

### Appendix: Stats about the simulated market

**Time horizon for simulation:** 100 time units, denoted as 1 "day". (For the meaning of 1 time units under physical measure, please refer to the original paper [Cont et al. (2011)](http://www.columbia.edu/~ww2040/orderbook.pdf))

**Episodes**: 10,000

(1) ADTV: 375,861 shares

(2) Daily vol: 
