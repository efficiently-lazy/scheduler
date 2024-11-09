# Scheduling Optimization Program
This optimization program serves to find the suitable schedule between set of product developers and product managers to review the set of products within the given possible timeslots.

## Usage Intruction

1. **Set Up Virtual Environment and Change Directory**
    
    In your terminal, set up a virtual environment, then navigate to the project directory `\or-projects`.
``` bash
# Create a virtual environment (optional but recommended)
python -m venv env

# Activate the virtual environment
# On Windows
.\env\Scripts\activate
# On macOS/Linux
source env/bin/activate

# Change directory to or-projects
cd path/to/or-projects
```

2. **Install Dependencies**
    
    Install the required packages specified in requirements.txt:
``` bash
pip install -r requirements.txt
```

3. **Adjust Input Data**

    Open src/data/input.xlsx and make the following adjustments:

- **Sheet "Ownership Products":** Update the matrix where each column header represents a manager, and each row header represents a product. Define ownership relations by filling in this matrix.
- **Sheet "Work Relation":** This matrix represents whether managers (columns) work with developers (rows). Fill in the cells to indicate collaboration.
- **Sheet "Blocked Calendar":** Update this matrix to specify blocked periods for managers and developers. Rows represent time periods, and columns represent each person (managers and developers).

4. **Run the Program**

    Execute the following command to run the program:
``` bash
python src/main.py
```
## Model Explanation

### Sets
- $p \in P$ : set of products to be reviewed
- $d \in D$ : set of product developers to review the products
- $m \in M$ : set of product managers to review the products
- $t \in T$ : set of time slots for product review to occur

### Parameters
- $O_{p}^{m} \in \{0,1\}$ : Binary matrix representing the ownership of product $p$ to the product manager $m$. If $O_{p}^{m} = 1$, product $p$ is owned by product manager $m$, otheriwse $O_{p}^{m} = 0$.
- $B^{d,m} \in \{0,1\}$ : Binary matrix reflecting whether product developer $d$ belongs to the same team of product manager $m$ $(B^{d,m} = 1)$ or not $(B^{d,m} = 0)$.
- $A^i_t \in \{0,1\}$: Binary matrix indicating whether developer or manager $(i\in \{D \cup P\})$ schedule in period $t$ is blocked $(A^i_t=1)$ or not $(A^i_t=0)$.

### Variables
- $y_{p,t} \in \{0,1\}$ : Binary variable to represent whether product $p$ has been reviewed in timeslot $t$ $(y_{p,t} = 1)$ or not $(y_{p,t} = 0)$.

- $x_{p,t}^{d,m} \in \{0,1\}$ : Binary variable to represent whether product $p$ is going to be reviewed by product developer $d$ and manager $m$ in the given timeslot $t$ $(x_{p,t}^{d,m} = 1)$

### Objective Function

$$
\text{max} \sum_{p \in P} \sum_{t \in T} y_{p,t} 
$$

Maximizing number of products $p$ to be reviewed within the provided timeslots $t$.

### Constraints

1. Products $p$ can only be reviewed maximum once within the available timeslots.

$$
\sum_{t \in T} y_{p,t} \leq 1 \qquad \forall p \in P 
$$

2. Product manager $m$ can only review the product belonging to him/her.

$$ 
\sum_{d \in D} \sum_{t \in T} x_{p,t}^{d,m} \leq O_p^m \qquad \forall m \in M, p \in P 
$$

3. Product manager $m$ can only review the product together with the developer belonging to the same team.

$$
\sum_{p \in P} \sum_{t \in T} x_{p,t}^{d,m} \leq B^{d,m} \cdot |P| \qquad \forall m \in M, d \in D 
$$

4. Linking constraint between $x_{p,t}^{d,m}$ and $y_{p,t}$.

$$
\sum_{d \in D} \sum_{m \in M} x_{p,t}^{d,m} \leq y_{p,t} \qquad \forall p \in P, t \in T 
$$

5. Each product developer $d$ can only review one product at a timeslot $t$.

$$
\sum_{m \in M} \sum_{p \in P} x_{p,t}^{d,m} \leq 1 \qquad \forall d \in D, t \in T 
$$

6. Each product manager $m$ can only review one product at a timeslot $t$.

$$
\sum_{d \in D} \sum_{p \in P} x_{p,t}^{d,m} \leq 1 \qquad \forall m \in M, t \in T 
$$

7. When a manager $m$ or developer $d$ is scheduled to review a product $p$ at time $t$, then they should not be blocked in their schedule at that period.

$$
2\cdot x_{p,t}^{d,m} \leq (2-A^d_t-A^m_t) \qquad \forall d \in D, m \in M, p \in P, t \in T
$$

8. Non-negativity constraints for the variables.

$$
x_{p,t}^{d,m} \in \{0,1\} \quad \forall m \in M, d \in D, p \in P, t \in T 
$$

$$
y_{p,t} \in \{0,1\} \quad \forall p \in P, t \in T
$$
