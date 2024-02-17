# Codes_for_EAA
The code is tested under Python38

# Dependencies
- Numpy 1.23.1
- Sympy 1.10.1
- matplotlib 3.5.2

# Usage
We provide functions for both "more qubits introduced (MQI)" and "more iteration performed (MIP)" to simulate a search in the database in "EAA.py".
Once users set the size of the database $N$ , the number of the goal records $M$ and the error bound $\epsilon$ which is pre-defined arbitrarily by the users, they can compare the performance of the two methods MQI and MIP by simulation.

The description of main functions in "EAA.py" are as follows:
>+ Grover(N,M) initializes the simulation for the database with size $N$ and some goal records whose number is $M$;
>+ self.setError(esp) sets an arbitrarily error;
>+ self.addQubits() calls the method MQI to achieve the probability of success within the pre-defined error;
>+ self.moreGrover() calls the method MIP to achieve the probability of success within the pre-defined error.

> We provide random instances in "RandomizedTest.py" by setting the number of goal records $M$ as a prime number randomly selected from "primes.py"
