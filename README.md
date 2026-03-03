# ⚡ SkillForge – Personal Skill Tracker

> A professional, console-based skill management system built with advanced Object-Oriented Programming principles in Python.

**Track. Measure. Master. 🚀**

---

# 🎯 Project Overview

**SkillForge** is a portfolio-ready Python application that demonstrates enterprise-level OOP architecture while remaining beginner-friendly.

It enables users to track their skill development journey using intelligent mastery scoring algorithms that differentiate between technical and soft skills.

This project emphasizes:

* Clean architecture
* Scalability
* Maintainability
* Real-world software design principles

---

# ✨ Features

* 🔹 Dual Skill Types (Technical & Soft Skills)
* 🔹 Intelligent Mastery Scoring (Type-specific formulas)
* 🔹 Progress Tracking (0–100%)
* 🔹 Practice Hour Logging
* 🔹 Real-World Soft Skill Application Logging
* 🔹 Persistent Storage (JSON-based `.txt` file)
* 🔹 Statistical Dashboard
* 🔹 Robust Input Validation
* 🔹 Professional Console UI
* 🔹 Automatic Save & Load System

---

# 🏗️ OOP Concepts Demonstrated

## 1️⃣ Abstraction

* `SkillBase` abstract class using Python `ABC`
* Abstract methods:

  * `calculate_mastery_score()`
  * `get_skill_type()`

---

## 2️⃣ Encapsulation

* Private attributes: `__name`, `__category`
* Protected attributes: `_progress`, `_practice_hours`
* Property decorators for controlled access

---

## 3️⃣ Inheritance

* `TechnicalSkill` and `SoftSkill` inherit from `SkillBase`
* Child classes extend parent functionality

---

## 4️⃣ Polymorphism

Method overriding for:

* `calculate_mastery_score()`
* `__str__()`
* `to_dict()`

Same interface → Different behavior.

---

## 5️⃣ Composition

`SkillForgeManager` manages a list of `SkillBase` objects.

Demonstrates **"has-a" relationship** instead of only "is-a".

---

## 6️⃣ Exception Handling

* Custom validation using `ValueError` and `TypeError`
* File handling with `try-except`
* Graceful recovery with user-friendly messages

---

## 7️⃣ File Handling

* JSON-based persistence (`skillforge_data.txt`)
* Automatic save/load functionality
* Serialization & deserialization

---

## 8️⃣ Dynamic Object Creation

* Runtime object instantiation
* Factory-like reconstruction during JSON loading

---

# 📦 Installation

## ✅ Prerequisites

* Python 3.7 or higher

## ▶️ Run the Application

```bash
python skillforge.py
```

No external dependencies required.
Uses only the Python standard library.

---

# 🚀 How It Works

### Application Flow

1. Application loads saved skills from `skillforge_data.txt`
2. Interactive console menu displays options
3. User adds skills with attributes
4. Updates progress & logs practice hours
5. Views statistics dashboard
6. Data automatically saves on exit

---

# 🧮 Mastery Score Formulas

## 🔧 Technical Skills

```
Mastery =
(Progress × 0.5)
+ (Practice_Factor × 0.3)
+ (Difficulty_Bonus × 0.2)
```

Where:

* Progress = 0–100%
* Practice_Factor = Normalized practice hours (capped at 100 hrs)
* Difficulty_Bonus = Difficulty level (1–10 converted to %)

✔ Focuses on measurable technical growth.

---

## 🤝 Soft Skills

```
Mastery =
(Progress × 0.4)
+ (Practice_Factor × 0.3)
+ (Application_Factor × 0.3)
```

Where:

* Practice capped at 50 hrs
* Applications capped at 20 uses

✔ Emphasizes real-world implementation.

---

# 📁 Project Structure

```
skillforge/
│
├── skillforge.py
├── skillforge_data.txt
└── README.md
```

---

!END
🏗️ Architecture(SkillForge – System Flow Diagram Structure)
---

# 🎯 Key Design Principles

* ✅ Separation of Concerns
* ✅ Layered Architecture
* ✅ SOLID Principles
* ✅ Composition over Inheritance
* ✅ Modular & Extendable Design
* ✅ Type Hint Support
* ✅ Production-style Validation

---

# 🔮 Future Enhancements

* Skill category filtering
* Goal & deadline tracking
* ASCII progress charts
* PDF/HTML report export
* AI-based skill suggestions
* Achievement badge system
* Industry benchmark comparison
* Multi-user profile support
* Data analytics module
* Optional cloud sync

---

# 🎓 Learning Outcomes

This project demonstrates:

* Designing scalable class hierarchies
* Applying abstraction effectively
* Proper encapsulation strategies
* Method overriding & polymorphism
* Composition-based architecture
* Professional error handling
* JSON-based persistence
* Clean separation of concerns

---

# 👨‍💻 Author

**Vishal Rathod**

🌐 Portfolio:
[https://vr8010.github.io/Vishal-Rathod-/](https://vr8010.github.io/Vishal-Rathod-/)

💻 GitHub:
[https://github.com/vr8010](https://github.com/vr8010)

🔗 LinkedIn:
[https://www.linkedin.com/in/vishal-rathod-508b89243/](https://www.linkedin.com/in/vishal-rathod-508b89243/)

---

# 📝 License

This project is open-source and available for educational purposes.

---

# 🤝 Contributing

Feel free to fork and enhance:

* Add new skill types
* Improve mastery algorithm
* Create GUI version (Tkinter)
* Add data visualization (Matplotlib)
* Build web version (Flask / Django)

---

⭐ If you found this useful, consider giving it a star on GitHub!

---

