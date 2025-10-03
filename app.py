import streamlit as st
import numpy as np
from main import Game2x2, best_response, rand_strategy
from io import StringIO
import sys

st.title("2x2 Game Theory Simulator")
st.write("Enter payoffs in each cell of the game matrix")

st.subheader("Game Payoff Matrix")
st.write("Enter payoffs as (Player 1, Player 2) for each cell")

# Create header row
header_cols = st.columns([1.5, 2.5, 2.5])
with header_cols[0]:
    st.write("")
with header_cols[1]:
    st.markdown("**P2: Strategy 0**")
with header_cols[2]:
    st.markdown("**P2: Strategy 1**")

st.divider()

# Row 1
col_label, col1, col2 = st.columns([1.5, 2.5, 2.5])
with col_label:
    st.markdown("**P1: Strat 0**")
with col1:
    with st.container(border=True):
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            p1_00 = st.number_input("P1", value=3, key="p1_00")
        with subcol2:
            p2_00 = st.number_input("P2", value=3, key="p2_00")
        st.markdown(f"**({int(p1_00)}, {int(p2_00)})**")
    
with col2:
    with st.container(border=True):
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            p1_01 = st.number_input("P1", value=0, key="p1_01")
        with subcol2:
            p2_01 = st.number_input("P2", value=5, key="p2_01")
        st.markdown(f"**({int(p1_01)}, {int(p2_01)})**")

st.divider()

# Row 2
col_label2, col3, col4 = st.columns([1.5, 2.5, 2.5])
with col_label2:
    st.markdown("**P1: Strat 1**")
with col3:
    with st.container(border=True):
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            p1_10 = st.number_input("P1", value=5, key="p1_10")
        with subcol2:
            p2_10 = st.number_input("P2", value=0, key="p2_10")
        st.markdown(f"**({int(p1_10)}, {int(p2_10)})**")
    
with col4:
    with st.container(border=True):
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            p1_11 = st.number_input("P1", value=1, key="p1_11")
        with subcol2:
            p2_11 = st.number_input("P2", value=1, key="p2_11")
        st.markdown(f"**({int(p1_11)}, {int(p2_11)})**")

st.divider()

# Create the game
p1_payoffs = [[p1_00, p1_01], [p1_10, p1_11]]
p2_payoffs = [[p2_00, p2_01], [p2_10, p2_11]]
game = Game2x2(p1_payoffs, p2_payoffs)

# Initial strategies
st.subheader("Settings")
use_random = st.checkbox("Use random initial strategies", value=True)

if not use_random:
    p1_init = st.slider("P1: Probability of Strategy 0", 0.0, 1.0, 0.5)
    p2_init = st.slider("P2: Probability of Strategy 0", 0.0, 1.0, 0.5)
    player1 = np.array([p1_init, 1-p1_init])
    player2 = np.array([p2_init, 1-p2_init])
else:
    player1, player2 = rand_strategy(game)

# Advanced options
with st.expander("Advanced options"):
    max_iterations = st.number_input("Max iterations", min_value=1, max_value=100, value=10)

