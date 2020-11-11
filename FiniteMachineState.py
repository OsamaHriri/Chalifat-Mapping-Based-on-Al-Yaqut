#!/usr/bin/env python
# coding: utf-8

# In[28]:


def prime(fn):
    def wrapper(*args, **kwargs):
        v = fn(*args, **kwargs)
        v.send(None)
        return v
    return wrapper


# In[36]:


class FSM:
    def __init__(self):
        # initializing states
        self.start = self._create_start()
        self.q1 = self._create_q1()
        self.q2 = self._create_q2()
        self.q4 = self._create_q4()
        self.q5 = self._create_q5()
        
        
        # setting current state of the system
        self.current_state = self.start

        # stopped flag to denote that iteration is stopped due to bad
        # input against which transition was not defined.
        self.stopped = False

    def send(self, char):
        """The function sends the curretn input to the current state
        It captures the StopIteration exception and marks the stopped flag.
        """
        try:
            self.current_state.send(char)
        except StopIteration:
            self.stopped = True
        
    def does_match(self):
        """The function at any point in time returns if till the current input
        the string matches the given regular expression.

        It does so by comparing the current state with the end state `q4`.
        It also checks for `stopped` flag which sees that due to bad input the iteration of FSM had to be stopped.
        """
        if self.stopped:
            return False
        return self.current_state == self.q4
    
    
    @prime
    def _create_start(self):
        while True:
            # Wait till the input is received.
            # once received store the input in `char`
            char = yield

            # depending on what we received as the input
            # change the current state of the fsm
            if char == 't':
                # on receiving `t` the state moves to `q1`
                self.current_state = self.q1
            else:
                # on receiving any other input, break the loop
                # so that next time when someone sends any input to
                # the coroutine it raises StopIteration
                break
    @prime
    def _create_q1(self):
        while True:
            # Wait till the input is received.
            # once received store the input in `char`
            char = yield

            # depending on what we received as the input
            # change the current state of the fsm
            if char == 'r':
                # on receiving `r` the state moves to `q2`
                self.current_state = self.q2

            else:
                # on receiving any other input, break the loop
                # so that next time when someone sends any input to
                # the coroutine it raises StopIteration
                break
                
    @prime
    def _create_q2(self):
        while True:
            # Wait till the input is received.
            # once received store the input in `char`
            char = yield

            # depending on what we received as the input
            # change the current state of the fsm
            if char == 't':
                
                # on receiving `t` the state moves to `q5`
                self.current_state = self.q5
            elif char =='p':
                # on receiving `p` the state moves to `q2`
                self.current_state = self.q4
                

            else:
                # on receiving any other input, break the loop
                # so that next time when someone sends any input to
                # the coroutine it raises StopIteration
                break    
                
                
#     def _create_q3(self):
#         while True:
#             # Wait till the input is received.
#             # once received store the input in `char`
#             char = yield

#             # depending on what we received as the input
#             # change the current state of the fsm
#             if char == 'r':
#                  # on receiving `r` the state moves to `q3`
#                 self.current_state = self.q2

                

#             else:
#                 # on receiving any other input, break the loop
#                 # so that next time when someone sends any input to
#                 # the coroutine it raises StopIteration
#                 break  
    @prime
    def _create_q4(self):
        while True:
            # Wait till the input is received.
            # once received store the input in `char`
            char = yield

            # depending on what we received as the input

            if char =='r':
                # on receiving `p` the state moves to `q2`
                self.current_state = self.q2
                

            else:
                # on receiving any other input, break the loop
                # so that next time when someone sends any input to
                # the coroutine it raises StopIteration
                break    
                
    @prime                
    def _create_q5(self):
        while True:
            # Wait till the input is received.
            # once received store the input in `char`
            char = yield

            # depending on what we received as the input
            # change the current state of the fsm
            if char == 'r':
                
                # on receiving `t` the state moves to `q5`
                self.current_state = self.q2
            elif char =='p':
                # on receiving `p` the state moves to `q4`
                self.current_state = self.q4
                

            else:
                # on receiving any other input, break the loop
                # so that next time when someone sends any input to
                # the coroutine it raises StopIteration
                break                    


# In[ ]:





# In[ ]:





# In[37]:


def grep_regex(text):
    evaluator = FSM()
    for ch in text:
        print(ch)
        evaluator.send(ch)
    return evaluator.does_match()


# In[38]:


grep_regex("trtp")


# In[ ]:





# In[ ]:




