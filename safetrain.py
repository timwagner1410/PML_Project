from stable_baselines3 import PPO  # Import RL algorithm (PPO in this case)
from stable_baselines3.common.env_util import make_vec_env
import gym

# Register the environment (if not already registered)
gym.envs.registration.register(
    id='SnakeSafetyEnv-v0',
    entry_point='safeagent:SnakeSafetyEnv',
)

train_mode: bool = False
model_nr: int = 2

# Create the environment
env = gym.make('SnakeSafetyEnv-v0')

# Optional: Wrap the environment for vectorized training
# (helps improve training performance)
vec_env = make_vec_env(lambda: env, n_envs=4)

# Initialize the RL model
model = PPO("MlpPolicy", vec_env, verbose=1)

if train_mode:
    # Training mode
    model.learn(total_timesteps=500000)

    # After training, collect safety cost data for diagnostics
    obs, info = env.reset()
    done = False
    while not done:
        action, _ = model.predict(obs)
        obs, reward, done, truncated, info = env.step(action)

    model.save(f"ppo_snake_safety_{model_nr}")

else:
    # Test mode
    model = PPO.load(f"ppo_snake_safety_{model_nr}")
    obs, info = env.reset()
    done = False
    total_safety_cost = 0  # Track safety costs during evaluation

    for _ in range(1000):
        env.render()  # Optional: Render the environment
        action, _ = model.predict(obs)  # Get the action from the trained model
        obs, reward, done, truncated, info = env.step(action)

        if done:
            obs, info = env.reset()

    print(f"Bot has won {env.bot_score} times")
    print(f"AI has won {env.ai_score} times")