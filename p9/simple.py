import tkinter as tk

root = tk.Tk()
root.title("User Form")
root.geometry("450x400")
root.configure(bg="#f5f6fa")

# Title
title = tk.Label(root, text="User Information Form", font=("Helvetica", 16, "bold"),
                 bg="#f5f6fa", fg="#2f3640")
title.pack(pady=15)

# Frame for form
form_frame = tk.Frame(root, bg="#f5f6fa")
form_frame.pack(pady=10)

# Name
tk.Label(form_frame, text="Full Name:", bg="#f5f6fa", fg="#2f3640", font=("Arial", 11)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
tk.Entry(form_frame, width=30, bd=2, relief="solid").grid(row=0, column=1, padx=10, pady=5)

# Email
tk.Label(form_frame, text="Email Address:", bg="#f5f6fa", fg="#2f3640", font=("Arial", 11)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
tk.Entry(form_frame, width=30, bd=2, relief="solid").grid(row=1, column=1, padx=10, pady=5)

# Gender
tk.Label(form_frame, text="Gender:", bg="#f5f6fa", fg="#2f3640", font=("Arial", 11)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
tk.Radiobutton(form_frame, text="Male", bg="#f5f6fa").grid(row=2, column=1, sticky="w", padx=10)
tk.Radiobutton(form_frame, text="Female", bg="#f5f6fa").grid(row=2, column=1, sticky="e", padx=10)

# Country
tk.Label(form_frame, text="Country:", bg="#f5f6fa", fg="#2f3640", font=("Arial", 11)).grid(row=3, column=0, sticky="w", padx=10, pady=5)
countries = ["India", "USA", "UK", "Canada", "Australia"]
country_menu = tk.OptionMenu(form_frame, tk.StringVar(value="Select"), *countries)
country_menu.config(width=26)
country_menu.grid(row=3, column=1, padx=10, pady=5)

# Terms and conditions
tk.Checkbutton(form_frame, text="I agree to the terms and conditions", bg="#f5f6fa").grid(row=4, columnspan=2, pady=10)

# Buttons
button_frame = tk.Frame(root, bg="#f5f6fa")
button_frame.pack(pady=15)

tk.Button(button_frame, text="Submit", font=("Arial", 11, "bold"),
          bg="#4a90e2", fg="white", activebackground="#357ABD",
          activeforeground="white", relief="flat", width=12).grid(row=0, column=0, padx=10)

tk.Button(button_frame, text="Clear", font=("Arial", 11, "bold"),
          bg="#e57373", fg="white", activebackground="#d32f2f",
          activeforeground="white", relief="flat", width=12).grid(row=0, column=1, padx=10)

# Footer
tk.Label(root, text="@2025 Form", font=("Arial", 9),
         bg="#f5f6fa", fg="#888").pack(side="bottom", pady=20)

root.mainloop()
