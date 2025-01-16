from stable_baselines3 import PPO
from agent import SnakeEnv


train_mode: bool = True
model_nr: int = 16

# Create the environment
env = SnakeEnv(show=not train_mode)

# Create the PPO model
model = PPO("MlpPolicy", env, verbose=1)

if train_mode:
    model.learn(total_timesteps=100000)
    model.save(f"ppo_snake_{model_nr}")
else:
    model = PPO.load(f"ppo_snake_{model_nr}")

    # Test the trained model
    obs, info = env.reset()
    for _ in range(2000):
        action, _states = model.predict(obs)
        obs, rewards, done, truncated, info = env.step(action)
        env.render()
        if done:
            obs, info = env.reset()

    print(f"Bot has won {env.bot_score} times")
    print(f"AI has won {env.ai_score} times")