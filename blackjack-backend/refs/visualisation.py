
import pandas as pd

def metric_cum_balance_by_player(table):
    val_dict = dict()
    for player in table.players:
        vals = [h.hand_value for h in player.history]
        # Take subtotal when splitting
        vals = [sum(item) for item in vals]
        
        # Create cumulative values
        cum_vals = [] 
        prev_val = 0
        for v in vals:
            cum_vals.append(v+prev_val)
            prev_val = v+prev_val
        val_dict[player.name] = cum_vals
        
    return pd.DataFrame(val_dict)
