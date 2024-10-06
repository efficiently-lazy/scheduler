# Scheduling Optimization Program
This optimization program serves to find the suitable schedule between set of product developers and product managers to review the set of products within the given possible timeslots.

## Objective
Maximizing number of items to be reviewed within the given periods while respecting set of constraints given to the problem.

## Sets
- $p \in P$ : set of products to be reviewed
- $d \in D$ : set of product developers to review the products
- $m \in M$ : set of product managers to review the products
- $t \in T$ : set of time slots for product review to occur

## Parameters
- $O_{p}^{m} \in \{0,1\}$ : Binary matrix representing the ownership of product $p$ to the product manager $m$. If $O_{p}^{m} = 1$, product $p$ is owned by product manager $m$, otheriwse $O_{p}^{m} = 0$.
- $B^{d,m} \in \{0,1\}$ : Binary matrix reflecting whether product developer $d$ belongs to the same team of product manager $m$ $(B^{d,m} = 1)$ or not $(B^{d,m} = 0)$.

## Variables
- $R_{p,t} \in \{0,1\}$ : Binary variable to represent whether product $p$ has been reviewed in timeslot $t$ $(R_{p,t} = 1)$ or not $(R_{p,t} = 0)$.
- $A_{p,t}^{d,m} \in \{0,1\}$ : Binary variable to represent whether product $p$ is going to be reviewed by product developer $d$ and manager $m$ in the given timeslot $t$ $(A_{p,t}^{d,m} = 1)$