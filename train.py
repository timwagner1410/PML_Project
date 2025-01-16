from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from agent import SnakeEnv


train_mode: bool = False

# Create the environment
env = DummyVecEnv([lambda: SnakeEnv(show=not train_mode)])

# Create the PPO model
model = PPO("MlpPolicy", env, verbose=1)

if train_mode:
    model.learn(total_timesteps=100000)
    model.save("ppo_snake_4")
else:
    model = PPO.load("ppo_snake_4")

# Test the trained model
obs = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()
    if done:
        obs = env.reset()