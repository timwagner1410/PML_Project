from stable_baselines3 import PPO
from safety_agent import SafeSnakeEnv


train_mode: bool = False
model_nr: int = 5

# Create the environment
env = SafeSnakeEnv(show=not train_mode)

# Create the PPO model
model = PPO("MlpPolicy", env, verbose=1)

if train_mode:
    model.learn(total_timesteps=250000)
    model.save(f"ppo_snake_safe_{model_nr}")
else:
    model = PPO.load(f"ppo_snake_safe_{model_nr}")

    # Test the trained model
    obs, info = env.reset()
    games = 0
    while games < 101:
        action, _states = model.predict(obs)
        obs, rewards, done, truncated, info = env.step(action)
        env.render()
        if done:
            games += 1
            obs, info = env.reset()

    print(f"Bot has won {env.bot_score} times")
    print(f"AI has won {env.ai_score} times")