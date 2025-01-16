from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from agent import SnakeEnv

# Create the environment
env = SnakeEnv()

# Check if the environment follows the Gym API
check_env(env, warn=True)

# Create the PPO model
model = PPO("MlpPolicy", env, verbose=1)

# Train the model
model.learn(total_timesteps=100000)

# Save the model
model.save("ppo_snake")

# To load the model later
# model = PPO.load("ppo_snake")

# Test the trained model
obs = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()
    if done:
        obs = env.reset()