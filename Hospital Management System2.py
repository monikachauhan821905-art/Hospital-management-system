import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

COLORS = {
    "primary": "steelblue", "secondary": "mediumvioletred", "accent": "darkorange",
    "success": "forestgreen", "danger": "firebrick", "light": "whitesmoke", "dark": "darkslategray"
}

class Doctor:
    def __init__(self, doc_id, name, department):
        self.doc_id, self.name, self.department = doc_id, name, department

class Patient:
    def __init__(self, patient_id, name, age, gender, disease, doctor):
        self.patient_id, self.name, self.age, self.gender, self.disease, self.doctor = patient_id, name, int(age), gender, disease, doctor

class Hospital:
    def __init__(self):
        self.patients = []
        self.doctors = [
            Doctor("D101", "Dr. Mehta", "Cardiology"),
            Doctor("D102", "Dr. Sharma", "Neurology"),
            Doctor("D103", "Dr. Verma", "Orthopedics"),
            Doctor("D104", "Dr. Patel", "Dermatology"),
            Doctor("D105", "Dr. Gupta", "Pediatrics")
        ]

    def assign_doctor(self, disease):
        disease = disease.lower()
        if "heart" in disease or "cardio" in disease: return self.doctors[0]
        elif "brain" in disease or "neuro" in disease: return self.doctors[1]
        elif "bone" in disease or "fracture" in disease: return self.doctors[2]
        elif "skin" in disease or "rash" in disease: return self.doctors[3]
        elif "child" in disease or "fever" in disease: return self.doctors[4]
        else: return Doctor("D000", "Dr. General", "General Medicine")

