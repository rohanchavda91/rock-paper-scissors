def player(prev_play, opponent_history=[], play_order={}):
    # 1. Reset history and order if it's the start of a new match
    if not prev_play:
        opponent_history.clear()
        play_order.clear()
        
    # 2. Track the opponent's move
    if prev_play:
        opponent_history.append(prev_play)

    # 3. Define how many past moves we want to look at (The "Context")
    # n=5 is usually a sweet spot for these bots to capture patterns without overfitting
    n = 5

    # 4. Update our frequency dictionary (Markov Chain training)
    last_n_moves = opponent_history[-(n+1):]
    if len(last_n_moves) == n + 1:
        # We turn the list into a string to use as a dictionary key
        # e.g., "RRPPS" -> frequency count
        last_pattern = "".join(last_n_moves)
        if last_pattern in play_order:
            play_order[last_pattern] += 1
        else:
            play_order[last_pattern] = 1

    # 5. Prediction Logic
    prediction = "P" # Default fallback

    # We only start predicting if we have enough history
    if len(opponent_history) >= n:
        # Look at the most recent sequence of 'n' moves
        current_pattern = "".join(opponent_history[-n:])
        
        # We want to see what usually comes AFTER this sequence
        # So we check "current_pattern + R", "current_pattern + P", "current_pattern + S"
        potential_moves = [
            current_pattern + "R",
            current_pattern + "P",
            current_pattern + "S"
        ]

        # Find which of these 3 next states has happened the most in the past
        sub_order = {
            k: play_order.get(k, 0)
            for k in potential_moves
        }

        # The prediction is the last character of the most frequent pattern
        prediction_pattern = max(sub_order, key=sub_order.get)
        
        # If we have no data on this pattern yet, just guess P (or random)
        if sub_order[prediction_pattern] != 0:
            prediction = prediction_pattern[-1]

    # 6. Counter the prediction
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[prediction]

