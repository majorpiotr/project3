from flask import Flask, render_template, request, flash, redirect, url_for, session


app.debug = True
@app.route('/')
def index():
	return render_template("index.html")

if __name__ == '__main__':
  app.run()