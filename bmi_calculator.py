# BMI Calculator

weight = float(input("Enter your weight (kg): "))
height = float(input("Enter your height (cm): "))

height = height/100

bmi = weight / (height ** 2)

print(f"Your BMI is: {bmi:.2f}")

#______________________
#BMI Classification
#______________________
if bmi < 18.5:
    print("Category: Underweight")
elif bmi < 25:
    print("Category: Normal weight")
elif bmi < 30:
    print("Category: Overweight")
else:
    print("Category: Obese")
