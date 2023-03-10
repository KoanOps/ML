import numpy as np
import pandas as pd
import random
from collections import deque

class CustomEnvironment:
    def __init__(self, data_frame, initial_balance=100, lookback_window_size=50):
        self.data_frame = data_frame.dropna().reset_index()
        self.total_data_frame_steps = len(self.data_frame)-1
        self.initial_balance = initial_balance
        self.lookback_window_size = lookback_window_size
        self.action_space = np.array([0, 1, 2])
        self.order_history = deque(maxlen=self.lookback_window_size)
        self.market_history = deque(maxlen=self.lookback_window_size)
        self.state_size = (self.lookback_window_size, 10)

    def reset(self, environment_steps_size = 0):
        self.balance = self.initial_balance
        self.portfolio = self.initial_balance
        self.previous_portfolio = self.initial_balance
        self.cryptocurrency_held = 0
        self.cryptocurrency_sold = 0
        self.cryptocurrency_bought = 0
        if environment_steps_size > 0:
            self.start_step = random.randint(self.lookback_window_size, self.total_data_frame_steps - environment_steps_size)
            self.end_step = self.start_step + environment_steps_size
        else:
            self.start_step = self.lookback_window_size
            self.end_step = self.total_data_frame_steps

        self.current_step = self.start_step
        
        for i in reversed(range(self.lookback_window_size)):
            current_step = self.current_step - i
            self.order_history.append([self.balance, self.portfolio, self.cryptocurrency_bought, self.cryptocurrency_sold, self.cryptocurrency_held])
            self.market_history.append([self.data_frame.loc[current_step, 'Open'],
            self.data_frame.loc[current_step, 'High'],
            self.data_frame.loc[current_step, 'Low'],
            self.data_frame.loc[current_step, 'Close'],
            self.data_frame.loc[current_step, 'Volume']
            ])
        state = np.concatenate((self.market_history, self.order_history), axis=1)
        return state

    def _next_observation(self):
        self.market_history.append([self.data_frame.loc[self.current_step, 'Open'],
        self.data_frame.loc[self.current_step, 'High'],
        self.data_frame.loc[self.current_step, 'Low'],
        self.data_frame.loc[self.current_step, 'Close'],
        self.data_frame.loc[self.current_step, 'Volume']
        ])
        observation = np.concatenate((self.market_history, self.order_history), axis=1)
        return observation

    def step(self, action):
        self.cryptocurrency_bought = 0
        self.cryptocurrency_sold = 0
        self.current_step += 1
        current_price = random.uniform(
            self.data_frame.loc[self.current_step, 'Open'],
            self.data_frame.loc[self.current_step, 'Close'])

        if action == 0:
            pass
    
        elif action == 1 and self.balance > 0:
            self.cryptocurrency_bought = self.balance / current_price
            self.balance -= self.cryptocurrency_bought * current_price
            self.cryptocurrency_held += self.cryptocurrency_bought

        elif action == 2 and self.cryptocurrency_held>0:
            self.cryptocurrency_sold = self.cryptocurrency_held
            self.balance += self.cryptocurrency_sold * current_price
            self.cryptocurrency_held -= self.cryptocurrency_sold
        self.previous_portfolio = self.portfolio
        self.portfolio = self.balance + self.cryptocurrency_held * current_price
        self.order_history.append([self.balance, self.portfolio, self.cryptocurrency_bought, self.cryptocurrency_sold, self.cryptocurrency_held])
        reward = self.portfolio - self.previous_portfolio
        if self.portfolio <= self.initial_balance/2:
            done = True
        else:
            done = False
        observation = self._next_observation()
        return observation, reward, done

    def render(self):
        print(f'Step: {self.current_step}, Portfolio: {self.portfolio}')

def RandomGames(environment, training_episodes = 50, training_batch_size=500):
    average_portfolio = 0
    for episode in range(training_episodes):
        state = environment.reset(environment_steps_size = training_batch_size)
        while True:
            environment.render()
            action = np.random.randint(3, size=1)[0]
            state, reward, done = environment.step(action)
            if environment.current_step == environment.end_step:
                average_portfolio += environment.portfolio
                print("Portfolio:", environment.portfolio)
                break
    print("Average portfolio:", average_portfolio/training_episodes)

data_frame = pd.read_csv('./data.csv')
data_frame = data_frame.sort_values('Date')

lookback_window_size = 10
training_data_frame = data_frame[:-720-lookback_window_size]
testing_data_frame = data_frame[-720-lookback_window_size:]

training_environment = CustomEnvironment(training_data_frame, lookback_window_size=lookback_window_size)
testing_environment = CustomEnvironment(testing_data_frame, lookback_window_size=lookback_window_size)

RandomGames(training_environment, training_episodes = 10, training_batch_size=500)