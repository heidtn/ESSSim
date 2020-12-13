# ESSSim
This is a simple simulation framework for the EVO Space Suit.  The intent here is to create a very rudimentary plug and play system for simulating different sensors and systems as well as integrating real sensors with simulated data.

NOTE:
As is, this framework is very rudimentary and is not yet versioned.  Future versions will not be backwards compatible until it's somewhat stable so don't count on it too much initially.  The idea is to have enough code to play around with and see what works and what doesn't work (and if this is even useful!).

### How to use
this can be installed by changing into the directory in a termal and executing `pip install .`

See the SimpleDemo.py in examples for a functioning implementation.  The general idea is that a series of nodes are created.  Nodes have inputs and outputs.  These inputs and outputs can be connected to each other to form a simulated system.  There are two types of nodes:
* Time Domain Nodes
* State Space Nodes

Time domain nodes are the easiest to grasp.  You pass a time domain node a current time and it updates its outputs based on it's inputs.  If you write a time domain node, you are responsible for figuring out how the system evolves through time.

State space nodes are a little more complicated, but are intended for dynamical systems that don't have a reasonable time domain solution (thermal systems are one example as is multibody gravitational simulation).  These nodes require two primary elements in addition to the inputs and outputs:
1. An internal state
2. The derivative of the internal state (a Jacobian)
Forward integration can be used to solve these systems (although there is some inherent error for nonlinear systems) and simulate them alongside other systems.  The beauty of state space systems is that most systems can be modelled as one fairly simply (at least a nonlinear state space system).

An example of state space is an object falling in gravity.  While this has a time domain solution, we can demonstrate the state space representation.  There are two states we track: position and velocity.  We can call them x, and d_dot.  We represent these in a numpy array [x, x_dot].  The derivative of the state is then just [x_dot, -9.8] because the derivative of position is the velocity and the derivative of velocity is acceleration, which in this case is gravity.  With just these two definitions we can simulate a falling object.

### What this isn't
* This system is not intended to be a final solution to integrate components for EVO Space Suit
* This system makes no realtime guarantees and just runs as fast as possible while keeping states synchronized (it is python after all)
* A complex simulation framework.  This is intended for simple sensors and systems.  Simulating complex dynamics


### TODO
* Switch to RK4 integration scheme, Forward Euler is fine for most things, but not the best.
* Add in physical sensor nodes and examples
* Add in GUI nodes and examples
* Add in server nodes and examples (for data delivery to the interface)
* Use a process pool to perform the steps in parallel and speed up execution