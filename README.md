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

The limit order book not only contains all orders remaining on the book, but also enables operations to manipulate it, including inserting, canceling, executing, etc. 

(2) Order Manager: (Author: SHEN, Kanchao)

### 2. Zero Intelligence Agent
(Author: MO, Zi and ZHOU, Zhen)

The zero intelligence agent is based on the paper [Cont et al. (2011)](http://www.columbia.edu/~ww2040/orderbook.pdf).