if st.button("Run Iterated Best Response"):
    st.subheader("Results")
    
    previous_states = []
    converged = False
    cycle_detected = False
    
    for i in range(max_iterations):
        # Player 1 responds
        player1 = best_response(game, player2, player=1)
        state_after_p1 = (tuple(player1), tuple(player2))
        previous_states.append(state_after_p1)
        
        # Check for convergence/cycle after P1's move
        if len(previous_states) > 1 and state_after_p1 in previous_states[:-1]:
            state = state_after_p1
            if previous_states[-2] == state:
                converged = True
                st.success(f"✓ Convergence detected after {i+1} iterations!")
                
                p1_strategy = np.argmax(player1)
                p2_strategy = np.argmax(player2)
                
                st.write(f"**Converged to:** Player 1 plays strategy {p1_strategy}, Player 2 plays strategy {p2_strategy}")
                st.write(f"**Payoffs:** P1 = {game.payoffs_p1[p1_strategy, p2_strategy]}, P2 = {game.payoffs_p2[p1_strategy, p2_strategy]}")
                
                # Visual grid
                grid_visual = [["·", "·"], ["·", "·"]]
                grid_visual[p1_strategy][p2_strategy] = "✓"
                
                st.write("**Convergence position:**")
                st.table({
                    "": ["P1: Strat 0", "P1: Strat 1"],
                    "P2: Strat 0": [grid_visual[0][0], grid_visual[1][0]],
                    "P2: Strat 1": [grid_visual[0][1], grid_visual[1][1]]
                })
                
                # Optional: Show full path
                with st.expander("Show full convergence path"):
                    st.write("**Full path to convergence:**")
                    
                    # Create a grid showing all visited states
                    grid_full = [["·", "·"], ["·", "·"]]
                    
                    for idx, hist_state in enumerate(previous_states):
                        p1_strat = np.argmax(hist_state[0])
                        p2_strat = np.argmax(hist_state[1])
                        
                        if grid_full[p1_strat][p2_strat] == "·":
                            grid_full[p1_strat][p2_strat] = str(idx + 1)
                        else:
                            # Multiple visits
                            grid_full[p1_strat][p2_strat] = f"{grid_full[p1_strat][p2_strat]},{idx + 1}"
                    
                    st.table({
                        "": ["P1: Strat 0", "P1: Strat 1"],
                        "P2: Strat 0": [grid_full[0][0], grid_full[1][0]],
                        "P2: Strat 1": [grid_full[0][1], grid_full[1][1]]
                    })
                    
                    # Show step-by-step
                    st.write("**Step-by-step:**")
                    for idx, hist_state in enumerate(previous_states):
                        p1_strat = np.argmax(hist_state[0])
                        p2_strat = np.argmax(hist_state[1])
                        st.write(f"- Step {idx + 1}: ({p1_strat}, {p2_strat})")
                
                break
            else:
                cycle_detected = True
                st.warning(f"⟳ Cycle detected after {i+1} iterations!")
                st.write("The strategies are cycling and not converging to a single equilibrium.")
                
                # Find where the cycle starts
                cycle_start_idx = previous_states.index(state)
                cycle_states = previous_states[cycle_start_idx:]
                
                st.write(f"**Cycle length:** {len(cycle_states)} states")
                
                # Visualize the cycle on the grid
                st.write("**Cycle path:**")
                
                # Create a grid showing the cycle with numbers
                grid_visual = [["·", "·"], ["·", "·"]]
                
                for idx, cycle_state in enumerate(cycle_states):
                    p1_strat = np.argmax(cycle_state[0])
                    p2_strat = np.argmax(cycle_state[1])
                    
                    if grid_visual[p1_strat][p2_strat] == "·":
                        grid_visual[p1_strat][p2_strat] = str(idx + 1)
                    else:
                        # Multiple visits - show as range
                        grid_visual[p1_strat][p2_strat] = f"{grid_visual[p1_strat][p2_strat]},{idx + 1}"
                
                st.table({
                    "": ["P1: Strat 0", "P1: Strat 1"],
                    "P2: Strat 0": [grid_visual[0][0], grid_visual[1][0]],
                    "P2: Strat 1": [grid_visual[0][1], grid_visual[1][1]]
                })
                
                # Show the sequence
                st.write("**Cycle sequence:**")
                cycle_sequence = []
                for idx, cycle_state in enumerate(cycle_states):
                    p1_strat = np.argmax(cycle_state[0])
                    p2_strat = np.argmax(cycle_state[1])
                    cycle_sequence.append(f"Step {idx + 1}: ({p1_strat}, {p2_strat})")
                
                for step in cycle_sequence:
                    st.write(f"- {step}")
                
                break
        
        # Player 2 responds
        player2 = best_response(game, player1, player=2)
        state_after_p2 = (tuple(player1), tuple(player2))
        previous_states.append(state_after_p2)
        
        # Check for convergence/cycle after P2's move
        if state_after_p2 in previous_states[:-1]:
            state = state_after_p2
            if previous_states[-2] == state:
                converged = True
                st.success(f"✓ Convergence detected after {i+1} iterations!")
                
                p1_strategy = np.argmax(player1)
                p2_strategy = np.argmax(player2)
                
                st.write(f"**Converged to:** Player 1 plays strategy {p1_strategy}, Player 2 plays strategy {p2_strategy}")
                st.write(f"**Payoffs:** P1 = {game.payoffs_p1[p1_strategy, p2_strategy]}, P2 = {game.payoffs_p2[p1_strategy, p2_strategy]}")
                
                # Visual grid
                grid_visual = [["·", "·"], ["·", "·"]]
                grid_visual[p1_strategy][p2_strategy] = "✓"
                
                st.write("**Convergence position:**")
                st.table({
                    "": ["P1: Strat 0", "P1: Strat 1"],
                    "P2: Strat 0": [grid_visual[0][0], grid_visual[1][0]],
                    "P2: Strat 1": [grid_visual[0][1], grid_visual[1][1]]
                })
                
                # Optional: Show full path
                with st.expander("Show full convergence path"):
                    st.write("**Full path to convergence:**")
                    
                    # Create a grid showing all visited states
                    grid_full = [["·", "·"], ["·", "·"]]
                    
                    for idx, hist_state in enumerate(previous_states):
                        p1_strat = np.argmax(hist_state[0])
                        p2_strat = np.argmax(hist_state[1])
                        
                        if grid_full[p1_strat][p2_strat] == "·":
                            grid_full[p1_strat][p2_strat] = str(idx + 1)
                        else:
                            # Multiple visits
                            grid_full[p1_strat][p2_strat] = f"{grid_full[p1_strat][p2_strat]},{idx + 1}"
                    
                    st.table({
                        "": ["P1: Strat 0", "P1: Strat 1"],
                        "P2: Strat 0": [grid_full[0][0], grid_full[1][0]],
                        "P2: Strat 1": [grid_full[0][1], grid_full[1][1]]
                    })
                    
                    # Show step-by-step
                    st.write("**Step-by-step:**")
                    for idx, hist_state in enumerate(previous_states):
                        p1_strat = np.argmax(hist_state[0])
                        p2_strat = np.argmax(hist_state[1])
                        st.write(f"- Step {idx + 1}: ({p1_strat}, {p2_strat})")
                
                break
            else:
                cycle_detected = True
                st.warning(f"⟳ Cycle detected after {i+1} iterations!")
                st.write("The strategies are cycling and not converging to a single equilibrium.")
                
                # Find where the cycle starts
                cycle_start_idx = previous_states.index(state)
                cycle_states = previous_states[cycle_start_idx:]
                
                st.write(f"**Cycle length:** {len(cycle_states)} states")
                
                # Visualize the cycle on the grid
                st.write("**Cycle path:**")
                
                # Create a grid showing the cycle with numbers
                grid_visual = [["·", "·"], ["·", "·"]]
                
                for idx, cycle_state in enumerate(cycle_states):
                    p1_strat = np.argmax(cycle_state[0])
                    p2_strat = np.argmax(cycle_state[1])
                    
                    if grid_visual[p1_strat][p2_strat] == "·":
                        grid_visual[p1_strat][p2_strat] = str(idx + 1)
                    else:
                        # Multiple visits - show as range
                        grid_visual[p1_strat][p2_strat] = f"{grid_visual[p1_strat][p2_strat]},{idx + 1}"
                
                st.table({
                    "": ["P1: Strat 0", "P1: Strat 1"],
                    "P2: Strat 0": [grid_visual[0][0], grid_visual[1][0]],
                    "P2: Strat 1": [grid_visual[0][1], grid_visual[1][1]]
                })
                
                # Show the sequence
                st.write("**Cycle sequence:**")
                cycle_sequence = []
                for idx, cycle_state in enumerate(cycle_states):
                    p1_strat = np.argmax(cycle_state[0])
                    p2_strat = np.argmax(cycle_state[1])
                    cycle_sequence.append(f"Step {idx + 1}: ({p1_strat}, {p2_strat})")
                
                for step in cycle_sequence:
                    st.write(f"- {step}")
                
                break
    
    if not converged and not cycle_detected:
        st.info(f"No convergence after {max_iterations} iterations. Try increasing max iterations.")