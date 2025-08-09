from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    
# Correr App 

# python run.py

# Correr Test

# pytest selenium_tests/test_app.py --html=report.html --self-contained-html


# Contraseña:# admin
# Usuario: # admin