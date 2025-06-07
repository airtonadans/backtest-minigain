import matplotlib.pyplot as plt
import io, base64

def generate_equity_curve_image(trades_df, equity_curve):
    plt.figure(); plt.plot(equity_curve); plt.title("Equity Curve")
    buf=io.BytesIO(); plt.savefig(buf,format="png"); plt.close()
    return "data:image/png;base64,"+base64.b64encode(buf.getvalue()).decode()
