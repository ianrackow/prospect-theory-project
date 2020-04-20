from flask import Flask, render_template, request
from scipy.optimize import curve_fit


from app import app


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/test', methods=['GET'])
def trial():
    return render_template("trial.html")


@app.route('/submit', methods=['POST'])
def submit():

    results = request.form['results'].split(",")

    vals = list(map(int, results[::4]))
    probs = list(map(float, results[1::4]))
    uppers = list(map(int, results[2::4]))
    lowers = list(map(int, results[3::4]))

    # compute expected certainty ratios
    cx = list(map(lambda x,y,z:(x+y)/(2*z), uppers, lowers, vals))

    points = str(list(map(lambda x,y:[x, y], probs, cx)))

    gamma = weight_regression(probs, cx)

    return render_template("results.html", gamma=gamma, data=points)


# Run least squares regression using the TK 1992 functional form
def weight_regression(probs, weights):

    popt, pcov = curve_fit(tk, probs, weights, bounds=(0, 1))

    return popt[0]


# Parametric Weighting function
def tk(x, g):

    return (x**g) / ((x**g + (1 - x)**g)**(1/g))


if __name__ == '__main__':
    app.run(debug=True)