class HospitalManagementSystem:
    def __init__(self, root):
        self.hospital = Hospital()
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1000x600")
        self.root.configure(bg=COLORS["light"])
        self.setup_ui()
        self.load_sample_data()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=COLORS["primary"], height=80)
        header.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(header, text="Hospital Management System", bg=COLORS["primary"], 
                fg="white", font=("Arial", 20, "bold")).pack(pady=20)
        
        self.stats_label = tk.Label(header, text="Patients: 0 | Doctors: 5", 
                                   bg=COLORS["secondary"], fg="white", font=("Arial", 10, "bold"),
                                   padx=10, pady=5)
        self.stats_label.pack()

        # Main container
        main_frame = tk.Frame(self.root, bg=COLORS["light"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Form section
        form_frame = tk.LabelFrame(main_frame, text="Patient Information", bg="white",
                                  fg=COLORS["primary"], font=("Arial", 12, "bold"), padx=10, pady=10)
        form_frame.pack(fill=tk.X, pady=(0, 10))

        # Input fields
        labels = ["Patient ID", "Name", "Age", "Gender", "Disease"]
        self.entries = {}
        input_container = tk.Frame(form_frame, bg="white")
        input_container.pack(expand=True, fill=tk.X, pady=10)
        
        for i in range(10):
            input_container.grid_columnconfigure(i, weight=1)

        for i, label in enumerate(labels):
            tk.Label(input_container, text=label, bg="white", font=("Arial", 9, "bold")).grid(
                row=0, column=i*2+1, padx=5, pady=5, sticky="ew")
            entry = tk.Entry(input_container, font=("Arial", 10), relief="solid", bd=1, width=15)
            entry.grid(row=1, column=i*2+1, padx=5, pady=5, sticky="ew")
            self.entries[label.lower().replace(" ", "_")] = entry

        # Buttons
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.pack(fill=tk.X, pady=15)
        center_frame = tk.Frame(btn_frame, bg="white")
        center_frame.pack(expand=True)
        
        buttons = [
            ("Add Patient", self.add_patient, COLORS["success"]),
            ("Update Patient", self.update_patient, COLORS["primary"]), 
            ("Delete Patient", self.delete_patient, COLORS["danger"]),
            ("View Charts", self.visualize_data, COLORS["accent"])
        ]

        for i, (text, cmd, color) in enumerate(buttons):
            tk.Button(center_frame, text=text, command=cmd, bg=color, fg="white", 
                     font=("Arial", 11, "bold"), relief="flat", padx=25, pady=12,
                     bd=0, cursor="hand2", width=12).grid(row=0, column=i, padx=8, pady=5)

        # Table
        table_frame = tk.Frame(main_frame, bg="white", relief="raised", bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(table_frame, 
                               columns=("id", "name", "age", "gender", "disease", "doctor", "department"), 
                               show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        columns = {
            "id": ("ID", 80), "name": ("Name", 120), "age": ("Age", 60), "gender": ("Gender", 80),
            "disease": ("Disease", 120), "doctor": ("Doctor", 120), "department": ("Department", 100)
        }

        for col, (text, width) in columns.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.bind("<Double-1>", self.on_item_select)

    def load_sample_data(self):
        sample_patients = [
            ("P001", "John Doe", "35", "Male", "Heart disease"),
            ("P002", "Jane Smith", "28", "Female", "Skin rash"),
            ("P003", "Mike Johnson", "45", "Male", "Bone fracture")
        ]
        
        for pid, name, age, gender, disease in sample_patients:
            doctor = self.hospital.assign_doctor(disease)
            patient = Patient(pid, name, age, gender, disease, doctor)
            self.hospital.patients.append(patient)
            self.tree.insert("", "end", values=(
                patient.patient_id, patient.name, patient.age, patient.gender, 
                patient.disease, patient.doctor.name, patient.doctor.department
            ))
        self.update_stats()

    def update_stats(self):
        self.stats_label.config(text=f"Patients: {len(self.hospital.patients)} | Doctors: 5")

    def on_item_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])["values"]
            fields = ["patient_id", "name", "age", "gender", "disease"]
            for field, value in zip(fields, values):
                if field in self.entries:
                    self.entries[field].delete(0, tk.END)
                    self.entries[field].insert(0, str(value))

    def add_patient(self):
        data = {key: entry.get() for key, entry in self.entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        if any(p.patient_id == data["patient_id"] for p in self.hospital.patients):
            messagebox.showwarning("Input Error", "Patient ID already exists.")
            return

        doctor = self.hospital.assign_doctor(data["disease"])
        patient = Patient(data["patient_id"], data["name"], data["age"], data["gender"], data["disease"], doctor)
        self.hospital.patients.append(patient)
        self.tree.insert("", "end", values=(
            patient.patient_id, patient.name, patient.age, patient.gender, 
            patient.disease, patient.doctor.name, patient.doctor.department
        ))
        messagebox.showinfo("Success", f"Patient added to {doctor.department}")
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.update_stats()

    def update_patient(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a patient.")
            return
        
        pid = self.tree.item(selected[0])["values"][0]
        for patient in self.hospital.patients:
            if patient.patient_id == pid:
                data = {key: entry.get() for key, entry in self.entries.items()}
                if not all(data.values()):
                    messagebox.showwarning("Input Error", "Please fill all fields.")
                    return
                
                patient.name, patient.age, patient.gender, patient.disease = data["name"], int(data["age"]), data["gender"], data["disease"]
                patient.doctor = self.hospital.assign_doctor(patient.disease)
                self.tree.item(selected[0], values=(
                    patient.patient_id, patient.name, patient.age, patient.gender, 
                    patient.disease, patient.doctor.name, patient.doctor.department
                ))
                messagebox.showinfo("Updated", "Patient record updated.")
                self.update_stats()
                return

    def delete_patient(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a patient.")
            return
        
        pid = self.tree.item(selected[0])["values"][0]
        self.hospital.patients = [p for p in self.hospital.patients if p.patient_id != pid]
        self.tree.delete(selected[0])
        messagebox.showinfo("Deleted", "Patient deleted.")
        self.update_stats()

    def visualize_data(self):
        if not self.hospital.patients:
            messagebox.showwarning("No Data", "No patients to visualize.")
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        
        # Department chart
        departments = [p.doctor.department for p in self.hospital.patients]
        unique_dept, dept_counts = np.unique(departments, return_counts=True)
        ax1.bar(unique_dept, dept_counts, color=[COLORS["primary"], COLORS["secondary"], COLORS["accent"]])
        ax1.set_title("Patients per Department")
        ax1.tick_params(axis='x', rotation=45)

        # Gender chart
        genders = [p.gender for p in self.hospital.patients]
        unique_gender, gender_counts = np.unique(genders, return_counts=True)
        ax2.pie(gender_counts, labels=unique_gender, autopct='%1.1f%%', 
               colors=[COLORS["primary"], COLORS["secondary"]])
        ax2.set_title("Gender Distribution")

        plt.tight_layout()

        chart_win = tk.Toplevel(self.root)
        chart_win.title("Hospital Analytics")
        chart_win.geometry("800x500")
        
        canvas = FigureCanvasTkAgg(fig, master=chart_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalManagementSystem(root)
    root.mainloop()